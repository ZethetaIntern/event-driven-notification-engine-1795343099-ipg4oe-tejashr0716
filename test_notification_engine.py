"""
Comprehensive Test Automation Suite for Event-Driven Notification Engine (Project 1D)
Validates 25+ event taxonomy, TRAI DND filter, quiet hours, idempotency, templates, and DLQ.
"""

import uuid
from fastapi.testclient import TestClient
from app import app
from engine.events import EVENT_TAXONOMY, FinancialNotificationEvent, EventCategory
from engine.dnd_and_compliance import evaluate_regulatory_clearance, is_dnd_registered
from engine.template_engine import render_notification
from engine.dispatcher import dispatcher

client = TestClient(app)

def test_1_event_taxonomy_completeness():
    """Verify 25+ financial event types exist across all 5 operational categories."""
    assert len(EVENT_TAXONOMY) >= 25, f"Expected at least 25 events, found {len(EVENT_TAXONOMY)}"

    categories = {meta["category"] for meta in EVENT_TAXONOMY.values()}
    assert EventCategory.CRITICAL in categories
    assert EventCategory.TRANSACTIONAL in categories
    assert EventCategory.REMINDER in categories
    assert EventCategory.REGULATORY in categories
    assert EventCategory.PROMOTIONAL in categories

    # Verify key high-risk events exist
    assert "MARGIN_CALL" in EVENT_TAXONOMY
    assert "SECURITY_OTP" in EVENT_TAXONOMY
    assert "TRADE_EXECUTED" in EVENT_TAXONOMY
    assert "SIP_DUE_ALERT" in EVENT_TAXONOMY
    assert "DAILY_MARKET_WRAP" in EVENT_TAXONOMY

    print(f"✓ Test 1 Passed: Event taxonomy verified with {len(EVENT_TAXONOMY)} financial event definitions.")

def test_2_trai_dnd_filtering_rules():
    """Verify promotional messages are blocked on DND numbers while critical alerts are exempt."""
    dnd_phone = "+919876543210"
    normal_phone = "+919111222333"

    assert is_dnd_registered(dnd_phone) is True
    assert is_dnd_registered(normal_phone) is False

    # Promotional event to DND number during daytime (14:00 IST) -> MUST BE BLOCKED
    cleared, reason = evaluate_regulatory_clearance("DAILY_MARKET_WRAP", dnd_phone, test_hour=14)
    assert cleared is False
    assert "DND" in reason

    # Critical Margin Call to DND number during daytime (14:00 IST) -> MUST BE EXEMPT & CLEARED
    cleared_crit, reason_crit = evaluate_regulatory_clearance("MARGIN_CALL", dnd_phone, test_hour=14)
    assert cleared_crit is True
    assert "EXEMPT" in reason_crit

    print("✓ Test 2 Passed: TRAI DND filtering enforces promotional block and critical exemption.")

def test_3_quiet_hours_enforcement():
    """Verify quiet hours (21:00 to 09:00 IST) block non-critical alerts but allow emergency alerts."""
    phone = "+919111222333"

    # Promotional event at 23:00 IST (Night) -> MUST BE BLOCKED
    cleared_night, reason_night = evaluate_regulatory_clearance("IPO_OPEN_SUBSCRIPTION", phone, test_hour=23)
    assert cleared_night is False
    assert "Quiet hours" in reason_night

    # Critical Security OTP at 23:00 IST (Night) -> MUST BE DELIVERED IMMEDIATELY
    cleared_otp, _ = evaluate_regulatory_clearance("SECURITY_OTP", phone, test_hour=23)
    assert cleared_otp is True

    # Promotional event at 11:00 IST (Daytime) -> APPROVED
    cleared_day, _ = evaluate_regulatory_clearance("IPO_OPEN_SUBSCRIPTION", phone, test_hour=11)
    assert cleared_day is True

    print("✓ Test 3 Passed: Quiet hours compliance (21:00–09:00 IST) verified.")

