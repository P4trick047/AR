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

st.set_page_config(
    page_title="AR Denial Assistant | Aayur Solutions",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Lato', sans-serif;
    font-size: 15px;
}

/* ── App background ── */
.stApp { background-color: #212121; color: #ececec; }
#MainMenu, footer, header { visibility: hidden; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #171717 !important;
    border-right: 1px solid #2e2e2e !important;
}
[data-testid="stSidebar"] * { color: #c4c4c4 !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #ffffff !important; }
[data-testid="collapsedControl"] {
    background: #2a2a2a !important;
}
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: none !important;
    color: #b0b0b0 !important;
    text-align: left !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    padding: 8px 12px !important;
    width: 100% !important;
    transition: background 0.15s;
    font-family: 'Lato', sans-serif !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: #2a2a2a !important;
    color: #ffffff !important;
}
[data-testid="stSidebar"] hr { border-color: #2e2e2e !important; }
[data-testid="stSidebar"] [data-testid="stMetric"] {
    background: #1e1e1e !important;
    border: 1px solid #2e2e2e !important;
    border-radius: 8px !important;
    padding: 8px !important;
}
[data-testid="stSidebar"] [data-testid="stMetricValue"] { color: #ffffff !important; }
[data-testid="stSidebar"] [data-testid="stMetricLabel"] { color: #666 !important; }
[data-testid="stSidebar"] .stFileUploader section {
    background: #1e1e1e !important;
    border: 1.5px dashed #3a3a3a !important;
    border-radius: 10px !important;
    padding: 12px !important;
}
[data-testid="stSidebar"] .stFileUploader section:hover {
    border-color: #666 !important;
    background: #252525 !important;
}

/* ── Main content area ── */
.block-container {
    max-width: 780px !important;
    margin: 0 auto !important;
    padding: 0 20px 180px !important;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 0 !important;
    margin-bottom: 22px !important;
    box-shadow: none !important;
}

/* User bubble — right-aligned dark pill */
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    display: flex !important;
    justify-content: flex-end !important;
}
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) .stMarkdown {
    background: #2f2f2f !important;
    border: 1px solid #3a3a3a !important;
    border-radius: 18px 18px 4px 18px !important;
    padding: 12px 18px !important;
    max-width: 72% !important;
    color: #ececec !important;
    font-size: 15px !important;
    line-height: 1.65 !important;
}

/* Assistant — no bubble, plain text */
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown {
    background: transparent !important;
    padding: 0 !important;
    font-size: 15px !important;
    line-height: 1.8 !important;
    color: #ececec !important;
}
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown p {
    margin-bottom: 10px !important;
    color: #dedede !important;
}
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown strong {
    color: #ffffff !important;
    font-weight: 700 !important;
}
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown ul,
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown ol {
    padding-left: 20px !important;
    margin-bottom: 10px !important;
}
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown li {
    margin-bottom: 5px !important;
    color: #dedede !important;
}
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown code {
    background: #2a2a2a !important;
    border: 1px solid #3a3a3a !important;
    border-radius: 5px !important;
    padding: 1px 6px !important;
    font-size: 13px !important;
    color: #f9a825 !important;
}
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown h3 {
    color: #ffffff !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    margin: 14px 0 4px !important;
}

/* Avatars */
[data-testid="chatAvatarIcon-assistant"] {
    background: #d97706 !important;
    border-radius: 50% !important;
    width: 32px !important; height: 32px !important;
    font-size: 16px !important;
    flex-shrink: 0 !important;
}
[data-testid="chatAvatarIcon-user"] {
    background: #4f46e5 !important;
    border-radius: 50% !important;
    width: 32px !important; height: 32px !important;
    font-size: 14px !important;
    flex-shrink: 0 !important;
}

/* ── Input bar ── */
[data-testid="stChatInput"] > div {
    background: #2f2f2f !important;
    border: 1px solid #3e3e3e !important;
    border-radius: 16px !important;
    box-shadow: 0 2px 16px rgba(0,0,0,0.4) !important;
    padding: 4px 8px !important;
}
[data-testid="stChatInput"] > div:focus-within {
    border-color: #555 !important;
    box-shadow: 0 2px 22px rgba(0,0,0,0.5) !important;
}
[data-testid="stChatInput"] textarea {
    font-family: 'Lato', sans-serif !important;
    font-size: 15px !important;
    color: #ececec !important;
    background: transparent !important;
    caret-color: #d97706 !important;
    padding: 10px 12px !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #666 !important;
}
[data-testid="stChatInput"] button[kind="primary"] {
    background: #d97706 !important;
    border-radius: 10px !important;
    color: white !important;
    border: none !important;
}
[data-testid="stChatInput"] button[kind="primary"]:hover {
    background: #b45309 !important;
}
[data-testid="stChatInput"] button[kind="primary"]:disabled {
    background: #2e2e2e !important;
    color: #555 !important;
}

/* ── 📎 Plus column uploader ── */
.plus-col [data-testid="stFileUploader"] section {
    border: none !important;
    background: transparent !important;
    border-radius: 10px !important;
    padding: 4px !important;
    min-height: 44px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
    transition: background 0.15s !important;
}
.plus-col [data-testid="stFileUploader"] section:hover {
    background: #2e2e2e !important;
}
.plus-col [data-testid="stFileUploaderDropzoneInstructions"],
.plus-col small,
.plus-col [data-testid="stFileUploaderDropzone"] > div,
.plus-col [data-testid="baseButton-secondary"] { display: none !important; }
.plus-col [data-testid="stFileUploader"] section::before {
    content: "📎";
    font-size: 20px;
    line-height: 1;
}
.plus-col { width: 44px !important; flex-shrink: 0 !important; }

/* ── Fixed bottom input wrapper ── */
section.main {
    padding-bottom: 0 !important;
}
.fixed-bar-wrapper {
    position: fixed;
    bottom: 0; left: 0; right: 0;
    z-index: 1000;
    background: linear-gradient(to top, #212121 75%, transparent);
    padding: 10px 20px 20px;
    display: flex;
    justify-content: center;
}
.fixed-bar-inner {
    width: 100%;
    max-width: 780px;
    display: flex;
    align-items: flex-end;
    gap: 6px;
    background: #2f2f2f;
    border: 1px solid #3e3e3e;
    border-radius: 16px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.5);
    padding: 6px 8px 6px 6px;
    transition: border-color 0.2s;
}
.fixed-bar-inner:focus-within {
    border-color: #555;
}

/* Hide default Streamlit chat input (we reposition it) */
[data-testid="stChatInput"] {
    position: static !important;
    transform: none !important;
    border: none !important;
    box-shadow: none !important;
    background: transparent !important;
    padding: 0 !important;
    flex: 1;
}
[data-testid="stChatInput"] > div {
    border: none !important;
    box-shadow: none !important;
    background: transparent !important;
    border-radius: 0 !important;
    padding: 0 !important;
}

/* Misc */
.stAlert { border-radius: 10px !important; }
p, li { color: #dedede !important; }
h1, h2, h3 { color: #ffffff !important; font-weight: 600 !important; }
[data-testid="stMarkdownContainer"] hr { border-color: #2e2e2e !important; margin: 20px 0 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  System prompt
# ─────────────────────────────────────────────
SYSTEM_PROMPT = """You are an expert AR (Accounts Receivable) Denial Resolution Assistant for Aayur Solutions. Help billing staff resolve claim denials fast and accurately.

DENIAL RESOLUTION PROCESSES:

1. CLAIM NOT FOUND
   Electronic: check Payer ID → update if wrong & resubmit. If right → clearinghouse accepted? If no → work rejections. If yes → payer accepted? If yes → contact payer with tracking# to reprocess. If no → resubmit.
   Paper: mailing address correct? If no → update & resubmit. If yes → resubmit.

2. POLICY TERMED
   Another policy in billing? If yes → active on service date? Yes → transfer balance to patient. No → contact patient/doctor for other insurance → found? Update as primary & bill. Not found → transfer to patient.

3. DUPLICATE CLAIM
   Corrected claim? If no → contact payer to void in adjudication. If yes → Freq Code 7 & Resubmission ID used? If no → resubmit with those. If yes → contact payer to reprocess.

4. TIMELY FILING
   Within payer timeframe? If no → query client. If yes → have POTF? If no → contact payer to confirm & reprocess. If yes → resubmit with POTF.

5. COORDINATION OF BENEFITS (COB) — Same flow as Timely Filing.

AR AGING: 0-30 | 31-60 | 61-90 | 91-120 | 121+ days. Medicare = 15 days. Pull files every 15-30 days. Run 3 AR cycles minimum.

BEHAVIOR: If PDF content is provided, prioritize it. Be clear, step-by-step, warm, and concise. Use markdown formatting."""

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
        system += f"\n\nUPLOADED PDF CONTENT:\n{pdf_text[:12000]}\n\nAnswer primarily from this document."
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
    if uploaded and st.session_state.pdf_name != uploaded.name:
        with st.spinner("Reading PDF..."):
            extracted = extract_pdf_text(uploaded.read())
        st.session_state.pdf_text = extracted
        st.session_state.pdf_name = uploaded.name
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"I've read **{uploaded.name}** ({len(extracted):,} characters extracted). What would you like to know about it?"
        })
        st.rerun()


# ═════════════════════════════════════════════
#  SIDEBAR
# ═════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="padding:16px 4px 20px;display:flex;align-items:center;gap:10px;">
        <div style="width:34px;height:34px;border-radius:8px;background:#d97706;
                    display:flex;align-items:center;justify-content:center;
                    font-size:18px;flex-shrink:0;">⚕️</div>
        <div>
            <div style="color:#fff;font-weight:700;font-size:14px;line-height:1.2;">AR Denial Assistant</div>
            <div style="color:#555;font-size:11px;">Aayur Solutions</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("✏️  New conversation", use_container_width=True, key="new_chat"):
        st.session_state.messages = []
        st.session_state.pdf_text = None
        st.session_state.pdf_name = None
        st.rerun()

    st.divider()

    # PDF status in sidebar
    st.markdown("<div style='color:#555;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;padding:0 4px;'>Documents</div>", unsafe_allow_html=True)

    side_pdf = st.file_uploader(
        "Upload PDF", type=["pdf"],
        label_visibility="collapsed",
        key="sidebar_pdf"
    )
    handle_pdf(side_pdf)

    if st.session_state.pdf_name:
        st.markdown(f"""
        <div style="background:#1e1e1e;border:1px solid #333;border-radius:8px;
                    padding:8px 10px;margin-top:6px;display:flex;align-items:center;gap:8px;">
            <span style="font-size:15px;">📄</span>
            <div style="flex:1;min-width:0;">
                <div style="color:#e5e5e5;font-size:12px;font-weight:500;
                            white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
                    {st.session_state.pdf_name}
                </div>
                <div style="color:#555;font-size:10px;">Active document</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("✕ Remove document", use_container_width=True, key="remove_pdf"):
            st.session_state.pdf_text = None
            st.session_state.pdf_name = None
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Document removed. I'll answer from my built-in AR knowledge now."
            })
            st.rerun()

    st.divider()

    st.markdown("<div style='color:#555;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px;padding:0 4px;'>Quick Actions</div>", unsafe_allow_html=True)
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

    st.markdown("""
    <div style="margin-top:16px;padding:0 4px;">
        <div style="color:#444;font-size:11px;">⚡ llama-3.3-70b via Groq</div>
        <div style="color:#444;font-size:11px;margin-top:3px;">🔒 Never enter real patient SSNs</div>
    </div>
    """, unsafe_allow_html=True)


# ═════════════════════════════════════════════
#  MAIN CHAT AREA
# ═════════════════════════════════════════════

# PDF active badge
if st.session_state.pdf_name:
    st.markdown(f"""
    <div style="display:flex;justify-content:center;padding:12px 0 4px;">
        <div style="display:inline-flex;align-items:center;gap:6px;
                    background:#2a2200;border:1px solid #5a3e00;
                    border-radius:20px;padding:4px 14px;
                    font-size:12px;color:#fbbf24;font-weight:500;">
            📎 {st.session_state.pdf_name}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Empty state ────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div style="display:flex;flex-direction:column;align-items:center;
                justify-content:center;min-height:52vh;text-align:center;
                padding:40px 20px 0;">
        <div style="width:58px;height:58px;border-radius:14px;background:#d97706;
                    display:flex;align-items:center;justify-content:center;
                    font-size:28px;margin-bottom:22px;
                    box-shadow:0 4px 24px rgba(217,119,6,0.35);">⚕️</div>
        <h1 style="font-size:26px;font-weight:600;margin:0 0 8px;color:#fff;">
            How can I help you today?
        </h1>
        <p style="color:#888;font-size:15px;max-width:400px;line-height:1.65;margin:0 0 36px;">
            I'm your AR Denial Resolution Assistant. Ask me about any claim denial,
            or upload a PDF to get answers from it directly.
        </p>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;
                    max-width:520px;width:100%;">
            <div style="background:#2a2a2a;border:1px solid #333;border-radius:12px;
                        padding:14px 16px;text-align:left;">
                <div style="font-size:18px;margin-bottom:5px;">🔍</div>
                <div style="font-size:13px;font-weight:600;color:#fff;margin-bottom:2px;">Claim Not Found</div>
                <div style="font-size:12px;color:#777;">Step-by-step resolution</div>
            </div>
            <div style="background:#2a2a2a;border:1px solid #333;border-radius:12px;
                        padding:14px 16px;text-align:left;">
                <div style="font-size:18px;margin-bottom:5px;">⏰</div>
                <div style="font-size:13px;font-weight:600;color:#fff;margin-bottom:2px;">Timely Filing</div>
                <div style="font-size:12px;color:#777;">Beat the filing deadline</div>
            </div>
            <div style="background:#2a2a2a;border:1px solid #333;border-radius:12px;
                        padding:14px 16px;text-align:left;">
                <div style="font-size:18px;margin-bottom:5px;">📄</div>
                <div style="font-size:13px;font-weight:600;color:#fff;margin-bottom:2px;">Upload a PDF</div>
                <div style="font-size:12px;color:#777;">Ask from any document</div>
            </div>
            <div style="background:#2a2a2a;border:1px solid #333;border-radius:12px;
                        padding:14px 16px;text-align:left;">
                <div style="font-size:18px;margin-bottom:5px;">📊</div>
                <div style="font-size:13px;font-weight:600;color:#fff;margin-bottom:2px;">AR Aging</div>
                <div style="font-size:12px;color:#777;">Prioritize AR buckets</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Chat history ───────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="⚕️" if msg["role"] == "assistant" else "👤"):
        st.markdown(msg["content"])

# ── Quick action trigger ───────────────────
if st.session_state.quick_trigger:
    trigger = st.session_state.quick_trigger
    st.session_state.quick_trigger = None
    st.session_state.messages.append({"role": "user", "content": trigger})
    with st.chat_message("user", avatar="👤"):
        st.markdown(trigger)
    with st.chat_message("assistant", avatar="⚕️"):
        with st.spinner(""):
            reply = call_groq(trigger, st.session_state.pdf_text)
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

# spacer
st.markdown("<div style='height:150px'></div>", unsafe_allow_html=True)

# ═════════════════════════════════════════════
#  BOTTOM INPUT BAR
#  📎 uploader  |  chat text input
# ═════════════════════════════════════════════
col_plus, col_chat = st.columns([1, 13])

with col_plus:
    st.markdown('<div class="plus-col">', unsafe_allow_html=True)
    bar_pdf = st.file_uploader(
        "pdf", type=["pdf"],
        label_visibility="collapsed",
        key="bar_uploader"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col_chat:
    prompt = st.chat_input(
        placeholder="Message AR Denial Assistant…",
        key="main_chat"
    )

handle_pdf(bar_pdf)

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    with st.chat_message("assistant", avatar="⚕️"):
        with st.spinner(""):
            reply = call_groq(prompt, st.session_state.pdf_text)
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
