import streamlit as st
import yfinance as yf
import pandas as pd
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

# إعدادات الصفحة
st.set_page_config(page_title="Gold Auto-Sniper Pro", layout="wide")

# تحديث الصفحة تلقائياً كل 60 ثانية (لضمان وصول التوصية فوراً)
st_autorefresh(interval=60 * 1000, key="gold_refresh")

st.title("🚀 قناص الذهب (تحديث تلقائي + SNR)")

@st.cache_data(ttl=50) # كاش لمدة أقل من دقيقة
def get_live_data():
    df = yf.Ticker("GC=F").history(period="5d", interval="15m")
    # حساب RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    # حساب EMA 200
    df['EMA_200'] = df['Close'].ewm(span=200, adjust=False).mean()
    return df

try:
    df = get_live_data()
    current_p = df['Close'].iloc[-1]
    rsi_v = df['RSI'].iloc[-1]
    ema_v = df['EMA_200'].iloc[-1]
    
    # تحديد أقوى مناطق SNR لآخر 100 شمعة
    resistance = df['High'].tail(100).max()
    support = df['Low'].tail(100).min()

    # لوحة البيانات العلوية
    m1, m2, m3 = st.columns(3)
    m1.metric("سعر الذهب اللحظي", f"${current_p:,.2f}")
    m2.metric("قوة السوق (RSI)", f"{rsi_v:.2f}")
    m3.metric("الاتجاه العام (EMA)", "صاعد 📈" if current_p > ema_v else "هابط 📉")

    st.write("---")
    
    # محرك التوصيات الذكي
    st.subheader("🎯 حالة التوصية الآن")
    
    if current_p <= support * 1.001 and rsi_v < 35:
        st.success(f"🔥 **فرصة شراء ذهبية:** السعر عند الدعم ({support:.2f}) مع تشبع بيعي. الهدف: {resistance:.2f}")
    elif current_p >= resistance * 0.999 and rsi_v > 65:
        st.error(f"⚠️ **فرصة بيع قوية:** السعر عند المقاومة ({resistance:.2f}) مع تشبع شرائي. الهدف: {support:.2f}")
    elif current_p > resistance:
        st.info(f"🚀 **اختراق مقلوب:** السعر اخترق المقاومة. انتظر ملامسة {resistance:.2f} للدخول شراء (RBS).")
    elif current_p < support:
        st.warning(f"📉 **كسر هابط:** السعر كسر الدعم. انتظر ملامسة {support:.2f} للدخول بيع (SBR).")
    else:
        st.write("⚖️ **الانتظار سيد الموقف:** السعر في منطقة سيولة محايدة. لا توجد توصية دخول حالياً.")

    # عرض شارت TradingView
    components.html(f"""
        <div class="tradingview-widget-container" style="height:500px;">
            <div id="tv_chart"></div>
            <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
            <script type="text/javascript">
            new TradingView.widget({{
                "autosize": true, "symbol": "OANDA:XAUUSD", "interval": "15",
                "timezone": "Etc/UTC", "theme": "dark", "style": "1",
                "locale": "en", "toolbar_bg": "#f1f3f6", "container_id": "tv_chart"
            }});
            </script>
        </div>
    """, height=520)

    st.caption("ملاحظة: الموقع يحدث نفسه تلقائياً كل دقيقة لجلب آخر الأسعار والتوصيات.")

except Exception as e:
    st.info("انتظر لحظة... يتم الآن الاتصال بخادم البورصة وتحديث البيانات.")
