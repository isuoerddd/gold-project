import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# إعدادات الواجهة البرمجية الاحترافية
st.set_page_config(page_title="EUR/USD Scalper Pro", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: #e0e0e0; }
    .stMetric { background-color: #161b22; border-radius: 10px; padding: 15px; border: 1px solid #30363d; }
    .signal-card {
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 20px;
        border: 2px solid #3b82f6;
        background: linear-gradient(145deg, #161b22, #0d1117);
    }
    .trend-up { color: #00ff00; font-weight: bold; }
    .trend-down { color: #ff4b4b; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# دالة جلب البيانات الحية
def fetch_data(symbol, period, interval):
    data = yf.download(symbol, period=period, interval=interval, progress=False)
    return data

# المحرك التحليلي (Logic Engine)
def analyze_scalp(df_m15, df_h1):
    # 1. تحديد الترند من الفريم الكبير (H1) باستخدام EMA 200
    df_h1['ema200'] = ta.ema(df_h1['Close'], length=200)
    current_h1 = df_h1['Close'].iloc[-1]
    ema_h1 = df_h1['ema200'].iloc[-1]
    
    trend = "UP" if current_h1 > ema_h1 else "DOWN"
    
    # 2. مؤشرات الدخول للفريم الصغير (M15)
    df_m15.ta.rsi(length=14, append=True)
    df_m15.ta.macd(append=True)
    
    last_rsi = df_m15['RSI_14'].iloc[-1]
    price = df_m15['Close'].iloc[-1]
    
    # منطق التوصية (مع الترند فقط)
    signal = "انتظار (No Setup)"
    if trend == "UP" and last_rsi < 40:
        signal = "BUY (شراء سكالب)"
    elif trend == "DOWN" and last_rsi > 60:
        signal = "SELL (بيع سكالب)"
        
    return trend, signal, price

# --- الواجهة الرئيسية ---
st.markdown("<h1 style='text-align: center; color: #58a6ff;'>💎 EUR/USD Scalper Intelligence</h1>", unsafe_allow_html=True)

symbol = "EURUSD=X"

if st.sidebar.button("تحديث النبض السعري 🔄"):
    # جلب البيانات
    df_m15 = fetch_data(symbol, "5d", "15m")
    df_h1 = fetch_data(symbol, "20d", "1h")
    
    trend, signal, current_price = analyze_scalp(df_m15, df_h1)
    
    # حساب الأهداف (50 نقطة = 0.0050)
    pip_value = 0.0050
    tp = current_price + pip_value if "BUY" in signal else current_price - pip_value
    sl = current_price - (pip_value * 0.6) if "BUY" in signal else current_price + (pip_value * 0.6)

    # عرض المقاييس الحية
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("السعر الحي الحالي", f"{current_price:.5f}")
    with c2:
        trend_class = "trend-up" if trend == "UP" else "trend-down"
        st.markdown(f"<div class='stMetric'>الاتجاه العام (H1): <span class='{trend_class}'>{trend}</span></div>", unsafe_allow_html=True)
    with c3:
        st.metric("قوة الزخم (RSI)", f"{df_m15['RSI_14'].iloc[-1]:.2f}")

    # كارت التوصية الاحترافي
    st.markdown(f"""
    <div class="signal-card">
        <h2 style='color: #58a6ff;'>إشارة القناص اللحظية</h2>
        <h1 style='color: {"#00ff00" if "BUY" in signal else "#ff4b4b" if "SELL" in signal else "#8b949e"}'>{signal}</h1>
        <p style='font-size: 1.2em;'>🎯 الهدف (TP): <b>{tp:.5f}</b> | 🛑 الوقف (SL): <b>{sl:.5f}</b></p>
        <small>سبب الدخول: توافق الترند الرئيسي مع تشبع لحظي على فريم 15 دقيقة</small>
    </div>
    """, unsafe_allow_html=True)

    # الشارت التفاعلي
    fig = go.Figure(data=[go.Candlestick(x=df_m15.index,
                open=df_m15['Open'], high=df_m15['High'],
                low=df_m15['Low'], close=df_m15['Close'])])
    fig.update_layout(template="plotly_dark", height=500, title="EUR/USD Scalping Chart (M15)")
    st.plotly_chart(fig, use_container_view=True)
else:
    st.info("اضغط على 'تحديث النبض السعري' لبدء التحليل اللحظي.")

st.sidebar.markdown("---")
st.sidebar.write("⚙️ **إدارة المخاطر:**")
st.sidebar.write("- أقصى عدد صفقات يومياً: 2")
st.sidebar.write("- المخاطرة لكل صفقة: 1% من الحساب")
st.sidebar.write("- نوع التحليل: Price Action + Trend Following")
