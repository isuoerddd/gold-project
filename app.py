import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import streamlit.components.v1 as components

# إعدادات الواجهة الاحترافية
st.set_page_config(page_title="Gold Alpha Pro Sniper", layout="wide")
st.title("🚀 قناص الذهب المحترف (SNR + RSI + Trend)")

@st.cache_data(ttl=60)
def get_advanced_data():
    # جلب بيانات 5 أيام بفريم 15 دقيقة
    df = yf.Ticker("GC=F").history(period="5d", interval="15m")
    # حساب مؤشر القوة النسبية RSI
    df['RSI'] = ta.rsi(df['Close'], length=14)
    # حساب المتوسط المتحرك EMA 200 لتحديد الاتجاه العام
    df['EMA_200'] = ta.ema(df['Close'], length=200)
    return df

try:
    df = get_advanced_data()
    current_p = df['Close'].iloc[-1]
    rsi_v = df['RSI'].iloc[-1]
    ema_v = df['EMA_200'].iloc[-1]
    
    # تحديد أقوى مناطق SNR لآخر 100 شمعة
    resistance = df['High'].tail(100).max()
    support = df['Low'].tail(100).min()

    # لوحة المؤشرات العلوية
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("سعر الذهب الآن", f"${current_p:,.2f}")
    with m2:
        st.metric("قوة السوق (RSI)", f"{rsi_v:.2f}")
    with m3:
        trend = "صاعد 📈" if current_p > ema_v else "هابط 📉"
        st.metric("الاتجاه العام", trend)

    st.write("---")

    # نظام التوصية الذكي
    st.subheader("🎯 التوصية البرمجية اللحظية")
    
    if current_p <= support * 1.001 and rsi_v < 35:
        st.success(f"🔥 فرصة شراء ذهبية: السعر عند الدعم ({support:.2f}) مع تشبع بيعي (RSI).")
    elif current_p >= resistance * 0.999 and rsi_v > 65:
        st.error(f"⚠️ فرصة بيع قوية: السعر عند المقاومة ({resistance:.2f}) مع تشبع شرائي (RSI).")
    elif current_p > resistance:
        st.info(f"🚀 اختراق: السعر فوق المقاومة. انتظر إعادة الاختبار لـ {resistance:.2f} للشراء (RBS).")
    elif current_p < support:
        st.warning(f"📉 كسر: السعر تحت الدعم. انتظر إعادة الاختبار لـ {support:.2f} للبيع (SBR).")
    else:
        st.write("⚖️ **الوضع الحالي:** السعر في منطقة محايدة. انتظر اقترابه من المناطق المحددة أعلاه.")

    # عرض الشارت المباشر
    tradingview_html = f"""
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
    """
    components.html(tradingview_html, height=520)

except Exception as e:
    st.info("جاري تحديث البيانات من البورصة... انتظر لحظة.")
