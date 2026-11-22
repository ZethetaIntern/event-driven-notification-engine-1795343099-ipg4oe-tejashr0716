"""
Financial Event Taxonomy & Payload Definitions (25+ Event Types)
Covers Categories: Critical, Transactional, Reminder, Regulatory, Promotional
"""

from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class EventCategory(str, Enum):
    CRITICAL = "CRITICAL"            # Zero quiet hours, bypass DND for emergency risk
    TRANSACTIONAL = "TRANSACTIONAL"  # Zero quiet hours, financial ledger alerts
    REMINDER = "REMINDER"            # Subject to quiet hours (21:00-09:00 IST)
    REGULATORY = "REGULATORY"        # Statutory notices
    PROMOTIONAL = "PROMOTIONAL"      # Strict TRAI DND and quiet hours enforcement

class DeliveryChannel(str, Enum):
    SMS = "SMS"
    EMAIL = "EMAIL"
    WHATSAPP = "WHATSAPP"
    PUSH = "PUSH"
    IN_APP = "IN_APP"

# 25+ Financial Event Types
EVENT_TAXONOMY = {
    # 1. Critical Category (P1)
    "MARGIN_CALL": {
        "category": EventCategory.CRITICAL,
        "default_channels": [DeliveryChannel.SMS, DeliveryChannel.WHATSAPP, DeliveryChannel.PUSH],
        "description": "Urgent margin shortfall requiring immediate funds deposit"
    },
    "FRAUD_ALERT_CRITICAL": {
        "category": EventCategory.CRITICAL,
        "default_channels": [DeliveryChannel.SMS, DeliveryChannel.EMAIL, DeliveryChannel.PUSH],
        "description": "High-risk fraudulent transaction detected on trading account"
    },
    "AUTH_BREACH_ALERT": {
        "category": EventCategory.CRITICAL,
        "default_channels": [DeliveryChannel.SMS, DeliveryChannel.EMAIL, DeliveryChannel.PUSH],
        "description": "Unauthorized login attempt from unrecognized device/IP"
    },
    "STOP_LOSS_EXECUTED": {
        "category": EventCategory.CRITICAL,
        "default_channels": [DeliveryChannel.PUSH, DeliveryChannel.SMS],
        "description": "Risk management stop-loss order triggered and squared off"
    },
    "SECURITY_OTP": {
        "category": EventCategory.CRITICAL,
        "default_channels": [DeliveryChannel.SMS, DeliveryChannel.WHATSAPP],
        "description": "One-Time Password for transaction authorization or withdrawal"
    },

    # 2. Transactional Category (P2)
    "TRADE_EXECUTED": {
        "category": EventCategory.TRANSACTIONAL,
        "default_channels": [DeliveryChannel.PUSH, DeliveryChannel.IN_APP, DeliveryChannel.EMAIL],
        "description": "Order fill confirmation (Equity, Derivatives, Commodities)"
    },
    "FUND_DEPOSITED": {
        "category": EventCategory.TRANSACTIONAL,
        "default_channels": [DeliveryChannel.SMS, DeliveryChannel.IN_APP],
        "description": "Bank transfer / UPI deposit credited to trading balance"
    },
    "WITHDRAWAL_APPROVED": {
        "category": EventCategory.TRANSACTIONAL,
        "default_channels": [DeliveryChannel.SMS, DeliveryChannel.EMAIL],
        "description": "Funds withdrawal processed to verified bank account"
    },
    "DIVIDEND_PAYOUT": {
        "category": EventCategory.TRANSACTIONAL,
        "default_channels": [DeliveryChannel.EMAIL, DeliveryChannel.IN_APP],
        "description": "Corporate action dividend credited to demat account"
    },
    "MANDATE_SUCCESS": {
        "category": EventCategory.TRANSACTIONAL,
        "default_channels": [DeliveryChannel.EMAIL, DeliveryChannel.SMS],
        "description": "eNACH / UPI Autopay mandate successfully registered"
    },

    # 3. Reminder & Market Alerts (P3)
    "SIP_DUE_ALERT": {
        "category": EventCategory.REMINDER,
        "default_channels": [DeliveryChannel.WHATSAPP, DeliveryChannel.PUSH, DeliveryChannel.EMAIL],
        "description": "Mutual fund SIP debit scheduled within 48 hours"
    },
    "PRICE_THRESHOLD_HIT": {
        "category": EventCategory.REMINDER,
        "default_channels": [DeliveryChannel.PUSH, DeliveryChannel.IN_APP],
        "description": "Stock watchlist price alert threshold crossed"
    },
    "F_AND_O_EXPIRY": {
        "category": EventCategory.REMINDER,
        "default_channels": [DeliveryChannel.PUSH, DeliveryChannel.SMS, DeliveryChannel.IN_APP],
        "description": "Monthly/Weekly derivatives contract expiring today"
    },
    "MARGIN_SHORTFALL_WARNING": {
        "category": EventCategory.REMINDER,
        "default_channels": [DeliveryChannel.WHATSAPP, DeliveryChannel.IN_APP],
        "description": "Available margin buffer dropped below 20%"
    },
    "PORTFOLIO_DRIFT_ALERT": {
        "category": EventCategory.REMINDER,
        "default_channels": [DeliveryChannel.IN_APP, DeliveryChannel.EMAIL],
        "description": "Asset allocation deviated by > 10% from target model"
    },

    # 4. Informational & Regulatory Notices (P4)
    "MONTHLY_STATEMENT_GENERATED": {
        "category": EventCategory.REGULATORY,
        "default_channels": [DeliveryChannel.EMAIL, DeliveryChannel.IN_APP],
        "description": "Official Monthly Demat & Trading Account Statement ready"
    },
    "ANNUAL_TAX_PNL": {
        "category": EventCategory.REGULATORY,
        "default_channels": [DeliveryChannel.EMAIL, DeliveryChannel.IN_APP],
        "description": "Annual Capital Gains Tax P&L Statement available for download"
    },
    "KYC_EXPIRY_WARNING": {
        "category": EventCategory.REGULATORY,
        "default_channels": [DeliveryChannel.SMS, DeliveryChannel.EMAIL, DeliveryChannel.WHATSAPP],
        "description": "SEBI periodic KYC re-verification due in 15 days"
    },
    "SEBI_MANDATE_UPDATE": {
        "category": EventCategory.REGULATORY,
        "default_channels": [DeliveryChannel.EMAIL, DeliveryChannel.IN_APP],
        "description": "Regulatory circular regarding margin rules or trading limits"
    },
    "TNC_REVISED": {
        "category": EventCategory.REGULATORY,
        "default_channels": [DeliveryChannel.EMAIL],
        "description": "Brokerage terms of service and tariff schedule update"
    },

    # 5. Marketing & Value-Added Services (P5)
    "DAILY_MARKET_WRAP": {
        "category": EventCategory.PROMOTIONAL,
        "default_channels": [DeliveryChannel.PUSH, DeliveryChannel.EMAIL],
        "description": "Evening market closing wrap-up and index analysis"
    },
    "IPO_OPEN_SUBSCRIPTION": {
        "category": EventCategory.PROMOTIONAL,
        "default_channels": [DeliveryChannel.WHATSAPP, DeliveryChannel.PUSH],
        "description": "New Mainline or SME IPO open for retail bidding"
    },
    "EQUITY_RESEARCH_REPORT": {
        "category": EventCategory.PROMOTIONAL,
        "default_channels": [DeliveryChannel.EMAIL, DeliveryChannel.IN_APP],
        "description": "Fresh fundamental research coverage on Bluechip sector"
    },
    "REACTIVATION_OFFER": {
        "category": EventCategory.PROMOTIONAL,
        "default_channels": [DeliveryChannel.SMS, DeliveryChannel.EMAIL],
        "description": "Zero brokerage voucher for dormant trading accounts"
    },
    "PRODUCT_UPDATE": {
        "category": EventCategory.PROMOTIONAL,
        "default_channels": [DeliveryChannel.IN_APP, DeliveryChannel.PUSH],
        "description": "New advanced charting and trading feature release announcement"
    }
}

class FinancialNotificationEvent(BaseModel):
    event_id: str = Field(..., description="Unique event UUID")
    idempotency_key: str = Field(..., description="Deduplication key")
    event_type: str = Field(..., description="One of the 25+ valid event types")
    user_id: str = Field(..., description="Target customer identifier")
    recipient_phone: str = Field(..., description="E.164 phone number (+91...)")
    recipient_email: str = Field(..., description="Target email address")
    preferred_language: str = Field(default="en", description="Language: en, hi, mr, ta, te")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Event dynamic context")
    override_channel: Optional[DeliveryChannel] = None
