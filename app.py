import streamlit as st
import yfinance as yf
from pandas_datareader import data as pdr
import time

# إعداد واجهة المستخدم
st.set_page_config(page_title="Live Gann Sniper", layout="centered")

# إضافة CSS لجعل الواجهة احترافية ومظلمة
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: white; }
    .live-price { font-size: 60px; font-weight: bold; color: #58a6ff; text-align: center; }
    .status-card { padding: 20px; border-radius: 15px; background: #161b22; border: 1px solid #30363d; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ رادار الذهب الهندسي (بث مباشر)")

# تحديد الرمز (Ticker) من الصور التي أرسلتها
symbol = "GC=F" # هذا يعطيك سعر الذهب العالمي المباشر

def get_live_data():
    ticker = yf.Ticker(symbol)
    # جلب بيانات آخر يومين لاستخراج الـ High والـ Low
    df = ticker.history(period="2d", interval="1m")
    if not df.empty:
        current = ticker.fast_info['last_price']
        high = df['High'].max()
        low = df['Low'].min()
        return current, high, low
    return None, None, None

# --- منطقة التحديث التلقائي ---
# سنقوم بعمل حلقة Loop لتحديث السعر كل 2 ثانية
placeholder = st.empty()

while True:
    current, high, low = get_live_data()
    
    with placeholder.container():
        if current:
            diff = high - low
            mid = low + (diff * 0.5)
            buy_zone = low + (diff * 0.225)
            sell_zone = high - (diff * 0.225)
            
            st.markdown(f"<div class='live-price'>{current:.2f}</div>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            col1.metric("أعلى سعر اليوم", f"{high:.2f}")
            col2.metric("أدنى سعر اليوم", f"{low:.2f}")
            
            st.write("---")
            
            # منطق اتخاذ القرار التلقائي
            if current >= buy_zone:
                target = current + (diff * 0.125)
                st.success(f"✅ إشارة شراء (Live): المستهدف القادم {target:.2f}")
            elif current <= sell_zone:
                target = current - (diff * 0.125)
                st.error(f"⚠️ إشارة بيع (Live): المستهدف القادم {target:.2f}")
            else:
                st.info("🔄 السعر في منطقة تذبذب.. بانتظار حركة الزوايا")
        else:
            st.warning("جاري الاتصال بمزود البيانات... تأكد من استقرار الإنترنت")
            
    # توقف لمدة ثانيتين قبل التحديث القادم
    time.sleep(2)
