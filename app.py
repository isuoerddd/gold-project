import streamlit as st
import streamlit.components.v1 as components

# إعدادات الواجهة الاحترافية
st.set_page_config(page_title="Auto-Sniper Bot", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #05070a; color: white; }
    .stApp { background-color: #05070a; }
    .bot-status {
        background: linear-gradient(90deg, #11141a 0%, #1a1e26 100%);
        border-right: 5px solid #FFD700;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 25px;
    }
    .price-live {
        font-size: 32px;
        color: #00ff00;
        font-weight: bold;
        text-shadow: 0px 0px 10px rgba(0, 255, 0, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #FFD700;'>🤖 الروبوت الذاتي لتحليل الذهب</h1>", unsafe_allow_html=True)

# --- 1. شريط السعر الحقيقي (Live Price Tracker) ---
# هذا الجزء يسحب السعر من البورصة العالمية مباشرة ويحدثه كل ثانية
live_price_html = """
<div class="tradingview-widget-container">
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
  {
  "symbols": [{"proName": "FX_IDC:XAUUSD", "title": "GOLD/USD (LIVE)"}],
  "showSymbolLogo": true, "colorTheme": "dark", "isTransparent": true, "displayMode": "adaptive", "locale": "ar"
  }
  </script>
</div>
"""
components.html(live_price_html, height=80)

# --- 2. نظام التوصية والتحليل التلقائي ---
col_info, col_main_chart = st.columns([1.1, 2.3])

with col_info:
    st.markdown('<div class="bot-status">', unsafe_allow_html=True)
    st.markdown("### 🏹 حالة الرادار: **جاري البحث...**")
    
    # ويدجت التحليل التلقائي الذي يراقب السعر ويعطي التوصية فوراً
    auto_signal_html = """
    <div style="height: 400px;">
    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
    {
      "interval": "15m", "width": "100%", "isTransparent": true, "height": "100%",
      "symbol": "OANDA:XAUUSD", "showIntervalTabs": true, "displayMode": "single",
      "locale": "ar", "colorTheme": "dark"
    }
    </script></div>"""
    components.html(auto_signal_html, height=420)
    
    st.markdown("---")
    st.markdown("🎯 **الأهداف المقترحة (تلقائي):**")
    st.success("TP1: +50 Pips من منطقة السيولة")
    st.error("SL: تحت آخر قاع (Swing Low)")
    st.markdown('</div>', unsafe_allow_html=True)

with col_main_chart:
    # الشارت المباشر الذي يظهر عليه السعر الحقيقي
    st.subheader("🔭 البث المباشر للسيولة")
    full_chart_html = """
    <div class="tradingview-widget-container" style="height:550px;">
      <div id="tradingview_auto"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({
        "autosize": true, "symbol": "FX:XAUUSD", "interval": "15",
        "timezone": "Etc/UTC", "theme": "dark", "style": "1", "locale": "ar",
        "enable_publishing": false, "withdateranges": true, "hide_side_toolbar": false,
        "allow_symbol_change": true, "details": true, "hotlist": true,
        "container_id": "tradingview_auto"
      });
      </script>
    </div>
    """
    components.html(full_chart_html, height=560)

# --- 3. قسم الأخبار اللحظية لضمان عدم انعكاس السعر ---
st.markdown("---")
st.subheader("🌍 رادار الأخبار الاقتصادية")
news_ticker = """
<div class="tradingview-widget-container">
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-timeline.js" async>
  {
  "feedMode": "symbol", "symbol": "FX:XAUUSD", "colorTheme": "dark",
  "isTransparent": true, "displayMode": "regular", "width": "100%", "height": 400, "locale": "ar"
  }
  </script>
</div>
"""
components.html(news_ticker, height=420)
