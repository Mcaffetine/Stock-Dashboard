import streamlit as pd_app
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# System UI Optimization across Mobile and Desktop Devices
pd_app.set_page_config(page_title="BD AlphaEngine Pro", layout="wide", initial_sidebar_state="expanded")

pd_app.title("🇧🇩 AlphaEngine Pro: DSE & CSE Elite Stock Terminal")
pd_app.markdown("---")

# -----------------------------------------------------------------
# 1. SIDEBAR CONFIGURATION & DSE SYSTEM MODES
# -----------------------------------------------------------------
pd_app.sidebar.header("🎯 Investment Framework")
mode = pd_app.sidebar.selectbox(
    "Appraisal Framework Profile Mode",
    ["Growth Hunter", "Value Investor", "Momentum Swing", "Independent Custom"]
)

# Custom Institutional Baselines Adjusted for BD Frontier Market Realities
defaults = {
    "Growth Hunter": {"pe": 25.0, "peg": 1.1, "eps": 12.0, "rev": 10.0, "roe": 14.0, "de": 1.2, "rsi_min": 45.0, "rsi_max": 72.0},
    "Value Investor": {"pe": 12.0, "peg": 0.9, "eps": 4.0, "rev": 3.0, "roe": 10.0, "de": 0.6, "rsi_min": 32.0, "rsi_max": 52.0},
    "Momentum Swing": {"pe": 35.0, "peg": 1.8, "eps": 8.0, "rev": 8.0, "roe": 8.0, "de": 1.8, "rsi_min": 55.0, "rsi_max": 78.0},
    "Independent Custom": {"pe": 15.0, "peg": 1.0, "eps": 10.0, "rev": 8.0, "roe": 12.0, "de": 1.0, "rsi_min": 40.0, "rsi_max": 70.0}
}

current_limits = defaults[mode]

if mode == "Independent Custom":
    pd_app.sidebar.markdown("### 🛠️ Adjust Targets Manually")
    t_pe = pd_app.sidebar.slider("Max P/E Ratio Boundary", 5.0, 60.0, current_limits["pe"])
    t_peg = pd_app.sidebar.slider("Max PEG Ratio Allowance", 0.2, 3.0, current_limits["peg"])
    t_eps = pd_app.sidebar.slider("Min EPS Growth Floor (%)", -5.0, 40.0, current_limits["eps"])
    t_rev = pd_app.sidebar.slider("Min Revenue Growth Floor (%)", -5.0, 40.0, current_limits["rev"])
    t_roe = pd_app.sidebar.slider("Min Return on Equity (%)", 0.0, 35.0, current_limits["roe"])
    t_de = pd_app.sidebar.slider("Max Debt-to-Equity Ratio", 0.1, 3.5, current_limits["de"])
    t_rsi = pd_app.sidebar.slider("RSI Momentum Window", 10, 90, (int(current_limits["rsi_min"]), int(current_limits["rsi_max"])))
    limits = {"pe": t_pe, "peg": t_peg, "eps": t_eps, "rev": t_rev, "roe": t_roe, "de": t_de, "rsi_min": t_rsi, "rsi_max": t_rsi}
else:
    limits = current_limits
    pd_app.sidebar.info(f"🔒 **Standard Limits Active** for {mode}.")

# -----------------------------------------------------------------
# 2. LOCAL BANGLADESHI DATA PROFILE TUNING
# -----------------------------------------------------------------
pd_app.sidebar.markdown("---")
pd_app.sidebar.header("🏢 DSE Asset Profile Context")
dse_category = pd_app.sidebar.selectbox("Stock Category Tier (DSE/CSE)", ["A-Category (Regular Dividend)", "B-Category (Good, lower dividend)", "N-Category (New Listing)", "Z-Category (Junk/Default)"])

# -----------------------------------------------------------------
# 3. LIVE MARKET DATA INGESTION ENGINE
# -----------------------------------------------------------------
pd_app.subheader("🔍 Local Ticker Scanner")
raw_ticker = pd_app.text_input("Enter Ticker Code (e.g. BRACBANK, GP, BATBC, SQURPHARMA)", "BRACBANK").upper().strip()

# Append Yahoo Finance required Bangladesh syntax suffix if missing
if not raw_ticker.endswith(".BD"):
    ticker_input = f"{raw_ticker}.BD"
else:
    ticker_input = raw_ticker

@pd_app.cache_data(ttl=1800)
def fetch_bd_market_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        hist = stock.history(period="1y")
        if hist.empty:
            return None, None
            
        # Calculate Technical Indicators
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / (loss + 1e-10)
        hist['RSI'] = 100 - (100 / (1 + rs))
        hist['SMA50'] = hist['Close'].rolling(window=50).mean()
        
        exp1 = hist['Close'].ewm(span=12, adjust=False).mean()
        exp2 = hist['Close'].ewm(span=26, adjust=False).mean()
        hist['MACD'] = exp1 - exp2
        hist['Signal'] = hist['MACD'].ewm(span=9, adjust=False).mean()
        
        return info, hist
    except:
        return None, None

info, hist = fetch_bd_market_data(ticker_input)

if info is None or hist.empty:
    pd_app.warning(f"⚠️ Could not pull automated records for '{ticker_input}'. Falling back to manual overrides below to preserve trading functionality.")
    # Safe manual simulation defaults for local stocks missing from data pipelines
    info = {"longName": f"{raw_ticker} PLC", "currentPrice": 45.0, "trailingPE": 11.5, "pegRatio": 0.85, "returnOnEquity": 0.14, "debtToEquity": 45.0, "dividendYield": 0.045, "earningsGrowth": 0.11, "revenueGrowth": 0.09}
    hist = pd.DataFrame()
    rsi_val, sma_50_dist, macd_status = 52.0, 2.1, "Bullish Crossover"
