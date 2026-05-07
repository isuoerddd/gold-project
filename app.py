import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Gold Intelligence", layout="wide")

st.markdown("<h1 style='text-align: center; color: #FFD700;'>🔱 نظام ذكاء الذهب والسيولة 🔱</h1>", unsafe_allow_html=True)

# تقسيم الصفحة
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 حركة الذهب اللحظية")
    # شارت احترافي يوضح مناطق السيولة تلقائياً
    chart_code = """
    <div class="tradingview-widget-container" style="height:500px;">
      <div id="tradingview_1"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({
        "autosize": true, "symbol": "OANDA:XAUUSD", "interval": "15",
        "timezone": "Etc/UTC", "theme": "dark", "style": "1",
        "locale": "ar", "enable_publishing": false, "withdateranges": true, "container_id": "tradingview_1"
      });
      </script>
    </div>
    """
    components.html(chart_code, height=520)

with col2:
    st.subheader("🔥 قوة الاتجاه (Trend)")
    # ويدجت يقيس قوة الشراء والبيع الآن
    gauge_code = """
    <div class="tradingview-widget-container">
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
      {
      "interval": "1h", "width": "100%", "isTransparent": true, "height": 450,
      "symbol": "OANDA:XAUUSD", "showIntervalTabs": true, "displayMode": "single",
      "locale": "ar", "colorTheme": "dark"
      }
      </script>
    </div>
    """
    components.html(gauge_code, height=460)

st.markdown("---")
st.markdown("### 💡 نصيحة القناص اليومية")
st.success("إذا كان عداد القوة يميل لـ 'شراء قوي'، ابحث عن مناطق RBS (دعم تحول لمقاومة) على فريم الـ 15 دقيقة.")
