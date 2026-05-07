import streamlit as st
import streamlit.components.v1 as components

# إعداد الصفحة لتكون احترافية
st.set_page_config(page_title="GOLD SNR SNIPER", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #05070a; color: white; }
    .stApp { background-color: #05070a; }
    .header-text {
        text-align: center; color: #FFD700;
        font-size: 35px; font-weight: bold; padding: 20px;
        text-shadow: 2px 2px 5px #000;
    }
    .signal-card {
        background-color: #11141a; border: 1px solid #FFD700;
        padding: 20px; border-radius: 15px; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header-text">🔱 رادار قناص الذهب (SNR) 🔱</div>', unsafe_allow_html=True)

# تقسيم الصفحة إلى قسمين: الشارت والتحليل
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📊 الشارت الموحد (Live)")
    # شارت احترافي يدعم التحليل الموحد
    chart_html = """
    <div class="tradingview-widget-container" style="height:550px;">
      <div id="tradingview_gold"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({
        "autosize": true, "symbol": "OANDA:XAUUSD", "interval": "15",
        "timezone": "Etc/UTC", "theme": "dark", "style": "1",
        "locale": "ar", "toolbar_bg": "#f1f3f6", "enable_publishing": false,
        "withdateranges": true, "hide_side_toolbar": false, "allow_symbol_change": true,
        "container_id": "tradingview_gold"
      });
      </script>
    </div>
    """
    components.html(chart_html, height=560)

with col2:
    st.markdown("### 🎯 إشارات القناص")
    
    # ويدجت التحليل الفني المتقدم (يعطي الترند والمناطق القوية)
    analysis_html = """
    <div class="tradingview-widget-container">
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
      {
      "interval": "1h",
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
    st.markdown('<div class="signal-card">', unsafe_allow_html=True)
    components.html(analysis_html, height=460)
    st.markdown('</div>', unsafe_allow_html=True)

st.write("---")
st.info("💡 **قاعدة الـ SNR:** ابحث عن مناطق 'الرفض' (Rejection) على فريم الـ 15 دقيقة لتأكيد الدخول مع الإشارة.")
