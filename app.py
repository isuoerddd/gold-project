import streamlit as st
import yfinance as yf
import pandas as pd
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

# 1. إعداد الصفحة
st.set_page_config(page_title="Gold Sniper Dashboard", layout="wide")
st_autorefresh(interval=60 * 1000, key="auto_refresh")

# 2. تصميم الرأس
st.markdown("<h1 style='text-align: center; color: #FFD700;'>🎯 رادار قناص الذهب</h1>", unsafe_allow_html=True)

# 3. جلب البيانات للتحليل البرمجي (خلف الكواليس)
@st.cache_data(ttl=60)
def analyze_market():
    df = yf.Ticker("GC=F").history(period="2d", interval="15m")
    # حساب RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

try:
    df = analyze_market()
    current_price = df['Close'].iloc[-1]
    rsi_val = df['RSI'].iloc[-1]
    high_50 = df['High'].tail(50).max()
    low_50 = df['Low'].tail(50).min()

    # 4. عرض الشارت (للمراقبة فقط)
    tradingview_widget = """
    <div style="height:400px;">
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({
        "autosize": true, "symbol": "OANDA:XAUUSD", "interval": "15",
        "timezone": "Etc/UTC", "theme": "dark", "style": "1",
        "locale": "ar", "container_id": "tv_chart", "hide_side_toolbar": true
      });
      </script>
      <div id="tv_chart"></div>
    </div>
    """
    components.html(tradingview_widget, height=410)

    # 5. قسم التوصيات والملاحظات (هذا المهم عندك)
    st.markdown("---")
    st.subheader("📋 تقرير القناص اللحظي")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("السعر الحالي", f"${current_price:,.2f}")
    col2.metric("قوة RSI", f"{rsi_val:.2f}")
    col3.metric("مستوى المقاومة", f"${high_50:.2f}")

    # صندوق الشروط والتوصية
    st.markdown("### 🔔 حالة الشروط الآن:")
    
    if current_price >= high_50 * 0.998:
        st.error(f"🔴 **توصية بيع محتملة:** السعر يقترب من المقاومة ({high_50:.2f}). إذا ظهرت شمعة انعكاسية في تطبيقك، ادخل بيع.")
    elif current_price <= low_50 * 1.002:
        st.success(f"🟢 **توصية شراء محتملة:** السعر عند منطقة الدعم ({low_50:.2f}). ابحث عن تأكيد دخول في تطبيقك.")
    elif rsi_val > 70:
        st.warning("⚠️ **ملاحظة:** الـ RSI مرتفع جداً (تشبع شرائي). لا تفتح صفقات شراء جديدة الآن.")
    elif rsi_val < 30:
        st.warning("⚠️ **ملاحظة:** الـ RSI منخفض جداً (تشبع بيعي). لا تفتح صفقات بيع جديدة الآن.")
    else:
        st.info("⚖️ **الوضع الحالي:** السعر يتحرك في منطقة آمنة بين الدعم والمقاومة. انتظر ملامسة الأطراف.")

    # ملاحظة إضافية لمدرسة SNR
    st.info(f"📍 **أهدافك القادمة:** إذا اخترق السعر {high_50:.2f} بقوة، انتظر العودة له (RBS) للشراء. إذا كسر {low_50:.2f}، انتظر العودة له (SBR) للبيع.")

except:
    st.write("جاري جلب بيانات السوق... حدث الصفحة بعد لحظات.")
