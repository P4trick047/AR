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
#  CSS — Claude-style interface
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Söhne:wght@400;500;600&family=Styrene+A:wght@400;500&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700&family=Source+Serif+4:ital,wght@0,300;0,400;1,300&display=swap');

/* ── Reset & Base ── */
html, body, [class*="css"] {
    font-family: 'Lato', -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 15px;
}
.stApp {
    background-color: #ffffff;
    color: #1a1a1a;
}
#MainMenu, footer, header { visibility: hidden; }

/* ── Sidebar — Claude-style dark ── */
[data-testid="stSidebar"] {
    background: #171717 !important;
    border-right: 1px solid #2a2a2a !important;
    width: 260px !important;
}
[data-testid="stSidebar"] * { color: #d4d4d4 !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #ffffff !important; }
[data-testid="collapsedControl"] {
    background: #2a2a2a !important;
    color: #aaa !important;
}
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: none !important;
    color: #c4c4c4 !important;
    text-align: left !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    padding: 8px 12px !important;
    width: 100% !important;
    transition: background 0.15s;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: #2a2a2a !important;
    color: #ffffff !important;
}
[data-testid="stSidebar"] hr { border-color: #2a2a2a !important; }
[data-testid="stSidebar"] .stFileUploader section {
    background: #1e1e1e !important;
    border: 1.5px dashed #444 !important;
    border-radius: 10px !important;
    padding: 12px !important;
}
[data-testid="stSidebar"] .stFileUploader section:hover {
    border-color: #888 !important;
    background: #252525 !important;
}
[data-testid="stSidebar"] [data-testid="stMetric"] {
    background: #1e1e1e !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 8px !important;
    padding: 8px !important;
}
[data-testid="stSidebar"] [data-testid="stMetricValue"] { color: #ffffff !important; }
[data-testid="stSidebar"] [data-testid="stMetricLabel"] { color: #888 !important; }

/* ── Main area — clean white like Claude ── */
section.main > div { padding-top: 0 !important; padding-bottom: 0 !important; }
.block-container {
    max-width: 780px !important;
    margin: 0 auto !important;
    padding: 0 20px 160px !important;
}

/* ── Chat messages — Claude style ── */
/* Hide default Streamlit chat styling */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
    box-shadow: none !important;
}
[data-testid="stChatMessage"] + [data-testid="stChatMessage"] {
    border-top: none !important;
}

/* User message pill — right aligned with gray bg */
[data-testid="stChatMessage"][data-testid*="user"],
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    display: flex !important;
    justify-content: flex-end !important;
}
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) .stMarkdown {
    background: #f4f4f4 !important;
    border-radius: 18px 18px 4px 18px !important;
    padding: 10px 16px !important;
    max-width: 75% !important;
    color: #1a1a1a !important;
    font-size: 15px !important;
    line-height: 1.6 !important;
}

/* Assistant message — no bubble, just text like Claude */
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    padding: 4px 0 !important;
}
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown {
    background: transparent !important;
    padding: 0 !important;
    font-size: 15px !important;
    line-height: 1.75 !important;
    color: #1a1a1a !important;
}
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown p {
    margin-bottom: 10px !important;
}
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown strong {
    color: #111 !important;
    font-weight: 600 !important;
}
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown ul,
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown ol {
    padding-left: 20px !important;
    margin-bottom: 10px !important;
}
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown li {
    margin-bottom: 4px !important;
}
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown code {
    background: #f4f4f4 !important;
    border-radius: 4px !important;
    padding: 1px 5px !important;
    font-size: 13px !important;
    color: #c7254e !important;
}

/* Avatar icons */
[data-testid="chatAvatarIcon-assistant"] {
    background: #d97706 !important;
    border-radius: 50% !important;
    width: 32px !important; height: 32px !important;
    font-size: 16px !important;
    flex-shrink: 0 !important;
}
[data-testid="chatAvatarIcon-user"] {
    background: #6366f1 !important;
    border-radius: 50% !important;
    width: 32px !important; height: 32px !important;
    font-size: 14px !important;
    flex-shrink: 0 !important;
}

/* Message row spacing */
[data-testid="stChatMessage"] {
    margin-bottom: 20px !important;
}

