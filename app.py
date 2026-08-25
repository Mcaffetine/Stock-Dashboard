import streamlit as st
import numpy as np

# Set page config for mobile and desktop responsiveness
st.set_page_config(
    page_title="AlphaQuant Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme and professional styling
st.markdown("""
<style>
    .reportview-container { background: #0e1117; }
    .metric-box {
        background-color: #1e222b;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #3b82f6;
        margin-bottom: 15px;
    }
    .flag-box {
        background-color: #2a1b1b;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #ef4444;
        margin-bottom: 10px;
    }
    .pass-box {
        background-color: #1b2a1c;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #10b981;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 AlphaQuant: Multi-Mode Stock Evaluator")
st.markdown("Evaluate stocks across **Growth**, **Value**, and **Momentum** archetypes with dynamic rules, thresholds, and clear risk flags.")

# Sidebar Configuration
st.sidebar.header("🕹️ Strategy & Thresholds")
mode = st.sidebar.selectbox(
    "Active Analysis Mode",
    ["Growth Hunter", "Value Investor", "Momentum Swing"],
    help="Changes evaluation focus, weight distributions, and red flag sensitivity."
)

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Adjustable Thresholds (Defaults Set)")

# Threshold Inputs
target_eps_growth = st.sidebar.slider("Min EPS Growth (%)", 0, 100, 15, help="Standard: 15%")
max_pe = st.sidebar.slider("Max P/E Ratio", 5, 100, 25, help="Standard: 25")
max_peg = st.sidebar.slider("Max PEG Ratio", 0.5, 4.0, 1.2, 0.1, help="Standard: 1.2")
min_roe = st.sidebar.slider("Min ROE (%)", 0, 50, 15, help="Standard: 15%")
min_div_yield = st.sidebar.slider("Min Dividend Yield (%)", 0.0, 15.0, 2.5, 0.5, help="Standard: 2.5%")
rsi_overbought = st.sidebar.slider("RSI Overbought Threshold", 50, 90, 70, help="Standard: 70")
rsi_oversold = st.sidebar.slider("RSI Oversold Threshold", 10, 50, 30, help="Standard: 30")

# Main Input Layout
st.subheader("📝 Stock Financial & Technical Inputs")
col1, col2, col3, col4 = st.columns(4)

with col1:
    ticker = st.text_input("Stock Ticker", "AAPL").upper()
    eps_growth = st.number_input("Current EPS Growth (%)", value=18.5)
with col2:
    pe_ratio = st.number_input("P/E Ratio", value=22.0)
    peg_ratio = st.number_input("PEG Ratio", value=1.1)
with col3:
    roe = st.number_input("Return on Equity (ROE %)", value=16.5)
    div_yield = st.number_input("Dividend Yield (%)", value=1.2)
with col4:
    rsi = st.number_input("RSI (14-Day)", value=65.0)
    macd_status = st.selectbox("MACD Line Status", ["Bullish Crossover", "Bearish Crossover", "Neutral/Flat"])

# Scoring Logic Engine
def calculate_scores():
    # Growth Score
    g_eps = min(100, (eps_growth / target_eps_growth) * 100) if eps_growth > 0 else 0
    g_peg = 100 if peg_ratio <= max_peg else max(0, 100 - (peg_ratio - max_peg) * 50)
    g_roe = min(100, (roe / min_roe) * 100) if roe > 0 else 0
    growth_score = (g_eps * 0.4) + (g_peg * 0.4) + (g_roe * 0.2)
    
    # Value Score
    v_pe = 100 if pe_ratio <= max_pe else max(0, 100 - (pe_ratio - max_pe) * 3)
    v_peg = 100 if peg_ratio <= max_peg else max(0, 100 - (peg_ratio - max_peg) * 40)
    v_div = min(100, (div_yield / min_div_yield) * 100) if div_yield > 0 else 0
    value_score = (v_pe * 0.4) + (v_peg * 0.3) + (v_div * 0.3)
    
    # Momentum Score
    m_rsi = 100 - abs(rsi - 60) * 2 if rsi >= 50 else max(0, rsi * 1.5)
    m_macd = 100 if macd_status == "Bullish Crossover" else (30 if macd_status == "Bearish Crossover" else 60)
    momentum_score = (m_rsi * 0.5) + (m_macd * 0.5)
    
    return round(growth_score, 1), round(value_score, 1), round(momentum_score, 1)

g_score, v_score, m_score = calculate_scores()

# Identify active framework context
active_score = g_score if mode == "Growth Hunter" else (v_score if mode == "Value Investor" else m_score)

# Process Flags based on user's specific picked mode
red_flags = []
green_flags = []

if mode == "Growth Hunter":
    if eps_growth < target_eps_growth: red_flags.append(f"EPS Growth ({eps_growth}%) is below your target milestone ({target_eps_growth}%).")
    if peg_ratio > max_peg: red_flags.append(f"PEG ratio ({peg_ratio}) points to growth overvaluation.")
    if roe < min_roe: red_flags.append(f"ROE ({roe}%) indicates management operational sub-efficiency.")
    if not red_flags: green_flags.append("Core business growth engines are running cleanly.")

elif mode == "Value Investor":
    if pe_ratio > max_pe: red_flags.append(f"P/E Ratio ({pe_ratio}) exceeds maximum margin of safety limit ({max_pe}).")
    if div_yield < min_div_yield: red_flags.append(f"Dividend yield ({div_yield}%) fails to meet baseline passive cash criteria.")
    if peg_ratio > 1.5: red_flags.append(f"PEG ratio ({peg_ratio}) indicates you are paying too much premium for value.")
    if not red_flags: green_flags.append("Stock displays strong protective margin of safety characteristics.")

elif mode == "Momentum Swing":
    if rsi > rsi_overbought: red_flags.append(f"RSI ({rsi}) is in hyper-overbought territory. High pullback vulnerability.")
    if macd_status == "Bearish Crossover": red_flags.append("MACD triggered a bearish downside crossover event.")
    if rsi < rsi_oversold: red_flags.append(f"RSI ({rsi}) indicates structural capital capitulation.")
    if not red_flags: green_flags.append("Price action shows clean structural chart accumulation.")

# Penalty application for strict contextual flags
if red_flags:
    active_score = max(0, active_score - (len(red_flags) * 12))

st.markdown("---")
st.subheader(f"📈 Engine Results for {ticker} (Mode: {mode})")

# Visual Display Section 1: All 3 Scores Progress Gauges
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Growth Archetype Score", f"{g_score}%")
    st.progress(g_score / 100)
with c2:
    st.metric("Value Archetype Score", f"{v_score}%")
    st.progress(v_score / 100)
with c3:
    st.metric("Momentum Swing Score", f"{m_score}%")
    st.progress(m_score / 100)

# Section 2: Detailed Text Grading, Visual Flags, and AI Summaries
st.markdown("---")
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("🔍 Contextual Health Check & Analysis")
    if red_flags:
        st.markdown("#### ⚠️ High-Risk Risk Flags Spotted")
        for flag in red_flags:
            st.markdown(f"<div class='flag-box'>❌ {flag}</div>", unsafe_allow_html=True)
    if green_flags or not red_flags:
        st.markdown("#### ✅ Alignment Signals Approved")
        for gf in green_flags:
            st.markdown(f"<div class='pass-box'>⭐ {gf}</div>", unsafe_allow_html=True)

with col_right:
    st.subheader("📝 Dynamic Archetype Summary")
    
    # 3-Way Comprehensive Text Feedback
    st.markdown("##### 🚀 Growth Assessment")
    if g_score >= 75: st.write("Strong compounding profile. Numbers support active business scale-up.")
    elif g_score >= 45: st.write("Moderate expansion. Some foundational metrics require macro stabilization.")
    else: st.write("Stagnant growth. Financial architecture suggests structural plateau risk.")
    
    st.markdown("##### 💎 Value Assessment")
    if v_score >= 75: st.write("Deep margin of safety present. Trading under intrinsic premium levels.")
    elif v_score >= 45: st.write("Fairly valued pricing structure. Limited built-in structural discount.")
    else: st.write("Premium price multiple trap. High risk of overpaying relative to assets.")
    
    st.markdown("##### ⚡ Momentum Assessment")
    if m_score >= 75: st.write("Clean bullish trend velocity. Strong institutional capital commitment.")
    elif m_score >= 45: st.write("Indecisive directional action. Consolidation phase ongoing.")
    else: st.write("Severe downward pressure. Bearish trend dominant.")

st.sidebar.markdown("---")
st.sidebar.caption("AlphaQuant v1.0.0 • Developed for cross-device web deployment.")
