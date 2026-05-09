import streamlit as st
import streamlit.components.v1 as components

# إعدادات الواجهة الاحترافية
st.set_page_config(page_title="Gann TV Sniper", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #131722; color: white; }
    .stNumberInput { border: 1px solid #2962ff !important; }
    .card { padding: 20px; border-radius: 10px; background: #1e222d; border: 1px solid #363c4e; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 رادار الذهب - TradingView Sniper")

# --- الجزء الأول: شارت TradingView المباشر ---
st.subheader("📈 نبض السوق المباشر (TradingView)")
tradingview_widget = """
<div class="tradingview-widget-container">
  <div id="tradingview_12345"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
  <script type="text/javascript">
  new TradingView.widget({
    "width": "100%",
    "height": 400,
    "symbol": "OANDA:XAUUSD",
    "interval": "1",
    "timezone": "Etc/UTC",
    "theme": "dark",
    "style": "1",
    "locale": "ar",
    "toolbar_bg": "#f1f3f6",
    "enable_publishing": false,
    "hide_top_toolbar": true,
    "save_image": false,
    "container_id": "tradingview_12345"
  });
  </script>
</div>
"""
components.html(tradingview_widget, height=420)

st.write("---")

# --- الجزء الثاني: حاسبة زوايا جان ---
st.subheader("🧮 حاسبة الأهداف الذكية")

with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        high = st.number_input("أعلى سعر اليوم (High)", value=2350.0, format="%.2f")
    with col2:
        low = st.number_input("أدنى سعر اليوم (Low)", value=2320.0, format="%.2f")
    with col3:
        current = st.number_input("السعر الحالي من الشارت", value=2335.0, format="%.2f")

if st.button("تحليل الزوايا واستخراج الأهداف 🚀"):
    diff = high - low
    buy_trigger = low + (diff * 0.225)
    sell_trigger = high - (diff * 0.225)
    
    st.write("")
    
    if current >= buy_trigger:
        tp1 = current + (diff * 0.125)
        st.success(f"🟢 إشارة شراء (BUY) | الهدف القادم: {tp1:.2f}")
    elif current <= sell_trigger:
        tp1 = current - (diff * 0.125)
        st.error(f"🔴 إشارة بيع (SELL) | الهدف القادم: {tp1:.2f}")
    else:
        st.info("🔄 السعر في منطقة انتظار (Wait Zone)")
