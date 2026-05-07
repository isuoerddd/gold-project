import streamlit as st
import yfinance as yf
import pandas as pd
import streamlit.components.v1 as components

# إعداد واجهة المنصة
st.set_page_config(page_title="SNR Alpha Sniper", layout="wide")
st.title("🏹 قناص الـ SNR الذكي - الذهب")

# جلب بيانات الذهب اللحظية
@st.cache_data(ttl=60)
def get_gold_data():
    gold = yf.Ticker("GC=F")
    df = gold.history(period="2d", interval="15m")
    return df

try:
    data = get_gold_data()
    current_price = data['Close'].iloc[-1]
    
    # حساب أعلى قمة وأدنى قاع لآخر 50 شمعة (مناطق السيولة)
    resistance = data['High'].tail(50).max()
    support = data['Low'].tail(50).min()

    # لوحة المعلومات السريعة
    col_price, col_signal = st.columns(2)
    with col_price:
        st.metric("سعر الذهب الآن", f"${current_price:,.2f}")
    
    with col_signal:
        # منطق التوصية المبني على مفاهيم SNR
        if current_price >= resistance * 0.999:
            st.error("⚠️ منطقة مقاومة: انتبه لارتداد بيعي أو اختراق (SBR)")
        elif current_price <= support * 1.001:
            st.success("✅ منطقة دعم: انتبه لارتداد شرائي أو كسر (RBS)")
        else:
            st.info("🔄 السعر يتحرك بين المناطق - انتظر السيولة")

    # عرض شارت TradingView للمتابعة البصرية
    tradingview_widget = """
    <div class="tradingview-widget-container" style="height:500px;">
      <div id="tradingview_gold"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({
        "autosize": true, "symbol": "OANDA:XAUUSD", "interval": "15",
        "timezone": "Etc/UTC", "theme": "dark", "style": "1",
        "locale": "en", "toolbar_bg": "#f1f3f6", "enable_publishing": false,
        "container_id": "tradingview_gold"
      });
      </script>
    </div>
    """
    components.html(tradingview_widget, height=520)

    # قسم شروط التوصية (SNR Checklist)
    st.subheader("📋 شروط التوصية الحالية")
    if current_price > resistance:
        st.write("🔥 **الحالة:** تم اختراق المقاومة! انتظر العودة لـ **$" + str(round(resistance,2)) + "** للشراء (RBS).")
    elif current_price < support:
        st.write("📉 **الحالة:** تم كسر الدعم! انتظر العودة لـ **$" + str(round(support,2)) + "** للبيع (SBR).")
    else:
        st.write(f"⚖️ **الوضع:** السعر محصور بين الدعم ({support:.2f}) والمقاومة ({resistance:.2f}). لا تدخل حتى يكسر أحدهما.")

except Exception as e:
    st.warning("جاري الاتصال بمزود البيانات... تأكد من تحديث الصفحة.")

