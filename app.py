### with anthropic API ###

# import streamlit as st
# import anthropic
# import base64

# # ─────────────────────────────────────────────
# #  Page config
# # ─────────────────────────────────────────────
# st.set_page_config(
#     page_title="AR Denial Assistant | Aayur Solutions",
#     page_icon="⚕️",
#     layout="centered",
# )

# # ─────────────────────────────────────────────
# #  Custom CSS
# # ─────────────────────────────────────────────
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

# html, body, [class*="css"] {
#     font-family: 'DM Sans', sans-serif;
# }

# /* Main background */
# .stApp { background-color: #070c18; color: #e2e8f0; }

# /* Hide default streamlit header */
# #MainMenu, footer, header { visibility: hidden; }

# /* Chat message styling */
# .stChatMessage {
#     background: rgba(14,165,233,0.06) !important;
#     border: 1px solid rgba(14,165,233,0.18) !important;
#     border-radius: 14px !important;
#     padding: 10px 14px !important;
# }

# /* Input box */
# .stChatInputContainer {
#     border: 1px solid rgba(14,165,233,0.35) !important;
#     border-radius: 14px !important;
#     background: rgba(255,255,255,0.04) !important;
# }

# /* Sidebar */
# [data-testid="stSidebar"] {
#     background: #0a0f1e !important;
#     border-right: 1px solid rgba(14,165,233,0.15) !important;
# }

# /* Buttons */
# .stButton > button {
#     background: rgba(14,165,233,0.12) !important;
#     border: 1px solid rgba(14,165,233,0.3) !important;
#     color: #7dd3fc !important;
#     border-radius: 20px !important;
#     font-size: 12px !important;
#     padding: 4px 14px !important;
#     font-family: 'DM Sans', sans-serif !important;
#     transition: all 0.2s;
# }
# .stButton > button:hover {
#     background: rgba(14,165,233,0.25) !important;
#     border-color: #0ea5e9 !important;
# }

# /* File uploader */
# [data-testid="stFileUploader"] {
#     background: rgba(14,165,233,0.05) !important;
#     border: 2px dashed rgba(14,165,233,0.3) !important;
#     border-radius: 12px !important;
#     padding: 10px !important;
# }

# /* Metric cards */
# [data-testid="stMetric"] {
#     background: rgba(14,165,233,0.08) !important;
#     border: 1px solid rgba(14,165,233,0.2) !important;
#     border-radius: 10px !important;
#     padding: 10px !important;
# }

# /* Alert / info boxes */
# .stAlert { border-radius: 10px !important; }

# h1, h2, h3 { color: #f0f9ff !important; }
# p, li { color: #cbd5e1 !important; }
# label { color: #7dd3fc !important; }
# </style>
# """, unsafe_allow_html=True)

# # ─────────────────────────────────────────────
# #  System prompt (full SOP knowledge)
# # ─────────────────────────────────────────────
# SYSTEM_PROMPT = """You are an expert AR (Accounts Receivable) Denial Resolution Assistant for Aayur Solutions, a healthcare billing company. You help billing staff quickly resolve insurance claim denials and process claims efficiently.

# You have deep knowledge of the following SOP:

# ## DENIAL RESOLUTION PROCESSES:

# ### 1. CLAIM NOT FOUND
# **If filed ELECTRONICALLY:**
# - Check if claim was sent to correct Payer ID
# - If wrong → Update correct Payer ID in Billing Software, resubmit
# - If correct → Check if accepted by Clearinghouse
#   - Not accepted → Work on clearinghouse/payer rejections
#   - Accepted → Check if accepted by Payer
#     - Yes → Contact payer, provide acceptance report/Tracking # and reprocess
#     - No → Resubmit the claim

# **If filed on PAPER:**
# - Verify sent to correct mailing address
# - If wrong → Update correct Payer ID in Billing Software
# - Resubmit the claim

# ### 2. POLICY TERMED
# - Check if patient has more than one policy in billing
# - If YES → Check if other policy active on service date
#   - If yes → Transfer balance to the patient
# - If NO → Contact patient or Doctor's office for other insurance
#   - Found active policy → Update as primary in billing software → Bill to new insurance
#   - No other policy → Transfer balance to patient

