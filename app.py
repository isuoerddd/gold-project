import streamlit as st
import yfinance as yf
import pandas as pd
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="SNR GOLD SNIPER", layout="centered")
st_autorefresh(interval=60 * 1000, key="snr_refresh")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1c2130; padding: 15px; border-radius: 15px; border: 1px solid #FFD700; }
    .zone-card { 
        padding: 20px; border-radius: 15px; text-align: center; margin: 10px 0; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: #FFD700;'>🎯 رادار العرض والطلب (SNR)</h2>", unsafe_allow_html=True)

def get_snr_logic():
    try:
        # استخدام السعر الموحد
        data = yf.download("XAUUSD=X", period="2d", interval="15m", progress=False)
        if data.empty: return None
        
        current_price = float(data['Close'].iloc[-1])
        supply_zone = float(data['High'].max()) # أعلى منطقة عرض لليوم
        demand_zone = float(data['Low'].min())  # أدنى منطقة طلب لليوم
        
        # حساب نسبة القرب من المناطق
        to_supply = ((supply_zone - current_price) / current_price) * 100
        to_demand = ((current_price - demand_zone) / current_price) * 100
        
        return current_price, supply_zone, demand_zone, to_supply, to_demand
    except: return None

result = get_snr_logic()

if result:
    price, supply, demand, dist_s, dist_d = result
    
    col1, col2 = st.columns(2)
    col1.metric("السعر الحالي", f"${price:,.2f}")
    col2.metric("حالة السيولة", "مستقرة" if dist_s > 0.5 and dist_d > 0.5 else "نشطة")

    # نظام التوصية الماليزي (الدخول من المناطق)
    if dist_d < 0.15: # السعر قريب جداً من منطقة الطلب
        st.markdown(f"""<div class='zone-card' style='background-color: #004d00; color: #00ff00;'>
            🔥 منطقة طلب ماليزية (Demand Zone)<br>اقتناص شراء مع وقف خسارة تحت {demand-2:.2f}
            </div>""", unsafe_allow_html=True)
    elif dist_s < 0.15: # السعر قريب جداً من منطقة العرض
        st.markdown(f"""<div class='zone-card' style='background-color: #4d0000; color: #ff3333;'>
            🚨 منطقة عرض ماليزية (Supply Zone)<br>اقتناص بيع مع وقف خسارة فوق {supply+2:.2f}
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class='zone-card' style='background-color: #1c2130; color: #FFD700;'>
            🔎 السعر بين المناطق (No Zone)<br><span style='font-size: 14px;'>انتظر وصول السعر لمناطق الانعكاس</span>
            </div>""", unsafe_allow_html=True)

    # تفاصيل المناطق للزوار
    st.write("---")
    st.info(f"📈 منطقة العرض القادمة: **${supply:.2f}**")
    st.success(f"📉 منطقة الطلب القادمة: **${demand:.2f}**")

else:
    st.warning("جاري تحليل مناطق السيولة...")
