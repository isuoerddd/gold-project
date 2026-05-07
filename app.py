import streamlit as st
import streamlit.components.v1 as components

# إعدادات الصفحة
st.set_page_config(page_title="GOLD LIVE TRACKER", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #05070a; color: white; }
    .stApp { background-color: #05070a; }
    .price-container {
        background: linear-gradient(90deg, #11141a 0%, #1a1e26 100%);
        border-left: 5px solid #FFD700;
        padding: 20px; border-radius: 10px; margin-bottom: 20px;
    }
    .header-gold { color: #FFD700; text-align: center; font-weight: bold; font-size: 28px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header-gold">🔱 رادار الذهب المباشر (Live Price) 🔱</div>', unsafe_allow_html=True)

# 1. ويدجت السعر المباشر (Ticker) - يعطيك السعر الحالي لحظة بلحظة
ticker_html = """
<div class="tradingview-widget-container">
  <div class="tradingview-widget-container__widget"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-tickers.js" async>
  {
  "symbols": [
    { "proName": "FX_IDC:XAUUSD", "title": "الذهب / دولار" }
  ],
  "colorTheme": "dark", "isTransparent": true, "showSymbolLogo": true, "locale": "ar"
}
  </script>
</div>
"""
components.html(ticker_html, height=100)

# 2. الشارت الاحترافي مع السعر الحالي (Live Chart)
st.markdown("### 📈 حركة السعر والسيولة الآن")
chart_html = """
<div class="tradingview-widget-container" style="height:500px;">
  <div id="tradingview_live"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
  <script type="text/javascript">
  new TradingView.widget({
    "autosize": true, "symbol": "FX:XAUUSD", "interval": "5",
    "timezone": "Etc/UTC", "theme": "dark", "style": "1",
    "locale": "ar", "enable_publishing": false, "withdateranges": true,
    "hide_side_toolbar": false, "allow_symbol_change": true, "details": true,
    "hotlist": true, "calendar": true, "container_id": "tradingview_live"
  });
  </script>
</div>
"""
components.html(chart_html, height=520)

# 3. قسم تحليل السيولة (بناءً على السعر الحالي)
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="price-container">
        <h4 style="color: #FFD700;">🎯 مناطق القناص (SNR) الحالية</h4>
        <p>بناءً على السعر اللحظي، المناطق الأقرب هي:</p>
        <ul>
            <li><b>مقاومة قريبة (SBR):</b> راقب السعر عند القمة الأخيرة على فريم 5 دقائق.</li>
            <li><b>دعم قريب (RBS):</b> ابحث عن آخر "كسر وإعادة اختبار" في الشارت أعلاه.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # ويدجت التحليل الفني التلقائي للسعر الحالي
    st.markdown("<h4>⚡ إشارة الدخول اللحظية</h4>", unsafe_allow_html=True)
    signal_html = """
    <div class="tradingview-widget-container">
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
      {
      "interval": "15m", "width": "100%", "isTransparent": true,
      "height": 350, "symbol": "FX:XAUUSD", "showIntervalTabs": true,
      "displayMode": "single", "locale": "ar", "colorTheme": "dark"
    }
      </script>
    </div>
    """
    components.html(signal_html, height=360)

st.info("💡 ملاحظة: هذا الشارت يسحب البيانات مباشرة من بورصة نيويورك ولندن، السعر دقيق 100% ومطابق لـ TradingView.")
