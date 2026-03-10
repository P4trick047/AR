import streamlit as st
import anthropic
import base64

# ─────────────────────────────────────────────
#  Page config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AR Denial Assistant | Aayur Solutions",
    page_icon="⚕️",
    layout="centered",
)

# ─────────────────────────────────────────────
#  Custom CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Main background */
.stApp { background-color: #070c18; color: #e2e8f0; }

/* Hide default streamlit header */
#MainMenu, footer, header { visibility: hidden; }

/* Chat message styling */
.stChatMessage {
    background: rgba(14,165,233,0.06) !important;
    border: 1px solid rgba(14,165,233,0.18) !important;
    border-radius: 14px !important;
    padding: 10px 14px !important;
}

/* Input box */
.stChatInputContainer {
    border: 1px solid rgba(14,165,233,0.35) !important;
    border-radius: 14px !important;
    background: rgba(255,255,255,0.04) !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0a0f1e !important;
    border-right: 1px solid rgba(14,165,233,0.15) !important;
}

/* Buttons */
.stButton > button {
    background: rgba(14,165,233,0.12) !important;
    border: 1px solid rgba(14,165,233,0.3) !important;
    color: #7dd3fc !important;
    border-radius: 20px !important;
    font-size: 12px !important;
    padding: 4px 14px !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: all 0.2s;
}
.stButton > button:hover {
    background: rgba(14,165,233,0.25) !important;
    border-color: #0ea5e9 !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: rgba(14,165,233,0.05) !important;
    border: 2px dashed rgba(14,165,233,0.3) !important;
    border-radius: 12px !important;
    padding: 10px !important;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: rgba(14,165,233,0.08) !important;
    border: 1px solid rgba(14,165,233,0.2) !important;
    border-radius: 10px !important;
    padding: 10px !important;
}

/* Alert / info boxes */
.stAlert { border-radius: 10px !important; }

h1, h2, h3 { color: #f0f9ff !important; }
p, li { color: #cbd5e1 !important; }
label { color: #7dd3fc !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  System prompt (full SOP knowledge)
# ─────────────────────────────────────────────
SYSTEM_PROMPT = """You are an expert AR (Accounts Receivable) Denial Resolution Assistant for Aayur Solutions, a healthcare billing company. You help billing staff quickly resolve insurance claim denials and process claims efficiently.

You have deep knowledge of the following SOP:

## DENIAL RESOLUTION PROCESSES:

### 1. CLAIM NOT FOUND
**If filed ELECTRONICALLY:**
- Check if claim was sent to correct Payer ID
- If wrong → Update correct Payer ID in Billing Software, resubmit
- If correct → Check if accepted by Clearinghouse
  - Not accepted → Work on clearinghouse/payer rejections
  - Accepted → Check if accepted by Payer
    - Yes → Contact payer, provide acceptance report/Tracking # and reprocess
    - No → Resubmit the claim

**If filed on PAPER:**
- Verify sent to correct mailing address
- If wrong → Update correct Payer ID in Billing Software
- Resubmit the claim

### 2. POLICY TERMED
- Check if patient has more than one policy in billing
- If YES → Check if other policy active on service date
  - If yes → Transfer balance to the patient
- If NO → Contact patient or Doctor's office for other insurance
  - Found active policy → Update as primary in billing software → Bill to new insurance
  - No other policy → Transfer balance to patient

### 3. DUPLICATE CLAIM
- Determine if this was a corrected claim
- If NO → Contact payer to void claim in adjudication system
- If YES → Check if submitted with Frequency Code 7 & Resubmission ID
  - If No → Resubmit with Frequency Code 7 & Resubmission ID
  - If Yes → Contact payer to get claim reprocessed

### 4. TIMELY FILING
- Check if claim submitted within payer's required timeframe
- If NO → Send query to client
- If YES → Check if you have proof of timely filing (POTF)
  - No POTF → Contact payer to confirm POTF received, send back for reprocessing
  - Have POTF → Resubmit claim with proof of timely filing

### 5. COORDINATION OF BENEFITS (COB)
- Check if claim submitted within payer timeframe
- If NO → Send query to client
- If YES → Check if proof of timely filing exists
  - No → Contact payer to confirm POTF, send back for reprocessing
  - Yes → Resubmit claim with proof of timely filing

## AR AGING BUCKETS:
- 0-30 days, 31-60 days, 61-90 days, 91-120 days, 121+ days
- Medicare claims: 15-day duration (not 30)
- New files should be pulled every 15-30 days
- Run at least 3 cycles of AR to track collections

## PHI COMPLIANCE:
- Never share patient info via text or unauthorized parties
- Always log off computers when leaving desk
- Never discuss health info in public areas

## YOUR BEHAVIOR:
- If a PDF is uploaded, prioritize reading it and answer from its content
- Ask clarifying questions to quickly diagnose denial type
- Provide clear step-by-step resolution instructions
- Be concise and action-oriented — billing staff need fast answers
- Highlight urgent actions (timely filing deadlines)
- Always end with a next-step reminder
"""

# ─────────────────────────────────────────────
#  Quick action definitions
# ─────────────────────────────────────────────
QUICK_ACTIONS = [
    ("🔍 Claim Not Found",   "How do I resolve a Claim Not Found denial?"),
    ("📋 Policy Termed",     "Patient's policy is termed, what should I do?"),
    ("🔄 Duplicate Claim",   "Got a duplicate claim denial, how to fix it?"),
    ("⏰ Timely Filing",     "Timely filing denial — what are my options?"),
    ("🤝 COB Issue",         "How do I handle a Coordination of Benefits denial?"),
    ("📊 AR Aging",          "Explain the AR aging buckets and how to prioritize work."),
]

# ─────────────────────────────────────────────
#  Session state initialisation
# ─────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pdf_data" not in st.session_state:
    st.session_state.pdf_data = None   # {"name": ..., "b64": ...}
if "quick_trigger" not in st.session_state:
    st.session_state.quick_trigger = None


# ─────────────────────────────────────────────
#  Helper — call Claude API
# ─────────────────────────────────────────────
def call_claude(user_text: str, pdf_b64: str | None = None):
    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

    # Build history from session
    api_messages = []
    for m in st.session_state.messages:
        api_messages.append({"role": m["role"], "content": m["content"]})

    # Current user turn — attach PDF if loaded
    if pdf_b64:
        user_content = [
            {
                "type": "document",
                "source": {
                    "type": "base64",
                    "media_type": "application/pdf",
                    "data": pdf_b64,
                },
            },
            {"type": "text", "text": user_text},
        ]
    else:
        user_content = user_text

    api_messages.append({"role": "user", "content": user_content})

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=api_messages,
    )
    return response.content[0].text


# ─────────────────────────────────────────────
#  Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚕️ AR Denial Assistant")
    st.markdown("*Aayur Solutions · AI-Powered*")
    st.divider()

    # ── PDF Upload ──────────────────────────
    st.markdown("### 📎 Upload PDF Document")
    st.caption("Upload any SOP, payer policy, EOB, or remit report. The AI will read and answer from it.")

    uploaded_file = st.file_uploader(
        label="Choose a PDF",
        type=["pdf"],
        label_visibility="collapsed",
    )

    if uploaded_file:
        b64 = base64.b64encode(uploaded_file.read()).decode("utf-8")
        if st.session_state.pdf_data is None or st.session_state.pdf_data["name"] != uploaded_file.name:
            st.session_state.pdf_data = {"name": uploaded_file.name, "b64": b64}
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"📄 **PDF loaded: `{uploaded_file.name}`**\n\nI've read this document. Ask me anything about it!"
            })
            st.rerun()

    if st.session_state.pdf_data:
        st.success(f"📄 Active: {st.session_state.pdf_data['name']}")
        if st.button("✕ Remove PDF"):
            st.session_state.pdf_data = None
            st.session_state.messages.append({
                "role": "assistant",
                "content": "PDF removed. I'll now answer from my built-in AR/SOP knowledge."
            })
            st.rerun()

    st.divider()

    # ── Quick actions ───────────────────────
    st.markdown("### ⚡ Quick Actions")
    for label, query in QUICK_ACTIONS:
        if st.button(label, use_container_width=True):
            st.session_state.quick_trigger = query
            st.rerun()

    st.divider()

    # ── Stats ───────────────────────────────
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Denial Types", "5")
        st.metric("AR Buckets", "5")
    with col2:
        st.metric("HIPAA", "✅")
        st.metric("PDF", "✅")

    st.divider()
    st.caption("🔒 All queries are HIPAA-compliant. Never enter real patient names or SSNs.")


# ─────────────────────────────────────────────
#  Main area header
# ─────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 10px 0 20px;">
  <h1 style="font-size:28px; margin:0;">⚕️ AR Denial Resolution Assistant</h1>
  <p style="color:#38bdf8; margin:4px 0 0; font-size:14px;">
    Aayur Solutions · Powered by Claude AI · PDF-Ready
  </p>
</div>
""", unsafe_allow_html=True)

# Active PDF notice in main area
if st.session_state.pdf_data:
    st.info(f"📄 Reading from: **{st.session_state.pdf_data['name']}** — Ask anything about this document!", icon="📎")

# Welcome message on first load
if not st.session_state.messages:
    with st.chat_message("assistant", avatar="⚕️"):
        st.markdown("""
👋 **Hello! I'm your AR Denial Resolution Assistant.**

I can help you:
- ✅ Resolve any denial — Claim Not Found, Policy Termed, Duplicate, Timely Filing, COB
- 📄 Answer questions from any **PDF you upload** via the sidebar
- 📊 Guide you through AR aging, resubmission steps, and claim prioritization

**Use the Quick Actions** in the sidebar or just describe your issue below!
        """)

# ─────────────────────────────────────────────
#  Render chat history
# ─────────────────────────────────────────────
for msg in st.session_state.messages:
    avatar = "⚕️" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ─────────────────────────────────────────────
#  Handle quick action trigger
# ─────────────────────────────────────────────
if st.session_state.quick_trigger:
    trigger_text = st.session_state.quick_trigger
    st.session_state.quick_trigger = None

    st.session_state.messages.append({"role": "user", "content": trigger_text})
    with st.chat_message("user", avatar="👤"):
        st.markdown(trigger_text)

    with st.chat_message("assistant", avatar="⚕️"):
        with st.spinner("Thinking..."):
            pdf_b64 = st.session_state.pdf_data["b64"] if st.session_state.pdf_data else None
            reply = call_claude(trigger_text, pdf_b64)
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

# ─────────────────────────────────────────────
#  Chat input
# ─────────────────────────────────────────────
pdf_placeholder = f'Ask anything about "{st.session_state.pdf_data["name"]}"...' if st.session_state.pdf_data else "Describe your denial or ask any AR question..."

if prompt := st.chat_input(pdf_placeholder):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="⚕️"):
        with st.spinner("Analyzing..."):
            pdf_b64 = st.session_state.pdf_data["b64"] if st.session_state.pdf_data else None
            reply = call_claude(prompt, pdf_b64)
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})

# ─────────────────────────────────────────────
#  Clear chat button (bottom)
# ─────────────────────────────────────────────
if st.session_state.messages:
    st.divider()
    col1, col2, col3 = st.columns([3, 2, 3])
    with col2:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
