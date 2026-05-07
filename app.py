import streamlit as st
import numpy as np
import cv2
from PIL import Image

st.set_page_config(page_title="SNR ANALYZER", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #05070a; color: white; }
    .header { text-align: center; color: #FFD700; padding: 20px; font-size: 30px; font-weight: bold; }
    .result-card { background-color: #11141a; border: 1px solid #FFD700; padding: 20px; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header">🔱 محلل الشارت الهندسي (بدون API) 🔱</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("ارفع صورة الشارت...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # تحويل الصورة إلى تنسيق يفهمه OpenCV
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    st.image(image, caption='تم رفع الشارت بنجاح', use_column_width=True)
    
    if st.button("🔍 تحليل المناطق الهندسية"):
        with st.spinner('جاري مسح مستويات السيولة...'):
            # 1. تحويل الصورة للأبيض والأسود لاكتشاف المناطق
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            
            # 2. اكتشاف الحواف (Edges) لتحديد القمم والقيعان
            edges = cv2.Canny(gray, 50, 150)
            
            # 3. حساب الكثافة السعرية (لاكتشاف مناطق العرض والطلب)
            # ملاحظة: هذا تحليل رياضي بحت بناءً على توزيع بكسلات السعر
            row_sums = np.sum(edges, axis=1)
            high_liquidity_zones = np.where(row_sums > (np.max(row_sums) * 0.7))[0]
            
            st.markdown("### 📊 نتائج المسح الهندي:")
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            
            if len(high_liquidity_zones) > 0:
                st.success("✅ تم رصد مناطق تمركز سيولة (SNR) في الصورة.")
                st.write(f"عدد المناطق القوية المكتشفة: {len(high_liquidity_zones) // 10}")
                st.info("نصيحة هندسية: السعر يميل للانعكاس عند المناطق التي تكثر فيها الذيول في الصورة.")
            else:
                st.warning("لم يتم اكتشاف مناطق واضحة، حاول رفع صورة بألوان متباينة.")
                
            st.markdown('</div>', unsafe_allow_html=True)

st.caption("هذا النظام يعتمد على معالجة البكسلات (Computer Vision) ولا يتطلب اتصالاً بسيرفرات خارجية.")
