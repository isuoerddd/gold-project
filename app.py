import streamlit as st
import streamlit.components.v1 as components

# إعدادات الصفحة الاحترافية
st.set_page_config(page_title="Gold Sniper Hub", layout="wide")

# تصميم الواجهة بالـ CSS لجعلها تبدو كمنصة تداول فاخرة
st.markdown("""
    <style>
    .main { background-color: #05070a; color: white; }
    .stApp { background-color: #05070a; }
    .recommendation-card {
        background: linear-gradient(135deg, #11141a 0%, #1a1e26 100%);
        border: 1px solid #FFD700;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0px 4px 15px rgba(255, 215, 0, 0.2);
    }
    .trend-up { color: #00ff00; font-size: 24px; font-weight: bold; }
    .trend-down { color: #ff4b4b; font-size: 24px; font-weight: bold; }
    .price-text { font-size: 20px; color: #FFD700; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #FFD700;'>🔱 منصة القناص المتكاملة للذهب 🔱</h1>", unsafe_allow_html=True)

# --- القسم الأول: التحكم والإعدادات ---
with st.sidebar:
    st.header("⚙️ إعدادات التحليل")
    symbol = "OANDA:XAUUSD"
    # اختيار الفريم الزمني الذي سيغير كل شيء في الموقع
    frame = st.selectbox("اختر الفريم الزمني للتحليل:", 
                         options=["1", "5", "15", "60", "240", "D"], 
                         format_func=lambda x: f"{x} دقيقة" if x.isdigit() else "يومي",
                         index=2)
    
    st.markdown("---")
    st.write("🎯 **حالة السوق:**")
    st.success("سيولة عالية - جلسة نشطة")

# --- القسم الثاني: عرض التوصية والترند بناءً على الفريم ---
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown('<div class="recommendation-card">', unsafe_allow_html=True)
    st.write("📈 **الاتجاه الحالي (Trend)**")
    # هذا الويدجت يعطي الاتجاه بناءً على الفريم المختار
    trend_html = f"""
    <div style="height: 100px; overflow: hidden;">
    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
    {{
      "interval": "{'1m' if frame=='1' else '5m' if frame=='5' else '15m' if frame=='15' else '1h' if frame=='60' else '4h' if frame=='240' else '1D'}",
      "width": "100%", "isTransparent": true, "height": "100%",
      "symbol": "{symbol}", "showIntervalTabs": false, "displayMode": "single",
      "locale": "ar", "colorTheme": "dark"
    }}
    </script></div>"""
    components.html(trend_html, height=120)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="recommendation-card">', unsafe_allow_html=True)
    st.write("🚀 **التوصية المقترحة**")
    # هنا يمكنك وضع معادلة أو تحديث التوصية يدوياً أو برمجياً
    st.markdown("<p class='price-text'>دخول معلق (Limit)</p>", unsafe_allow_html=True)
    st.markdown("<p style='color: #00ff00;'>السعر المستهدف: مراقبة RBS</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="recommendation-card">', unsafe_allow_html=True)
    st.write("🎯 **الأهداف (Targets)**")
    st.write("الهدف الأول: 1:2 Risk Ratio")
    st.write("الهدف الثاني: سيولة القمة التالية")
    st.markdown('</div>', unsafe_allow_html=True)

# --- القسم الثالث: الشارت التفاعلي المباشر ---
st.markdown("---")
st.subheader(f"📊 شارت الذهب اللحظي - فريم {frame}")

chart_code = f"""
<div class="tradingview-widget-container" style="height:550px;">
  <div id="tv_chart_main"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
  <script type="text/javascript">
  new TradingView.widget({{
    "autosize": true, "symbol": "{symbol}", "interval": "{frame}",
    "timezone": "Etc/UTC", "theme": "dark", "style": "1", "locale": "ar",
    "enable_publishing": false, "withdateranges": true, "hide_side_toolbar": false,
    "allow_symbol_change": true, "details": true, "hotlist": true, "calendar": true,
    "container_id": "tv_chart_main"
  }});
  </script>
</div>
"""
components.html(chart_code, height=560)

# --- القسم الرابع: مصفاة السيولة والأخبار ---
st.markdown("---")
col_news, col_summary = st.columns([2, 1])

with col_news:
    st.subheader("🗓️ المفكرة الاقتصادية (تأثير الدولار)")
    news_html = """
    <div class="tradingview-widget-container">
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-events.js" async>
      {"colorTheme": "dark", "isTransparent": true, "width": "100%", "height": "400", "locale": "ar", "importanceFilter": "0,1", "currencyFilter": "USD"}
      </script>
    </div>"""
    components.html(news_html, height=420)

with col_summary:
    st.subheader("📝 ملاحظات القناص")
    note = st.text_area("سجل تحليلك لمناطق SNR هنا:", height=200)
    if st.button("حفظ الملاحظة"):
        st.success("تم حفظ الملاحظة لجلسة اليوم.")

