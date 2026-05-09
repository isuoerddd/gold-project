import streamlit as st

# إعداد واجهة فخمة تليق بمبرمج
st.set_page_config(page_title="Gann Price Geometry", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0d1117; color: white; }
    .stNumberInput { border: 1px solid #30363d !important; }
    .stButton>button { width: 100%; background-color: #238636; color: white; border: none; padding: 10px; font-weight: bold; }
    .stButton>button:hover { background-color: #2ea043; border: none; }
    .card {
        padding: 25px;
        border-radius: 15px;
        background: #161b22;
        border: 1px solid #30363d;
        text-align: right;
        direction: rtl;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    .buy-signal { color: #39d353; font-size: 28px; font-weight: bold; }
    .target-text { color: #58a6ff; font-weight: bold; }
    .stop-text { color: #f85149; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #58a6ff;'>📐 مهندس زوايا جان (Gann Pro)</h1>", unsafe_allow_html=True)
st.write("---")

# خانات الإدخال اليدوي
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📝 إدخال بيانات السوق")
    
    col1, col2 = st.columns(2)
    with col1:
        high = st.number_input("أعلى سعر لليوم (High)", value=0.0, format="%.5f")
    with col2:
        low = st.number_input("أدنى سعر لليوم (Low)", value=0.0, format="%.5f")
    
    current = st.number_input("السعر الحالي (Current Price)", value=0.0, format="%.5f")
    st.markdown("</div>", unsafe_allow_html=True)

st.write("")

if st.button("تحليل الزوايا واستخراج الأهداف 🚀"):
    if high > 0 and low > 0 and current > 0:
        # معادلة حساب النطاق (Range)
        range_val = high - low
        
        # حساب الأهداف بناءً على تقسيمات زوايا جان (1/8 و 1/4)
        # زاوية 22.5 تمثل 0.125 من الدائرة، وزاوية 45 تمثل 0.25
        tp1 = current + (range_val * 0.125)
        tp2 = current + (range_val * 0.250)
        sl = current - (range_val * 0.100) # وقف خسارة فني
        
        st.markdown(f"""
        <div class="card">
            <h3 style="text-align: center;">🎯 التوصية المستخرجة</h3>
            <hr>
            <p>سعر الدخول المقترح: <span class="buy-signal">{current:.5f}</span></p>
            <p>الهدف الأول (زاوية 22.5): <span class="target-text">{tp1:.5f}</span></p>
            <p>الهدف الثاني (زاوية 45.0): <span class="target-text">{tp2:.5f}</span></p>
            <p>وقف الخسارة (SL): <span class="stop-text">{sl:.5f}</span></p>
            <br>
            <small>تم الحساب بناءً على هندسة السعر والزمن لـ ويليام جان</small>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("يرجى إدخال الأسعار أولاً لتتمكن الأداة من الحساب.")

st.markdown("<br><p style='text-align: center; color: #8b949e;'>خاص ببرمجة المهندس - 2026</p>", unsafe_allow_html=True)
