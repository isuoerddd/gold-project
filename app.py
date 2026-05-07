import streamlit as st
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

# 1. إعداد واجهة المستخدم السينمائية
st.set_page_config(page_title="Gold Sniper Live", layout="wide")

# 2. تحديث تلقائي للنظام كل دقيقتين لضمان استقرار الاتصال
st_autorefresh(interval=120 * 1000, key="auto_refresh_prime")

# 3. عنوان المنصة بتصميم أنيق
st.markdown("""
    <h1 style='text-align: center; color: #FFD700; font-family: sans-serif;'>🏹 رادار الذهب المباشر | GOLD LIVE SNIPER</h1>
    <p style='text-align: center; color: #888;'>تحليل SNR و RSI مباشر - بدون تأخير - تحديث لحظي</p>
    """, unsafe_allow_html=True)

# 4. دمج شارت TradingView المتقدم (النسخة الاحترافية)
# أضفت لك مؤشرات ZigZag لتحديد القمم والقيعان (SNR) تلقائياً
tradingview_widget = """
<div class="tradingview-widget-container" style="height:650px;">
  <div id="tradingview_gold_pro"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
  <script type="text/javascript">
  new TradingView.widget({
    "autosize": true,
    "symbol": "OANDA:XAUUSD",
    "interval": "15",
    "timezone": "Etc/UTC",
    "theme": "dark",
    "style": "1",
    "locale": "ar",
    "toolbar_bg": "#131722",
    "enable_publishing": false,
    "withdateranges": true,
    "hide_side_toolbar": false,
    "allow_symbol_change": true,
    "details": true,
    "hotlist": true,
    "calendar": true,
    "show_popup_button": true,
    "popup_width": "1000",
    "popup_height": "650",
    "studies": [
      "RSI@tv-basicstudies",
      "StochasticRSI@tv-basicstudies",
      "ZigZag@tv-basicstudies"
    ],
    "container_id": "tradingview_gold_pro"
  });
  </script>
</div>
"""

# عرض الشارت في الموقع
components.html(tradingview_widget, height=660)

# 5. شريط التنبيهات الذكي في الأسفل
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.info("💡 **كيف تقرأ الشارت؟** مؤشر ZigZag (الخطوط الملونة) يحدد لك مناطق الدعم والمقاومة SNR تلقائياً.")

with col2:
    st.success("✅ **توصية RSI:** إذا وصل الخط الأزرق في الأسفل تحت مستوى 30، ابحث عن فرصة شراء فوراً.")

st.caption("التحديث: مباشر بالثانية من خوادم البورصة العالمية.")