# ### 3. DUPLICATE CLAIM
# - Determine if this was a corrected claim
# - If NO → Contact payer to void claim in adjudication system
# - If YES → Check if submitted with Frequency Code 7 & Resubmission ID
#   - If No → Resubmit with Frequency Code 7 & Resubmission ID
#   - If Yes → Contact payer to get claim reprocessed

# ### 4. TIMELY FILING
# - Check if claim submitted within payer's required timeframe
# - If NO → Send query to client
# - If YES → Check if you have proof of timely filing (POTF)
#   - No POTF → Contact payer to confirm POTF received, send back for reprocessing
#   - Have POTF → Resubmit claim with proof of timely filing

# ### 5. COORDINATION OF BENEFITS (COB)
# - Check if claim submitted within payer timeframe
# - If NO → Send query to client
# - If YES → Check if proof of timely filing exists
#   - No → Contact payer to confirm POTF, send back for reprocessing
#   - Yes → Resubmit claim with proof of timely filing

# ## AR AGING BUCKETS:
# - 0-30 days, 31-60 days, 61-90 days, 91-120 days, 121+ days
# - Medicare claims: 15-day duration (not 30)
# - New files should be pulled every 15-30 days
# - Run at least 3 cycles of AR to track collections

# ## PHI COMPLIANCE:
# - Never share patient info via text or unauthorized parties
# - Always log off computers when leaving desk
# - Never discuss health info in public areas

# ## YOUR BEHAVIOR:
# - If a PDF is uploaded, prioritize reading it and answer from its content
# - Ask clarifying questions to quickly diagnose denial type
# - Provide clear step-by-step resolution instructions
# - Be concise and action-oriented — billing staff need fast answers
# - Highlight urgent actions (timely filing deadlines)
# - Always end with a next-step reminder
# """

# # ─────────────────────────────────────────────
# #  Quick action definitions
# # ─────────────────────────────────────────────
# QUICK_ACTIONS = [
#     ("🔍 Claim Not Found",   "How do I resolve a Claim Not Found denial?"),
#     ("📋 Policy Termed",     "Patient's policy is termed, what should I do?"),
#     ("🔄 Duplicate Claim",   "Got a duplicate claim denial, how to fix it?"),
#     ("⏰ Timely Filing",     "Timely filing denial — what are my options?"),
#     ("🤝 COB Issue",         "How do I handle a Coordination of Benefits denial?"),
#     ("📊 AR Aging",          "Explain the AR aging buckets and how to prioritize work."),
# ]

# # ─────────────────────────────────────────────
# #  Session state initialisation
# # ─────────────────────────────────────────────
# if "messages" not in st.session_state:
#     st.session_state.messages = []
# if "pdf_data" not in st.session_state:
#     st.session_state.pdf_data = None   # {"name": ..., "b64": ...}
# if "quick_trigger" not in st.session_state:
#     st.session_state.quick_trigger = None


# # ─────────────────────────────────────────────
# #  Helper — call Claude API
# # ─────────────────────────────────────────────
# def call_claude(user_text: str, pdf_b64: str | None = None):
#     client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

#     # Build history from session
#     api_messages = []
#     for m in st.session_state.messages:
#         api_messages.append({"role": m["role"], "content": m["content"]})

#     # Current user turn — attach PDF if loaded
#     if pdf_b64:
#         user_content = [
#             {
#                 "type": "document",
#                 "source": {
#                     "type": "base64",
#                     "media_type": "application/pdf",
#                     "data": pdf_b64,
#                 },
#             },
#             {"type": "text", "text": user_text},
#         ]
#     else:
#         user_content = user_text

#     api_messages.append({"role": "user", "content": user_content})

#     response = client.messages.create(
#         model="claude-sonnet-4-20250514",
#         max_tokens=1024,
#         system=SYSTEM_PROMPT,
#         messages=api_messages,
#     )
#     return response.content[0].text


# # ─────────────────────────────────────────────
# #  Sidebar
# # ─────────────────────────────────────────────
# with st.sidebar:
#     st.markdown("## ⚕️ AR Denial Assistant")
#     st.markdown("*Aayur Solutions · AI-Powered*")
#     st.divider()