/* ── Input bar — Claude-style ── */
[data-testid="stChatInput"] {
    position: fixed !important;
    bottom: 0 !important;
    left: 0 !important;
    right: 0 !important;
    z-index: 999 !important;
    max-width: 780px !important;
    margin: 0 auto !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    background: #ffffff !important;
    border: 1.5px solid #e0e0e0 !important;
    border-radius: 16px !important;
    box-shadow: 0 2px 16px rgba(0,0,0,0.08) !important;
    padding: 4px 8px !important;
    margin-bottom: 20px !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #b4b4b4 !important;
    box-shadow: 0 2px 20px rgba(0,0,0,0.12) !important;
}
[data-testid="stChatInput"] textarea {
    font-family: 'Lato', sans-serif !important;
    font-size: 15px !important;
    color: #1a1a1a !important;
    background: transparent !important;
    border: none !important;
    padding: 10px 12px !important;
    line-height: 1.5 !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #aaa !important;
    font-size: 15px !important;
}
[data-testid="stChatInput"] button[kind="primary"] {
    background: #1a1a1a !important;
    border-radius: 10px !important;
    width: 36px !important; height: 36px !important;
    color: white !important;
    border: none !important;
}
[data-testid="stChatInput"] button[kind="primary"]:hover {
    background: #333 !important;
}
[data-testid="stChatInput"] button[kind="primary"]:disabled {
    background: #e5e5e5 !important;
    color: #aaa !important;
}