def test_4_template_localization():
    """Verify multi-language template rendering across EN, HI, MR, TA, TE."""
    ctx = {"amount": "75,000", "account": "DEMAT-1234"}

    msg_en = render_notification("MARGIN_CALL", "en", ctx)
    assert "URGENT" in msg_en and "₹75,000" in msg_en

    msg_hi = render_notification("MARGIN_CALL", "hi", ctx)
    assert "अत्यावश्यक" in msg_hi and "₹75,000" in msg_hi

    msg_mr = render_notification("MARGIN_CALL", "mr", ctx)
    assert "तातडीचे" in msg_mr

    msg_ta = render_notification("MARGIN_CALL", "ta", ctx)
    assert "அவசரம்" in msg_ta

    msg_te = render_notification("MARGIN_CALL", "te", ctx)
    assert "అత్యవసరం" in msg_te

    print("✓ Test 4 Passed: Multi-language template engine verified across 5 Indian regional languages.")

def test_5_idempotency_deduplication():
    """Verify identical idempotency keys drop duplicate dispatches."""
    unique_key = f"TEST_IDEMP_{uuid.uuid4()}"
    ev = FinancialNotificationEvent(
        event_id=str(uuid.uuid4()),
        idempotency_key=unique_key,
        event_type="FUND_DEPOSITED",
        user_id="USR_TEST_42",
        recipient_phone="+919111222333",
        recipient_email="test@example.com",
        payload={"amount": "25,000", "account": "ACC-99"}
    )

    first_res = dispatcher.dispatch(ev)
    assert first_res["status"] == "DELIVERED"

    # Re-dispatch with same key
    duplicate_res = dispatcher.dispatch(ev)
    assert duplicate_res["status"] == "DUPLICATE_DROPPED"

    print("✓ Test 5 Passed: Idempotency deduplication guard verified.")

def test_6_dead_letter_queue_and_retry():
    """Verify defective payload quarantining to DLQ and automated retry."""
    ev = FinancialNotificationEvent(
        event_id=str(uuid.uuid4()),
        idempotency_key=f"TEST_DLQ_{uuid.uuid4()}",
        event_type="WITHDRAWAL_APPROVED",
        user_id="USR_DLQ_10",
        recipient_phone="+919111222333",
        recipient_email="dlq@example.com",
        payload={"amount": "10,000"}
    )

    # Dispatch with simulated socket failure
    fail_res = dispatcher.dispatch(ev, simulate_failure=True)
    assert fail_res["status"] == "DLQ_QUARANTINED"
    assert len(dispatcher.dead_letter_queue) >= 1

    # Retry DLQ
    retry_res = dispatcher.retry_dlq()
    assert retry_res["reprocessed_count"] >= 1
    assert len(dispatcher.dead_letter_queue) == 0

    print("✓ Test 6 Passed: Dead-Letter Queue (DLQ) quarantine and retry cycle verified.")

def test_7_fastapi_rest_endpoints_and_trustsphere_ui():
    """Verify REST API and TrustSphere HTML dashboard load correctly."""
    # Stats
    res_stats = client.get("/api/v1/stats")
    assert res_stats.status_code == 200
    assert "stats" in res_stats.json()

    # Feed
    res_feed = client.get("/api/v1/events/feed")
    assert res_feed.status_code == 200
    assert isinstance(res_feed.json(), list)

    # HTML UI
    res_ui = client.get("/")
    assert res_ui.status_code == 200
    assert "text/html" in res_ui.headers.get("content-type", "")
    assert "TrustSphere Technologies" in res_ui.text
    assert "Lora" in res_ui.text
    assert "Work Sans" in res_ui.text
    assert "Simulate Real-Time Financial Event Dispatch" in res_ui.text

    print("✓ Test 7 Passed: FastAPI endpoints and TrustSphere Technologies dashboard verified.")

if __name__ == "__main__":
    print("=" * 70)
    print("Running Event-Driven Notification Engine Test Automation (Project 1D)")
    print("=" * 70)
    test_1_event_taxonomy_completeness()
    test_2_trai_dnd_filtering_rules()
    test_3_quiet_hours_enforcement()
    test_4_template_localization()
    test_5_idempotency_deduplication()
    test_6_dead_letter_queue_and_retry()
    test_7_fastapi_rest_endpoints_and_trustsphere_ui()
    print("=" * 70)
    print("ALL 7 TESTS PASSED WITH 100% SUCCESS RATE!")
    print("=" * 70)
