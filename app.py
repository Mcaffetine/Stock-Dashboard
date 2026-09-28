import streamlit as pd_app
import pandas as pd
import datetime
import plotly.graph_objects as go

# Advanced Terminal Configuration
pd_app.set_page_config(page_title="BD AlphaEngine Beast-v1", layout="wide", initial_sidebar_state="expanded")

pd_app.title("⚡ ALPHAENGINE BEAST v1.0: DSE/CSE HIGH-SPEED APPRAISAL TERMINAL")
pd_app.markdown("<style>div.block-container{padding-top:1.5rem;}</style>", unsafe_allow_html=True)
pd_app.markdown("---")

# -----------------------------------------------------------------
# 1. CORE ARCHITECTURE & SYSTEM FRAMEWORKS
# -----------------------------------------------------------------
pd_app.sidebar.header("🎯 Active Appraisal Framework")
mode = pd_app.sidebar.selectbox(
    "Select System Filter Mode",
    ["Growth Hunter", "Value Investor", "Momentum Swing", "Independent Custom"]
)

# Professional Frontiers Matrix
defaults = {
    "Growth Hunter": {"pe": 22.0, "peg": 1.1, "eps": 15.0, "rev": 12.0, "roe": 15.0, "de": 1.0, "rsi_min": 45.0, "rsi_max": 72.0, "min_sponsor": 30.0},
    "Value Investor": {"pe": 12.0, "peg": 0.9, "eps": 5.0, "rev": 4.0, "roe": 11.0, "de": 0.5, "rsi_min": 30.0, "rsi_max": 52.0, "min_sponsor": 30.0},
    "Momentum Swing": {"pe": 35.0, "peg": 1.8, "eps": 8.0, "rev": 8.0, "roe": 8.0, "de": 1.5, "rsi_min": 55.0, "rsi_max": 78.0, "min_sponsor": 20.0},
    "Independent Custom": {"pe": 16.0, "peg": 1.0, "eps": 10.0, "rev": 8.0, "roe": 12.0, "de": 0.9, "rsi_min": 40.0, "rsi_max": 70.0, "min_sponsor": 30.0}
}

current_limits = defaults[mode]

if mode == "Independent Custom":
    pd_app.sidebar.markdown("### 🛠️ Manual Limit Overwrite")
    t_pe = pd_app.sidebar.slider("Max P/E Ratio Boundary", 5.0, 60.0, current_limits["pe"])
    t_peg = pd_app.sidebar.slider("Max PEG Ratio Allowance", 0.2, 3.0, current_limits["peg"])
    t_eps = pd_app.sidebar.slider("Min EPS Growth Floor (%)", -5.0, 40.0, current_limits["eps"])
    t_rev = pd_app.sidebar.slider("Min Revenue Growth Floor (%)", -5.0, 40.0, current_limits["rev"])
    t_roe = pd_app.sidebar.slider("Min Return on Equity (%)", 0.0, 35.0, current_limits["roe"])
    t_de = pd_app.sidebar.slider("Max Debt-to-Equity Ratio", 0.1, 3.5, current_limits["de"])
    t_sponsor = pd_app.sidebar.slider("Min Sponsor Requirement (%)", 0.0, 100.0, current_limits["min_sponsor"])
    t_rsi = pd_app.sidebar.slider("RSI Momentum Window", 10, 90, (int(current_limits["rsi_min"]), int(current_limits["rsi_max"])))
    limits = {"pe": t_pe, "peg": t_peg, "eps": t_eps, "rev": t_rev, "roe": t_roe, "de": t_de, "rsi_min": t_rsi, "rsi_max": t_rsi, "min_sponsor": t_sponsor}
else:
    limits = current_limits
    pd_app.sidebar.info(f"🔒 System locks active for {mode}.")

pd_app.sidebar.markdown("---")
pd_app.sidebar.header("🏢 DSE Governance Profile")
dse_category = pd_app.sidebar.selectbox("Stock Category Tier (DSE/CSE)", ["A-Category (Regular Dividend)", "B-Category (Good, lower dividend)", "N-Category (New Listing)", "Z-Category (Junk/Default)"])
audit_status = pd_app.sidebar.selectbox("Auditor Report Certification Status", ["Unqualified / Clean Audit", "Qualified / Disclaimer Signalled", "Failed / Non-Compliant Layout"])

