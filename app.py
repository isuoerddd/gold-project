import streamlit as st
import yfinance as yf
from streamlit_autorefresh import st_autorefresh

# إعداد واجهة المهندس
st.set_page_config(page_title="Gann TV Radar", layout="wide")

# تحديث تلقائي كل 10 ثوانٍ لضمان استقرار السيرفر
st_autorefresh(interval=10000, key="gold_refresh")

st.markdown("""
    <style>
    .main { background-color: #131722; color: #d1d4dc; }
    .price-card { background: #1e222d; border-radius: 10px; padding: 25px; border: 1px solid #363c4e; text-align: center; }
    .live-price { font-size: 55px; font-weight: bold; color: #2962ff; }
    .status-msg { padding: 10px; border-radius: 5px; background: #2a2e39; color: #b2b5be; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 رادار الذهب - TradingView Style")

# الرمز السعري للذهب (XAU/USD)
symbol = "GC=F" # عقود الذهب هي الأكثر استقراراً في البيانات

try:
    # جلب البيانات مع معالجة الأخطاء
    gold_data = yf.download(symbol, period="2d", interval="1m", progress=False)
    
    if not gold_data.empty:
        # استخراج الأسعار بشكل آمن لتجنب TypeError
        current_price = float(gold_data['Close'].iloc[-1])
        high_day = float(gold_data['High'].max())
        low_day = float(gold_data['Low'].min())
        
        # حساب زوايا جان (Logic)
        diff = high_day - low_day
        buy_trigger = low_day + (diff * 0.225)
        sell_trigger = high_day - (diff * 0.225)
        
        # العرض الاحترافي
        st.markdown(f"""
            <div class="price-card">
                <p style="color: #b2b5be;">GOLD / USD - LIVE FEED</p>
                <div class="live-price">${current_price:.2f}</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        col1, col2 = st.columns(2)
        col1.metric("أعلى سعر اليوم (H)", f"{high_day:.2f}")
        col2.metric("أدنى سعر اليوم (L)", f"{low_day:.2f}")
        
        st.write("---")
        # محرك التوصيات بناءً على السعر الحي
        if current_price >= buy_trigger:
            target = current_price + (diff * 0.125)
            st.success(f"🟢 إشارة شراء: السعر فوق زاوية الانطلاق | المستهدف: {target:.2f}")
        elif current_price <= sell_trigger:
            target = current_price - (diff * 0.125)
            st.error(f"🔴 إشارة بيع: السعر كسر مستويات الدعم | المستهدف: {target:.2f}")
        else:
            st.info("🔄 السعر حالياً في منطقة تذبذب (عرضي) - بانتظار اختراق الزوايا")
            
    else:
        st.warning("⚠️ السوق معزل حالياً أو جاري إعادة الاتصال بمزود الأسعار...")

except Exception as e:
    # عرض رسالة هادئة بدلاً من الكود الأحمر المزعج
    st.markdown("<div class='status-msg'>🔄 جاري تحديث نبض السوق... تأكد من اتصال الإنترنت</div>", unsafe_allow_html=True)
