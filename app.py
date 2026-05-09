import streamlit as st
import yfinance as yf
import pandas as pd

# إعدادات الواجهة المستوحاة من TradingView
st.set_page_config(page_title="Expert Gann Radar", layout="wide")

# وظيفة الخبراء: جلب البيانات وتخزينها مؤقتاً لسرعة الاستجابة
@st.cache_data(ttl=10) # تحديث التخزين كل 10 ثوانٍ
def fetch_pro_data(symbol):
    ticker = yf.Ticker(symbol)
    df = ticker.history(period="1d", interval="1m")
    if not df.empty:
        return {
            "current": ticker.fast_info['last_price'],
            "high": df['High'].max(),
            "low": df['Low'].min()
        }
    return None

# واجهة الرادار
st.title("🛡️ رادار الذهب - نسخة المهندسين")

symbol = "XAUUSD=X" # رمز الذهب العالمي
data = fetch_pro_data(symbol)

if data:
    # عرض السعر الحالي بشكل ضخم
    st.markdown(f"""
        <div style="background:#1e222d; padding:30px; border-radius:15px; border-left:5px solid #2962ff; text-align:center;">
            <h3 style="color:#d1d4dc; margin:0;">XAUUSD LIVE</h3>
            <h1 style="color:#2962ff; font-size:70px; margin:0;">{data['current']:.2f}</h1>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    col1.metric("أعلى سعر (High)", f"{data['high']:.2f}")
    col2.metric("أدنى سعر (Low)", f"{data['low']:.2f}")

    # زر التوصية الذكية
    st.write("---")
    if st.button("🚀 استخراج تحليل الزوايا الآن"):
        h, l, c = data['high'], data['low'], data['current']
        diff = h - l
        # معادلة جان المختصرة
        buy_zone = l + (diff * 0.225)
        sell_zone = h - (diff * 0.225)
        
        if c >= buy_zone:
            st.success(f"📈 الإشارة: شراء (BUY) | المستهدف: {c + (diff * 0.125):.2f}")
        elif c <= sell_zone:
            st.error(f"📉 الإشارة: بيع (SELL) | المستهدف: {c - (diff * 0.125):.2f}")
        else:
            st.info("🔄 السعر في منطقة انتظار عرضية")
else:
    st.warning("⚠️ جاري تحديث البيانات من خادم البورصة...")
