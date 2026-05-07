import streamlit as st
import google.generativeai as genai
from PIL import Image

# إعداد الـ API
genai.configure(api_key="AIzaSyDq4XiDDuRLitWDClLCLlgh1sfu2Gj9ITw")
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🔱 رادار الذهب الذكي")

file = st.file_uploader("ارفع الشارت هنا", type=["jpg", "png"])

if file:
    img = Image.open(file)
    st.image(img)
    if st.button("تحليل الأهداف والمناطق"):
        # هنا الذكاء الاصطناعي هو اللي "بيشوف" وينطق المناطق
        res = model.generate_content(["حلل شارت الذهب هذا واستخرج مناطق SNR والسيولة بدقة، واعطني السعر والهدف والوقف بالعربي", img])
        st.write(res.text)
