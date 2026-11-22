"""
Multi-Channel Dispatcher, Idempotency Guard & Dead-Letter Queue (DLQ) Engine
"""

import time
import random
from typing import Dict, Any, List
from engine.events import FinancialNotificationEvent, DeliveryChannel, EVENT_TAXONOMY
from engine.dnd_and_compliance import evaluate_regulatory_clearance
from engine.template_engine import render_notification

class NotificationDispatcher:
    def __init__(self):
        # In-memory storage for demonstration & testing
        self.idempotency_vault: Dict[str, float] = {}  # key -> timestamp
        self.dispatched_events: List[Dict[str, Any]] = []
        self.dead_letter_queue: List[Dict[str, Any]] = []
        self.stats = {
            "total_ingested": 0,
            "delivered": 0,
            "blocked_dnd": 0,
            "blocked_quiet_hours": 0,
            "dlq_quarantined": 0,
            "channel_counts": {
                "SMS": 0,
                "EMAIL": 0,
                "WHATSAPP": 0,
                "PUSH": 0,
                "IN_APP": 0
            }
        }

    def dispatch(self, event: FinancialNotificationEvent, test_hour: int = None, simulate_failure: bool = False) -> Dict[str, Any]:
        """Processes event through Idempotency -> Compliance -> Template -> Channel -> DLQ Pipeline."""
        self.stats["total_ingested"] += 1

        # 1. Idempotency Check
        now = time.time()
        if event.idempotency_key in self.idempotency_vault:
            # Duplicate event within TTL (24h)
            return {
                "status": "DUPLICATE_DROPPED",
                "message": f"Idempotency key {event.idempotency_key} already processed. Dropped duplicate.",
                "event_id": event.event_id
            }
        self.idempotency_vault[event.idempotency_key] = now

        # 2. Regulatory & DND Clearance
        cleared, reason = evaluate_regulatory_clearance(event.event_type, event.recipient_phone, test_hour=test_hour)
        if not cleared:
            if "DND" in reason:
                self.stats["blocked_dnd"] += 1
                status = "DND_BLOCKED"
            else:
                self.stats["blocked_quiet_hours"] += 1
                status = "QUIET_HOURS_BLOCKED"

            entry = {
                "event_id": event.event_id,
                "event_type": event.event_type,
                "user_id": event.user_id,
                "channel": event.override_channel or "MULTI",
                "status": status,
                "reason": reason,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
            self.dispatched_events.insert(0, entry)
            return entry

        # 3. Determine Channels
        meta = EVENT_TAXONOMY.get(event.event_type, {})
        channels = [event.override_channel] if event.override_channel else meta.get("default_channels", [DeliveryChannel.IN_APP])

        # 4. Render Message Template
        context = {**event.payload, "user_id": event.user_id, "event_id": event.event_id, "event_type": event.event_type}
        rendered_text = render_notification(event.event_type, event.preferred_language, context)

        # 5. Simulated Channel Dispatch & Fault Simulation
        if simulate_failure:
            # Move to DLQ
            dlq_item = {
                "dlq_id": f"DLQ_{int(now*1000)}_{random.randint(100, 999)}",
                "event_id": event.event_id,
                "event_type": event.event_type,
                "user_id": event.user_id,
                "error_reason": "Downstream Gateway Timeout / Provider Socket Error (504)",
                "retry_count": 1,
                "original_event": event.dict(),
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
            self.dead_letter_queue.append(dlq_item)
            self.stats["dlq_quarantined"] += 1
            return {"status": "DLQ_QUARANTINED", "dlq_id": dlq_item["dlq_id"], "reason": dlq_item["error_reason"]}

        # Successful Delivery
        self.stats["delivered"] += 1
        for ch in channels:
            ch_name = ch.value if hasattr(ch, "value") else str(ch)
            if ch_name in self.stats["channel_counts"]:
                self.stats["channel_counts"][ch_name] += 1

        dispatch_record = {
            "event_id": event.event_id,
            "event_type": event.event_type,
            "category": meta.get("category", "GENERAL"),
            "user_id": event.user_id,
            "recipient_phone": event.recipient_phone,
            "channels": [c.value if hasattr(c, "value") else str(c) for c in channels],
            "language": event.preferred_language,
            "rendered_message": rendered_text,
            "status": "DELIVERED",
            "latency_ms": round(random.uniform(12.5, 38.0), 2),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        self.dispatched_events.insert(0, dispatch_record)
        return dispatch_record

    def retry_dlq(self) -> Dict[str, Any]:
        """Flushes and reprocesses queued defective records."""
        count = len(self.dead_letter_queue)
        reprocessed = []
        for item in list(self.dead_letter_queue):
            orig = item["original_event"]
            # Clear idempotency to allow retry
            if orig.get("idempotency_key") in self.idempotency_vault:
                del self.idempotency_vault[orig["idempotency_key"]]
            ev = FinancialNotificationEvent(**orig)
            res = self.dispatch(ev, simulate_failure=False)
            reprocessed.append(res)

        self.dead_letter_queue.clear()
        self.stats["dlq_quarantined"] = 0
        return {"reprocessed_count": count, "details": reprocessed}

# Global engine instance
dispatcher = NotificationDispatcher()