#     # ── PDF Upload ──────────────────────────
#     st.markdown("### 📎 Upload PDF Document")
#     st.caption("Upload any SOP, payer policy, EOB, or remit report. The AI will read and answer from it.")

#     uploaded_file = st.file_uploader(
#         label="Choose a PDF",
#         type=["pdf"],
#         label_visibility="collapsed",
#     )

#     if uploaded_file:
#         b64 = base64.b64encode(uploaded_file.read()).decode("utf-8")
#         if st.session_state.pdf_data is None or st.session_state.pdf_data["name"] != uploaded_file.name:
#             st.session_state.pdf_data = {"name": uploaded_file.name, "b64": b64}
#             st.session_state.messages.append({
#                 "role": "assistant",
#                 "content": f"📄 **PDF loaded: `{uploaded_file.name}`**\n\nI've read this document. Ask me anything about it!"
#             })
#             st.rerun()

#     if st.session_state.pdf_data:
#         st.success(f"📄 Active: {st.session_state.pdf_data['name']}")
#         if st.button("✕ Remove PDF"):
#             st.session_state.pdf_data = None
#             st.session_state.messages.append({
#                 "role": "assistant",
#                 "content": "PDF removed. I'll now answer from my built-in AR/SOP knowledge."
#             })
#             st.rerun()

#     st.divider()

#     # ── Quick actions ───────────────────────
#     st.markdown("### ⚡ Quick Actions")
#     for label, query in QUICK_ACTIONS:
#         if st.button(label, use_container_width=True):
#             st.session_state.quick_trigger = query
#             st.rerun()

#     st.divider()

#     # ── Stats ───────────────────────────────
#     col1, col2 = st.columns(2)
#     with col1:
#         st.metric("Denial Types", "5")
#         st.metric("AR Buckets", "5")
#     with col2:
#         st.metric("HIPAA", "✅")
#         st.metric("PDF", "✅")

#     st.divider()
#     st.caption("🔒 All queries are HIPAA-compliant. Never enter real patient names or SSNs.")


# # ─────────────────────────────────────────────
# #  Main area header
# # ─────────────────────────────────────────────
# st.markdown("""
# <div style="text-align:center; padding: 10px 0 20px;">
#   <h1 style="font-size:28px; margin:0;">⚕️ AR Denial Resolution Assistant</h1>
#   <p style="color:#38bdf8; margin:4px 0 0; font-size:14px;">
#     Aayur Solutions · Powered by Claude AI · PDF-Ready
#   </p>
# </div>
# """, unsafe_allow_html=True)

# # Active PDF notice in main area
# if st.session_state.pdf_data:
#     st.info(f"📄 Reading from: **{st.session_state.pdf_data['name']}** — Ask anything about this document!", icon="📎")

# # Welcome message on first load
# if not st.session_state.messages:
#     with st.chat_message("assistant", avatar="⚕️"):
#         st.markdown("""
# 👋 **Hello! I'm your AR Denial Resolution Assistant.**

# I can help you:
# - ✅ Resolve any denial — Claim Not Found, Policy Termed, Duplicate, Timely Filing, COB
# - 📄 Answer questions from any **PDF you upload** via the sidebar
# - 📊 Guide you through AR aging, resubmission steps, and claim prioritization

# **Use the Quick Actions** in the sidebar or just describe your issue below!
#         """)

# # ─────────────────────────────────────────────
# #  Render chat history
# # ─────────────────────────────────────────────
# for msg in st.session_state.messages:
#     avatar = "⚕️" if msg["role"] == "assistant" else "👤"
#     with st.chat_message(msg["role"], avatar=avatar):
#         st.markdown(msg["content"])

# # ─────────────────────────────────────────────
# #  Handle quick action trigger
# # ─────────────────────────────────────────────
# if st.session_state.quick_trigger:
#     trigger_text = st.session_state.quick_trigger
#     st.session_state.quick_trigger = None

#     st.session_state.messages.append({"role": "user", "content": trigger_text})
#     with st.chat_message("user", avatar="👤"):
#         st.markdown(trigger_text)

