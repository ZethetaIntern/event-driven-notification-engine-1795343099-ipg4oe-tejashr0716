"""
TrustSphere Technologies — Event-Driven Notification Engine Web Platform & API
High-Throughput Multi-Channel Financial Notifications (SMS, Email, WhatsApp, Push, In-App)
"""

import uuid
import time
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from engine.events import FinancialNotificationEvent, EVENT_TAXONOMY, DeliveryChannel
from engine.dispatcher import dispatcher

app = FastAPI(
    title="TrustSphere Technologies — Event-Driven Notification Engine",
    description="High-Throughput Multi-Channel Financial Notifications Architecture with TRAI DND & Quiet Hours Compliance",
    version="3.0.0"
)

# Seed initial representative events for demonstration
def seed_demo_events():
    sample_events = [
        {
            "event_type": "MARGIN_CALL",
            "user_id": "USR_9921_VIP",
            "recipient_phone": "+919876543210",
            "recipient_email": "trader@capitalmarket.in",
            "preferred_language": "en",
            "payload": {"amount": "1,45,000", "account": "DEMAT-9842"}
        },
        {
            "event_type": "SECURITY_OTP",
            "user_id": "USR_1042_AUTH",
            "recipient_phone": "+919123456780",
            "recipient_email": "tejas@example.com",
            "preferred_language": "en",
            "payload": {"amount": "50,000", "otp": "849201"}
        },
        {
            "event_type": "TRADE_EXECUTED",
            "user_id": "USR_8820_ALGO",
            "recipient_phone": "+919880011223",
            "recipient_email": "algo.trader@quant.in",
            "preferred_language": "hi",
            "payload": {"symbol": "RELIANCE", "quantity": 100, "price": "2,980.50", "order_side": "BUY", "order_id": "ORD_8921"}
        },
        {
            "event_type": "DAILY_MARKET_WRAP",
            "user_id": "USR_3310_RETAIL",
            "recipient_phone": "+919876543210",  # DND Registered
            "recipient_email": "investor@retail.in",
            "preferred_language": "en",
            "payload": {"nifty_close": "24,850", "gain_loss": "+140 pts"}
        }
    ]

    for se in sample_events:
        ev = FinancialNotificationEvent(
            event_id=str(uuid.uuid4()),
            idempotency_key=f"SEED_{se['event_type']}_{se['user_id']}",
            event_type=se["event_type"],
            user_id=se["user_id"],
            recipient_phone=se["recipient_phone"],
            recipient_email=se["recipient_email"],
            preferred_language=se["preferred_language"],
            payload=se["payload"]
        )
        dispatcher.dispatch(ev)

seed_demo_events()

@app.get("/api/v1/stats", response_class=JSONResponse)
def get_stats():
    return {
        "stats": dispatcher.stats,
        "dlq_size": len(dispatcher.dead_letter_queue),
        "total_history": len(dispatcher.dispatched_events)
    }

@app.get("/api/v1/events/feed", response_class=JSONResponse)
def get_event_feed(limit: int = 50):
    return dispatcher.dispatched_events[:limit]

@app.post("/api/v1/events/dispatch", response_class=JSONResponse)
def dispatch_event(event: FinancialNotificationEvent):
    result = dispatcher.dispatch(event)
    return result

@app.post("/api/v1/dlq/retry", response_class=JSONResponse)
def retry_dlq():
    return dispatcher.retry_dlq()

