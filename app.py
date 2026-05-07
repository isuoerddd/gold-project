import streamlit as st
import google.generativeai as genai
from PIL import Image

# إعدادات الواجهة
st.set_page_config(page_title="GOLD AI SNIPER", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #05070a; color: white; }
    .header-text { text-align: center; color: #FFD700; font-size: 32px; font-weight: bold; padding: 25px; }
    .report-box { background-color: #11141a; border: 2px solid #FFD700; padding: 25px; border-radius: 20px; direction: rtl; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header-text">🔱 قناص الذهب بالذكاء الاصطناعي 🔱</div>', unsafe_allow_html=True)

# المفتاح الخاص بك
API_KEY = "AIzaSyDq4XiDDuRLitWDClLCLlgh1sfu2Gj9ITw"

try:
    genai.configure(api_key=API_KEY)
    # تعريف الموديل بدون كلمة models/ لتجنب مشاكل الإصدارات
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("فشل في تهيئة محرك الذكاء الاصطناعي")

uploaded_file = st.file_uploader("ارفع شارت الذهب (TradingView)...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='الشارت المرفوع', use_column_width=True)
    
    if st.button("🚀 ابدأ تحليل القناص"):
        with st.spinner('⏳ جاري فحص السيولة و SNR...'):
            try:
                # البرومبت المركز
                prompt = "أنت محلل ذهب خبير. حلل الصورة واستخرج مناطق SNR (RBS/SBR) والسيولة والجاب. اعطِ توصية: دخول، هدف، وقف."
                
                # إرسال الطلب
                response = model.generate_content([prompt, image])
                
                st.markdown("### 🎯 تقرير القناص الذكي")
                st.markdown(f'<div class="report-box">{response.text}</div>', unsafe_allow_html=True)
                st.balloons()
            except Exception as e:
                st.error(f"حدث خطأ في السيرفر: {str(e)}")
                st.info("ملاحظة: إذا ظهر خطأ 404، يرجى إعادة تشغيل التطبيق (Reboot) بعد تحديث الـ requirements.")
