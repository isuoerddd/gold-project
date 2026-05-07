import streamlit as st
import yfinance as yf
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# إعدادات الواجهة
st.set_page_config(page_title="GOLD VIP SNIPER", layout="centered")
st_autorefresh(interval=60 * 1000, key="vip_refresh")

# التصميم الفخم
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1c2130; padding: 15px; border-radius: 15px; border: 1px solid #FFD700; }
    .recommendation-card { 
        padding: 30px; border-radius: 20px; text-align: center; margin: 20px 0;
        font-weight: bold; font-size: 24px; border: 2px solid #FFD700;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #FFD700;'>👑 VIP GOLD RADAR</h1>", unsafe_allow_html=True)

# دالة جلب السعر الموحد XAU/USD
def get_unified_price():
    try:
        # الرمز الموحد للذهب الفوري
        ticker = "XAUUSD=X"
        data = yf.download(ticker, period="2d", interval="5m", progress=False)
        
        if not data.empty:
            last_price = float(data['Close'].iloc[-1])
            # حساب RSI
            delta = data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi_val = float(100 - (100 / (1 + rs.iloc[-1])))
            
            high_day = float(data['High'].max())
            low_day = float(data['Low'].min())
            
            return last_price, rsi_val, high_day, low_day
    except Exception as e:
        return None

result = get_unified_price()

if result:
    price, rsi, d_high, d_low = result
    
    # عرض الأرقام
    col1, col2 = st.columns(2)
    col1.metric("سعر الذهب الموحد (LIVE)", f"${price:,.2f}")
    col2.metric("قوة السوق (RSI)", f"{rsi:.1f}%")

    st.write("---")

    # بطاقة التوصية
    if rsi < 32:
        st.markdown(f"<div class='recommendation-card' style='background-color: #004d00; color: #00ff00;'>🏹 اقتناص شراء فوراً</div>", unsafe_allow_html=True)
        st.balloons()
    elif rsi > 68:
        st.markdown(f"<div class='recommendation-card' style='background-color: #4d0000; color: #ff3333;'>📉 اقتناص بيع فوراً</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='recommendation-card' style='background-color: #1c2130; color: #FFD700;'>⏳ جاري رصد السيولة...<br><span style='font-size: 14px;'>السعر الآن في منطقة توازن</span></div>", unsafe_allow_html=True)

    st.info(f"📍 نطاق التحرك اليومي: ${d_low:.2f} — ${d_high:.2f}")
else:
    st.error("⚠️ جاري الاتصال بمزود الأسعار العالمي... يرجى الانتظار ثواني.")
    st.info("إذا استمرت هذه الرسالة، تأكد من تحديث ملف requirements.txt")

st.caption("ملاحظة: السعر مطابق لسعر الذهب الفوري العالمي XAU/USD")
