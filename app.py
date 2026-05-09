import streamlit as st
import yfinance as yf
import pandas as pd

# إعدادات الواجهة الاحترافية (Dark Mode)
st.set_page_config(page_title="Gann Live Sniper", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0d1117; color: white; }
    .price-container { 
        background: #161b22; 
        border-radius: 15px; 
        padding: 20px; 
        border: 2px solid #58a6ff; 
        text-align: center; 
        margin-bottom: 20px;
    }
    .live-label { color: #8b949e; font-size: 18px; }
    .price-value { font-size: 50px; font-weight: bold; color: #58a6ff; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ رادار الذهب الهندسي (بث حي)")

# الرمز السعري (استخدمنا الرمز الأكثر دقة للذهب الفوري)
symbol = "XAUUSD=X"

# دالة جلب البيانات اللحظية
def get_live_market_data():
    ticker = yf.Ticker(symbol)
    # جلب بيانات دقيقة جداً (آخر 1 دقيقة)
    data = ticker.history(period="1d", interval="1m")
    if not data.empty:
        current = ticker.fast_info['last_price']
        high = float(data['High'].max())
        low = float(data['Low'].min())
        return current, high, low
    return None, None, None

# --- عرض السعر الحي ---
current, high, low = get_live_market_data()

if current:
    st.markdown(f"""
        <div class="price-container">
            <div class="live-label">سعر الذهب الآن (مباشر)</div>
            <div class="price-value">{current:.2f}</div>
        </div>
    """, unsafe_allow_html=True)

    # عرض القمة والقاع لليوم
    c1, c2 = st.columns(2)
    c1.metric("أعلى سعر اليوم", f"{high:.2f}")
    c2.metric("أدنى سعر اليوم", f"{low:.2f}")
    
    st.write("---")

    # --- زر استخراج التوصية ---
    if st.button("🎯 استخراج التوصية بناءً على السعر الحالي"):
        diff = high - low
        # حساب الزوايا
        buy_trigger = low + (diff * 0.225)
        sell_trigger = high - (diff * 0.225)
        
        if current >= buy_trigger:
            target = current + (diff * 0.125)
            st.success(f"🟢 إشارة شراء (BUY): السعر مستقر فوق الزاوية | المستهدف: {target:.2f}")
        elif current <= sell_trigger:
            target = current - (diff * 0.125)
            st.error(f"🔴 إشارة بيع (SELL): السعر كسر زاوية الدعم | المستهدف: {target:.2f}")
        else:
            st.info("🔄 السعر في منطقة تذبذب عرضي.. انتظر ملامسة الزوايا")
else:
    st.warning("⚠️ جاري الاتصال بمزود الأسعار.. تأكد من افتتاح السوق")

# إضافة تنبيه بسيط للمستخدم
st.sidebar.info("الموقع يحدّث السعر تلقائياً عند إعادة تحميل الصفحة أو الضغط على زر التحليل.")
