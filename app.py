import streamlit as st
import yfinance as yf
import pandas as pd

# إعدادات واجهة المستخدم الاحترافية
st.set_page_config(page_title="Gann Auto-Sniper Pro", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: #e0e0e0; }
    .stMetric { background-color: #161b22; border-radius: 10px; padding: 15px; border: 1px solid #30363d; }
    .card { padding: 20px; border-radius: 15px; background: #161b22; border: 1px solid #30363d; text-align: center; }
    .buy-zone { border: 2px solid #39d353; background: rgba(57, 211, 83, 0.05); }
    .sell-zone { border: 2px solid #f85149; background: rgba(248, 81, 73, 0.05); }
    </style>
    """, unsafe_allow_html=True)

# دالة جلب البيانات الحية
def get_market_data(ticker):
    data = yf.download(ticker, period="2d", interval="1h")
    # الـ High والـ Low لشمعة البارحة (أو آخر شمعة مكتملة)
    daily_high = data['High'].max()
    daily_low = data['Low'].min()
    current_price = yf.Ticker(ticker).fast_info['last_price']
    return daily_high, daily_low, current_price

# --- الواجهة الرئيسية ---
st.markdown("<h1 style='text-align: center; color: #58a6ff;'>🚀 Gann Auto-Sniper Intelligence</h1>", unsafe_allow_html=True)
st.write("---")

# اختيار الزوج المراد تحليله
symbol_map = {
    "الذهب (XAU/USD)": "GC=F",
    "اليورو دولار (EUR/USD)": "EURUSD=X",
    "الباوند دولار (GBP/USD)": "GBPUSD=X"
}
choice = st.selectbox("اختر الزوج لتحليله فوراً:", list(symbol_map.keys()))

if st.button("تحديث النبض السعري والتحليل ⚡"):
    with st.spinner('جاري سحب البيانات الحية من البورصة...'):
        high, low, current = get_market_data(symbol_map[choice])
        
        diff = high - low
        # مستويات جان (Angles)
        level_22_buy = low + (diff * 0.225)
        level_22_sell = high - (diff * 0.225)
        
        # عرض البيانات الأساسية
        c1, c2, c3 = st.columns(3)
        c1.metric("السعر الحالي", f"{current:.2f}")
        c2.metric("أعلى سعر (High)", f"{high:.2f}")
        c3.metric("أدنى سعر (Low)", f"{low:.2f}")
        
        st.write("---")

        # --- محرك التوصيات الذكي ---
        if current >= level_22_buy and current < high:
            # حالة الشراء
            tp1 = current + (diff * 0.125)
            tp2 = current + (diff * 0.250)
            sl = current - (diff * 0.08)
            
            st.markdown(f"""
            <div class="card buy-zone">
                <h2 style="color: #39d353;">🟢 إشارة شراء (BUY) مؤكدة</h2>
                <p>السعر دخل منطقة القوة بناءً على زاوية 22.5°</p>
                <div style="display: flex; justify-content: space-around;">
                    <div><p>الهدف الأول</p><h3>{tp1:.2f}</h3></div>
                    <div><p>الهدف الثاني</p><h3>{tp2:.2f}</h3></div>
                    <div><p>وقف الخسارة</p><h3 style="color:#f85149">{sl:.2f}</h3></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        elif current <= level_22_sell and current > low:
            # حالة البيع
            tp1 = current - (diff * 0.125)
            tp2 = current - (range_val * 0.250)
            sl = current + (diff * 0.08)
            
            st.markdown(f"""
            <div class="card sell-zone">
                <h2 style="color: #f85149;">🔴 إشارة بيع (SELL) مؤكدة</h2>
                <p>السعر كسر زوايا الدعم العلوي وبدأ الهبوط</p>
                <div style="display: flex; justify-content: space-around;">
                    <div><p>الهدف الأول</p><h3>{tp1:.2f}</h3></div>
                    <div><p>الهدف الثاني</p><h3>{tp2:.2f}</h3></div>
                    <div><p>وقف الخسارة</p><h3 style="color:#39d353">{sl:.2f}</h3></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ السعر حالياً في منطقة تذبذب (Wait Zone). بانتظار الخروج من زوايا جان الجانبية.")

st.sidebar.markdown("### 🛠️ إعدادات المهندس")
st.sidebar.info("هذا الموقع يسحب البيانات من ياهو فاينانس مباشرة. التحديث يتم لحظياً عند الضغط على الزر.")
st.sidebar.write("تذكر: إدارة المخاطر أهم من التوصية نفسها.")
