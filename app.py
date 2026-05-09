import streamlit as st
import yfinance as yf
from streamlit_autorefresh import st_autorefresh

# إعداد واجهة المهندس
st.set_page_config(page_title="Gann Live Sniper", layout="wide")

# تحديث تلقائي كل 5 ثوانٍ لضمان "نبض" السعر
st_autorefresh(interval=5000, key="price_refresh")

st.markdown("""
    <style>
    .main { background-color: #0d1117; color: white; }
    .price-card { 
        background: #161b22; 
        border-radius: 15px; 
        padding: 30px; 
        border: 2px solid #58a6ff; 
        text-align: center; 
    }
    .live-val { font-size: 60px; font-weight: bold; color: #58a6ff; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ رادار الذهب الهندسي (بث حي)")

# الرمز السعري (بناءً على صورتك 4715 هو الفضة XAGUSD=X)
# إذا تريد الذهب الفوري غيره إلى XAUUSD=X
symbol = "XAGUSD=X" 

try:
    ticker = yf.Ticker(symbol)
    # جلب بيانات دقيقة جداً
    df = ticker.history(period="1d", interval="1m")
    
    if not df.empty:
        current_price = float(df['Close'].iloc[-1])
        high_day = float(df['High'].max())
        low_day = float(df['Low'].min())
        
        # عرض السعر الحي
        st.markdown(f"""
            <div class="price-card">
                <p style="color: #8b949e;">السعر الحالي المباشر</p>
                <div class="live-val">{current_price:.3f}</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        c1, c2 = st.columns(2)
        c1.metric("أعلى سعر اليوم", f"{high_day:.3f}")
        c2.metric("أدنى سعر اليوم", f"{low_day:.3f}")
        
        # حساب الزوايا بضغطة زر
        st.write("---")
        if st.button("🎯 استخراج التوصية والهدف"):
            diff = high_day - low_day
            buy_trigger = low_day + (diff * 0.225)
            sell_trigger = high_day - (diff * 0.225)
            
            if current_price >= buy_trigger:
                tp = current_price + (diff * 0.125)
                st.success(f"🟢 إشارة شراء: المستهدف القادم {tp:.3f}")
            elif current_price <= sell_trigger:
                tp = current_price - (diff * 0.125)
                st.error(f"🔴 إشارة بيع: المستهدف القادم {tp:.3f}")
            else:
                st.info("🔄 السعر في منطقة انتظار الزوايا")
    else:
        # رسالة في حال كان السوق مغلق (مثل الآن)
        st.warning("⚠️ السوق معزّل حالياً. سيتم عرض البيانات فور افتتاح البورصة.")
        st.info("ملاحظة: يمكنك تجربة الموقع يوم الاثنين لمشاهدة السعر يتحرك لحظياً.")

except Exception as e:
    st.error("جاري إعادة الاتصال بمزود الأسعار العالمي...")