/* ── Plus uploader button column ── */
.plus-col [data-testid="stFileUploader"] section {
    border: none !important;
    background: transparent !important;
    border-radius: 10px !important;
    padding: 6px !important;
    min-height: 44px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
    transition: background 0.15s !important;
}
.plus-col [data-testid="stFileUploader"] section:hover {
    background: #f4f4f4 !important;
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

/* ── Input row layout fix ── */
.input-row {
    position: fixed;
    bottom: 0; left: 0; right: 0;
    z-index: 1000;
    background: linear-gradient(to top, #fff 80%, transparent);
    padding: 10px 20px 18px;
    display: flex;
    justify-content: center;
}
.input-inner {
    width: 100%;
    max-width: 780px;
    display: flex;
    align-items: flex-end;
    gap: 8px;
    background: #fff;
    border: 1.5px solid #e0e0e0;
    border-radius: 16px;
    box-shadow: 0 2px 16px rgba(0,0,0,0.08);
    padding: 6px 8px 6px 8px;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.input-inner:focus-within {
    border-color: #b4b4b4;
    box-shadow: 0 2px 20px rgba(0,0,0,0.12);
}

/* Hide default Streamlit chat input — we build our own row */
[data-testid="stChatInput"] { display: none !important; }

/* ── Drag overlay ── */
#drag-overlay {
    display: none;
    position: fixed; inset: 0;
    z-index: 9999;
    background: rgba(255,255,255,0.92);
    backdrop-filter: blur(10px);
    align-items: center; justify-content: center;
    flex-direction: column; gap: 14px;
    pointer-events: none;
}
#drag-overlay.active { display: flex !important; }
.drop-box {
    border: 3px dashed #d97706;
    border-radius: 24px;
    padding: 56px 90px;
    text-align: center;
    background: rgba(217,119,6,0.05);
    animation: pulseBorder 1.4s ease-in-out infinite;
    pointer-events: none;
}
@keyframes pulseBorder {
    0%,100% { border-color: #d97706; box-shadow: 0 0 0 0 rgba(217,119,6,0.3); }
    50%      { border-color: #f59e0b; box-shadow: 0 0 0 12px rgba(217,119,6,0); }
}

/* ── Misc ── */
.stAlert { border-radius: 10px !important; }
.stInfo { background: #fefce8 !important; border-color: #fde68a !important; color: #92400e !important; }
p { color: #1a1a1a !important; }
li { color: #1a1a1a !important; }
h1,h2,h3 { color: #111 !important; font-weight: 600 !important; }
[data-testid="stMarkdownContainer"] hr {
    border-color: #e8e8e8 !important;
    margin: 20px 0 !important;
}

/* PDF badge */
.pdf-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: #fefce8; border: 1px solid #fde68a;
    border-radius: 20px; padding: 4px 12px;
    font-size: 13px; color: #92400e; font-weight: 500;
    margin-bottom: 12px;
}

/* Scroll padding */
.main .block-container { padding-bottom: 160px !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  System prompt
# ─────────────────────────────────────────────
SYSTEM_PROMPT = """You are an expert AR (Accounts Receivable) Denial Resolution Assistant for Aayur Solutions. Help billing staff resolve claim denials fast and accurately.

DENIAL RESOLUTION PROCESSES:

1. CLAIM NOT FOUND
   Electronic: check Payer ID correct? → If wrong, update & resubmit. If right, check clearinghouse acceptance → if rejected, work rejections; if accepted, check payer acceptance → if yes, contact payer with tracking# to reprocess; if no, resubmit.
   Paper: check mailing address correct? → If wrong, update Payer ID & resubmit. If right, resubmit.

2. POLICY TERMED
   Does patient have another policy? → If yes, is it active on service date? → If yes, transfer balance to patient. If no other policy or not active → contact patient/doctor for other insurance → found? update as primary & bill new insurance. Not found → transfer to patient.

3. DUPLICATE CLAIM
   Was it a corrected claim? → If no, contact payer to void in adjudication. If yes, was it submitted with Freq Code 7 & Resubmission ID? → If no, resubmit with those. If yes, contact payer to reprocess.

4. TIMELY FILING
   Submitted within payer timeframe? → If no, send query to client. If yes, do we have POTF? → If no, contact payer to confirm receipt & reprocess. If yes, resubmit with POTF.

5. COORDINATION OF BENEFITS (COB) — Same flow as Timely Filing.

AR AGING BUCKETS: 0-30 | 31-60 | 61-90 | 91-120 | 121+ days. Medicare = 15 days. Pull new files every 15-30 days. Run at least 3 AR cycles.

BEHAVIOR:
- If PDF content is provided, prioritize answering from it
- Be warm, clear, and step-by-step
- Highlight urgent actions (timely filing deadlines, etc.)
- Format responses cleanly with markdown"""

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
            "content": f"I've read **{uploaded.name}** ({len(extracted):,} characters). What would you like to know about it?"
        })
        st.rerun()


# ═════════════════════════════════════════════
#  SIDEBAR — Claude dark sidebar style
# ═════════════════════════════════════════════
with st.sidebar:
    # Logo / brand
    st.markdown("""
    <div style="padding:16px 4px 20px; display:flex; align-items:center; gap:10px;">
        <div style="width:34px;height:34px;border-radius:8px;
                    background:#d97706;display:flex;align-items:center;
                    justify-content:center;font-size:18px;flex-shrink:0;">⚕️</div>
        <div>
            <div style="color:#fff;font-weight:600;font-size:14px;line-height:1.2;">AR Denial Assistant</div>
            <div style="color:#888;font-size:11px;">Aayur Solutions</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # New chat button style
    if st.button("✏️  New conversation", use_container_width=True, key="new_chat"):
        st.session_state.messages = []
        st.session_state.pdf_text = None
        st.session_state.pdf_name = None
        st.rerun()

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # PDF upload in sidebar
    st.markdown("<div style='color:#888;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;padding:0 4px;'>Documents</div>", unsafe_allow_html=True)

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
            <span style="font-size:16px;">📄</span>
            <div style="flex:1;min-width:0;">
                <div style="color:#e5e5e5;font-size:12px;font-weight:500;
                            white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
                    {st.session_state.pdf_name}
                </div>
                <div style="color:#666;font-size:10px;">Active document</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Remove document", use_container_width=True, key="remove_pdf"):
            st.session_state.pdf_text = None
            st.session_state.pdf_name = None
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Document removed. I'll answer from my built-in AR knowledge now."
            })
            st.rerun()

    st.divider()

    # Quick actions
    st.markdown("<div style='color:#888;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px;padding:0 4px;'>Quick Actions</div>", unsafe_allow_html=True)
    for label, query in QUICK_ACTIONS:
        if st.button(label, use_container_width=True, key=f"qa_{label}"):
            st.session_state.quick_trigger = query
            st.rerun()

    st.divider()

    # Stats
    c1, c2 = st.columns(2)
    c1.metric("Denials", "5 Types")
    c2.metric("Buckets", "5")
    c1.metric("PDF", "✅")
    c2.metric("HIPAA", "✅")

    st.markdown("""
    <div style="margin-top:16px;padding:0 4px;">
        <div style="color:#555;font-size:11px;">⚡ llama-3.3-70b via Groq</div>
        <div style="color:#555;font-size:11px;margin-top:3px;">🔒 Never enter real patient SSNs</div>
    </div>
    """, unsafe_allow_html=True)


# ═════════════════════════════════════════════
#  MAIN — Claude-style chat
# ═════════════════════════════════════════════

# Thin top border
st.markdown("<div style='height:1px;background:#f0f0f0;margin-bottom:0;'></div>", unsafe_allow_html=True)

# PDF active badge
if st.session_state.pdf_name:
    st.markdown(f"""
    <div style="display:flex;justify-content:center;padding:10px 0 0;">
        <div class="pdf-badge">📎 {st.session_state.pdf_name}</div>
    </div>
    """, unsafe_allow_html=True)

# ── Welcome / empty state ──────────────────
if not st.session_state.messages:
    st.markdown("""
    <div style="display:flex;flex-direction:column;align-items:center;
                justify-content:center;min-height:50vh;text-align:center;
                padding:40px 20px 0;">
        <div style="width:56px;height:56px;border-radius:14px;background:#d97706;
                    display:flex;align-items:center;justify-content:center;
                    font-size:28px;margin-bottom:20px;
                    box-shadow:0 4px 20px rgba(217,119,6,0.3);">⚕️</div>
        <h1 style="font-size:26px;font-weight:600;margin:0 0 8px;color:#111;">
            How can I help you today?
        </h1>
        <p style="color:#666;font-size:15px;max-width:420px;line-height:1.6;margin:0 0 32px;">
            I'm your AR Denial Resolution Assistant. Ask me about any claim denial,
            or upload a PDF document to get answers from it directly.
        </p>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;max-width:500px;width:100%;">
            <div style="background:#f9f9f9;border:1px solid #e8e8e8;border-radius:12px;
                        padding:14px 16px;text-align:left;cursor:pointer;">
                <div style="font-size:18px;margin-bottom:4px;">🔍</div>
                <div style="font-size:13px;font-weight:600;color:#111;margin-bottom:2px;">Claim Not Found</div>
                <div style="font-size:12px;color:#888;">Step-by-step resolution guide</div>
            </div>
            <div style="background:#f9f9f9;border:1px solid #e8e8e8;border-radius:12px;
                        padding:14px 16px;text-align:left;">
                <div style="font-size:18px;margin-bottom:4px;">⏰</div>
                <div style="font-size:13px;font-weight:600;color:#111;margin-bottom:2px;">Timely Filing</div>
                <div style="font-size:12px;color:#888;">Beat the filing deadline</div>
            </div>
            <div style="background:#f9f9f9;border:1px solid #e8e8e8;border-radius:12px;
                        padding:14px 16px;text-align:left;">
                <div style="font-size:18px;margin-bottom:4px;">📄</div>
                <div style="font-size:13px;font-weight:600;color:#111;margin-bottom:2px;">Upload a PDF</div>
                <div style="font-size:12px;color:#888;">Ask questions from any document</div>
            </div>
            <div style="background:#f9f9f9;border:1px solid #e8e8e8;border-radius:12px;
                        padding:14px 16px;text-align:left;">
                <div style="font-size:18px;margin-bottom:4px;">📊</div>
                <div style="font-size:13px;font-weight:600;color:#111;margin-bottom:2px;">AR Aging</div>
                <div style="font-size:12px;color:#888;">Prioritize your AR buckets</div>
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

# spacer before fixed input bar
st.markdown("<div style='height:140px'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  Drag-drop overlay
# ─────────────────────────────────────────────
st.markdown("""
<div id="drag-overlay">
    <div class="drop-box">
        <div style="font-size:48px;margin-bottom:10px;">📄</div>
        <div style="color:#111;font-size:20px;font-weight:600;margin-bottom:4px;">
            Drop your PDF here
        </div>
        <div style="color:#888;font-size:14px;">Release to upload and read the document</div>
    </div>
    <div style="color:#aaa;font-size:12px;">PDF files only</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  INPUT ROW — Plus (📎) + Chat input
# ─────────────────────────────────────────────
col_plus, col_input = st.columns([1, 14])

with col_plus:
    st.markdown('<div class="plus-col">', unsafe_allow_html=True)
    bar_pdf = st.file_uploader(
        "pdf", type=["pdf"],
        label_visibility="collapsed",
        key="bar_uploader"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col_input:
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

# ─────────────────────────────────────────────
#  JS — drag & drop to Streamlit file input
# ─────────────────────────────────────────────
st.markdown("""
<script>
(function () {
    function getSTInput() {
        const inputs = document.querySelectorAll('input[type="file"][accept="application/pdf"]');
        return inputs.length ? inputs[0] : null;
    }
    function pushFile(file) {
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
            overlay && overlay.classList.add('active');
        }
    });
    document.addEventListener('dragleave', () => {
        counter = Math.max(0, counter - 1);
        if (counter === 0) overlay && overlay.classList.remove('active');
    });
    document.addEventListener('dragover', (e) => e.preventDefault());
    document.addEventListener('drop', (e) => {
        e.preventDefault();
        counter = 0;
        overlay && overlay.classList.remove('active');
        const file = e.dataTransfer.files[0];
        if (!file) return;
        if (file.type !== 'application/pdf') { alert('Please drop a PDF file.'); return; }
        pushFile(file);
    });
})();
</script>
""", unsafe_allow_html=True)
