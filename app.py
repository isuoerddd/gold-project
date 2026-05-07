import streamlit as st
import yfinance as yf
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# إعدادات الفخامة والواجهة
st.set_page_config(page_title="GOLD VIP SNIPER", layout="centered")
st_autorefresh(interval=60 * 1000, key="vip_refresh")

# ستايل CSS لتنسيق البطاقات والألوان
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1c2130; padding: 15px; border-radius: 15px; border: 1px solid #FFD700; }
    .recommendation-card { 
        padding: 30px; 
        border-radius: 20px; 
        text-align: center; 
        margin: 20px 0;
        font-weight: bold;
        font-size: 24px;
        border: 2px solid #FFD700;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #FFD700;'>👑 VIP GOLD RADAR</h1>", unsafe_allow_html=True)

@st.cache_data(ttl=30) # تقليل الكاش لزيادة الدقة
def get_signals():
    # استخدام رمز الذهب الفوري الموحد XAUUSD=X
    ticker = "XAUUSD=X"
    data = yf.Ticker(ticker).history(period="2d", interval="5m")
    
    # حساب RSI سريع
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rsi = 100 - (100 / (1 + (gain/loss)))
    
    return data['Close'].iloc[-1], rsi.iloc[-1], data['High'].max(), data['Low'].min()

try:
    price, rsi, daily_high, daily_low = get_signals()

    # لوحة المعلومات الرقمية
    col1, col2 = st.columns(2)
    col1.metric("سعر الذهب الفوري (LIVE)", f"${price:,.2f}")
    col2.metric("قوة السوق (RSI)", f"{rsi:.1f}%")

    st.write("---")

    # بطاقة التوصية الذكية
    if rsi < 32:
        st.markdown(f"""<div class='recommendation-card' style='background-color: #004d00; color: #00ff00;'>
            🏹 اقتناص شراء فوراً<br><span style='font-size: 15px;'>السعر موحد عند الدعم والـ RSI منخفض</span>
            </div>""", unsafe_allow_html=True)
        st.balloons()
    elif rsi > 68:
        st.markdown(f"""<div class='recommendation-card' style='background-color: #4d0000; color: #ff3333;'>
            📉 اقتناص بيع فوراً<br><span style='font-size: 15px;'>السعر موحد عند المقاومة والـ RSI مرتفع</span>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class='recommendation-card' style='background-color: #1c2130; color: #FFD700;'>
            ⏳ جاري رصد السيولة...<br><span style='font-size: 15px;'>السعر في منطقة محايدة، انتظر إشارة القناص</span>
            </div>""", unsafe_allow_html=True)

    # نصيحة تقنية
    st.markdown("### 💡 مراقبة السعر الموحد:")
    st.info(f"أعلى سعر لليوم: ${daily_high:.2f} | أدنى سعر لليوم: ${daily_low:.2f}")

except:
    st.warning("جاري مزامنة السعر الموحد مع البورصة العالمية...")

st.caption("ملاحظة: السعر المعتمد هو XAU/USD (الذهب الفوري) لضمان المطابقة مع منصات التداول.")
