import streamlit as st
import yfinance as yf
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(page_title="Gold Pro Sniper", layout="wide")
st.title("🚀 قناص الذهب المحترف (SNR + RSI)")

@st.cache_data(ttl=60)
def get_data():
    df = yf.Ticker("GC=F").history(period="5d", interval="15m")
    # حساب RSI يدوياً لتجنب أخطاء السيرفر
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    # حساب EMA 200
    df['EMA_200'] = df['Close'].ewm(span=200, adjust=False).mean()
    return df

try:
    df = get_data()
    current_p = df['Close'].iloc[-1]
    rsi_v = df['RSI'].iloc[-1]
    ema_v = df['EMA_200'].iloc[-1]
    resistance = df['High'].tail(100).max()
    support = df['Low'].tail(100).min()

    m1, m2, m3 = st.columns(3)
    m1.metric("سعر الذهب الآن", f"${current_p:,.2f}")
    m2.metric("قوة السوق (RSI)", f"{rsi_v:.2f}")
    m3.metric("الاتجاه (EMA 200)", "صاعد 📈" if current_p > ema_v else "هابط 📉")

    st.subheader("🎯 التوصية اللحظية")
    if current_p <= support * 1.001 and rsi_v < 35:
        st.success(f"🔥 فرصة شراء: السعر عند الدعم ({support:.2f}) مع تشبع بيعي.")
    elif current_p >= resistance * 0.999 and rsi_v > 65:
        st.error(f"⚠️ فرصة بيع: السعر عند المقاومة ({resistance:.2f}) مع تشبع شرائي.")
    elif current_p > resistance:
        st.info(f"🚀 اختراق: انتظر إعادة الاختبار لـ {resistance:.2f} للشراء.")
    else:
        st.warning("⚖️ انتظر: السعر في منطقة محايدة حالياً.")

    components.html(f"""
        <div class="tradingview-widget-container" style="height:500px;">
            <div id="tv_chart"></div>
            <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
            <script type="text/javascript">
            new TradingView.widget({{
                "autosize": true, "symbol": "OANDA:XAUUSD", "interval": "15",
                "theme": "dark", "style": "1", "container_id": "tv_chart"
            }});
            </script>
        </div>
    """, height=520)
except:
    st.info("جاري تحديث البيانات...")
