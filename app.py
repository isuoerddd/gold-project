import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- إعدادات الواجهة ---
st.set_page_config(page_title="GOLD AI SNIPER", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #05070a; color: white; }
    .stApp { background-color: #05070a; }
    .header-text {
        text-align: center; color: #FFD700;
        font-size: 32px; font-weight: bold; padding: 25px;
    }
    .report-box {
        background-color: #11141a; border: 2px solid #FFD700;
        padding: 25px; border-radius: 20px; margin-top: 20px;
        color: #e0e0e0; line-height: 1.8; font-size: 17px;
        direction: rtl; text-align: right;
    }
    .stFileUploader { background-color: #11141a; border-radius: 12px; border: 1px dashed #FFD700; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header-text">🔱 قناص الذهب بالذكاء الاصطناعي 🔱</div>', unsafe_allow_html=True)

# --- إعداد مفتاح الـ API الخاص بك ---
GOOGLE_API_KEY = "AIzaSyDq4XiDDuRLitWDClLCLlgh1sfu2Gj9ITw" 

# تهيئة موديل Gemini (تم تغيير التسمية لتعمل على v1beta و v1)
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    # جربنا كل الأسماء، هذا هو الاسم الرسمي الآن في نظام جوجل
    model = genai.GenerativeModel('gemini-1.5-flash') 
except Exception as e:
    st.error("فشل الاتصال بمحرك الذكاء الاصطناعي.")

# --- منطقة رفع الشارت ---
st.write("---")
uploaded_file = st.file_uploader("اختر صورة للشارت (TradingView)...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='الشارت المرفوع', use_column_width=True)
    
    if st.button("🚀 ابدأ تحليل القناص الآن"):
        with st.spinner('⏳ جاري تحليل السيولة ومناطق SNR...'):
            try:
                prompt = """
                تحليل فني لمدرسة SNR الماليزية والسيولة لشارت الذهب:
                1. حدد مناطق RBS و SBR.
                2. حدد مناطق العرض والطلب.
                3. ابحث عن سحب السيولة والجاب.
                اكتب تقرير بالعربية: (دخول، هدف، وقف).
                """
                
                # إرسال الصورة للموديل
                response = model.generate_content([prompt, image])
                
                st.markdown("---")
                st.markdown("### 🎯 تقرير القناص الذكي")
                st.markdown(f'<div class="report-box">{response.text}</div>', unsafe_allow_html=True)
                st.balloons()
                
            except Exception as e:
                # إذا فشل الأول، جرب الموديل الثاني (خطة بديلة أوتوماتيكية)
                try:
                    alt_model = genai.GenerativeModel('gemini-1.5-pro')
                    response = alt_model.generate_content([prompt, image])
                    st.markdown(f'<div class="report-box">{response.text}</div>', unsafe_allow_html=True)
                except Exception as e2:
                    st.error(f"خطأ في السيرفر: يرجى التأكد من أن مكتبة google-generativeai محدثة.")
                    st.code(f"Error Log: {str(e2)}")
else:
    st.info("💡 ارفع صورة واضحة للشارت لبدء التحليل.")

st.markdown("<br><hr><center><p style='color: #555;'>نظام تحليل الذهب الموحد - 2026</p></center>", unsafe_allow_html=True)
