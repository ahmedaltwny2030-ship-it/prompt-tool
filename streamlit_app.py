import streamlit as st
import google.generativeai as genai
from PIL import Image

# إعداد الصفحة
st.set_page_config(page_title="Nano Banana Pro Generator", layout="centered", page_icon="🍌")

# محاولة الاتصال بمفتاح جوجل
api_working = False
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        vision_model = genai.GenerativeModel('gemini-1.5-flash')
        api_working = True
except Exception as e:
    pass

st.title("🍌 Nano Banana Pro | المساعد الشامل")
st.markdown("---")

# نظام التبويبات
tab1, tab2 = st.tabs(["📝 توليد من نص", "🖼️ توليد من صورة"])

# --- التبويب 1: نص ---
with tab1:
    subject = st.text_area("وصف الفكرة", placeholder="اكتب هنا...")
    style = st.selectbox("النمط", ["فوتوغرافية", "سينمائي", "ثلاثي الأبعاد"], key="s1")
    if st.button("توليد البرومبت", key="b1"):
        st.code(f"Generate image of {subject}, Style: {style}, 8k resolution", language="text")

# --- التبويب 2: تحليل صورة ---
with tab2:
    st.write("ارفع صورة وسأقوم بتحليلها وكتابة الوصف لك")
    uploaded_file = st.file_uploader("اختر صورة", type=["jpg", "png"])
    
    if uploaded_file and st.button("تحليل الصورة"):
        if api_working:
            img = Image.open(uploaded_file)
            st.image(img, width=200)
            with st.spinner('جاري التحليل...'):
                response = vision_model.generate_content(["Describe this image for AI generation", img])
                st.success("الوصف المقترح:")
                st.write(response.text)
                st.code(f"Generate image based on: {response.text}, 8k resolution", language="text")
        else:
            st.error("⚠️ يجب إعداد مفتاح API Key في إعدادات Streamlit أولاً لتفعيل هذه الميزة.")
