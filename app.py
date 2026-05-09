import streamlit as st

st.set_page_config(page_title="Gann Multi-Direction Sniper", layout="centered")

# التنسيق البرمجي
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: white; }
    .card { padding: 20px; border-radius: 15px; background: #161b22; border: 1px solid #30363d; text-align: right; direction: rtl; }
    .buy-signal { color: #39d353; font-size: 24px; font-weight: bold; }
    .sell-signal { color: #f85149; font-size: 24px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>📐 رادار جان الثنائي (شراء / بيع)</h2>", unsafe_allow_html=True)

# المدخلات
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        high = st.number_input("أعلى سعر (High)", value=0.0, format="%.2f")
    with col2:
        low = st.number_input("أدنى سعر (Low)", value=0.0, format="%.2f")
    current = st.number_input("السعر الحالي", value=0.0, format="%.2f")
    st.markdown("</div>", unsafe_allow_html=True)

if st.button("تحليل الاتجاه واستخراج الأهداف 🚀"):
    if high > low and current > 0:
        range_val = high - low
        mid_point = low + (range_val / 2) # نقطة التوازن 50%
        
        st.write("---")
        
        # منطق الشراء والبيع بناءً على نقطة التوازن (Gann 50% Rule)
        if current > mid_point:
            # السعر في منطقة القوة -> شراء
            tp1 = current + (range_val * 0.125)
            tp2 = current + (range_val * 0.250)
            sl = low # الوقف عند القاع
            
            st.markdown(f"""
            <div class="card">
                <h3 style="color: #39d353;">🟢 إشارة شراء (BUY)</h3>
                <p>السعر فوق منطقة التعادل، المستهدف زوايا جان الصاعدة:</p>
                <p>الهدف الأول: <b>{tp1:.2f}</b></p>
                <p>الهدف الثاني: <b>{tp2:.2f}</b></p>
                <p>وقف الخسارة: <b style="color:#f85149">{sl:.2f}</b></p>
            </div>
            """, unsafe_allow_html=True)
            
        else:
            # السعر في منطقة الضعف -> بيع
            tp1 = current - (range_val * 0.125)
            tp2 = current - (range_val * 0.250)
            sl = high # الوقف عند القمة
            
            st.markdown(f"""
            <div class="card">
                <h3 style="color: #f85149;">🔴 إشارة بيع (SELL)</h3>
                <p>السعر تحت منطقة التعادل، المستهدف زوايا جان الهابطة:</p>
                <p>الهدف الأول: <b>{tp1:.2f}</b></p>
                <p>الهدف الثاني: <b>{tp2:.2f}</b></p>
                <p>وقف الخسارة: <b style="color:#39d353">{sl:.2f}</b></p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.error("يرجى إدخال أرقام صحيحة.")
