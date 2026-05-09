import streamlit as st
import yfinance as yf
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# إعداد واجهة المهندس
st.set_page_config(page_title="Gann TV Radar", layout="wide")

# تحديث تلقائي كل 5 ثوانٍ (مثل تريدنج فيو)
st_autorefresh(interval=5000, key="datarefresh")

st.markdown("""
    <style>
    .main { background-color: #131722; color: #d1d4dc; }
    .price-card { background: #1e222d; border-radius: 10px; padding: 20px; border: 1px solid #363c4e; text-align: center; }
    .live-price { font-size: 48px; font-weight: bold; color: #2962ff; }
    .signal-buy { color: #089981; font-size: 24px; font-weight: bold; }
    .signal-sell { color: #f23645; font-size: 24px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 رادار الذهب - TradingView Style")

# الرمز السعري للذهب
symbol = "XAUUSD=X"

try:
    # جلب البيانات الحية
    gold = yf.Ticker(symbol)
    data = gold.history(period="2d", interval="1m")
    
    if not data.empty:
        current_price = gold.fast_info['last_price']
        high_day = data['High'].max()
        low_day = data['Low'].min()
        
        # حساب زوايا جان
        diff = high_day - low_day
        buy_zone = low_day + (diff * 0.225)
        sell_zone = high_day - (diff * 0.225)
        
        # عرض السعر في كارت فخم
        st.markdown(f"""
            <div class="price-card">
                <p>XAUUSD / GOLD (LIVE)</p>
                <div class="live-price">${current_price:.2f}</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("أعلى سعر اليوم (H)", f"{high_day:.2f}")
        with col2:
            st.metric("أدنى سعر اليوم (L)", f"{low_day:.2f}")

        # محرك القرار (التوصية)
        st.write("---")
        if current_price >= buy_zone:
            tp = current_price + (diff * 0.125)
            st.markdown(f"<div class='price-card'><span class='signal-buy'>🟢 إشارة شراء: المستهدف {tp:.2f}</span></div>", unsafe_allow_html=True)
        elif current_price <= sell_zone:
            tp = current_price - (diff * 0.125)
            st.markdown(f"<div class='price-card'><span class='signal-sell'>🔴 إشارة بيع: المستهدف {tp:.2f}</span></div>", unsafe_allow_html=True)
        else:
            st.info("🔄 السعر داخل منطقة التذبذب (عرضي)")

    else:
        st.error("جاري انتظار افتتاح السوق أو تحديث البيانات...")

except Exception as e:
    st.warning("⚠️ جاري الاتصال بخادم الأسعار العالمي...")
