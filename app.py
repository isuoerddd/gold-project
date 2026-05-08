import streamlit as st
import yfinance as yf
import pandas_ta as ta
import plotly.graph_objects as go

# إعداد الصفحة
st.set_page_config(page_title="EURUSD Scalper", layout="wide")

st.title("🇪🇺🇺🇸 رادار سكالب اليورو دولار")

# جلب البيانات
symbol = "EURUSD=X"
data = yf.download(symbol, period="5d", interval="15m")

if not data.empty:
    # حساب المؤشرات
    data.ta.rsi(length=14, append=True)
    data.ta.ema(length=200, append=True)
    
    current_price = data['Close'].iloc[-1]
    rsi = data['RSI_14'].iloc[-1]
    ema200 = data['EMA_200'].iloc[-1]
    
    # منطق التوصية
    trend = "صاعد 📈" if current_price > ema200 else "هابط 📉"
    signal = "انتظار ⏳"
    color = "white"
    
    if current_price > ema200 and rsi < 40:
        signal = "شراء (BUY) 🛒"
        color = "#00ff00"
    elif current_price < ema200 and rsi > 60:
        signal = "بيع (SELL) 🚀"
        color = "#ff4b4b"
    
    # عرض النتائج
    c1, c2 = st.columns(2)
    c1.metric("السعر الحالي", f"{current_price:.5f}")
    c2.markdown(f"### الإشارة: <span style='color:{color}'>{signal}</span>", unsafe_allow_html=True)
    
    st.write(f"**الاتجاه العام:** {trend}")
    
    # الرسم البياني
    fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], 
                    high=data['High'], low=data['Low'], close=data['Close'])])
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_view=True)
  
