# TrustSphere Technologies — Event-Driven Financial Notification Engine
> Enterprise-grade event-driven notification backbone processing 25+ financial event types across SMS, Email, WhatsApp, Mobile Push, and In-App channels with TRAI DND filtering, Quiet Hours enforcement (21:00–09:00 IST), and Dead-Letter Queue (DLQ) retry orchestration, built on the **TrustSphere Technologies** design system and **TrustCore** platform architecture.
> **Official Project Specification:** [specs/493560D_Event_Driven_Notification_Engine.pdf](specs/493560D_Event_Driven_Notification_Engine.pdf)

---

## 🛡️ Enterprise Design System & Typography

The Dispatch & Live Telemetry Dashboard implements the complete **TrustSphere Technologies** ([https://www.trustspheretechnologies.com/](https://www.trustspheretechnologies.com/)) frontend design language:

- **Typography**:
  - **Headings & Metric Dials**: `'Lora', serif` (Weights: 500, 600, 700) — authoritative, institutional, and board-ready.
  - **Body, UI, & Event Feed**: `'Work Sans', sans-serif` (Weights: 400, 500, 600, 700) — crisp tabular typography and high-frequency stream legibility.
- **Color Palette**:
  - **Obsidian Dark Surfaces**: `#090302` to `#0F0503` base charcoal, `#180806` card panels, `#201008` elevated surfaces.
  - **Gold Accents**: Core Gold `#B8860B`, Light Gold `#D4A020`, Borders `rgba(184, 134, 11, 0.22)`.
  - **Rust Red Primary**: Core Rust `#C0392B`, Button Gradient `linear-gradient(135deg, #B83A26 0%, #A3301F 50%, #7E2814 100%)`.
  - **Royal Blue**: `#2655C5` with `#5B8BF0` high-tech accent highlights.
  - **Text Colors**: Warm Cream `#F0E8DC` for primary text and headings, Muted Bronze `#B3A18A` for body text.
- **Components**:
  - TrustSphere navigation bar with metallic shield logo and wordmark.
  - Animated `.section-tag` badge with glowing amber pulse indicator: `• EVENT-DRIVEN ARCHITECTURE · TRAI DND & QUIET HOURS REGULATORY COMPLIANCE`.
  - Live throughput counters, channel delivery breakdown, and real-time dispatch form.
  - Real-time event feed table with status badges (`DELIVERED`, `DND_BLOCKED`, `QUIET_HOURS_BLOCKED`, `DLQ_QUARANTINED`).

---

## 📋 Deliverables & Specification Compliance Matrix

Adhering strictly to the official ZeTheta specification document `493560D_Event_Driven_Notification_Engine.pdf`:

| Deliverable Part | Status | Technical Implementation Details |
|---|:---:|---|
| **Event Taxonomy & Schema Engine** | **Completed** | Full Pydantic & JSON Schema validation for 25+ financial event types across Critical, Transactional, Reminder, Regulatory, and Promotional categories. |
| **TRAI DND Filtering & Compliance** | **Completed** | Indian National Do Not Call (NDNC) registry lookup blocking commercial/promotional messages while guaranteeing delivery of critical regulatory/transactional alerts. |
| **Quiet Hours Enforcement** | **Completed** | Automatic suppression of non-critical communications between 21:00 and 09:00 IST with statutory override for Margin Calls, Fraud Alerts, and 2FA OTPs. |
| **Multi-Language Template Engine** | **Completed** | Dynamic personalization pipeline supporting 5 Indian regional languages (**English, Hindi, Marathi, Tamil, Telugu**) with 160-char SMS constraint compliance. |
| **Idempotency & Deduplication Guard** | **Completed** | Distributed TTL-based idempotency key vault preventing duplicate notification dispatches during network retries. |
| **Dead-Letter Queue (DLQ) & Resilience** | **Completed** | Automatic quarantine of failed provider dispatches with exponential backoff and interactive 1-click batch DLQ retry orchestration. |
| **Real-Time Web Console & Dispatcher** | **Completed** | TrustSphere-styled interactive web dashboard with live channel volume breakdown, interactive dispatch form, and real-time event feed. |
| **Automated Verification Suite** | **Completed** | Comprehensive test suite in `test_notification_engine.py` validating taxonomy, compliance, localization, and DLQ with **100% pass rate**. |

---

## 🏛️ Event Processing Architecture

```
[Incoming Financial Event Stream] (Kafka / Redis Streams)
                │
                ▼
  [Idempotency Deduplication Guard] ──(Duplicate)──► [Drop with Audit Log]
                │ (Unique Event)
                ▼
  [Regulatory & Compliance Gate]
  ├── TRAI NDNC DND Registry Check
  └── Quiet Hours Check (21:00 - 09:00 IST)
        │
        ├── Blocked Promotional ───────────────► [Suppress & Log Compliance Audit]
        │
        └── Cleared / Statutory Override
                │
                ▼
  [Intelligent Channel Routing Engine]
  ├── Critical: Push + SMS + WhatsApp Parallel Fan-Out
  ├── Transactional: In-App + Email + SMS
  └── Informational: Email + In-App Feed
                │
                ▼
  [Multi-Language Personalization Engine]
  └── Templates: English · हिंदी · मराठी · தமிழ் · తెలుగు
                │
                ▼
  [Downstream Provider Gateways]
  ├── SMS (DLT Approved)
  ├── WhatsApp Business API
  ├── Push Notifications (FCM / APNs)
  ├── Amazon SES (Transactional Email)
  └── In-App WebSocket Feed
                │
                ├── Failed Delivery (Timeout / 5xx) ──► [Dead-Letter Queue (DLQ)]
                │                                             │
                │                                             ▼
                │                                 [Exponential Backoff Retries]
                ▼
  [Live Telemetry Dashboard & SEBI Audit Trail]
```

---

## 📊 25+ Financial Event Taxonomy

1. **Critical Alerts (P1 — 24x7 Statutory Delivery)**:
   - `MARGIN_CALL`: Immediate margin shortfall requiring collateral deposit.
   - `SECURITY_OTP`: Two-factor authorization for trade/withdrawal execution.
   - `FRAUD_ALERT_CRITICAL`: High-risk anomalous login or geographic divergence.
   - `STOP_LOSS_EXECUTED`: Risk management square-off notification.
   - `AUTH_BREACH_ALERT`: Unauthorized password reset or token hijacking alert.
2. **Transactional Ledger Alerts (P2)**:
   - `TRADE_EXECUTED`: Order fill confirmation across equities, F&O, commodities.
   - `FUND_DEPOSITED`: Bank transfer / UPI credit reflected in trading balance.
   - `WITHDRAWAL_APPROVED`: Payout settlement confirmation.
   - `DIVIDEND_PAYOUT`: Corporate action dividend credit.
   - `MANDATE_SUCCESS`: eNACH / UPI Autopay mandate active.
3. **Reminders & Alerts (P3 — Subject to Quiet Hours)**:
   - `SIP_DUE_ALERT`: Mutual fund auto-debit scheduled in 48 hours.
   - `PRICE_THRESHOLD_HIT`: User watchlist price threshold trigger.
   - `F_AND_O_EXPIRY`: Derivatives contract expiry notification.
   - `MARGIN_SHORTFALL_WARNING`: Margin buffer dropped below 20%.
   - `PORTFOLIO_DRIFT_ALERT`: Target asset allocation rebalancing alert.
4. **Informational & Regulatory Notices (P4)**:
   - `MONTHLY_STATEMENT_GENERATED`: Demat holding & transaction statement.
   - `ANNUAL_TAX_PNL`: Capital gains tax statement available.
   - `KYC_EXPIRY_WARNING`: SEBI periodic re-KYC deadline notice.
   - `SEBI_MANDATE_UPDATE`: Regulatory framework updates.
   - `TNC_REVISED`: Brokerage terms & tariff revision.
5. **Promotional & Research (P5 — Strict DND & Quiet Hours Enforcement)**:
   - `DAILY_MARKET_WRAP`: Evening post-market closing summary.
   - `IPO_OPEN_SUBSCRIPTION`: New Mainline/SME IPO bidding window open.
   - `EQUITY_RESEARCH_REPORT`: Fundamental sector research report.
   - `REACTIVATION_OFFER`: Inactive client zero-brokerage incentive.
   - `PRODUCT_UPDATE`: New feature and charting release note.

---

## 🧪 Automated Verification & Testing

```bash
# Run all automated tests
python3 test_notification_engine.py
```

### Verified Test Results
- **Test 1:** Event taxonomy verified with 25 financial event definitions across all categories.
- **Test 2:** TRAI DND filtering enforces promotional block and critical exemption.
- **Test 3:** Quiet hours compliance (21:00–09:00 IST) verified.
- **Test 4:** Multi-language template engine verified across 5 Indian regional languages (EN, HI, MR, TA, TE).
- **Test 5:** Idempotency deduplication guard verified.
- **Test 6:** Dead-Letter Queue (DLQ) quarantine and retry cycle verified.
- **Test 7:** FastAPI endpoints and TrustSphere Technologies dashboard verified.

---

## 🚀 Running the Notification Engine Locally

1. Install dependencies:
   ```bash
   pip install fastapi uvicorn pydantic httpx
   ```
2. Launch the notification server and dashboard:
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000 --reload
   ```
3. Open `http://localhost:8000` to interact with the TrustSphere dispatch console.

---

## 📄 Repository Structure

```
├── specs/
│   └── 493560D_Event_Driven_Notification_Engine.pdf # Official Requirement Spec
├── engine/
│   ├── events.py             # 25+ Event Taxonomy Definitions & Pydantic Schemas
│   ├── dnd_and_compliance.py # TRAI DND Filter & Quiet Hours Regulatory Engine
│   ├── template_engine.py    # Multi-Language Template Engine (EN, HI, MR, TA, TE)
│   └── dispatcher.py         # Multi-Channel Dispatcher, Idempotency & DLQ Engine
├── app.py                    # FastAPI Web Application & TrustSphere Console
├── test_notification_engine.py # Automated Test Automation Suite
└── README.md                 # System Architecture & Documentation
```

---
*Engineered by **Tejas H R** on the **TrustSphere Technologies** platform architecture.*
