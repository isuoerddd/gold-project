import streamlit as st
import yfinance as yf
import pandas as pd

# كود احترافي مستوحى من أنظمة الـ Scalping على GitHub
def get_pro_market_data(ticker_symbol):
    try:
        # جلب البيانات اللحظية (بث حي)
        ticker = yf.Ticker(ticker_symbol)
        # ميزة الخبراء: استخدام fast_info لجلب سعر اللحظة بدون تأخير
        current_price = ticker.fast_info['last_price']
        
        # جلب بيانات اليوم لحساب القمة والقاع (High/Low)
        df = ticker.history(period="1d", interval="1m")
        if not df.empty:
            daily_high = df['High'].max()
            daily_low = df['Low'].min()
            return current_price, daily_high, daily_low
    except Exception as e:
        return None, None, None
    return None, None, None

# واجهة المستخدم (User Interface)
st.set_page_config(page_title="Pro Gann Radar", layout="wide")
st.title("🛡️ رادار الذهب - نسخة الخبراء")

# الرمز السعري للذهب الفوري
symbol = "XAUUSD=X"

# تنفيذ الجلب
price, h, l = get_pro_market_data(symbol)

if price:
    # تنسيق العرض (Dashboard)
    st.markdown(f"""
        <div style="background-color:#161b22; padding:20px; border-radius:10px; border:2px solid #238636; text-align:center;">
            <h2 style="color:#8b949e;">السعر المباشر الآن</h2>
            <h1 style="color:#58a6ff; font-size:60px;">{price:.2f}</h1>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    col1.metric("أعلى سعر اليوم", f"{h:.2f}")
    col2.metric("أدنى سعر اليوم", f"{l:.2f}")

    # محرك التوصية (هذا الجزء مخصص لك بناءً على معادلة جان)
    st.write("---")
    if st.button("🚀 استخراج التوصية الذكية"):
        range_val = h - l
        buy_point = l + (range_val * 0.225)
        sell_point = h - (range_val * 0.225)
        
        if price >= buy_point:
            st.success(f"📈 الإشارة: شراء (Buy) - الهدف: {price + (range_val * 0.125):.2f}")
        elif price <= sell_point:
            st.error(f"📉 الإشارة: بيع (Sell) - الهدف: {price - (range_val * 0.125):.2f}")
        else:
            st.info("🔄 حالة السوق: تذبذب - انتظر حركة السعر نحو الزوايا")
else:
    st.warning("⚠️ بانتظار اتصال السيرفر بالبورصة العالمية (السوق مغلق حالياً)")