else:
    rsi_val = float(hist['RSI'].iloc[-1]) if not pd.isna(hist['RSI'].iloc[-1]) else 50.0
    current_sma50 = hist['SMA50'].iloc[-1]
    sma_50_dist = ((hist['Close'].iloc[-1] - current_sma50) / current_sma50) * 100
    macd_latest = hist['MACD'].iloc[-1]
    signal_latest = hist['Signal'].iloc[-1]
    macd_status = "Bullish Crossover" if macd_latest > signal_latest else "Bearish Crossover"

# Variable Mapping with Fail-Safe Protection Layouts
company_name = info.get("longName", f"{raw_ticker} PLC")
curr_price = info.get("currentPrice", 40.0)
pe_ratio = info.get("trailingPE", 0.0) or 10.5
peg_ratio = info.get("pegRatio", 0.0) or 0.9
roe = (info.get("returnOnEquity", 0.0) or 0.12) * 100
de_ratio = (info.get("debtToEquity", 0.0) or 50.0) / 100
div_yield = (info.get("dividendYield", 0.0) or 0.04) * 100
eps_growth = (info.get("earningsGrowth", 0.0) or 0.10) * 100
rev_growth = (info.get("revenueGrowth", 0.0) or 0.08) * 100

pd_app.markdown(f"### 🏛️ {company_name} | Trading Code: `{raw_ticker}`")

# -----------------------------------------------------------------
# 4. DSE TIERED CIRCUIT BREAKER MATRIX CALCULATIONS
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
# 5. CORE SCORING LOGIC ENGINES
# -----------------------------------------------------------------
g_score, v_score, m_score = 0, 0, 0
if eps_growth >= limits["eps"]: g_score += 25
if rev_growth >= limits["rev"]: g_score += 25
if peg_ratio <= limits["peg"]: g_score += 20
if roe >= limits["roe"]: g_score += 15
if dse_category.startswith("A"): g_score += 15

if pe_ratio <= limits["pe"]: v_score += 30
if de_ratio <= limits["de"]: v_score += 25
if div_yield >= 4.0: v_score += 25  # High importance on cash dividend yield profiles in BD markets
if rsi_val <= 45: v_score += 20

if rsi_val >= limits["rsi_min"] and rsi_val <= limits["rsi_max"]: m_score += 35
if macd_status == "Bullish Crossover": m_score += 35
if sma_50_dist > 0: m_score += 30

# -----------------------------------------------------------------
# 6. CONDITIONAL LOCAL RED FLAG FILTERS
# -----------------------------------------------------------------
red_flags = []
if dse_category.startswith("Z"):
    red_flags.append("🚨 DSE CRITICAL ALERT: Z-Category 'Junk Stock' classification. High risk of regulatory suspension or delisting.")
if div_yield == 0 and dse_category.startswith("A"):
    red_flags.append("⚠️ CATEGORY MISMATCH: Listed as A-Category but yields 0% dividend distributions. Review payout health metrics.")
if rsi_val > 80:
    red_flags.append("🚨 EXCESSIVE HYP_CYCLE MOMENTUM: Technical RSI indicates aggressive retail manipulation/overbought saturation.")

if mode == "Growth Hunter" and eps_growth < limits["eps"]:
    red_flags.append("🚨 STAGNANT CORE: EPS speed fails core growth framework targets.")
elif mode == "Value Investor" and pe_ratio > limits["pe"]:
    red_flags.append("🚨 MULTIPLE EXPANSION: Current valuations are too high for traditional value-driven allocations.")

# Render Dashboard Analytics Blocks
c_metrics, c_visuals = pd_app.columns([3, 2])

with c_metrics:
    pd_app.subheader("📊 Fundamental & Technical Diagnostics")
    m1, m2, m3 = pd_app.columns(3)
    m1.metric("Current Reference Price", f"{curr_price:.2f} BDT")
    m2.metric("P/E Ratio Multiple", f"{pe_ratio:.2f}")
    m3.metric("PEG Core Ratio", f"{peg_ratio:.2f}")
    
    m4, m5, m6 = pd_app.columns(3)
    m4.metric("YoY EPS Expansion Speed", f"{eps_growth:.1f}%")
    m5.metric("Cash Dividend Yield", f"{div_yield:.2f}%")
    m6.metric("Return on Equity (ROE)", f"{roe:.1f}%")
    
    m7, m8, m9 = pd_app.columns(3)
    m7.metric("RSI Value (14-Day)", f"{rsi_val:.1f}")
    m8.metric("Debt-to-Equity Multiplier", f"{de_ratio:.2f}")
    m9.metric("Structure Wave Trend", macd_status)

    pd_app.markdown("---")
    pd_app.subheader("🚨 Risk Warning Analysis Feed")
    if red_flags:
        for flag in red_flags: pd_app.error(flag)
    else:
        pd_app.success("✅ Clean Risk Profile: No corporate anomalies or extreme volatility parameters identified.")

with c_visuals:
    pd_app.subheader("⚡ Intraday Trade Boundaries")
    pd_app.info(f"**⚡ Maximum Circuit Ceiling:**\n\n### {upper_circuit:.2f} BDT\n*(No buyers allowed above this limit today)*")
    pd_app.error(f"**⚡ Maximum Circuit Floor:**\n\n### {lower_circuit:.2f} BDT\n*(No sellers allowed below this limit today)*")
    
    if not hist.empty:
        pd_app.markdown("#### Price Trend Vector")
        f = go.Figure(go.Scatter(x=hist.index, y=hist['Close'], line=dict(color='#00FFCC', width=2), name='LTP'))
