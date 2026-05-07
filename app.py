import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="GOLD LIQUIDITY RADAR", layout="centered")

# تصميم الواجهة الاحترافية (بدون تعقيد)
st.markdown("""
    <style>
    .main { background-color: #05070a; color: white; }
    .price-box { 
        font-size: 50px; font-weight: bold; text-align: center; 
        color: #FFD700; padding: 20px; border: 2px solid #FFD700; border-radius: 20px;
    }
    .status-tag { 
        text-align: center; padding: 10px; border-radius: 10px; 
        font-weight: bold; margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>💎 GOLD LIQUIDITY RADAR</h2>", unsafe_allow_html=True)

def fetch_data():
    # محاولة جلب السعر الموحد بطريقة إجبارية
    ticker = yf.Ticker("XAUUSD=X")
    df = ticker.history(period="1d", interval="1m")
    if df.empty:
        # خطة بديلة فورية للذهب الآجل لضمان عدم توقف الموقع
        ticker = yf.Ticker("GC=F")
        df = ticker.history(period="1d", interval="1m")
    return df

try:
    data = fetch_data()
    current_p = data['Close'].iloc[-1]
    high_p = data['High'].max()
    low_p = data['Low'].min()
    
    # عرض السعر الموحد الكبير
    st.markdown(f"<div class='price-box'>${current_p:,.2f}</div>", unsafe_allow_html=True)
    
    st.write("---")
    
    # تحليل مناطق السيولة (المنطق الماليزي)
    # المنطقة العلوية (Supply) والمنطقة السفلية (Demand)
    col1, col2 = st.columns(2)
    
    with col1:
        st.error(f"🚨 منطقة العرض (Supply)\n\n${high_p:,.2f}")
    with col2:
        st.success(f"✅ منطقة الطلب (Demand)\n\n${low_p:,.2f}")

    # التوصية الذكية بناءً على المسافة من المناطق
    dist_to_high = high_p - current_p
    dist_to_low = current_p - low_p
    
    if dist_to_low < 1.5:
        st.markdown("<div class='status-tag' style='background-color: #00ff00; color: black;'>🏹 اقتناص شراء من منطقة الطلب</div>", unsafe_allow_html=True)
    elif dist_to_high < 1.5:
        st.markdown("<div class='status-tag' style='background-color: #ff0000; color: white;'>📉 اقتناص بيع من منطقة العرض</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='status-tag' style='background-color: #1c2130; color: #FFD700;'>🔎 مراقبة السيولة.. السعر بين المناطق</div>", unsafe_allow_html=True)

except Exception as e:
    st.error("جاري إعادة الربط بالبورصة العالمية...")
    time.sleep(2)
    st.rerun()

st.caption("نظام الرادار: يعتمد على أعلى وأدنى مستويات السيولة لليوم الحالي.")