# -----------------------------------------------------------------
# 2. SECTOR AUTO-DETECTION ENTRY INTERFACE
# -----------------------------------------------------------------
pd_app.subheader("🔍 Active Workspace Console")
raw_ticker = pd_app.text_input("Enter Ticker Code (e.g. BRACBANK, GP, BATBC, SQURPHARMA, JAMUNAOIL)", "BRACBANK").upper().strip()

# Smart Core Sector Flag Processing Engine
financial_keywords = ["BANK", "ICB", "FINANCE", "INSURANCE", "PRIME", "MIDLAND", "TRUST", "LEASING", "UTILITY", "POWER"]
is_financial_sector = any(keyword in raw_ticker for keyword in financial_keywords)

if is_financial_sector:
    pd_app.sidebar.success("⚡ AUTOMATIC MODE: Banking/NBFI Profile Detected. Debt-to-Equity checks bypassed.")
else:
    pd_app.sidebar.info("🏭 AUTOMATIC MODE: Industrial/Manufacturing Profile Detected. D/E checks enforced.")

col_u1, col_u2, col_u3, col_u4 = pd_app.columns(4)
with col_u1:
    curr_price = pd_app.number_input("Last Traded Price - LTP (BDT)", min_value=0.1, value=42.50, step=0.1)
    pe_ratio = pd_app.number_input("Current Trailing P/E Multiple", min_value=0.0, value=11.20, step=0.1)
    nav_per_share = pd_app.number_input("Net Asset Value (NAVPS) (BDT)", min_value=0.0, value=34.80, step=0.1)

with col_u2:
    eps_growth = pd_app.number_input("Realized EPS Growth YoY (%)", value=14.50, step=0.5)
    rev_growth = pd_app.number_input("Corporate Revenue Growth YoY (%)", value=11.20, step=0.5)
    net_profit_margin = pd_app.number_input("Net Profit Margin (%)", value=13.40, step=0.5)

with col_u3:
    roe = pd_app.number_input("Return on Equity (ROE %)", value=15.20, step=0.1)
    if is_financial_sector:
        de_ratio = pd_app.number_input("Capital Adequacy Ratio (CAR %) [Replaces D/E]", value=13.50, step=0.1)
    else:
        de_ratio = pd_app.number_input("Debt to Equity Ratio (D/E)", value=0.45, step=0.05)
    div_yield = pd_app.number_input("Cash Dividend Yield (%)", value=4.80, step=0.1)

with col_u4:
    sponsor_share = pd_app.number_input("Sponsor / Director Shareholding (%)", min_value=0.0, max_value=100.0, value=32.40, step=0.5)
    rsi_val = pd_app.slider("Real-time RSI (14-Day Value)", 10, 90, 54)
    macd_status = pd_app.selectbox("MACD Signalling Cross Status", ["Bullish Crossover", "Bearish Crossover", "Neutral / Horizontal Trend"])

# Clear Derived Valuation Formulas
peg_ratio = pe_ratio / (eps_growth if eps_growth > 0 else 1.0)
pb_ratio = curr_price / (nav_per_share if nav_per_share > 0 else 1.0)

# -----------------------------------------------------------------
# 3. DSE REGULATORY CIRCUIT BREAKER ENGINE
# -----------------------------------------------------------------
def calculate_dse_circuit_breaker(price):
    if price < 200: return price * 0.10
    elif price < 500: return price * 0.0875
    elif price < 1000: return price * 0.075
    elif price < 2000: return price * 0.0625
    else: return price * 0.05

variance = calculate_dse_circuit_breaker(curr_price)
upper_circuit = curr_price + variance
lower_circuit = curr_price - variance

# -----------------------------------------------------------------
# 4. TRIPLE STRATEGY MATCH COMPLIANCE ALGORITHM
# -----------------------------------------------------------------
g_score, v_score, m_score = 0, 0, 0

# Growth Engine Architecture
if eps_growth >= limits["eps"]: g_score += 20
if rev_growth >= limits["rev"]: g_score += 20
if peg_ratio <= limits["peg"] and peg_ratio > 0: g_score += 20
if roe >= limits["roe"]: g_score += 15
if net_profit_margin >= 10: g_score += 15
if dse_category.startswith("A"): g_score += 10

