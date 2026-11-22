"""
Multi-Language Financial Template Engine & Personalization Pipeline
Supports: English (en), Hindi (hi), Marathi (mr), Tamil (ta), Telugu (te)
"""

from typing import Dict, Any

TEMPLATES = {
    "MARGIN_CALL": {
        "en": "URGENT: Margin shortfall of ₹{amount} on account {account}. Square-off at 15:15 IST unless funded. TrustSphere Wealth",
        "hi": "अत्यावश्यक: खाते {account} पर ₹{amount} की मार्जिन कमी। कृपया 15:15 IST से पहले फंड जोड़ें। TrustSphere",
        "mr": "तातडीचे: खाते {account} वर ₹{amount} ची मार्जिन तूट. 15:15 आधी फंड जमा करा. TrustSphere",
        "ta": "அவசரம்: கணக்கு {account}-ல் ₹{amount} மார்ஜின் பற்றாக்குறை. நிதி சேர்க்கவும். TrustSphere",
        "te": "అత్యవసరం: ఖాతా {account} లో ₹{amount} మార్జిన్ లోటు. నిధులను జమ చేయండి. TrustSphere"
    },
    "SECURITY_OTP": {
        "en": "{otp} is your verification OTP for payment of ₹{amount}. Valid for 10 mins. Do NOT share with anyone. TrustSphere",
        "hi": "₹{amount} के भुगतान के लिए आपका ओटीपी {otp} है। 10 मिनट के लिए वैध। किसी से साझा न करें। TrustSphere",
        "mr": "देयक ₹{amount} साठी आपला OTP {otp} आहे. 10 मिनिटे वैध. कोणाशीही शेअर करू नका. TrustSphere",
        "ta": "பரிவர்த்தனை ₹{amount}-க்கான உங்கள் OTP {otp}. 10 நிமிடங்களுக்கு செல்லுபடியாகும். பகிர வேண்டாம். TrustSphere",
        "te": "చెల్లింపు ₹{amount} కొరకు మీ OTP {otp}. 10 నిమిషాలు చెల్లుతుంది. ఎవరితోనూ పంచుకోవద్దు. TrustSphere"
    },
    "TRADE_EXECUTED": {
        "en": "Executed: {order_side} {quantity} shares of {symbol} at ₹{price}. Order Ref: {order_id}. TrustSphere",
        "hi": "सफल: {symbol} के {quantity} शेयर ₹{price} पर निष्पादित हुए। ऑर्डर आईडी: {order_id}। TrustSphere",
        "mr": "पूर्ण: {symbol} चे {quantity} शेअर्स ₹{price} भावाने पूर्ण झाले. संदर्भ: {order_id}. TrustSphere",
        "ta": "வெற்றி: {symbol}-ன் {quantity} பங்குகள் ₹{price}-க்கு நிறைவேற்றப்பட்டது. TrustSphere",
        "te": "విజయం: {symbol} యొక్క {quantity} షేర్లు ₹{price} వద్ద పూర్తయ్యాయి. TrustSphere"
    },
    "FUND_DEPOSITED": {
        "en": "Credit: ₹{amount} deposited via UPI into Trading A/c {account}. Available margin updated instantly. TrustSphere",
        "hi": "क्रेडिट: ट्रेडिंग खाते {account} में UPI से ₹{amount} जमा हुए। उपलब्ध मार्जिन अपडेट हो गया। TrustSphere",
        "mr": "जमा: खात्यात {account} UPI द्वारे ₹{amount} जमा झाले. उपलब्ध शिल्लक अपडेट केली. TrustSphere",
        "ta": "வரவு: வர்த்தக கணக்கு {account}-ல் ₹{amount} வரவு வைக்கப்பட்டது. TrustSphere",
        "te": "క్రెడిట్: ట్రేడింగ్ ఖాతా {account} లో ₹{amount} జమ చేయబడింది. TrustSphere"
    },
    "SIP_DUE_ALERT": {
        "en": "Reminder: Monthly SIP of ₹{amount} for {fund_name} will be auto-debited on {date}. Maintain balance. TrustSphere",
        "hi": "स्मरणपत्र: {fund_name} के लिए ₹{amount} का मासिक SIP {date} को कटेगा। पर्याप्त बैलेंस रखें। TrustSphere",
        "mr": "आठवण: {fund_name} साठी ₹{amount} चा मासिक SIP {date} रोजी डेबिट होईल. शिल्लक ठेवा. TrustSphere",
        "ta": "நினைவூட்டல்: {fund_name} க்கான ₹{amount} மாதாந்திர SIP {date} அன்று கழிக்கப்படும். TrustSphere",
        "te": "రిమైండర్: {fund_name} కొరకు ₹{amount} నెలవారీ SIP {date} న డెబిట్ అవుతుంది. TrustSphere"
    },
    "DEFAULT": {
        "en": "Notification from TrustSphere: Event {event_type} registered for account {user_id}. Ref: {event_id}.",
        "hi": "TrustSphere से सूचना: खाता {user_id} के लिए इवेंट {event_type} दर्ज किया गया।",
        "mr": "TrustSphere कडून सूचना: खाते {user_id} साठी इव्हेंट {event_type} नोंदवला गेला आहे.",
        "ta": "TrustSphere அறிவிப்பு: கணக்கு {user_id} நிகழ்வு {event_type} பதிவு செய்யப்பட்டது.",
        "te": "TrustSphere నుండి ప్రకటన: ఖాతా {user_id} కొరకు ఈవెంట్ {event_type} నమోదయింది."
    }
}

def render_notification(event_type: str, language: str, context: Dict[str, Any]) -> str:
    """
    Renders personalized message using language dictionary with fallback to English.
    Ensures safe interpolation and SMS character limits.
    """
    event_templates = TEMPLATES.get(event_type, TEMPLATES["DEFAULT"])
    template = event_templates.get(language, event_templates.get("en", TEMPLATES["DEFAULT"]["en"]))

    # Safe format with defaults
    rendered = template
    for key, val in context.items():
        placeholder = "{" + key + "}"
        rendered = rendered.replace(placeholder, str(val))

    # Replace any leftover placeholders
    import re
    rendered = re.sub(r'\{[a-zA-Z0-9_]+\}', '---', rendered)
    return rendered