#     with st.chat_message("assistant", avatar="⚕️"):
#         with st.spinner("Thinking..."):
#             pdf_b64 = st.session_state.pdf_data["b64"] if st.session_state.pdf_data else None
#             reply = call_claude(trigger_text, pdf_b64)
#         st.markdown(reply)

#     st.session_state.messages.append({"role": "assistant", "content": reply})
#     st.rerun()

# # ─────────────────────────────────────────────
# #  Chat input
# # ─────────────────────────────────────────────
# pdf_placeholder = f'Ask anything about "{st.session_state.pdf_data["name"]}"...' if st.session_state.pdf_data else "Describe your denial or ask any AR question..."

# if prompt := st.chat_input(pdf_placeholder):
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user", avatar="👤"):
#         st.markdown(prompt)

#     with st.chat_message("assistant", avatar="⚕️"):
#         with st.spinner("Analyzing..."):
#             pdf_b64 = st.session_state.pdf_data["b64"] if st.session_state.pdf_data else None
#             reply = call_claude(prompt, pdf_b64)
#         st.markdown(reply)

#     st.session_state.messages.append({"role": "assistant", "content": reply})

# # ─────────────────────────────────────────────
# #  Clear chat button (bottom)
# # ─────────────────────────────────────────────
# if st.session_state.messages:
#     st.divider()
#     col1, col2, col3 = st.columns([3, 2, 3])
#     with col2:
#         if st.button("🗑️ Clear Chat", use_container_width=True):
#             st.session_state.messages = []
#             st.rerun()


### with groq API key ###
import streamlit as st
from groq import Groq
import pdfplumber
import io

# ─────────────────────────────────────────────
#  Page config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AR Denial Assistant | Aayur Solutions",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background-color: #070c18; color: #e2e8f0; }
#MainMenu, footer, header { visibility: hidden; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0a0f1e !important;
    border-right: 1px solid rgba(14,165,233,0.2) !important;
}
[data-testid="collapsedControl"] {
    background: #0ea5e9 !important;
    border-radius: 0 8px 8px 0 !important;
}

/* Chat messages */
.stChatMessage {
    background: rgba(14,165,233,0.06) !important;
    border: 1px solid rgba(14,165,233,0.18) !important;
    border-radius: 14px !important;
}

/* Native chat input styling */
[data-testid="stChatInput"] {
    border: 1px solid rgba(14,165,233,0.4) !important;
    border-radius: 0 18px 18px 0 !important;
    background: rgba(255,255,255,0.04) !important;
}
[data-testid="stChatInput"] textarea {
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
}
[data-testid="stChatInput"] > div {
    border-radius: 0 18px 18px 0 !important;
    background: rgba(10,15,30,0.98) !important;
    border: none !important;
}
/* Send button inside chat input */
[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, #0ea5e9, #0284c7) !important;
    border-radius: 50% !important;
    color: white !important;
}

/* Plus upload button column */
div[data-testid="stColumn"]:first-child [data-testid="stFileUploader"] {
    margin: 0 !important;
}
div[data-testid="stColumn"]:first-child [data-testid="stFileUploader"] section {
    border: 2px solid rgba(14,165,233,0.45) !important;
    background: rgba(14,165,233,0.12) !important;
    border-radius: 18px 0 0 18px !important;
    padding: 0 !important;
    min-height: 52px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
}
div[data-testid="stColumn"]:first-child [data-testid="stFileUploader"] section:hover {
    background: rgba(14,165,233,0.25) !important;
    border-color: #38bdf8 !important;
}
/* Hide the default file uploader text, show only icon */
div[data-testid="stColumn"]:first-child [data-testid="stFileUploaderDropzoneInstructions"] {
    display: none !important;
}
div[data-testid="stColumn"]:first-child [data-testid="stFileUploader"] section::before {
    content: "＋";
    color: #0ea5e9;
    font-size: 26px;
    font-weight: 300;
    line-height: 1;
}
div[data-testid="stColumn"]:first-child small { display: none !important; }
div[data-testid="stColumn"]:first-child [data-testid="stFileUploaderDropzone"] > div { display: none !important; }
div[data-testid="stColumn"]:first-child [data-testid="baseButton-secondary"] { display: none !important; }

/* Bottom input area wrapper */
.input-wrapper {
    position: fixed;
    bottom: 0; left: 0; right: 0;
    z-index: 200;
    background: linear-gradient(to top, #070c18 85%, transparent);
    padding: 10px 16px 18px;
}

/* Sidebar buttons */
.stButton > button {
    background: rgba(14,165,233,0.12) !important;
    border: 1px solid rgba(14,165,233,0.3) !important;
    color: #7dd3fc !important;
    border-radius: 20px !important;
    font-size: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: all 0.2s;
}
.stButton > button:hover {
    background: rgba(14,165,233,0.28) !important;
    border-color: #0ea5e9 !important;
    color: #fff !important;
}

/* Drag overlay */
#drag-overlay {
    display: none;
    position: fixed;
    inset: 0;
    z-index: 9999;
    background: rgba(7,12,24,0.88);
    backdrop-filter: blur(8px);
    align-items: center;
    justify-content: center;
    flex-direction: column;
    gap: 16px;
    pointer-events: none;
}
#drag-overlay.active { display: flex !important; }
.drop-box {
    border: 3px dashed #0ea5e9;
    border-radius: 24px;
    padding: 60px 100px;
    text-align: center;
    background: rgba(14,165,233,0.08);
    animation: pulseBorder 1.4s ease-in-out infinite;
    pointer-events: none;
}
@keyframes pulseBorder {
    0%,100% { border-color: #0ea5e9; box-shadow: 0 0 0 0 rgba(14,165,233,0.4); }
    50%      { border-color: #38bdf8; box-shadow: 0 0 0 14px rgba(14,165,233,0); }
}

[data-testid="stMetricValue"] { color: #38bdf8 !important; }
[data-testid="stMetricLabel"] { color: #94a3b8 !important; }
.stAlert { border-radius: 10px !important; }
h1,h2,h3 { color: #f0f9ff !important; }
p, li { color: #cbd5e1 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  System prompt
# ─────────────────────────────────────────────
SYSTEM_PROMPT = """You are an expert AR (Accounts Receivable) Denial Resolution Assistant for Aayur Solutions. Help billing staff resolve claim denials fast.

DENIAL PROCESSES:
1. CLAIM NOT FOUND — Electronic: check Payer ID → clearinghouse → payer acceptance → resubmit. Paper: check mailing address → update Payer ID → resubmit.
2. POLICY TERMED — Check for other active policy on service date. Found → bill new insurance. Not found → transfer to patient.
3. DUPLICATE CLAIM — Corrected: check Freq Code 7 & Resubmission ID → resubmit or contact payer. Not corrected: void in adjudication.
4. TIMELY FILING — Late: query client. On time: check POTF → resubmit with proof or contact payer.
5. COB — Same flow as Timely Filing.

AR AGING: 0-30 | 31-60 | 61-90 | 91-120 | 121+ days. Medicare = 15 days. Pull files every 15-30 days. Run 3 AR cycles.

If PDF content is provided, answer from it first. Be concise, step-by-step, action-oriented."""

QUICK_ACTIONS = [
    ("🔍 Claim Not Found",  "How do I resolve a Claim Not Found denial?"),
    ("📋 Policy Termed",    "Patient's policy is termed, what should I do?"),
    ("🔄 Duplicate Claim",  "Got a duplicate claim denial, how to fix it?"),
    ("⏰ Timely Filing",    "Timely filing denial — what are my options?"),
    ("🤝 COB Issue",        "How do I handle a Coordination of Benefits denial?"),
    ("📊 AR Aging",         "Explain the AR aging buckets and how to prioritize work."),
]

# ─────────────────────────────────────────────
#  Session state
# ─────────────────────────────────────────────
for key, val in {
    "messages": [], "pdf_text": None,
    "pdf_name": None, "quick_trigger": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ─────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────
def extract_pdf_text(file_bytes: bytes) -> str:
    parts = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for i, page in enumerate(pdf.pages):
            t = page.extract_text()
            if t:
                parts.append(f"--- Page {i+1} ---\n{t}")
    return "\n\n".join(parts) if parts else "No readable text found in PDF."


def call_groq(user_text: str, pdf_text: str | None = None) -> str:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    system = SYSTEM_PROMPT
    if pdf_text:
        system += f"\n\nUPLOADED PDF CONTENT:\n{pdf_text[:12000]}"
    history = st.session_state.messages[-10:]
    api_msgs = [{"role": m["role"], "content": m["content"]} for m in history]
    api_msgs.append({"role": "user", "content": user_text})
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system}] + api_msgs,
        max_tokens=1024,
        temperature=0.3,
    )
    return resp.choices[0].message.content


def handle_pdf(uploaded):
    """Process a newly uploaded PDF file."""
    if uploaded and st.session_state.pdf_name != uploaded.name:
        with st.spinner("📖 Reading PDF..."):
            extracted = extract_pdf_text(uploaded.read())
        st.session_state.pdf_text = extracted
        st.session_state.pdf_name = uploaded.name
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"📄 **PDF loaded: `{uploaded.name}`**\n\nRead {len(extracted):,} characters. Ask me anything about it!"
        })
        st.rerun()


# ═════════════════════════════════════════════
#  SIDEBAR
# ═════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="padding:0 4px 10px;">
        <div style="font-size:26px;">⚕️</div>
        <div style="color:#f0f9ff;font-weight:700;font-size:17px;">AR Denial Assistant</div>
        <div style="color:#38bdf8;font-size:11px;margin-top:2px;">Aayur Solutions · Groq AI</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;
                background:rgba(34,197,94,0.1);border:1px solid rgba(34,197,94,0.3);
                border-radius:8px;padding:6px 11px;">
        <div style="width:8px;height:8px;border-radius:50%;background:#22c55e;
                    box-shadow:0 0 6px #22c55e;"></div>
        <span style="color:#86efac;font-size:12px;font-weight:500;">Assistant Online</span>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.pdf_name:
        st.success(f"📄 {st.session_state.pdf_name}")
        if st.button("✕ Remove PDF", use_container_width=True):
            st.session_state.pdf_text = None
            st.session_state.pdf_name = None
            st.session_state.messages.append({
                "role": "assistant",
                "content": "PDF removed. Using built-in AR/SOP knowledge now."
            })
            st.rerun()

    st.divider()
    st.markdown("### ⚡ Quick Actions")
    for label, query in QUICK_ACTIONS:
        if st.button(label, use_container_width=True, key=f"qa_{label}"):
            st.session_state.quick_trigger = query
            st.rerun()

    st.divider()
    c1, c2 = st.columns(2)
    c1.metric("Denials", "5 Types")
    c2.metric("Buckets", "5")
    c1.metric("PDF", "✅")
    c2.metric("HIPAA", "✅")
    st.divider()
    st.caption("⚡ llama-3.3-70b via Groq")
    st.caption("🔒 Never enter real patient SSNs.")


# ═════════════════════════════════════════════
#  MAIN AREA
# ═════════════════════════════════════════════
st.markdown("""
<div style="text-align:center;padding:8px 0 14px;">
    <h1 style="font-size:24px;margin:0;letter-spacing:-0.02em;">
        ⚕️ AR Denial Resolution Assistant
    </h1>
    <p style="color:#38bdf8;margin:3px 0 0;font-size:13px;">
        Aayur Solutions · Powered by Groq AI · PDF-Ready
    </p>
</div>
""", unsafe_allow_html=True)

if st.session_state.pdf_name:
    st.info(f"📎 **PDF active:** {st.session_state.pdf_name} — Ask anything about this document!", icon="📄")

# Welcome message
if not st.session_state.messages:
    with st.chat_message("assistant", avatar="⚕️"):
        st.markdown("""
👋 **Welcome! I'm your AR Denial Resolution Assistant.**

- ✅ Resolve any denial — Claim Not Found, Policy Termed, Duplicate, Timely Filing, COB
- 📄 **Upload a PDF** using the **＋ button** beside the text box, or **drag & drop** anywhere
- 📊 AR aging, resubmission steps, claim prioritization

👈 Use **Quick Actions** in the sidebar, or type your question below!
        """)

# Chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="⚕️" if msg["role"] == "assistant" else "👤"):
        st.markdown(msg["content"])

# Quick action trigger
if st.session_state.quick_trigger:
    trigger = st.session_state.quick_trigger
    st.session_state.quick_trigger = None
    st.session_state.messages.append({"role": "user", "content": trigger})
    with st.chat_message("user", avatar="👤"):
        st.markdown(trigger)
    with st.chat_message("assistant", avatar="⚕️"):
        with st.spinner("Thinking..."):
            reply = call_groq(trigger, st.session_state.pdf_text)
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

# Spacer so chat content isn't hidden behind fixed bar
st.markdown("<div style='height:100px'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  Drag & Drop Overlay (pure HTML, no Streamlit widgets)
# ─────────────────────────────────────────────
st.markdown("""
<div id="drag-overlay">
    <div class="drop-box">
        <div style="font-size:52px;margin-bottom:10px;">📄</div>
        <div style="color:#f0f9ff;font-size:20px;font-weight:700;margin-bottom:4px;">
            Drop your PDF here
        </div>
        <div style="color:#7dd3fc;font-size:13px;">
            Release to upload and read the document
        </div>
    </div>
    <div style="color:#475569;font-size:11px;">PDF files only · Max 10MB</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  BOTTOM INPUT BAR  ─  native Streamlit widgets
#  Layout: [＋ uploader col] [chat input col]
# ─────────────────────────────────────────────
st.markdown("""
<div style="position:fixed;bottom:0;left:0;right:0;z-index:200;
            background:linear-gradient(to top,#070c18 80%,transparent);
            padding:8px 16px 14px;">
  <div style="max-width:900px;margin:0 auto;">
""", unsafe_allow_html=True)

bar_col1, bar_col2 = st.columns([1, 11])

with bar_col1:
    # ＋ button = styled file uploader
    plus_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"],
        label_visibility="collapsed",
        key="plus_uploader",
    )

with bar_col2:
    prompt = st.chat_input(
        placeholder="Type your AR question or drag & drop a PDF anywhere…",
        key="main_chat_input",
    )

st.markdown("</div></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  Process inputs
# ─────────────────────────────────────────────
handle_pdf(plus_file)

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    with st.chat_message("assistant", avatar="⚕️"):
        with st.spinner("Analyzing..."):
            reply = call_groq(prompt, st.session_state.pdf_text)
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})

# Clear chat
if st.session_state.messages:
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([3, 2, 3])
    with col2:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

# ─────────────────────────────────────────────
#  JavaScript — drag & drop only
#  (bridges dropped file to the native st.file_uploader)
# ─────────────────────────────────────────────
st.markdown("""
<script>
(function () {
    // Find the Streamlit file uploader input
    function getSTInput() {
        const inputs = document.querySelectorAll('input[type="file"][accept="application/pdf"]');
        return inputs.length ? inputs[0] : null;
    }

    function pushFileToStreamlit(file) {
        const inp = getSTInput();
        if (!inp) return;
        const dt = new DataTransfer();
        dt.items.add(file);
        inp.files = dt.files;
        inp.dispatchEvent(new Event('change', { bubbles: true }));
    }

    const overlay = document.getElementById('drag-overlay');
    let counter = 0;

    document.addEventListener('dragenter', (e) => {
        if ([...e.dataTransfer.types].includes('Files')) {
            counter++;
            if (overlay) overlay.classList.add('active');
        }
    });
    document.addEventListener('dragleave', () => {
        counter = Math.max(0, counter - 1);
        if (counter === 0 && overlay) overlay.classList.remove('active');
    });
    document.addEventListener('dragover', (e) => e.preventDefault());
    document.addEventListener('drop', (e) => {
        e.preventDefault();
        counter = 0;
        if (overlay) overlay.classList.remove('active');
        const file = e.dataTransfer.files[0];
        if (!file) return;
        if (file.type !== 'application/pdf') {
            alert('Please drop a PDF file.');
            return;
        }
        pushFileToStreamlit(file);
    });
})();
</script>
""", unsafe_allow_html=True)
