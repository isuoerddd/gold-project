import streamlit as st
import streamlit.components.v1 as components

# إعداد الصفحة لتكون عريضة واحترافية
st.set_page_config(page_title="Gold SNR Sniper", layout="wide")

st.title("📊 رادار الذهب (TradingView + SNR)")

# كود تضمين شارت TradingView المباشر
tradingview_widget = """
<div class="tradingview-widget-container" style="height:550px;">
  <div id="tradingview_gold"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
  <script type="text/javascript">
  new TradingView.widget({
    "autosize": true,
    "symbol": "OANDA:XAUUSD",
    "interval": "15",
    "timezone": "Etc/UTC",
    "theme": "dark",
    "style": "1",
    "locale": "en",
    "toolbar_bg": "#f1f3f6",
    "enable_publishing": false,
    "hide_side_toolbar": false,
    "allow_symbol_change": true,
    "container_id": "tradingview_gold"
  });
  </script>
</div>
"""

# عرض الشارت في الموقع
components.html(tradingview_widget, height=560)

st.write("---")
st.subheader("🎯 استراتيجية قنص الـ SNR")

col1, col2 = st.columns(2)
with col1:
    st.success("🟢 مناطق الشراء (RBS)")
    st.info("انتظر كسر مقاومة قوية، ثم ابحث عن إعادة اختبارها لتتحول إلى دعم جديد.")

with col2:
    st.error("🔴 مناطق البيع (SBR)")
    st.info("انتظر كسر دعم قوي، ثم ابحث عن إعادة اختباره ليتحول إلى مقاومة جديدة.")
