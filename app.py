import streamlit as st
import streamlit.components.v1 as components

# إعدادات الواجهة
st.set_page_config(page_title="Gold AI Robot", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #040609; color: white; }
    .stApp { background-color: #040609; }
    .bot-card {
        background: linear-gradient(145deg, #0f1218, #1a1e26);
        border: 2px solid #FFD700;
        padding: 25px;
        border-radius: 25px;
        text-align: center;
        box-shadow: 0px 0px 20px rgba(255, 215, 0, 0.3);
    }
    .status-box {
        background-color: #000;
        border-radius: 10px;
        padding: 15px;
        margin-top: 15px;
        border: 1px solid #333;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #FFD700;'>🤖 روبوت قناص الذهب الذكي </h1>", unsafe_allow_html=True)

# --- لوحة التحكم الجانبية ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=100)
    st.title("إعدادات الروبوت")
    frame = st.selectbox("اختر فريم المسح الذكي:", ["5", "15", "60", "240"], index=1)
    st.write("---")
    st.info("الروبوت يقوم بتحديث البيانات تلقائياً من البورصة كل ثانية.")

# --- القسم الرئيسي: الروبوت ---
col_bot, col_chart = st.columns([1, 2])

with col_bot:
    st.markdown('<div class="bot-card">', unsafe_allow_html=True)
    st.markdown("### ⚡ معالج البيانات الذكي")
    
    # ويدجت التحليل التقني اللحظي (هو قلب الروبوت)
    analysis_html = f"""
    <div style="height: 380px;">
    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
    {{
      "interval": "{'5m' if frame=='5' else '15m' if frame=='15' else '1h' if frame=='60' else '4h'}",
      "width": "100%", "isTransparent": true, "height": "100%",
      "symbol": "FX:XAUUSD", "showIntervalTabs": false, "displayMode": "single",
      "locale": "ar", "colorTheme": "dark"
    }}
    </script></div>"""
    components.html(analysis_html, height=400)
    
    if st.button("🚀 تحديث إشارة القناص"):
        st.toast("جاري سحب السيولة الحالية...")
        st.balloons()
    
    st.markdown('<div class="status-box">', unsafe_allow_html=True)
    st.write("🎯 **التوصية اللحظية:**")
    st.write("راقب إشارة (Strong Buy/Sell) في المعالج أعلاه للدخول.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_chart:
    st.subheader("📡 البث المباشر للأسعار والسيولة")
    # شارت احترافي يتحدث لحظياً
    chart_html = f"""
    <div class="tradingview-widget-container" style="height:530px;">
      <div id="tv_robot"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({{
        "autosize": true, "symbol": "FX:XAUUSD", "interval": "{frame}",
        "timezone": "Etc/UTC", "theme": "dark", "style": "1", "locale": "ar",
        "withdateranges": true, "hide_side_toolbar": false, "allow_symbol_change": true,
        "details": true, "hotlist": true, "container_id": "tv_robot"
      }});
      </script>
    </div>
    """
    components.html(chart_html, height=550)

# --- حاسبة إدارة المخاطر (لإكمال عمل الروبوت) ---
st.markdown("---")
st.subheader("🧮 حاسبة إدارة مخاطر القناص")
c1, c2, c3 = st.columns(3)
with c1:
    balance = st.number_input("حجم المحفظة ($):", value=1000)
with c2:
    risk = st.slider("نسبة المخاطرة (%):", 1, 5, 1)
with c3:
    stop_loss = st.number_input("عدد نقاط الستوب (Pips):", value=30)

risk_amount = balance * (risk/100)
lot_size = risk_amount / (stop_loss * 10) # معادلة تقريبية للذهب
st.warning(f"🛡️ لتقليل المخاطرة، ادخل بلوت حجمه: **{lot_size:.2f}**")
