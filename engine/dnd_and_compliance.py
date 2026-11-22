"""
TRAI DND & Quiet Hours Regulatory Compliance Engine
Implements Telecom Commercial Communications Customer Preference Regulations (TCCCPR, 2018).
"""

from datetime import datetime, timezone, timedelta
from typing import Tuple
from engine.events import EventCategory, EVENT_TAXONOMY

# Simulated National Do Not Call (NDNC) Registered Phone Numbers
DND_REGISTRY = {
    "+919876543210",
    "+919988776655",
    "+919123456789",
    "+919880011223"
}

def is_dnd_registered(phone: str) -> bool:
    """Check if the recipient's phone number is registered on TRAI NDNC."""
    clean_phone = phone.replace(" ", "").replace("-", "")
    if not clean_phone.startswith("+91"):
        clean_phone = "+91" + clean_phone[-10:]
    return clean_phone in DND_REGISTRY

def is_in_quiet_hours(current_time: datetime = None) -> bool:
    """
    Check if the current time falls within Indian Quiet Hours (21:00 to 09:00 IST).
    IST is UTC+5:30.
    """
    if current_time is None:
        ist_tz = timezone(timedelta(hours=5, minutes=30))
        current_time = datetime.now(ist_tz)
    
    hour = current_time.hour
    # Quiet hours: 9 PM (21:00) to 9 AM (09:00)
    return hour >= 21 or hour < 9

def evaluate_regulatory_clearance(event_type: str, recipient_phone: str, test_hour: int = None) -> Tuple[bool, str]:
    """
    Evaluates whether an event can be dispatched based on TRAI guidelines:
    - CRITICAL and TRANSACTIONAL events bypass DND and quiet hours.
    - REMINDER events honor quiet hours.
    - PROMOTIONAL events honor both DND and quiet hours.
    """
    meta = EVENT_TAXONOMY.get(event_type)
    if not meta:
        return False, f"Unknown event type: {event_type}"

    category = meta["category"]

    # 1. Critical & Transactional are exempt
    if category in [EventCategory.CRITICAL, EventCategory.TRANSACTIONAL]:
        return True, "EXEMPT: Critical or Transactional financial alert"

    # 2. Check Quiet Hours (21:00 - 09:00 IST)
    ist_tz = timezone(timedelta(hours=5, minutes=30))
    now = datetime.now(ist_tz)
    if test_hour is not None:
        now = now.replace(hour=test_hour)

    if is_in_quiet_hours(now):
        return False, "BLOCKED: Quiet hours active (21:00–09:00 IST). Queued for morning dispatch."

    # 3. Check DND Registry for Promotional events
    if category == EventCategory.PROMOTIONAL:
        if is_dnd_registered(recipient_phone):
            return False, "BLOCKED: Recipient phone number active on TRAI DND Registry."

    return True, "APPROVED: Cleared regulatory filter"