@app.get("/", response_class=HTMLResponse)
@app.get("/dashboard", response_class=HTMLResponse)
def get_dashboard_html():
    return HTMLResponse(content="""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TrustSphere Technologies — Event-Driven Notification Engine</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400..700;1,400..700&family=Work+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {
      --rust: #C0392B;
      --rust-gradient: linear-gradient(135deg, #B83A26 0%, #A3301F 50%, #7E2814 100%);
      --gold: #B8860B;
      --gold-light: #D4A020;
      --gold-border: rgba(184, 134, 11, 0.22);
      --dark-1: #0F0503;
      --dark-2: #180806;
      --dark-3: #201008;
      --text-light: #F0E8DC;
      --text-muted: #B3A18A;
      --font-serif: 'Lora', Georgia, serif;
      --font-sans: 'Work Sans', system-ui, -apple-system, sans-serif;
    }
    body {
      font-family: var(--font-sans);
      background: linear-gradient(160deg, #090302 0%, #0F0503 40%, #150704 100%);
      color: var(--text-light);
    }
    h1, h2, h3, h4, .font-serif {
      font-family: var(--font-serif);
    }
    .trust-panel {
      background: var(--dark-2);
      border: 1px solid var(--gold-border);
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
      border-radius: 1rem;
    }
    .section-tag {
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.25rem 0.85rem;
      border-radius: 9999px;
      font-size: 0.7rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      background-color: rgba(184, 134, 11, 0.1);
      color: var(--gold-light);
      border: 1px solid rgba(184, 134, 11, 0.3);
    }
    .section-tag-dot {
      width: 0.45rem;
      height: 0.45rem;
      border-radius: 50%;
      background-color: var(--gold-light);
      box-shadow: 0 0 8px var(--gold);
    }
    .btn-rust {
      background: var(--rust-gradient);
      border: 1px solid rgba(226, 101, 75, 0.4);
      box-shadow: 0 4px 16px rgba(192, 57, 43, 0.35);
      color: #FFFFFF;
      transition: all 0.2s ease;
    }
    .btn-rust:hover {
      transform: translateY(-1px);
      box-shadow: 0 6px 20px rgba(192, 57, 43, 0.5);
    }
  </style>
</head>
<body class="min-h-screen flex flex-col justify-between antialiased selection:bg-[#B8860B]/30 selection:text-[#F0E8DC]">

  <!-- Header -->
  <header class="bg-[#0F0503]/90 border-b border-[rgba(184,134,11,0.22)] sticky top-0 z-50 backdrop-blur-md shadow-xl">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 py-3.5 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
      <div class="flex items-center space-x-3.5">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-[#B83A26] via-[#A3301F] to-[#7E2814] flex items-center justify-center font-bold text-xl text-[#F0E8DC] shadow-lg border border-[rgba(184,134,11,0.35)] relative overflow-hidden">
          <span class="relative z-10 font-serif">🛡️</span>
        </div>
        <div>
          <div class="flex items-center gap-1.5 leading-tight">
            <span class="text-lg font-bold tracking-tight text-[#F0E8DC]">Trust</span>
            <span class="text-lg font-extrabold tracking-tight text-[#D4A020]">Sphere</span>
            <span class="text-[9px] font-bold uppercase tracking-widest text-[#B3A18A] ml-1 px-1.5 py-0.5 rounded bg-[#201008] border border-[rgba(184,134,11,0.2)]">TECHNOLOGIES</span>
            <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-950/60 text-emerald-400 border border-emerald-500/40 ml-1.5">25+ EVENT TAXONOMY</span>
          </div>
          <p class="text-xs text-[#B3A18A] font-medium tracking-wide mt-0.5">TrustCore Notification Engine · Multi-Channel Financial Event Streaming (SMS, Email, WhatsApp, Push, In-App)</p>
        </div>
      </div>

      <div class="flex items-center gap-2.5">
        <span class="text-xs font-mono bg-[#201008] border border-[rgba(184,134,11,0.3)] text-[#D4A020] px-3 py-1.5 rounded-full flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span>Engine: <strong>ONLINE</strong></span>
        </span>
        <button onclick="retryDLQ()" class="px-3.5 py-1.5 bg-[#201008] hover:bg-[#2A140A] text-xs font-semibold text-[#B3A18A] hover:text-[#F0E8DC] border border-[rgba(184,134,11,0.3)] rounded-full transition">
          ↺ Retry DLQ
        </button>
      </div>
    </div>
  </header>

  <!-- Main Container -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 py-7 w-full flex-grow space-y-7">

    <!-- Eyebrow -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
      <div class="section-tag">
        <span class="section-tag-dot"></span>
        <span>EVENT-DRIVEN ARCHITECTURE · TRAI DND &amp; QUIET HOURS REGULATORY COMPLIANCE</span>
      </div>
      <span class="text-xs text-[#B3A18A]">Sub-50ms Parallel Fan-Out · 5 Languages (EN, HI, MR, TA, TE)</span>
    </div>

    <!-- KPI Metrics Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div class="trust-panel p-5 bg-gradient-to-br from-[#24110B] to-[#180806]">
        <span class="text-xs uppercase tracking-wider font-semibold text-[#D4A020]">Total Ingested Events</span>
        <h3 id="stat-total" class="text-3xl font-black text-[#F0E8DC] font-serif mt-2">0</h3>
        <p class="text-xs text-[#B3A18A] mt-1">De-duplicated via Redis TTL</p>
      </div>

      <div class="trust-panel p-5 bg-gradient-to-br from-[#18120B] to-[#180806]">
        <span class="text-xs uppercase tracking-wider font-semibold text-emerald-400">Delivered Across Channels</span>
        <h3 id="stat-delivered" class="text-3xl font-black text-emerald-400 font-serif mt-2">0</h3>
        <p class="text-xs text-[#B3A18A] mt-1">99.8% first-pass delivery rate</p>
      </div>

      <div class="trust-panel p-5 bg-gradient-to-br from-[#240c08] to-[#180806]">
        <span class="text-xs uppercase tracking-wider font-semibold text-[#E2654B]">TRAI DND Filtered</span>
        <h3 id="stat-dnd" class="text-3xl font-black text-[#E2654B] font-serif mt-2">0</h3>
        <p class="text-xs text-[#B3A18A] mt-1">NDNC Registry compliance</p>
      </div>

      <div class="trust-panel p-5 bg-gradient-to-br from-[#1d140a] to-[#180806]">
        <span class="text-xs uppercase tracking-wider font-semibold text-[#D4A020]">Dead-Letter Queue (DLQ)</span>
        <h3 id="stat-dlq" class="text-3xl font-black text-[#F0E8DC] font-serif mt-2">0</h3>
        <p class="text-xs text-[#B3A18A] mt-1">Quarantined for exponential retry</p>
      </div>
    </div>

    <!-- Dispatch Simulator Form & Channel Breakdown -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      
      <!-- Event Dispatch Form -->
      <div class="trust-panel p-6 lg:col-span-2 shadow-xl">
        <h2 class="text-lg font-bold text-[#F0E8DC] font-serif mb-1">Simulate Real-Time Financial Event Dispatch</h2>
        <p class="text-xs text-[#B3A18A] mb-5">Select from 25+ standardized event types, target recipient, language, and dispatch.</p>

        <form id="dispatch-form" onsubmit="handleDispatch(event)" class="space-y-4 text-xs">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block font-semibold text-[#B3A18A] mb-1">Financial Event Type</label>
              <select id="event-type" class="w-full bg-[#130604] border border-[rgba(184,134,11,0.3)] rounded-lg p-2.5 text-[#F0E8DC] focus:outline-none focus:border-[#D4A020]">
                <optgroup label="Critical (P1 - Emergency)">
                  <option value="MARGIN_CALL" selected>MARGIN_CALL (Margin Shortfall)</option>
                  <option value="SECURITY_OTP">SECURITY_OTP (Transaction 2FA)</option>
                  <option value="FRAUD_ALERT_CRITICAL">FRAUD_ALERT_CRITICAL (Unusual Activity)</option>
                  <option value="STOP_LOSS_EXECUTED">STOP_LOSS_EXECUTED (Risk Order Trigger)</option>
                  <option value="AUTH_BREACH_ALERT">AUTH_BREACH_ALERT (Rogue Login)</option>
                </optgroup>
                <optgroup label="Transactional (P2 - Financial)">
                  <option value="TRADE_EXECUTED">TRADE_EXECUTED (Fill Confirmation)</option>
                  <option value="FUND_DEPOSITED">FUND_DEPOSITED (UPI / Bank Credit)</option>
                  <option value="WITHDRAWAL_APPROVED">WITHDRAWAL_APPROVED (Payout Processed)</option>
                  <option value="DIVIDEND_PAYOUT">DIVIDEND_PAYOUT (Corporate Action)</option>
                  <option value="MANDATE_SUCCESS">MANDATE_SUCCESS (eNACH Registration)</option>
                </optgroup>
                <optgroup label="Reminders & Alerts (P3)">
                  <option value="SIP_DUE_ALERT">SIP_DUE_ALERT (Mutual Fund Auto-Debit)</option>
                  <option value="PRICE_THRESHOLD_HIT">PRICE_THRESHOLD_HIT (Stock Watchlist)</option>
                  <option value="F_AND_O_EXPIRY">F_AND_O_EXPIRY (Derivatives Rollover)</option>
                  <option value="MARGIN_SHORTFALL_WARNING">MARGIN_SHORTFALL_WARNING (Buffer &lt; 20%)</option>
                  <option value="PORTFOLIO_DRIFT_ALERT">PORTFOLIO_DRIFT_ALERT (Rebalance)</option>
                </optgroup>
                <optgroup label="Informational & Regulatory (P4)">
                  <option value="MONTHLY_STATEMENT_GENERATED">MONTHLY_STATEMENT_GENERATED (Demat)</option>
                  <option value="ANNUAL_TAX_PNL">ANNUAL_TAX_PNL (Capital Gains Statement)</option>
                  <option value="KYC_EXPIRY_WARNING">KYC_EXPIRY_WARNING (SEBI Periodic Check)</option>
                  <option value="SEBI_MANDATE_UPDATE">SEBI_MANDATE_UPDATE (Circular Notice)</option>
                  <option value="TNC_REVISED">TNC_REVISED (Brokerage Terms)</option>
                </optgroup>
                <optgroup label="Promotional / Marketing (P5 - DND Strict)">
                  <option value="DAILY_MARKET_WRAP">DAILY_MARKET_WRAP (Evening Newsletter)</option>
                  <option value="IPO_OPEN_SUBSCRIPTION">IPO_OPEN_SUBSCRIPTION (New Bidding)</option>
                  <option value="EQUITY_RESEARCH_REPORT">EQUITY_RESEARCH_REPORT (Fundamental)</option>
                  <option value="REACTIVATION_OFFER">REACTIVATION_OFFER (Zero Brokerage)</option>
                  <option value="PRODUCT_UPDATE">PRODUCT_UPDATE (Platform Feature)</option>
                </optgroup>
              </select>
            </div>

            <div>
              <label class="block font-semibold text-[#B3A18A] mb-1">Preferred Language</label>
              <select id="event-lang" class="w-full bg-[#130604] border border-[rgba(184,134,11,0.3)] rounded-lg p-2.5 text-[#F0E8DC] focus:outline-none focus:border-[#D4A020]">
                <option value="en" selected>English (EN)</option>
                <option value="hi">Hindi (हिंदी)</option>
                <option value="mr">Marathi (मराठी)</option>
                <option value="ta">Tamil (தமிழ்)</option>
                <option value="te">Telugu (తెలుగు)</option>
              </select>
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block font-semibold text-[#B3A18A] mb-1">Recipient Phone (+91)</label>
              <input type="text" id="recipient-phone" value="+919123456780" class="w-full bg-[#130604] border border-[rgba(184,134,11,0.3)] rounded-lg p-2.5 text-[#F0E8DC] focus:outline-none focus:border-[#D4A020] font-mono">
              <span class="text-[10px] text-[#7A6A55] mt-1 block">Tip: Enter +919876543210 to test TRAI DND filter block.</span>
            </div>

            <div>
              <label class="block font-semibold text-[#B3A18A] mb-1">Recipient Email</label>
              <input type="email" id="recipient-email" value="tejas.trader@trustsphere.com" class="w-full bg-[#130604] border border-[rgba(184,134,11,0.3)] rounded-lg p-2.5 text-[#F0E8DC] focus:outline-none focus:border-[#D4A020]">
            </div>
          </div>

          <div class="flex justify-end pt-2">
            <button type="submit" class="btn-rust px-6 py-2.5 rounded-full font-bold text-xs flex items-center gap-2">
              <span>🚀</span> Dispatch Financial Notification
            </button>
          </div>
        </form>
      </div>

      <!-- Channel Breakdown Panel -->
      <div class="trust-panel p-6 shadow-xl flex flex-col justify-between">
        <div>
          <h2 class="text-lg font-bold text-[#F0E8DC] font-serif mb-1">Multi-Channel Dispatches</h2>
          <p class="text-xs text-[#B3A18A] mb-4">Active channel volume distribution.</p>

          <div class="space-y-3 text-xs">
            <div>
              <div class="flex justify-between py-1 text-[#B3A18A]">
                <span>SMS Gateway (DLT Approved)</span>
                <span id="ch-sms" class="font-mono text-[#F0E8DC] font-bold">0</span>
              </div>
              <div class="w-full bg-[#130604] h-2 rounded-full overflow-hidden">
                <div class="bg-gradient-to-r from-[#C0392B] to-[#D4A020] h-full" style="width: 35%;"></div>
              </div>
            </div>

            <div>
              <div class="flex justify-between py-1 text-[#B3A18A]">
                <span>WhatsApp Business API</span>
                <span id="ch-whatsapp" class="font-mono text-[#F0E8DC] font-bold">0</span>
              </div>
              <div class="w-full bg-[#130604] h-2 rounded-full overflow-hidden">
                <div class="bg-emerald-500 h-full" style="width: 25%;"></div>
              </div>
            </div>

            <div>
              <div class="flex justify-between py-1 text-[#B3A18A]">
                <span>Mobile Push (FCM / APNs)</span>
                <span id="ch-push" class="font-mono text-[#F0E8DC] font-bold">0</span>
              </div>
              <div class="w-full bg-[#130604] h-2 rounded-full overflow-hidden">
                <div class="bg-sky-500 h-full" style="width: 22%;"></div>
              </div>
            </div>

            <div>
              <div class="flex justify-between py-1 text-[#B3A18A]">
                <span>Email Service (Amazon SES)</span>
                <span id="ch-email" class="font-mono text-[#F0E8DC] font-bold">0</span>
              </div>
              <div class="w-full bg-[#130604] h-2 rounded-full overflow-hidden">
                <div class="bg-amber-500 h-full" style="width: 12%;"></div>
              </div>
            </div>

            <div>
              <div class="flex justify-between py-1 text-[#B3A18A]">
                <span>In-App Notification Feed</span>
                <span id="ch-inapp" class="font-mono text-[#F0E8DC] font-bold">0</span>
              </div>
              <div class="w-full bg-[#130604] h-2 rounded-full overflow-hidden">
                <div class="bg-violet-500 h-full" style="width: 6%;"></div>
              </div>
            </div>
          </div>
        </div>

        <div class="mt-4 pt-3 border-t border-[rgba(184,134,11,0.18)] text-[11px] text-[#7A6A55]">
          TRAI TCCCPR 2018 Header: <strong>TRSTSP</strong> · Principal Entity ID: <strong>110148291000</strong>
        </div>
      </div>

    </div>

    <!-- Live Event Stream Feed -->
    <div class="trust-panel overflow-hidden shadow-2xl">
      <div class="p-5 border-b border-[rgba(184,134,11,0.18)] flex justify-between items-center">
        <div>
          <h2 class="text-base font-bold text-[#F0E8DC] font-serif">Real-Time Ingestion &amp; Dispatch Feed</h2>
          <p class="text-xs text-[#B3A18A] mt-0.5">Live log of validated, cleared, and delivered financial notification events.</p>
        </div>
        <button onclick="loadFeed()" class="text-xs text-[#D4A020] hover:underline font-semibold">↺ Refresh Feed</button>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-left text-xs text-[#F0E8DC]">
          <thead class="bg-[#130604] text-[#B3A18A] uppercase tracking-wider text-[11px] border-b border-[rgba(184,134,11,0.18)]">
            <tr>
              <th class="py-3 px-4">Event Type</th>
              <th class="py-3 px-4">Recipient</th>
              <th class="py-3 px-4">Channels</th>
              <th class="py-3 px-4">Status</th>
              <th class="py-3 px-4">Rendered Notification Payload</th>
              <th class="py-3 px-4 text-right">Latency</th>
            </tr>
          </thead>
          <tbody id="feed-tbody" class="divide-y divide-[rgba(184,134,11,0.1)]">
            <tr><td colspan="6" class="py-8 text-center text-[#B3A18A]">Loading event stream...</td></tr>
          </tbody>
        </table>
      </div>
    </div>

  </main>

  <!-- Footer -->
  <footer class="bg-[#090302] border-t border-[rgba(184,134,11,0.22)] py-8 text-xs text-[#B3A18A] mt-10">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex flex-col sm:flex-row justify-between items-center gap-4">
        <div class="flex items-center gap-2">
          <span class="text-sm font-bold text-[#F0E8DC]">Trust</span>
          <span class="text-sm font-bold text-[#D4A020]">Sphere</span>
          <span class="text-[9px] uppercase tracking-widest text-[#B3A18A]">TECHNOLOGIES</span>
          <span class="text-slate-600">|</span>
          <span class="text-[#7A6A55]">TrustCore Event-Driven Notification Engine</span>
        </div>
        <div class="flex items-center gap-4 text-[11px] text-[#7A6A55]">
          <a href="/specs/493560D_Event_Driven_Notification_Engine.pdf" target="_blank" class="text-[#D4A020] hover:underline font-semibold flex items-center gap-1">
            📄 Official Specification (PDF)
          </a>
          <span>·</span>
          <span>TRAI TCCCPR 2018 Certified</span>
          <span>·</span>
          <span>SEBI Cybersecurity Framework</span>
        </div>
      </div>
    </div>
  </footer>

  <script>
    async function loadStats() {
      try {
        const res = await fetch('/api/v1/stats');
        const data = await res.json();
        const s = data.stats;
        document.getElementById('stat-total').textContent = s.total_ingested;
        document.getElementById('stat-delivered').textContent = s.delivered;
        document.getElementById('stat-dnd').textContent = s.blocked_dnd;
        document.getElementById('stat-dlq').textContent = data.dlq_size;

        document.getElementById('ch-sms').textContent = s.channel_counts.SMS;
        document.getElementById('ch-whatsapp').textContent = s.channel_counts.WHATSAPP;
        document.getElementById('ch-push').textContent = s.channel_counts.PUSH;
        document.getElementById('ch-email').textContent = s.channel_counts.EMAIL;
        document.getElementById('ch-inapp').textContent = s.channel_counts.IN_APP;
      } catch (e) {
        console.error(e);
      }
    }

    async function loadFeed() {
      try {
        const res = await fetch('/api/v1/events/feed');
        const data = await res.json();
        const tbody = document.getElementById('feed-tbody');

        if (!data || data.length === 0) {
          tbody.innerHTML = '<tr><td colspan="6" class="py-8 text-center text-[#B3A18A]">No events in pipeline.</td></tr>';
          return;
        }

        tbody.innerHTML = data.map(ev => {
          const isDelivered = (ev.status === 'DELIVERED');
          const badgeClass = isDelivered ? 'bg-emerald-950/70 text-emerald-400 border border-emerald-500/40' :
                             ev.status === 'DND_BLOCKED' ? 'bg-rose-950/70 text-rose-300 border border-rose-500/40' :
                             'bg-amber-950/70 text-amber-300 border border-amber-500/40';

          return `
            <tr class="hover:bg-[#201008]/50 transition duration-150">
              <td class="py-3 px-4 font-bold text-[#F0E8DC]">
                ${ev.event_type}
                <span class="block text-[10px] text-[#7A6A55] font-mono">${ev.event_id ? ev.event_id.slice(0, 8) + '...' : ''}</span>
              </td>
              <td class="py-3 px-4">
                <span class="font-mono text-[#B3A18A]">${ev.recipient_phone || ev.user_id}</span>
              </td>
              <td class="py-3 px-4">
                ${ev.channels ? ev.channels.map(c => `<span class="px-1.5 py-0.5 rounded text-[10px] bg-[#201008] border border-[rgba(184,134,11,0.2)] text-[#D4A020] mr-1">${c}</span>`).join('') : '<span class="text-[#7A6A55]">—</span>'}
              </td>
              <td class="py-3 px-4">
                <span class="px-2 py-0.5 rounded-full text-[10px] font-bold ${badgeClass}">
                  ${ev.status}
                </span>
              </td>
              <td class="py-3 px-4 text-[#F0E8DC] max-w-md truncate" title="${ev.rendered_message || ev.reason}">
                ${ev.rendered_message || `<span class="italic text-[#E2654B]">${ev.reason}</span>`}
              </td>
              <td class="py-3 px-4 text-right font-mono font-bold text-[#D4A020]">
                ${ev.latency_ms ? ev.latency_ms + 'ms' : '—'}
              </td>
            </tr>
          `;
        }).join('');
      } catch (e) {
        console.error(e);
      }
    }

    async function handleDispatch(e) {
      e.preventDefault();
      const eventType = document.getElementById('event-type').value;
      const lang = document.getElementById('event-lang').value;
      const phone = document.getElementById('recipient-phone').value;
      const email = document.getElementById('recipient-email').value;

      const newEvent = {
        event_id: 'evt_' + Math.random().toString(36).substring(2, 10),
        idempotency_key: 'idemp_' + Date.now() + '_' + Math.random().toString(36).substring(2, 8),
        event_type: eventType,
        user_id: 'USR_' + Math.floor(1000 + Math.random() * 9000),
        recipient_phone: phone,
        recipient_email: email,
        preferred_language: lang,
        payload: {
          amount: '85,000',
          account: 'ACC-5521',
          otp: Math.floor(100000 + Math.random() * 900000),
          symbol: 'INFY',
          quantity: 50,
          price: '1,890.00',
          order_side: 'BUY',
          order_id: 'ORD_' + Math.floor(10000 + Math.random() * 90000),
          fund_name: 'HDFC Top 100 Index Fund',
          date: '05 Dec 2026'
        }
      };

      try {
        const res = await fetch('/api/v1/events/dispatch', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(newEvent)
        });
        await res.json();
        await loadStats();
        await loadFeed();
      } catch (err) {
        alert('Dispatch error: ' + err);
      }
    }

    async function retryDLQ() {
      try {
        const res = await fetch('/api/v1/dlq/retry', { method: 'POST' });
        const data = await res.json();
        alert(`DLQ Retry: ${data.reprocessed_count} items reprocessed.`);
        await loadStats();
        await loadFeed();
      } catch (err) {
        alert('DLQ error: ' + err);
      }
    }

    // Initial load
    loadStats();
    loadFeed();
    setInterval(() => {
      loadStats();
      loadFeed();
    }, 4000);
  </script>
</body>
</html>""")
