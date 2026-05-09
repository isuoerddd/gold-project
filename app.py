import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Pro Order Flow Sniper", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: white; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #161b22; border-radius: 5px; color: white; padding: 10px 20px; }
    .pro-box { padding: 20px; border-radius: 10px; border: 1px solid #30363d; background: #161b22; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ رادار السكالبينج وعمق السوق (Bookmap Style)")

# إنشاء تبويبات (Tabs) للتنقل بين الأدوات
tab1, tab2 = st.tabs(["📊 شاشة السيولة (Order Flow)", "🎯 حاسبة السكالب"])

with tab1:
    st.subheader("بث تدفق الأوامر المباشر (Aggr Live)")
    # دمج شاشة Aggr الشهيرة لعرض البوك ماب والسيولة
    # هذا الرابط يجلب بيانات الذهب والعملات بنظام الفقاعات (Bubbles) والسيولة
    aggr_url = "https://aggr.trade/" 
    components.iframe(aggr_url, height=600, scrolling=True)

with tab2:
    st.subheader("تحليل العمق وتوصية السكالب")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.info("قم بمراقبة الفقاعات الكبيرة في الشاشة السابقة؛ الفقاعات الخضراء تعني دخول سيولة شراء قوية.")
        high = st.number_input("أعلى سعر مسجل الآن (High)", value=2350.0)
        low = st.number_input("أدنى سعر مسجل الآن (Low)", value=2340.0)
        current = st.number_input("السعر الحالي", value=2345.0)
        
    with col2:
        if st.button("🔥 تحليل سكالب سريع"):
            diff = high - low
            # معادلة السكالب السريع (زوايا جان الصغرى)
            scalp_target = current + (diff * 0.0625) # هدف سكالب سريع
            
            if current > (low + (diff * 0.5)):
                st.success(f"✅ سيولة شرائية مسيطرة\nالهدف: {scalp_target:.2f}")
            else:
                st.error(f"⚠️ سيولة بيعية مسيطرة\nالهدف: {current - (diff * 0.0625):.2f}")

st.sidebar.markdown("""
### 💡 كيف تستخدم الموقع؟
1. **شاشة السيولة:** راقب "الفقاعات" الكبيرة، هي تمثل أوامر (Big Orders) الحيتان.
2. **Bookmap:** إذا رأيت خطوطاً ملونة ثابتة، فهي "جدران سيولة" (Liquidity Walls).
3. **التوصية:** ادخل شراء مع الفقاعات الخضراء وبيكرر (Aggressive Buying).
""")
