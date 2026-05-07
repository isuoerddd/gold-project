import streamlit as st
import streamlit.components.v1 as components

# إعدادات الصفحة
st.set_page_config(page_title="Alpha Gold Live", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #05070a; color: white; }
    .stApp { background-color: #05070a; }
    .signal-card {
        background: linear-gradient(135deg, #0d1117 0%, #1a1e26 100%);
        border: 2px solid #FFD700;
        padding: 25px;
        border-radius: 20px;
        text-align: center;
    }
    .live-price-box {
        background-color: #11141a;
        border: 1px solid #FFD700;
        padding: 15px;
        border-radius: 10px;
        color: #00ff00;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #FFD700;'>⚡ روبوت القناص الرقمي المباشر ⚡</h1>", unsafe_allow_html=True)

# --- القسم الأول: السعر المباشر (Live Ticker) ---
# هذا الويدجت يجلب السعر الحقيقي الآن من البورصة
ticker_html = """
<div class="tradingview-widget-container">
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-tickers.js" async>
  {
  "symbols": [{ "proName": "OANDA:XAUUSD", "title": "XAU/USD (LIVE)" }],
  "colorTheme": "dark", "isTransparent": true, "showSymbolLogo": true, "locale": "ar"
  }
  </script>
</div>
"""
components.html(ticker_html, height=100)

# --- القسم الثاني: التوصية والشارت ---
col_sig, col_chart = st.columns([1, 2.2])

with col_sig:
    st.markdown('<div class="signal-card">', unsafe_allow_html=True)
    st.markdown("### 🎯 توصية الروبوت اللحظية")
    
    # محاكاة إشارة مرتبطة بالسعر المباشر
    st.markdown("<p style='color: #00ff00; font-size: 22px;'>BUY LIMIT</p>", unsafe_allow_html=True)
    
    st.write("📍 **نقطة الدخول المقترحة:**")
    st.info("ابحث عن ارتداد من أقرب منطقة RBS")
    
    st.write("🏁 **الأهداف الرقمية:**")
    st.success("Target 1: +40 Pips")
    st.success("Target 2: +100 Pips")
    
    st.write("🛑 **وقف الخسارة:**")
    st.error("-30 Pips من سعر الدخول")
    
    st.markdown("---")
    st.write("💡 **حالة السوق الآن:**")
    # ويدجت يعطي الإشارة بناءً على السعر الحالي تماماً
    signal_gauge = """
    <div style="height: 200px;">
    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
    {
      "interval": "15m", "width": "100%", "isTransparent": true, "height": "100%",
      "symbol": "OANDA:XAUUSD", "showIntervalTabs": false, "displayMode": "single",
      "locale": "ar", "colorTheme": "dark"
    }
    </script></div>"""
    components.html(signal_gauge, height=220)
    st.markdown('</div>', unsafe_allow_html=True)

with col_chart:
    # الشارت الاحترافي المباشر (يتحدث كل ثانية)
    st.subheader("🔭 الرادار الرقمي (Live Chart)")
    chart_html = """
    <div class="tradingview-widget-container" style="height:550px;">
      <div id="tv_live_robot"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({
        "autosize": true, "symbol": "OANDA:XAUUSD", "interval": "15",
        "timezone": "Etc/UTC", "theme": "dark", "style": "1", "locale": "ar",
        "toolbar_bg": "#f1f3f6", "enable_publishing": false, "withdateranges": true,
        "hide_side_toolbar": false, "allow_symbol_change": true, "details": true,
        "container_id": "tv_live_robot"
      });
      </script>
    </div>
    """
    components.html(chart_html, height=560)

# ملف الـ Requirements.txt سيبقى: streamlit فقط
