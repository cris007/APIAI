import streamlit as st
import google.generativeai as genai
import yfinance as yf
import feedparser

# 1. Page Configuration for optimal mobile browser responsive viewing
st.set_page_config(
    page_title="Forex Intelligence Oracle",
    page_icon="🔮",
    layout="centered"
)

# Custom Premium Dark Theme Style Sheets Injection
st.markdown("""
    <style>
    .reportview-container .main .block-container { padding-top: 1.5rem; }
    .chat-bubble {
        background-color: #161B22;
        border: 1px solid #21262D;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 12px;
    }
    .macro-label {
        font-size: 11px;
        text-transform: uppercase;
        color: #8B949E;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🔮 Forex Fundamental AI Oracle")
st.markdown("##### Real-Time Online Macroeconomic Prompting & Analysis Engine")

# 2. Get Live Background Market Metrics to pass into the AI context memory banks
def fetch_live_forex_context():
    symbols = {"DXY": "DX-Y.NYB", "US10Y": "^TNX", "Gold": "GC=F", "EURUSD": "EURUSD=X", "GBPUSD": "GBPUSD=X"}
    market_snapshot = ""
    for key, sym in symbols.items():
        try:
            data = yf.Ticker(sym).history(period="2d")
            if not data.empty:
                last_price = data['Close'].iloc[-1]
                pct = ((last_price - data['Close'].iloc[-2]) / data['Close'].iloc[-2]) * 100
                market_snapshot += f"- {key}: {last_price:.2f} ({pct:+.2f}% change today)\n"
        except: pass
    return market_snapshot
# 3. Securely Initialize Manual API Key Entry Panel
API_KEY = st.sidebar.text_input("Enter Free Gemini API Key:", type="password")

if not API_KEY:
    st.info("💡 Action Required: Please verify your Gemini API key in the sidebar input box to turn on your Online AI.")
    st.stop()

# Configure the online connection bridge securely using your manual string
genai.configure(api_key=API_KEY)

# Fetch latest price context rows
live_prices = fetch_live_forex_context()

# 4. Inject the Strict Institutional Brain Constraints (System Prompt Matrix)
SYSTEM_PROMPT = f"""
You are an elite, world-class global macro portfolio manager and institutional Forex analyst.
Your core objective is to analyze economic fundamentals, data releases, and cross-market sentiments.
You have a live real-time connection to current market pricing closing streams:
{live_prices}

When answering user prompts, you must always cross-reference how the macro data affects the major pairs (EUR/USD, GBP/USD, USD/JPY).
Focus heavily on:
1. Interest Rate Differentials (Central Bank hawkish/dovish paths between Fed, ECB, BOE, BOJ).
2. High-Impact News Triggers: CPI Inflation metrics, NFP Employment numbers, and retail liquidity flow sentiment shifts.
3. Safe Haven Inflow Currents: How Volatility shifts (VIX) redirect liquidity between the US Dollar and Gold.

Keep your layout responses direct, highly analytical, scannable, and formatted with clean bullet points. Avoid generic trading copy.
"""

# Initialize persistent chatbot conversation memory caches cleanly inside st.session_state
if "forex_chat_history" not in st.session_state:
    st.session_state.forex_chat_history = []

if "oracle_session" not in st.session_state:
    # FIXED: Updated the identifier model string name to follow the official full absolute resource routing path
    model = genai.GenerativeModel(
        model_name="models/gemini-1.5-flash",
        system_instruction=SYSTEM_PROMPT
    )
    st.session_state.oracle_session = model.start_chat(history=[])

# Render chat record loops onto the browser dashboard
for msg in st.session_state.forex_chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["text"])
# 5. Interactive Chat Prompt Input Window Block
if user_input := st.chat_input("Ask about CPI news, interest rate differentials, or ask to evaluate a setup..."):
    
    # Display user entry immediately
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.forex_chat_history.append({"role": "user", "text": user_input})
    
    # Send user data through the online server data loop
    with st.chat_message("assistant"):
        with st.spinner("AI is scraping global fundamentals and tracking intermarket flows..."):
            try:
                # Pointed directly and exclusively to st.session_state memory array loops
                response = st.session_state.oracle_session.send_message(user_input)
                ai_text = response.text
                st.markdown(ai_text)
                st.session_state.forex_chat_history.append({"role": "assistant", "text": ai_text})
            except Exception as e:
                st.error(f"⚠️ API processing timeout loop failed. Error details: {str(e)}")

# Clear History Button
if st.button("RESET ORACLE ANALYSIS MEMORY", type="secondary", use_container_width=True):
    st.session_state.forex_chat_history = []
    st.rerun()
