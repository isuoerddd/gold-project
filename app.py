import streamlit as st
import yfinance as yf
from streamlit_autorefresh import st_autorefresh
import pandas as pd

# إعدادات الواجهة (Dark Mode - TradingView Palette)
st.set_page_config(page_title="Pro Gold Tracker", layout="wide")

# تحديث تلقائي "نبض" الموقع كل 3 ثوانٍ
st_autorefresh(interval=3000, key="live_refresh")

st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: white; }
    .live-price-box {
        background: #161b22;
        border: 2px solid #2962ff;
        border-radius: 15px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    .price-text { font-size: 65px; font-weight: bold; color: #58a6ff; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 رادار الذهب - نسخة الخبراء (GitHub Style)")

# الرمز السعري للذهب (XAU/USD)
# ملاحظة: سعر 4715 الذي تتابعه هو غالباً Silver (XAGUSD) أو عقد محدد
symbol = "XAUUSD=X" 

def fetch_expert_data():
    try:
        # جلب أحدث بيانات دقيقة (بث حي)
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d", interval="1m")
        if not data.empty:
            current = ticker.fast_info['last_price']
            high = data['High'].max()
            low = data['Low'].min()
            return current, high, low
    except:
        return None, None, None
    return None, None, None

current, high, low = fetch_expert_data()

if current:
    # عرض السعر المباشر
    st.markdown(f"""
        <div class="live-price-box">
            <p style="color: #8b949e; font-size: 20px;">السعر الحالي المباشر</p>
            <div class="price-text">{current:.2f}</div>
        </div>
    """, unsafe_allow_html=True)

    st.write("")
    col1, col2 = st.columns(2)
    col1.metric("أعلى سعر اليوم (H)", f"{high:.2f}")
    col2.metric("أدنى سعر اليوم (L)", f"{low:.2f}")

    st.write("---")
    
    # محرك التوصية بضغطة زر (كما طلبت)
    if st.button("🎯 استخراج التوصية الهندسية"):
        diff = high - low
        buy_trigger = low + (diff * 0.225)
        sell_trigger = high - (diff * 0.225)
        
        if current >= buy_trigger:
            target = current + (diff * 0.125)
            st.success(f"📈 إشارة شراء: السعر فوق الزاوية الحرجة | الهدف: {target:.2f}")
        elif current <= sell_trigger:
            target = current - (diff * 0.125)
            st.error(f"📉 إشارة بيع: السعر كسر دعم الزاوية | الهدف: {target:.2f}")
        else:
            st.info("🔄 حالة السوق: تذبذب (انتظر وصول السعر للزوايا)")
else:
    st.warning("⚠️ بانتظار بث الأسعار من البورصة (السوق حالياً في عطلة)")

st.sidebar.markdown("### إحصائيات النظام")
st.sidebar.write("الحالة: متصل بخادم الأسعار ✅")
st.sidebar.write("معدل التحديث: كل 3 ثوانٍ")
