import streamlit as st
import streamlit.components.v1 as components

# إعدادات الصفحة الفخمة
st.set_page_config(page_title="GOLD VIP SNIPER", layout="centered")

# تصميم الواجهة
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    h1 { text-align: center; color: #FFD700; font-family: 'Arial'; margin-bottom: 20px; }
    .footer { text-align: center; color: #888; font-size: 12px; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>👑 VIP GOLD RADAR</h1>")

# دمج "عداد التحليل الفني المباشر" من TradingView
# هذا العداد يعطي توصية (شراء/بيع) بناءً على أكثر من 20 مؤشر فني لحظياً
analysis_widget = """
<div class="tradingview-widget-container" style="margin: auto;">
  <div class="tradingview-widget-container__widget"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
  {
  "interval": "15m",
  "width": "100%",
  "isTransparent": true,
  "height": 450,
  "symbol": "OANDA:XAUUSD",
  "showIntervalTabs": true,
  "displayMode": "single",
  "locale": "ar",
  "colorTheme": "dark"
}
  </script>
</div>
"""

# دمج "شريط السعر المباشر" الموحد
price_ticker = """
<div class="tradingview-widget-container">
  <div class="tradingview-widget-container__widget"></div>
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

# عرض العناصر
components.html(price_ticker, height=130)
st.write("---")
components.html(analysis_widget, height=460)

st.markdown("<div class='footer'>ملاحظة: البيانات مباشرة وموحدة من بورصة الذهب العالمية XAU/USD</div>", unsafe_allow_html=True)
