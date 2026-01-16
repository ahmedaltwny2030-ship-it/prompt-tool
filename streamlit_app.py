import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Nano Banana Pro", layout="centered", page_icon="🍌")

# التحقق من المفتاح
api_working = False
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # هذا هو الموديل الوحيد الذي يعمل باستقرار حالياً
        vision_model = genai.GenerativeModel('gemini-1.5-flash')
        api_working = True
except Exception as e:
    pass

st.title("🍌 Nano Banana Pro")
st.markdown("---")

tab1, tab2 = st.tabs(["📝 توليد نصي", "🖼️ تحليل صورة"])

# تبويب النصوص
with tab1:
    subject = st.text_area("اكتب فكرتك:", height=100)
    if st.button("توليد"):
        st.code(f"Imagine {subject}, 8k resolution", language="text")

# تبويب الصور (سبب المشكلة)
with tab2:
    st.write("ارفع صورة وسأقوم بتحليلها:")
    uploaded_file = st.file_uploader("اختر صورة", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, width=250)
        
        if st.button("🚀 تحليل الصورة", key="btn2"):
            if api_working:
                with st.spinner('جاري الاتصال...'):
                    try:
                        # الأمر المحدث للنسخة الجديدة
                        response = vision_model.generate_content(["Describe this image", image])
                        st.success("تم التحليل:")
                        st.write(response.text)
                        st.code(response.text, language="text")
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.error("⚠️ تأكد من وضع مفتاح API Key")
