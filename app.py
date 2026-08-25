import streamlit as pd_app
import pandas as pd

# Page Configuration for Cross-Device Layout
pd_app.set_page_config(page_title="Pro Stock Terminal", layout="wide", initial_sidebar_state="expanded")

pd_app.title("📊 AlphaEngine: Multi-Strategy Stock Appraisal Terminal")
pd_app.markdown("---")

# -----------------------------------------------------------------
# 1. CORE CONFIGURATION & DYNAMIC THRESHOLDS MODE
# -----------------------------------------------------------------
pd_app.sidebar.header("🎯 System Mode Configuration")
mode = pd_app.sidebar.selectbox(
    "Select Appraisal Framework Mode",
    ["Growth Hunter", "Value Investor", "Momentum Swing", "Independent Custom"]
)

# Standard Institutional Baseline Definitions
defaults = {
    "Growth Hunter": {"pe": 40.0, "peg": 1.2, "eps": 15.0, "rev": 12.0, "roe": 15.0, "de": 1.5, "rsi_min": 45.0, "rsi_max": 70.0},
    "Value Investor": {"pe": 18.0, "peg": 1.0, "eps": 5.0, "rev": 4.0, "roe": 12.0, "de": 0.8, "rsi_min": 30.0, "rsi_max": 55.0},
    "Momentum Swing": {"pe": 60.0, "peg": 2.0, "eps": 10.0, "rev": 10.0, "roe": 10.0, "de": 2.0, "rsi_min": 55.0, "rsi_max": 75.0},
    "Independent Custom": {"pe": 25.0, "peg": 1.2, "eps": 10.0, "rev": 8.0, "roe": 14.0, "de": 1.2, "rsi_min": 40.0, "rsi_max": 70.0}
}

current_limits = defaults[mode]

# Render interactive sliders ONLY if independent custom mode is active
if mode == "Independent Custom":
    pd_app.sidebar.markdown("### 🛠️ Adjust Targets Manually")
    t_pe = pd_app.sidebar.slider("Max P/E Ratio Allowance", 5.0, 100.0, current_limits["pe"])
    t_peg = pd_app.sidebar.slider("Max PEG Ratio Allowance", 0.2, 3.5, current_limits["peg"])
    t_eps = pd_app.sidebar.slider("Min EPS Growth Floor (%)", -10.0, 50.0, current_limits["eps"])
    t_rev = pd_app.sidebar.slider("Min Revenue Growth Floor (%)", -10.0, 50.0, current_limits["rev"])
    t_roe = pd_app.sidebar.slider("Min Return on Equity (%)", 0.0, 40.0, current_limits["roe"])
    t_de = pd_app.sidebar.slider("Max Debt-to-Equity Ratio", 0.1, 4.0, current_limits["de"])
    t_rsi = pd_app.sidebar.slider("Acceptable RSI Target Window", 10, 90, (int(current_limits["rsi_min"]), int(current_limits["rsi_max"])))
    
    limits = {"pe": t_pe, "peg": t_peg, "eps": t_eps, "rev": t_rev, "roe": t_roe, "de": t_de, "rsi_min": t_rsi[0], "rsi_max": t_rsi[1]}
else:
    limits = current_limits
    pd_app.sidebar.info(f"🔒 **Standard Limits Locked** for {mode}. Switch to 'Independent Custom' to adjust values manually.")

# -----------------------------------------------------------------
# 2. EXPANDED USER DATA INPUT MATRIX
# -----------------------------------------------------------------
pd_app.subheader("📝 Stock Financial & Technical Metric Entry")
col_meta, col_fund1, col_fund2, col_tech = pd_app.columns(4)

with col_meta:
    ticker = pd_app.text_input("Ticker Symbol", "AAPL").upper()
    curr_price = pd_app.number_input("Current Share Price ($)", min_value=0.01, value=150.00, step=1.0)
    div_yield = pd_app.number_input("Dividend Yield (%)", min_value=0.0, value=1.5, step=0.1)

with col_fund1:
    pe_ratio = pd_app.number_input("P/E Ratio", min_value=0.0, value=28.5, step=0.5)
    peg_ratio = pd_app.number_input("PEG Ratio", min_value=0.0, value=1.1, step=0.1)
    roe = pd_app.number_input("Return on Equity (ROE %)", min_value=-50.0, value=18.5, step=0.5)

with col_fund2:
    eps_growth = pd_app.number_input("EPS Growth Rate YoY (%)", min_value=-100.0, value=16.0, step=0.5)
    rev_growth = pd_app.number_input("Revenue Growth YoY (%)", min_value=-100.0, value=14.0, step=0.5)
    de_ratio = pd_app.number_input("Debt to Equity Ratio", min_value=0.0, value=0.9, step=0.1)

with col_tech:
    rsi_val = pd_app.number_input("RSI (14-Day)", min_value=0.0, max_value=100.0, value=58.0, step=1.0)
    sma_50_dist = pd_app.number_input("Distance from 50 SMA (%)", min_value=-50.0, value=4.5, step=0.5)
    macd_status = pd_app.selectbox("MACD Signal Line Status", ["Bullish Crossover", "Bearish Crossover", "Neutral / Flat"])

# -----------------------------------------------------------------
# 3. ADVANCED TRIPLE ARCHETYPE SCORING MATRIX ENGINE
# -----------------------------------------------------------------
# Growth Core Score
g_score = 0
if eps_growth >= limits["eps"]: g_score += 25
if rev_growth >= limits["rev"]: g_score += 25
if peg_ratio <= limits["peg"]: g_score += 20
if roe >= limits["roe"]: g_score += 15
if macd_status == "Bullish Crossover": g_score += 15

