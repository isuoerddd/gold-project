import streamlit as st

st.set_page_config(page_title="Gann Precision Sniper", layout="centered")

# تنسيق واجهة المستخدم
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: white; }
    .card { padding: 20px; border-radius: 15px; background: #161b22; border: 1px solid #30363d; text-align: right; direction: rtl; }
    .buy-zone { border: 2px solid #39d353; padding: 10px; border-radius: 10px; background: rgba(57, 211, 83, 0.1); }
    .sell-zone { border: 2px solid #f85149; padding: 10px; border-radius: 10px; background: rgba(248, 81, 73, 0.1); }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>🎯 قناص زوايا جان الاحترافي</h2>", unsafe_allow_html=True)

# المدخلات اليدوية
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        high = st.number_input("أعلى سعر لليوم (High)", value=0.0, format="%.2f")
    with col2:
        low = st.number_input("أدنى سعر لليوم (Low)", value=0.0, format="%.2f")
    current = st.number_input("السعر الحالي (Current)", value=0.0, format="%.2f")
    st.markdown("</div>", unsafe_allow_html=True)

if st.button("تحليل الزوايا الآن 🚀"):
    if high > low and current > 0:
        diff = high - low
        
        # مستويات جان الرئيسية (Angles)
        level_22 = low + (diff * 0.225) # زاوية 22.5 صاعدة
        level_77 = high - (diff * 0.225) # زاوية 22.5 هابطة
        mid_point = low + (diff * 0.5)   # مستوى الـ 50%
        
        st.write("---")

        # --- المنطق الجديد للدقة العالية ---
        # إذا كان السعر فوق مستوى الـ 22.5% الصاعد -> شراء
        if current >= level_22 and current < high:
            tp1 = current + (diff * 0.125)
            sl = current - (diff * 0.05)
            st.markdown(f"""
            <div class="buy-zone">
                <h3 style="color: #39d353; text-align:center;">🟢 توصية شراء (BUY)</h3>
                <p style="text-align:center;">السعر بدأ باختراق زوايا الصعود</p>
                <hr>
                <p>الهدف القادم: <b>{tp1:.2f}</b></p>
                <p>وقف الخسارة: <b>{sl:.2f}</b></p>
            </div>
            """, unsafe_allow_html=True)

        # إذا كان السعر كسر مستوى الـ 22.5% الهابط من الأعلى -> بيع
        elif current <= level_77 and current > low:
            tp1 = current - (diff * 0.125)
            sl = current + (diff * 0.05)
            st.markdown(f"""
            <div class="sell-zone">
                <h3 style="color: #f85149; text-align:center;">🔴 توصية بيع (SELL)</h3>
                <p style="text-align:center;">السعر كسر زوايا الدعم العلوي</p>
                <hr>
                <p>الهدف القادم: <b>{tp1:.2f}</b></p>
                <p>وقف الخسارة: <b>{sl:.2f}</b></p>
            </div>
            """, unsafe_allow_html=True)
            
        else:
            st.info("السعر في منطقة تذبذب (Wait) - بانتظار اختراق الزوايا")
    else:
        st.error("تأكد من إدخال الـ High والـ Low بشكل صحيح.")
