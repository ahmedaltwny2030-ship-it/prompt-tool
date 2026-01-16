import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Nano Banana Pro", layout="centered", page_icon="🍌")

# التحقق من المفتاح
api_working = False
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # نستخدم الاسم القياسي المستقر
        vision_model = genai.GenerativeModel('gemini-1.5-flash')
        api_working = True
except Exception as e:
    pass

st.title("🍌 Nano Banana Pro | المساعد الشامل")
st.markdown("---")

tab1, tab2 = st.tabs(["📝 توليد من نص", "🖼️ توليد من صورة"])

# === التبويب 1 ===
with tab1:
    subject = st.text_area("وصف الفكرة", height=100, placeholder="اكتب هنا...")
    style = st.selectbox("النمط", ["فوتوغرافية", "سينمائي", "ثلاثي الأبعاد"], key="s1")
    if st.button("توليد", key="b1"):
        st.code(f"Generate image of {subject}, Style: {style}, 8k", language="text")

# === التبويب 2 (تحليل الصور) ===
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
                        response = vision_model.generate_content(["Describe this image for AI prompt", image])
                        st.success("تم التحليل:")
                        st.write(response.text)
                        st.code(response.text, language="text")
                    except Exception as e:
                        # هذا السطر سيظهر لك سبب الخطأ الحقيقي بدلاً من الرسالة العامة
                        st.error(f"حدث خطأ: {e}")
            else:
                st.error("⚠️ تأكد من وضع مفتاح API Key في الـ Secrets")
