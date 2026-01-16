import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Nano Banana Pro", layout="centered", page_icon="🍌")

# التحقق من المفتاح والاتصال بجوجل
api_working = False
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # التصحيح النهائي: استخدام الموديل الأحدث لتجنب الأخطاء
        vision_model = genai.GenerativeModel('gemini-1.5-flash-latest')
        api_working = True
except Exception as e:
    pass

st.title("🍌 Nano Banana Pro | المساعد الشامل")
st.markdown("---")

# التبويبات
tab1, tab2 = st.tabs(["📝 توليد من نص", "🖼️ توليد من صورة"])

# === التبويب 1: الكتابة ===
with tab1:
    st.write("حول فكرتك إلى وصف دقيق:")
    subject = st.text_area("اكتب فكرتك هنا", height=100, placeholder="مثال: سيارة سباق حمراء في الصحراء...")
    style = st.selectbox("النمط", ["فوتوغرافية (Realistic)", "ثلاثي الأبعاد (3D)", "رسم (Art)", "سينمائي (Cinematic)"])
    
    if st.button("✨ توليد البرومبت", key="btn1"):
        st.success("النتيجة:")
        st.code(f"Generate an image of {subject}, Style: {style}, 8k resolution, highly detailed masterpiece", language="text")

# === التبويب 2: الصور ===
with tab2:
    st.write("ارفع صورة وسأقوم بتحليلها لك:")
    uploaded_file = st.file_uploader("ارفع الصورة هنا", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, width=250, caption="الصورة المرفوعة")
        
        if st.button("🚀 تحليل الصورة", key="btn2"):
            if api_working:
                with st.spinner('جاري الاتصال بـ Nano Banana...'):
                    try:
                        # طلب التحليل
                        response = vision_model.generate_content(["Describe this image in detail for AI image generation prompt", image])
                        st.success("تم التحليل بنجاح! انسخ هذا الوصف:")
                        st.write(response.text)
                        st.code(f"{response.text}, 8k resolution, highly detailed", language="text")
                    except Exception as e:
                        st.error("حدث خطأ بسيط، حاول مرة أخرى.")
            else:
                st.error("⚠️ المفتاح (API Key) غير موجود في إعدادات Secrets.")
