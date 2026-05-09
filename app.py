import streamlit as st

# إعداد واجهة المهندس الاحترافية
st.set_page_config(page_title="Ultra-Light Gold Radar", layout="wide")

# تصميم الثيم المظلم (Dark Mode) لراحة العين أثناء السكالبينج
st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: white; }
    .stNumberInput { background-color: #161b22 !important; border: 1px solid #2962ff !important; color: white !important; }
    .reportview-container .main .block-container { padding-top: 2rem; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ رادار الذهب السريع - نسخة السكالبينج")

# تقسيم الشاشة إلى جزءين: الشارت والحاسبة
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("📈 نبض السعر المباشر (TradingView)")
    # استخدام Widget مجاني وخفيف جداً لضمان عدم التعليق
    tradingview_widget = """
    <div class="tradingview-widget-container">
      <div id="tradingview_expert"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({
        "width": "100%",
        "height": 550,
        "symbol": "OANDA:XAUUSD",
        "interval": "1",
        "timezone": "Etc/UTC",
        "theme": "dark",
        "style": "1",
        "locale": "ar",
        "enable_publishing": false,
        "hide_side_toolbar": false,
        "allow_symbol_change": true,
        "container_id": "tradingview_expert"
      });
      </script>
    </div>
    """
    st.components.v1.html(tradingview_widget, height=560)

with col2:
    st.subheader("🧮 حاسبة السكالب")
    st.write("أدخل البيانات من الشارت:")
    
    # مدخلات يدوية لضمان سرعة الموقع وعدم حدوث خطأ في الاتصال
    high = st.number_input("أعلى سعر (High)", format="%.2f", value=2350.00)
    low = st.number_input("أدنى سعر (Low)", format="%.2f", value=2320.00)
    current = st.number_input("السعر الحالي", format="%.2f", value=2335.00)
    
    st.write("---")
    
    if st.button("🚀 تحليل فوري"):
        # معادلة الزوايا الهندسية (نسخة السكالب السريع)
        diff = high - low
        # مناطق الدخول الحرجة
        buy_trigger = low + (diff * 0.236)
        sell_trigger = high - (diff * 0.236)
        
        if current >= buy_trigger:
            target = current + (diff * 0.125)
            st.success(f"📈 إشارة شراء (سكالب)\nالهدف: {target:.2f}")
        elif current <= sell_trigger:
            target = current - (diff * 0.125)
            st.error(f"📉 إشارة بيع (سكالب)\nالهدف: {target:.2f}")
        else:
            st.info("🔄 السعر في منطقة توازن (انتظر)")

# شريط الأسعار السفلي (Ticker Tape) - خفيف جداً ومجاني
st.write("---")
ticker_tape = """
<div class="tradingview-widget-container">
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
  {
  "symbols": [
    {"proName": "FOREXCOM:XAUUSD", "title": "الذهب"},
    {"proName": "OANDA:XAGUSD", "title": "الفضة"},
    {"proName": "FX_IDC:USDIQD", "title": "الدولار/دينار"}
  ],
  "showSymbolLogo": true, "colorTheme": "dark", "isTransparent": true, "displayMode": "adaptive", "locale": "ar"
  }
  </script>
</div>
"""
st.components.v1.html(ticker_tape, height=100)
