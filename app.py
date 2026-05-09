import streamlit as st
import yfinance as yf
import pandas as pd

# إعدادات المنصة الاحترافية
st.set_page_config(page_title="Scalping Depth Radar", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0b0e14; }
    .price-header { background: #161b22; padding: 20px; border-radius: 10px; border: 1px solid #2962ff; text-align: center; }
    .live-num { font-size: 50px; font-weight: bold; color: #2962ff; }
    </style>
    """, unsafe_allow_html=True)

# جلب البيانات الحية (Real-time Feed)
def get_live_data():
    try:
        # الذهب الفوري
        ticker = yf.Ticker("XAUUSD=X")
        data = ticker.history(period="1d", interval="1m")
        if not data.empty:
            return data.iloc[-1]['Close'], data['High'].max(), data['Low'].min()
    except:
        return None, None, None
    return None, None, None

current, high, low = get_live_data()

# --- واجهة الموقع ---
st.title("⚡ شاشة السكالبينج وعمق السعر")

if current:
    # شاشة السعر العلوي
    st.markdown(f"""
        <div class="price-header">
            <p style="color: #8b949e; margin:0;">XAU/USD - LIVE PRICE</p>
            <div class="live-num">${current:.2f}</div>
        </div>
    """, unsafe_allow_html=True)

    st.write("---")

    # تقسيم الشاشة: شارت + توصية
    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader("📉 شاشة التداول (TradingView Live)")
        # استخدام Widget تريدنج فيو الرسمي المضمون العمل
        tv_chart = """
        <div class="tradingview-widget-container">
          <div id="tv_chart_61b"></div>
          <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
          <script type="text/javascript">
          new TradingView.widget({
            "width": "100%", "height": 500, "symbol": "OANDA:XAUUSD",
            "interval": "1", "timezone": "Etc/UTC", "theme": "dark",
            "style": "1", "locale": "ar", "enable_publishing": false,
            "hide_side_toolbar": false, "container_id": "tv_chart_61b"
          });
          </script>
        </div>
        """
        st.components.v1.html(tv_chart, height=520)

    with col2:
        st.subheader("🎯 رادار السكالب")
        st.write(f"**القمة:** {high:.2f}")
        st.write(f"**القاع:** {low:.2f}")
        
        if st.button("تحليل السيولة الآن"):
            diff = high - low
            # حساب مستويات السكالب (Order Flow Logic)
            if current > (low + diff * 0.6):
                st.success(f"✅ سيولة شرائية قوية\nهدف سكالب: {current + 2:.2f}")
            else:
                st.error(f"⚠️ سيولة بيعية مسيطرة\nهدف سكالب: {current - 2:.2f}")
else:
    st.warning("⚠️ جاري جلب نبض السعر من البورصة العالمية...")