# Value Core Score
v_score = 0
if pe_ratio <= limits["pe"]: v_score += 30
if peg_ratio <= (limits["peg"] * 0.8): v_score += 25
if de_ratio <= limits["de"]: v_score += 20
if div_yield > 2.5: v_score += 15
if rsi_val <= 45: v_score += 10

# Momentum Swing Score
m_score = 0
if rsi_val >= limits["rsi_min"] and rsi_val <= limits["rsi_max"]: m_score += 30
if macd_status == "Bullish Crossover": m_score += 25
if sma_50_dist > 0: m_score += 25
if eps_growth > 5: m_score += 20

# -----------------------------------------------------------------
# 4. CONDITIONAL MODE-DRIVEN RED FLAG ENGINE
# -----------------------------------------------------------------
red_flags = []

if rsi_val > 75:
    red_flags.append("⚠️ OVERBOUGHT MOMENTUM: Technical RSI indicates near-term exhaustion risks.")
if de_ratio > limits["de"]:
    red_flags.append(f"⚠️ LEVERAGE RISK: Debt-to-Equity ({de_ratio}) exceeds target boundary limits ({limits['de']}).")

if mode == "Growth Hunter":
    if eps_growth < limits["eps"]: red_flags.append("🚨 STAGNANT EARNINGS: EPS growth fails baseline framework standards.")
    if peg_ratio > limits["peg"]: red_flags.append("🚨 OVERPRICED GROWTH: PEG valuation framework indicates heavy premiums.")
elif mode == "Value Investor":
    if pe_ratio > limits["pe"]: red_flags.append("🚨 VALUATION PREMIUM: P/E metric is too high for conservative target allocation.")
    if div_yield == 0: red_flags.append("⚠️ NO DIVIDEND BUFFER: Stock offers no downside cash protection yield safety net.")
elif mode == "Momentum Swing":
    if macd_status == "Bearish Crossover": red_flags.append("🚨 TREND DECAY: MACD technical structure signals strong distribution.")
    if sma_50_dist < -5: red_flags.append("🚨 TECHNICAL BREAKDOWN: Asset price values are dropping below core structural support layers.")

# Render Red Flag Notifications
pd_app.subheader("🚨 Risk Warning Analysis Feed")
if red_flags:
    for flag in red_flags:
        pd_app.error(flag)
else:
    pd_app.success("✅ Clean Risk Profile: No system parameters triggered critical threshold warnings.")

# Display Quantitative Score Metrics
pd_app.markdown("---")
pd_app.subheader("📊 Tactical Asset Suitability Breakdowns")
c_g, c_v, c_m = pd_app.columns(3)
c_g.metric("Growth Allocation Match Score", f"{g_score}%", f"Target: >= 75%")
c_v.metric("Value Framework Match Score", f"{v_score}%", f"Target: >= 70%")
c_m.metric("Momentum Swing Match Score", f"{m_score}%", f"Target: >= 80%")

# -----------------------------------------------------------------
# 5. ALGORITHMIC PRICING ENTRY & EXIT BOUNDARIES
# -----------------------------------------------------------------
pd_app.markdown("---")
pd_app.subheader("🎯 Automated Entry / Target Bounds Pricing Matrix")

# Calculate targets dynamically based on input health metrics
discount_factor = 0.85 if mode == "Value Investor" else 0.92
target_premium = 1.25 if mode == "Growth Hunter" else 1.15

calculated_buy = curr_price * discount_factor
calculated_sell = curr_price * target_premium

col_p1, col_p2, col_p3 = pd_app.columns(3)
col_p1.info(f"**Current Reference Price:**\n\n### ${curr_price:,.2f}")
col_p2.success(f"**Calculated Entry Target Zone:**\n\n### ${calculated_buy:,.2f}\n*(Includes margin of safety adjustments)*")
col_p3.warning(f"**Target Take-Profit Target Zone:**\n\n### ${calculated_sell:,.2f}\n*(Calculated valuation expansion target)*")

# -----------------------------------------------------------------
# 6. HISTORICAL LEGEND INSIGHT CONSOLE
# -----------------------------------------------------------------
pd_app.markdown("---")
pd_app.subheader("📖 Elite Investor Framework Commentary")

exp_growth, exp_value, exp_swing = pd_app.columns(3)

with exp_growth:
    pd_app.markdown("⭐ **Peter Lynch & William O'Neil Viewpoint:**")
    if eps_growth >= 15 and peg_ratio <= 1.2:
        pd_app.write("*\"This asset displays textbook CANSLIM properties. Strong underlying earnings speed combined with a fair valuation matrix means room to run.\"*")
    else:
        pd_app.write("*\"Growth must be clean. If earnings velocity stalls or the PEG breaks into premium numbers, you are overpaying for structural risks.\"*")

with exp_value:
    pd_app.markdown("⭐ **Benjamin Graham & Warren Buffett Viewpoint:**")
    if pe_ratio <= 20 and de_ratio <= 1.0:
        pd_app.write("*\"Capital safety relies entirely on a wide margin of safety. Low debt and reasonable valuations protect your investment foundation.\"*")
    else:
        pd_app.write("*\"Do not confuse a cyclical valuation peak with true business value. High debt footprints erode corporate compounding speed.\"*")

with exp_swing:
    pd_app.markdown("⭐ **Mark Minervini Trend Viewpoint:**")
    if rsi_val >= 50 and macd_status == "Bullish Crossover":
        pd_app.write("*\"Never buy structural asset drops. Only long positions above moving averages backed by momentum acceleration protect alpha generation.\"*")
    else:
        pd_app.write("*\"Momentum is absent here. Entering an asset before a clear structural structural turn traps trading liquidity unnecessarily.\"*")
