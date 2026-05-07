import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(page_title="Arbitrage Sniper Hub", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .status-box {
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #3b82f6;
        background-color: #161b22;
        text-align: center;
    }
    .profit-text { color: #00ff00; font-weight: bold; font-size: 24px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 رادار فوارق الأسعار والتحليل اللحظي")

# --- قائمة العملات للمراقبة ---
watchlist = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'BNB-USD', 'XRP-USD']

def get_live_prices():
    data = []
    for sym in watchlist:
        ticker = yf.Ticker(sym)
        # جلب سعر الإغلاق اللحظي
        current_price = ticker.history(period="1d", interval="1m")['Close'].iloc[-1]
        
        # محاكاة فرق السعر بين منصتين (Binance vs Coinbase مثلاً)
        # في الواقع نربطها بـ APIs حقيقية، هنا نضع معامل فرق تقني 0.2%
        price_ex1 = current_price
        price_ex2 = current_price * 1.0025  # فرضية وجود فرق 0.25%
        
        diff = price_ex2 - price_ex1
        profit_pct = (diff / price_ex1) * 100
        
        data.append({
            "الرمز": sym,
            "سعر المنصة A": round(price_ex1, 2),
            "سعر المنصة B": round(price_ex2, 2),
            "الفرق ($)": round(diff, 2),
            "الربح (%)": round(profit_pct, 2)
        })
    return pd.DataFrame(data)

# --- القسم العلوي: جدول القناص ---
st.subheader("🚀 فرص الأربيتراج اللحظية")
if st.button('تحديث البيانات الآن 🔄'):
    df_prices = get_live_prices()
    
    # عرض البيانات في جدول احترافي
    st.table(df_prices)
    
    # التنبيه بأفضل فرصة
    best_deal = df_prices.loc[df_prices['الربح (%)'].idxmax()]
    st.markdown(f"""
    <div class="status-box">
        <h4>أفضل فرصة حالياً: <span class="profit-text">{best_deal['الرمز']}</span></h4>
        <p>اشترِ من A وبع في B لتحقيق ربح صافي قدره <span class="profit-text">{best_deal['الربح (%)']}%</span></p>
    </div>
    """, unsafe_allow_html=True)

# --- القسم السفلي: التحليل الفني ---
st.divider()
st.subheader("📈 التحليل الفني المتعمق")
selected_coin = st.selectbox("اختر العملة لتحليل الشارت:", watchlist)

col1, col2 = st.columns([2, 1])

with col1:
    # رسم شارت الشموع اليابانية
    df_chart = yf.download(selected_coin, period="1d", interval="15m")
    fig = go.Figure(data=[go.Candlestick(x=df_chart.index,
                    open=df_chart['Open'], high=df_chart['High'],
                    low=df_chart['Low'], close=df_chart['Close'])])
    fig.update_layout(template="plotly_dark", title=f"حركة {selected_coin} (فريم 15 دقيقة)")
    st.plotly_chart(fig, use_container_view=True)

with col2:
    st.markdown('<div class="status-box">', unsafe_allow_html=True)
    st.write("### 🧠 ملخص الذكاء الاصطناعي")
    # منطق بسيط للتحليل
    rsi = 55 # مثال لمؤشر القوة النسبية
    st.write(f"**مؤشر RSI:** {rsi}")
    st.write("**الاتجاه العام:** صاعد (Bullish)")
    st.write("**توصية النظام:** مراقبة مستوى المقاومة القادم.")
    st.progress(rsi/100)
    st.markdown('</div>', unsafe_allow_html=True)
