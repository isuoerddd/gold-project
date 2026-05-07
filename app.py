import streamlit as st
import yfinance as yf
import pandas as pd

# إعدادات الواجهة
st.set_page_config(page_title="GOLD DEEP ANALYSIS", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #05070a; color: white; }
    .report-card { 
        padding: 20px; border-radius: 15px; border: 1px solid #FFD700;
        background-color: #11141a; text-align: center; margin-bottom: 20px;
    }
    .signal-buy { color: #00ff00; font-size: 24px; font-weight: bold; }
    .signal-sell { color: #ff0000; font-size: 24px; font-weight: bold; }
    .trend-box { padding: 10px; border-radius: 5px; font-weight: bold; display: inline-block; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: #FFD700;'>👑 نظام التحليل العميق للذهب</h2>", unsafe_allow_html=True)

@st.cache_data(ttl=60)
def analyze_gold():
    # جلب بيانات الذهب الفوري (السعر الموحد)
    # نستخدم السعر المباشر ونحلل آخر 100 شمعة لفهم الترند والمناطق
    data = yf.download("XAUUSD=X", period="5d", interval="15m", progress=False)
    if data.empty:
        data = yf.download("GC=F", period="5d", interval="15m", progress=False)
    
    # 1. تحليل السعر الحالي
    current_price = float(data['Close'].iloc[-1])
    
    # 2. تحديد مناطق العرض والطلب القوية (أقوى قمة وقاع في 5 أيام)
    strong_supply = float(data['High'].max())
    strong_demand = float(data['Low'].min())
    
    # 3. تحليل الترند (استخدام المتوسطات المتحركة)
    sma_50 = data['Close'].rolling(window=50).mean().iloc[-1]
    trend = "صاعد 📈" if current_price > sma_50 else "هابط 📉"
    trend_color = "#00ff00" if trend == "صاعد 📈" else "#ff0000"
    
    # 4. منطق الإشارة (Signal)
    signal = "انتظر سيولة"
    instruction = "السعر في منطقة محايدة، لا تفتح صفقات عشوائية."
    
    if current_price >= (strong_supply - 2):
        signal = "بيع قوي (Strong Sell)"
        instruction = f"السعر عند منطقة عرض تاريخية ({strong_supply:.2f}). ابحث عن تأكيد انعكاسي."
    elif current_price <= (strong_demand + 2):
        signal = "شراء قوي (Strong Buy)"
        instruction = f"السعر عند منطقة طلب تاريخية ({strong_demand:.2f}). ابحث عن تأكيد شرائي."
    
    return current_price, strong_supply, strong_demand, trend, trend_color, signal, instruction

try:
    price, supply, demand, trend, t_color, signal, instr = analyze_gold()
    
    # عرض النتائج
    st.markdown(f"<div class='report-card'><h3>السعر الموحد الآن</h3><h1 style='color:#FFD700;'>${price:,.2f}</h1></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("🚩 **اتجاه الترند الحالي:**")
        st.markdown(f"<div class='trend-box' style='background-color:{t_color}; color:black;'>{trend}</div>", unsafe_allow_html=True)
    with col2:
        st.write("🎯 **حالة الإشارة:**")
        color = "#00ff00" if "Buy" in signal else ("#ff0000" if "Sell" in signal else "#FFD700")
        st.markdown(f"<b style='color:{color}; font-size:20px;'>{signal}</b>", unsafe_allow_html=True)

    st.write("---")
    
    # تفصيل المناطق القوية
    st.markdown("### 🔍 خريطة المناطق القوية (SNR)")
    st.error(f"🔴 منطقة العرض (Supply Zone): **${supply:.2f}**")
    st.success(f"🟢 منطقة الطلب (Demand Zone): **${demand:.2f}**")
    
    st.info(f"💡 **توجيه القناص:** {instr}")

except:
    st.error("جاري سحب البيانات الموحدة وتحليل الاتجاه... يرجى تحديث الصفحة.")

st.caption("التحليل يعتمد على دمج حركة السعر (Price Action) مع المتوسطات المتحركة (SMA 50).")
