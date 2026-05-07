import streamlit as st
import streamlit.components.v1 as components

# إعداد الصفحة لتكون واسعة وفخمة
st.set_page_config(page_title="GOLD SNR RADAR", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .title-text {
        text-align: center; color: #FFD700;
        font-size: 32px; font-weight: bold; margin-bottom: 10px;
    }
    .status-bar {
        background-color: #1c2130; color: #FFD700;
        padding: 10px; border-radius: 10px; text-align: center;
        border: 1px solid #FFD700; margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="title-text">🎯 رادار العرض والطلب (SNR)</p>', unsafe_allow_html=True)
st.markdown('<div class="status-bar">🟢 النظام يعمل الآن بالسعر الموحد من البورصة العالمية</div>', unsafe_allow_html=True)

# 1. ويدجت السعر اللحظي الموحد (Ticker)
price_ticker = """
<div class="tradingview-widget-container">
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-single-quote.js" async>
  {
  "symbol": "OANDA:XAUUSD",
  "colorTheme": "dark",
  "width": "100%",
  "locale": "ar"
}
  </script>
</div>
"""

# 2. ويدجت التحليل الفني (العداد) لإعطاء التوصية الجاهزة
analysis_widget = """
<div class="tradingview-widget-container">
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
  {
  "interval": "15m",
  "width": "100%",
  "isTransparent": true,
  "height": 430,
  "symbol": "OANDA:XAUUSD",
  "showIntervalTabs": true,
  "displayMode": "single",
  "locale": "ar",
  "colorTheme": "dark"
}
  </script>
</div>
"""

# توزيع العناصر في أعمدة
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 💰 السعر الموحد والسيولة")
    components.html(price_ticker, height=150)
    st.write("---")
    st.markdown("### 📊 توصية القناص (SNR)")
    components.html(analysis_widget, height=450)

with col2:
    st.markdown("### 🕯️ شارت العرض والطلب (LIVE)")
    # ويدجت الشارت المصغر للمتابعة
    mini_chart = """
    <div class="tradingview-widget-container" style="height:550px;">
      <div id="tradingview_gold"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({
          "autosize": true, "symbol": "OANDA:XAUUSD", "interval": "15",
          "timezone": "Etc/UTC", "theme": "dark", "style": "1",
          "locale": "ar", "enable_publishing": false, "hide_top_toolbar": true,
          "save_image": false, "container_id": "tradingview_gold"
      });
      </script>
    </div>
    """
    components.html(mini_chart, height=560)

st.info("💡 ملاحظة: العداد يحلل مناطق العرض والطلب بناءً على 26 مؤشر فني ليعطيك الخلاصة.")
