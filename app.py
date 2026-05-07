import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="محرر التقارير الذكي", layout="centered")

# تصميم الواجهة (فخامة وبساطة)
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .report-container {
        background-color: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.05);
        direction: rtl;
        text-align: right;
    }
    h1, h2, h3 { color: #1e3a8a; font-family: 'Arial'; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>📄 نظام توليد التقارير الجامعية</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>ادخل اسم الموضوع واترك الباقي للمهندس الذكي</p>", unsafe_allow_html=True)

# مدخلات المستخدم
with st.container():
    st.markdown('<div class="report-container">', unsafe_allow_html=True)
    topic = st.text_input("عنوان التقرير أو الموضوع:", placeholder="مثلاً: هندسة المكامن، التسويق الرقمي، القضاء العشائري...")
    subject_type = st.selectbox("نوع المادة:", ["هندسة", "قانون", "إدارة أعمال", "ثقافة عامة"])
    
    generate_btn = st.button("🚀 توليد التقرير الآن")
    st.markdown('</div>', unsafe_allow_html=True)

if generate_btn and topic:
    with st.spinner("جاري صياغة التقرير باللغة العربية الفصحى..."):
        # هنا يتم بناء هيكل التقرير
        # ملاحظة: يمكنك ربط هذا الجزء بـ API للذكاء الاصطناعي لاحقاً ليكون المحتوى متجدداً
        report_content = f"""
        # تقرير عن: {topic}
        
        ## المقدمة
        يعد موضوع {topic} من المواضيع الجوهرية في مجال {subject_type}، حيث يلعب دوراً حيوياً في فهم التطورات الحديثة...
        
        ## المحاور الرئيسية
        1. **الأهمية التاريخية والتقنية:** تطور مفهوم {topic} عبر العصور ليصل إلى ما هو عليه الآن.
        2. **التطبيقات العملية:** يتم استخدام {topic} في العديد من المجالات المهنية والأكاديمية.
        3. **التحديات والحلول:** واجه هذا المجال عدة معوقات تم تجاوزها من خلال البحث والتطوير.
        
        ## الخاتمة
        بناءً على ما سبق، نستنتج أن {topic} سيظل حجر الزاوية في الدراسات المستقبلية لمادة {subject_type}.
        
        ---
        **المراجع:**
        - ويكيبيديا العربية.
        - مصادر أكاديمية متخصصة في {subject_type}.
        """
        
        st.markdown("---")
        st.markdown(report_content)
        
        # خيارات التصدير
        col1, col2 = st.columns(2)
        with col1:
            st.download_button("📥 تحميل كملف نصي (TXT)", report_content, file_name=f"{topic}.txt")
        with col2:
            st.info("💡 يمكنك نسخ النص ولصقه مباشرة في ملف Word وتنسيقه.")

else:
    st.info("بانتظار إدخال الموضوع لبدء العمل...")
