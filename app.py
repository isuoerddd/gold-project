import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Multi-Frame Sniper", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #05070a; color: white; }
    .stApp { background-color: #05070a; }
    .sidebar .sidebar-content { background-color: #11141a; }
    .f-choice { color: #FFD700; font-size: 20px; font-weight: bold; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# العنوان
st.markdown("<h1 style='text-align: center; color: #FFD700;'>🔱 قناص الذهب المتعدد الفريمات 🔱</h1>", unsafe_allow_html=True)

# 1. قائمة اختيار الفريم في الجانب
with st.sidebar:
    st.markdown("<p class='f-choice'>إعدادات الرادار</p>", unsafe_allow_html=True)
    frame = st.selectbox("اختر الفريم الزمني:", ["1", "5", "15", "60", "240", "D"], index=2)
    st.info("💡 نصيحة: استخدم الفريمات الكبيرة لتحديد الاتجاه، والصغيرة لنقطة الدخول.")

# 2. الشارت الذكي (يتغير حسب الفريم المختار)
st.subheader(f"📊 شارت الذهب - فريم ({frame}) دقيقة")

chart_code = f"""
<div class="tradingview-widget-container" style="height:550px;">
  <div id="tv_chart"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
  <script type="text/javascript">
  new TradingView.widget({{
    "autosize": true,
    "symbol": "OANDA:XAUUSD",
    "interval": "{frame}",
    "timezone": "Etc/UTC",
    "theme": "dark",
    "style": "1",
    "locale": "ar",
    "enable_publishing": false,
    "withdateranges": true,
    "hide_side_toolbar": false,
    "allow_symbol_change": true,
    "details": true,
    "container_id": "tv_chart"
  }});
  </script>
</div>
"""
components.html(chart_code, height=560)

# 3. تحليل القوة اللحظي (يتوافق مع الفريم المختار)
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🏹 استراتيجية القناص لهذا الفريم")
    if frame in ["1", "5"]:
        st.warning("⚠️ أنت الآن في 'منطقة القنص'. ابحث عن سحب سيولة (Liquidity Sweep) للدخول السريع.")
    elif frame in ["15", "60"]:
        st.info("ℹ️ أنت في 'فريم التأكيد'. ابحث عن كسر مناطق RBS/SBR واضحة.")
    else:
        st.success("🎯 أنت في 'فريم المستثمر'. حدد مناطق الدعم والمقاومة التاريخية.")

with col2:
    # ويدجت التحليل التقني يتغير أيضاً مع الفريم
    gauge_code = f"""
    <div class="tradingview-widget-container">
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
      {{
      "interval": "{'1m' if frame=='1' else '5m' if frame=='5' else '15m' if frame=='15' else '1h' if frame=='60' else '4h' if frame=='240' else '1D'}",
      "width": "100%", "isTransparent": true, "height": 380,
      "symbol": "OANDA:XAUUSD", "showIntervalTabs": false, "displayMode": "single",
      "locale": "ar", "colorTheme": "dark"
      }}
      </script>
    </div>
    """
    components.html(gauge_code, height=400)
