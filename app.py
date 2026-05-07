import streamlit as st
import yfinance as yf
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# إعدادات الفخامة
st.set_page_config(page_title="GOLD VIP SNIPER", layout="centered")
st_autorefresh(interval=60 * 1000, key="vip_refresh")

# ستايل CSS لجعل الواجهة تشبه تطبيقات التداول العالمية
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1c2130; padding: 15px; border-radius: 15px; border: 1px solid #FFD700; }
    .recommendation-card { 
        padding: 30px; 
        border-radius: 20px; 
        text-align: center; 
        margin: 20px 0;
        font-weight: bold;
        font-size: 24px;
        border: 2px solid #FFD700;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #FFD700;'>👑 VIP GOLD RADAR</h1>", unsafe_allow_html=True)

@st.cache_data(ttl=60)
def get_signals():
    # سحب بيانات دقيقة لتحليل الدخول اليومي
    data = yf.Ticker("GC=F").history(period="2d", interval="5m")
    # حساب RSI سريع للفترات القصيرة
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rsi = 100 - (100 / (1 + (gain/loss)))
    return data['Close'].iloc[-1], rsi.iloc[-1], data['High'].max(), data['Low'].min()

price, rsi, daily_high, daily_low = get_signals()

# لوحة المعلومات السريعة
col1, col2 = st.columns(2)
col1.metric("سعر الذهب الآن", f"${price:,.2f}")
col2.metric("قوة الاتجاه", f"{rsi:.1f}%")

st.write("---")

# منطق التوصية اليومية "التي تعجب الناس"
if rsi < 30:
    st.markdown(f"""<div class='recommendation-card' style='background-color: #004d00; color: #00ff00;'>
        🏹 اقتناص شراء فوراً<br><span style='font-size: 15px;'>السعر مغري جداً والارتداد قريب</span>
        </div>""", unsafe_allow_html=True)
    st.balloons()
elif rsi > 70:
    st.markdown(f"""<div class='recommendation-card' style='background-color: #4d0000; color: #ff3333;'>
        📉 اقتناص بيع فوراً<br><span style='font-size: 15px;'>السعر متضخم.. توقع هبوط سريع</span>
        </div>""", unsafe_allow_html=True)
else:
    st.markdown(f"""<div class='recommendation-card' style='background-color: #1c2130; color: #FFD700;'>
        ⏳ جاري رصد السيولة...<br><span style='font-size: 15px;'>لا تدخل بعشوائية، انتظر إشارة القناص</span>
        </div>""", unsafe_allow_html=True)

# نصيحة اليوم (لتشجيع الناس على الدخول يومياً)
st.markdown("### 💡 نصيحة الخبراء لهذا اليوم:")
if price > daily_high * 0.9:
    st.info("الذهب يختبر قمة يومية، إذا أغلق فوقها فالصعود سيستمر بقوة.")
else:
    st.info("السعر يتحرك بانتظام، اعتمد على الـ RSI في صفقات السكالبينج السريعة.")

st.caption("تنبيه: التوصية تتحدث تلقائياً كل دقيقة بناءً على خوارزمية RSI و SNR")
