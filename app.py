import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- إعدادات الواجهة الفخمة ---
st.set_page_config(page_title="GOLD AI SNIPER", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #05070a; color: white; }
    .stApp { background-color: #05070a; }
    .header-text {
        text-align: center; color: #FFD700;
        font-size: 32px; font-weight: bold; padding: 25px;
        text-shadow: 2px 2px 8px #000;
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

# تهيئة موديل Gemini (استخدام الاسم البرمجي المباشر)
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    # هذا الاسم هو الأكثر استقراراً لتجاوز خطأ 404
    model = genai.GenerativeModel('gemini-1.5-flash') 
except Exception as e:
    st.error("فشل الاتصال بمحرك الذكاء الاصطناعي.")

# --- منطقة رفع الشارت ---
st.write("---")
st.markdown("### 📸 ارفع سكرين شوت لشارت الذهب (TradingView)")
uploaded_file = st.file_uploader("اختر صورة للشارت لتحليلها فوريًا...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='الشارت المرفوع', use_column_width=True)
    
    if st.button("🚀 ابدأ تحليل القناص الآن"):
        with st.spinner('⏳ جاري تحليل السيولة ومناطق SNR...'):
            try:
                # البرومبت الموجه لمدرسة SNR والسيولة
                prompt = """
                أنت الآن محلل فني خبير متخصص في الذهب (XAUUSD) بمدرستي SNR الماليزية والسيولة (Liquidity).
                قم بفحص الصورة المرفوعة بدقة واستخرج منها التحليل التالي باللغة العربية:
                
                1. رصد مناطق الانعكاس القوية: RBS و SBR.
                2. تحديد مناطق العرض والطلب (Supply & Demand).
                3. البحث عن الجابات السعرية (Gaps).
                4. تحديد مناطق سحب السيولة (Liquidity Sweep).
                
                صغ التقرير بشكل احترافي يتضمن نقطة الدخول، الهدف، ووقف الخسارة.
                """
                
                # استخدام generate_content مباشرة
                response = model.generate_content([prompt, image])
                
                st.markdown("---")
                st.markdown("### 🎯 تقرير القناص الذكي")
                st.markdown(f'<div class="report-box">{response.text}</div>', unsafe_allow_html=True)
                st.balloons()
                
            except Exception as e:
                # محاولة ثانية باسم موديل مختلف إذا فشل الأول (خطة بديلة)
                try:
                    alt_model = genai.GenerativeModel('gemini-pro-vision')
                    response = alt_model.generate_content([prompt, image])
                    st.markdown(f'<div class="report-box">{response.text}</div>', unsafe_allow_html=True)
                except:
                    st.error(f"حدث خطأ في النظام: {str(e)}")
else:
    st.info("💡 نصيحة: ارفع صورة واضحة للشارت لضمان دقة تحديد مناطق الدخول.")

st.markdown("<br><hr><center><p style='color: #555;'>نظام تحليل الذهب الموحد - 2026</p></center>", unsafe_allow_html=True)
