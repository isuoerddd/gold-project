import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="SNR RADAR", layout="centered")

# التنسيق
st.markdown("<h1 style='text-align: center; color: #FFD700;'>🎯 رادار العرض والطلب (SNR)</h1>", unsafe_allow_html=True)

# تهيئة الـ API بمفتاحك
API_KEY = "AIzaSyDq4XiDDuRLitWDClLCLlgh1sfu2Gj9ITw"
genai.configure(api_key=API_KEY)

uploaded_file = st.file_uploader("ارفع صورة الشارت هنا...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_column_width=True)
    
    if st.button("🚀 ابدأ تحليل القناص"):
        with st.spinner('⏳ جاري التحليل...'):
            try:
                # محاولة استخدام الموديل الأحدث
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = "حلل هذا الشارت بدقة: استخرج مناطق SNR والسيولة والأهداف بالعربي."
                response = model.generate_content([prompt, image])
                st.success("✅ اكتمل التحليل:")
                st.write(response.text)
            except Exception as e:
                st.error("السيرفر يواجه صعوبة في الاتصال بمحرك الذكاء الاصطناعي.")
                st.info("تأكد من أن تطبيقك محدث في لوحة تحكم Streamlit.")
