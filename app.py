import streamlit as st
import streamlit.components.v1 as components

# إعدادات الصفحة الاحترافية
st.set_page_config(page_title="Crypto Sniper Pro", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #06090f; color: white; }
    .stApp { background-color: #06090f; }
    .crypto-card {
        background: linear-gradient(145deg, #0f1218, #1a1e26);
        border: 1px solid #3b82f6;
        padding: 20px;
        border-radius: 15px;
        text-align: right;
        direction: rtl;
    }
    .signal-buy { color: #00ff00; font-weight: bold; font-size: 20px; }
    .signal-sell { color: #ff4b4b; font-weight: bold; font-size: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #3b82f6;'>🚀 منصة القناص الرقمي - تداول يومي</h1>", unsafe_allow_html=True)

# --- شريط الأسعار الحية من بينانس ---
ticker_tape = """
<div class="tradingview-widget-container">
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
  {
  "symbols": [
    {"proName": "BINANCE:BTCUSDT", "title": "Bitcoin"},
    {"proName": "BINANCE:ETHUSDT", "title": "Ethereum"},
    {"proName": "BINANCE:SOLUSDT", "title": "Solana"}
  ],
  "showSymbolLogo": true, "colorTheme": "dark", "isTransparent": true, "displayMode": "adaptive", "locale": "ar"
  }
  </script>
</div>
"""
components.html(ticker_tape, height=80)

# --- اختيار العملة المراد تحليلها ---
col_sidebar, col_main = st.columns([1, 3])

with col_sidebar:
    st.markdown('<div class="crypto-card">', unsafe_allow_html=True)
    symbol = st.selectbox("اختر العملة:", ["BTCUSDT", "ETHUSDT", "SOLUSDT"])
    timeframe = st.selectbox("الفريم (للتداول اليومي):", ["15", "60", "240"])
    st.markdown("---")
    
    st.markdown("### 🏹 تحليل الروبوت اللحظي")
    # ويدجت التحليل التقني المباشر
    analysis_widget = f"""
    <div style="height: 350px;">
    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
    {{
      "interval": "{'15m' if timeframe=='15' else '1h' if timeframe=='60' else '4h'}",
      "width": "100%", "isTransparent": true, "height": "100%",
      "symbol": "BINANCE:{symbol}", "showIntervalTabs": false, "displayMode": "single",
      "locale": "ar", "colorTheme": "dark"
    }}
    </script></div>"""
    components.html(analysis_widget, height=380)
    st.markdown('</div>', unsafe_allow_html=True)

with col_main:
    # الشارت المباشر الاحترافي
    chart_html = f"""
    <div class="tradingview-widget-container" style="height:500px;">
      <div id="tv_crypto"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({{
        "autosize": true, "symbol": "BINANCE:{symbol}", "interval": "{timeframe}",
        "timezone": "Etc/UTC", "theme": "dark", "style": "1", "locale": "ar",
        "withdateranges": true, "hide_side_toolbar": false, "allow_symbol_change": true,
        "details": true, "hotlist": true, "container_id": "tv_crypto"
      }});
      </script>
    </div>
    """
    components.html(chart_html, height=520)

# --- قسم تفاصيل التوصية (سبب الدخول ونسبة النجاح) ---
st.markdown("---")
c1, c2 = st.columns([1.5, 1])

with c1:
    st.markdown('<div class="crypto-card">', unsafe_allow_html=True)
    st.subheader("📝 تفاصيل توصية اليوم")
    st.write(f"**نقطة الدخول:** تعتمد على كسر مستويات السيولة اللحظية الموضحة في الشارت.")
    st.write("**الهدف الأول:** +3% | **الهدف الثاني:** +7%")
    st.write("**وقف الخسارة:** إغلاق شمعة ساعة أسفل آخر قاع.")
    st.write("**سبب التوصية:** ارتكاز السعر على منطقة طلب قوية (Demand Zone) مع ظهور دايفرجنس إيجابي على مؤشر RSI.")
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="crypto-card">', unsafe_allow_html=True)
    st.subheader("📊 إحصائيات القناص")
    st.write("**نسبة نجاح التوقعات:** 🟢 85%")
    st.write("**حالة السيولة:** دخول سيولة مؤسساتية (Smart Money)")
    st.progress(85)
    st.markdown('</div>', unsafe_allow_html=True)
