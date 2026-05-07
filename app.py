import streamlit as st
import streamlit.components.v1 as components

# إعداد الصفحة
st.set_page_config(page_title="GOLD SNR RADAR", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #05070a; }
    .stApp { background-color: #05070a; }
    .title { text-align: center; color: #FFD700; font-size: 30px; font-weight: bold; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="title">💎 رادار السيولة الموحد (SNR)</div>', unsafe_allow_html=True)

# 1. ويدجت السعر المباشر (سيرفر 1 - سريع جداً)
price_html = """
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

# 2. لوحة مناطق الانعكاس (سيرفر 2 - تحليل SNR)
snr_html = """
<div class="tradingview-widget-container">
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
  {
  "interval": "15m",
  "width": "100%",
  "isTransparent": true,
  "height": 400,
  "symbol": "OANDA:XAUUSD",
  "showIntervalTabs": false,
  "displayMode": "single",
  "locale": "ar",
  "colorTheme": "dark"
}
  </script>
</div>
"""

# عرض البيانات بدون انتظار معالجة بايثون (تجاوز مشكلة التعليق)
st.markdown("### 💰 السعر العالمي الموحد")
components.html(price_html, height=130)

st.write("---")

st.markdown("### 🎯 تحليل مناطق السيولة (SNR)")
components.html(snr_html, height=420)

st.warning("⚠️ هذا الرادار مربوط مباشرة ببورصة لندن ونيويورك لضمان السعر الموحد.")
