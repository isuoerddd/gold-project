import streamlit as st
import yfinance as yf
import time

# إعدادات الواجهة
st.set_page_config(page_title="Gann Live Sniper", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0d1117; color: white; }
    .price-display { font-size: 55px; font-weight: bold; color: #58a6ff; text-align: center; padding: 15px; background: #161b22; border-radius: 15px; border: 1px solid #30363d; margin-bottom: 20px; }
    .card { padding: 20px; border-radius: 15px; background: #161b22; border: 1px solid #30363d; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ رادار الذهب الهندسي المباشر")

# الرمز السعري للذهب الفوري
ticker_symbol = "XAUUSD=X"

# حاوية التحديث التلقائي
placeholder = st.empty()

while True:
    try:
        # جلب البيانات الحية
        gold = yf.Ticker(ticker_symbol)
        current_price = gold.fast_info['last_price']
        
        # جلب القمة والقاع لليوم
        hist = gold.history(period="1d")
        high_price = hist['High'].iloc[-1]
        low_price = hist['Low'].iloc[-1]
        
        with placeholder.container():
            # عرض السعر الكبير
            st.markdown(f"<div class='price-display'>{current_price:.2f}</div>", unsafe_allow_html=True)
            
            # حساب مستويات جان
            diff = high_price - low_price
            buy_trigger = low_price + (diff * 0.225)
            sell_trigger = high_price - (diff * 0.225)
            
            col1, col2 = st.columns(2)
            col1.metric("أعلى سعر اليوم", f"{high_price:.2f}")
            col2.metric("أدنى سعر اليوم", f"{low_price:.2f}")
            
            st.write("---")
            
            # محرك القرار
            if current_price >= buy_trigger:
                target = current_price + (diff * 0.125)
                st.success(f"🟢 إشارة شراء: المستهدف القادم {target:.2f}")
            elif current_price <= sell_trigger:
                target = current_price - (diff * 0.125)
                st.error(f"🔴 إشارة بيع: المستهدف القادم {target:.2f}")
            else:
                st.info("🔄 السعر في منطقة انتظار الزوايا...")
                
    except Exception as e:
        st.error("جاري إعادة الاتصال بمزود الأسعار...")
    
    # تحديث كل 5 ثوانٍ لضمان الاستقرار
    time.sleep(5)
