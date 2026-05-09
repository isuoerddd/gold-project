import streamlit as st
import yfinance as yf

# إعدادات الصفحة
st.set_page_config(page_title="Gann Auto-Sniper", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: #e0e0e0; }
    .stMetric { background-color: #161b22; border-radius: 10px; padding: 15px; border: 1px solid #30363d; }
    .card { padding: 20px; border-radius: 15px; background: #161b22; border: 1px solid #30363d; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Gann Intelligence - النسخة الاحترافية")

# قائمة الأزواج
symbol_map = {
    "الذهب (XAU/USD)": "GC=F",
    "اليورو دولار (EUR/USD)": "EURUSD=X",
    "الباوند دولار (GBP/USD)": "GBPUSD=X"
}
choice = st.selectbox("اختر الزوج:", list(symbol_map.keys()))

if st.button("تحديث وتحليل الزوايا ⚡"):
    try:
        # جلب البيانات
        ticker = yf.Ticker(symbol_map[choice])
        hist = ticker.history(period="2d")
        
        if len(hist) < 2:
            st.error("عذراً، تعذر جلب بيانات كافية حالياً.")
        else:
            # استخراج الأرقام بدقة
            high = float(hist['High'].iloc[-2]) # قمة البارحة
            low = float(hist['Low'].iloc[-2])   # قاع البارحة
            current = float(ticker.fast_info['last_price'])
            
            # عرض المقاييس الأساسية
            c1, c2, c3 = st.columns(3)
            c1.metric("السعر الحالي", f"{current:.2f}")
            c2.metric("أعلى سعر (أمس)", f"{high:.2f}")
            c3.metric("أدنى سعر (أمس)", f"{low:.2f}")
            
            # حساب زوايا جان (Logic)
            diff = high - low
            mid_point = low + (diff * 0.5)
            buy_angle = low + (diff * 0.225)
            sell_angle = high - (diff * 0.225)
            
            st.write("---")
            
            # محرك التوصيات
            if current >= buy_angle and current < high:
                tp1 = current + (diff * 0.125)
                st.success(f"🟢 إشارة شراء (BUY) - الهدف الأول: {tp1:.2f}")
            elif current <= sell_angle and current > low:
                tp1 = current - (diff * 0.125)
                st.error(f"🔴 إشارة بيع (SELL) - الهدف الأول: {tp1:.2f}")
            else:
                st.warning("⚠️ منطقة تذبذب - انتظر اختراق الزوايا")
                
    except Exception as e:
        st.error(f"حدث خطأ أثناء جلب البيانات: {e}")

st.sidebar.write("خاص ببرمجة المهندس - 2026")