# Value Engine Architecture
if pe_ratio <= limits["pe"] and pe_ratio > 0: v_score += 25
if pb_ratio <= 1.5: v_score += 20
if is_financial_sector:
    if de_ratio >= 12.5: v_score += 20  # Standard safety benchmark for financial entities
else:
    if de_ratio <= limits["de"]: v_score += 20
if div_yield >= 4.5: v_score += 20  
if sponsor_share >= limits["min_sponsor"]: v_score += 15

# Momentum Engine Architecture
if rsi_val >= limits["rsi_min"] and rsi_val <= limits["rsi_max"]: m_score += 35
if macd_status == "Bullish Crossover": m_score += 35
if dse_category.startswith("A") or dse_category.startswith("B"): m_score += 30

# -----------------------------------------------------------------
# 5. RISK ANALYSIS & REGULATORY FLAG FEED (RED FLAGS)
# -----------------------------------------------------------------
red_flags = []
if dse_category.startswith("Z"):
    red_flags.append("🚨 DSE CRITICAL ALERT: Z-Category 'Junk Stock' classification. High risk of suspension.")
if audit_status != "Unqualified / Clean Audit":
    red_flags.append(f"🚨 AUDIT COMPLIANCE EXPOSURE: Company financial books flagged with '{audit_status}'. Risk of window dressing.")
if sponsor_share < 30.0:
    red_flags.append(f"⚠️ REGULATORY WARNING: Sponsor holdings are at {sponsor_share:.1f}%, failing BSEC's mandatory 30% baseline threshold.")
if div_yield == 0 and dse_category.startswith("A"):
    red_flags.append("🚨 CASH FLOW DRIFT: Classified as A-Category asset but pays out 0% cash distributions.")
if not is_financial_sector and de_ratio > limits["de"]:
    red_flags.append(f"🚨 LEVERAGE THREAT: Industrial Debt-to-Equity ratio ({de_ratio}) breaches maximum limits ({limits['de']}).")
if is_financial_sector and de_ratio < 12.0:
    red_flags.append(f"🚨 CAPITALIZATION EMERGENCY: Capital Adequacy Ratio ({de_ratio}%) is dangerously thin compared to Central Bank standards.")

# Unified Portfolio Alpha Direction Calculation
master_health_rating = int((g_score + v_score + m_score) / 3)
if red_flags:
    master_health_rating -= (len(red_flags) * 12)
master_health_rating = max(0, min(100, master_health_rating))

# Output Core Interface Matrix Columns
c_metrics, c_visuals = pd_app.columns(2)

with c_metrics:
    pd_app.subheader("📊 Dynamic Financial Diagnostics")
    m1, m2, m3, m4 = pd_app.columns(4)
    m1.metric("Current Price", f"{curr_price:.2f} BDT")
    m2.metric("Trailing P/E", f"{pe_ratio:.2f}")
    m3.metric("Calculated PEG", f"{peg_ratio:.2f}")
    m4.metric("Price-to-Book (P/B)", f"{pb_ratio:.2f}")
    
    m5, m6, m7, m8 = pd_app.columns(4)
    m5.metric("EPS Growth YoY", f"{eps_growth:.1f}%")
    m6.metric("Revenue Growth", f"{rev_growth:.1f}%")
    m7.metric("Profit Margin", f"{net_profit_margin:.1f}%")
    m8.metric("Return on Equity", f"{roe:.1f}%")
    
    m9, m10, m11, m12 = pd_app.columns(4)
    m9.metric("Cash Yield %", f"{div_yield:.2f}%")
    m10.metric("Sponsor Position", f"{sponsor_share:.1f}%")
    if is_financial_sector:
        m11.metric("Capital Adequacy (CAR)", f"{de_ratio:.1f}%")
    else:
        m11.metric("Debt-to-Equity (D/E)", f"{de_ratio:.2f}")
    m12.metric("RSI Wave Level", f"{rsi_val}")

    pd_app.markdown("---")
    pd_app.subheader("🚨 Risk Warning Analysis Feed")
    if red_flags:
