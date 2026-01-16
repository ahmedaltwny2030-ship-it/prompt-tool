import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Nano Banana Pro", layout="centered", page_icon="🍌")

# التحقق من المفتاح
api_working = False
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # الحل الجذري: استخدام الموديل القياسي المتوافق مع الجميع
        vision_model = genai.GenerativeModel('gemini-pro-vision')
        api_working = True
except Exception as e:
    pass

st.title("🍌 Nano Banana Pro | المساعد الشامل")
st.markdown("---")

tab1, tab2 = st.tabs(["📝 توليد من نص", "🖼️ توليد من صورة"])

# === تبويب النصوص ===
with tab1:
    st.write("💡 اكتب فكرتك وسأحولها لبرومبت احترافي:")
    subject = st.text_area("وصف الفكرة", height=100, placeholder="مثال: علبة عطر زرقاء على الشاطئ...")
    style = st.selectbox("النمط", ["فوتوغرافية (Realistic)", "سينمائي (Cinematic)", "ثلاثي الأبعاد (3D)"], key="s1")
    
    if st.button("✨ توليد البرومبت", key="btn1"):
        st.success("النتيجة (انسخ النص بالأسفل):")
        st.code(f"Generate an image of {subject}, Style: {style}, 8k resolution, highly detailed masterpiece", language="text")

# === تبويب الصور (المعدل) ===
with tab2:
    st.write("📸 ارفع صورة المنتج/التصميم وسأقوم بتحليلها:")
    uploaded_file = st.file_uploader("اختر صورة", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, width=250, caption="الصورة المرفوعة")
        
        if st.button("🚀 تحليل الصورة", key="btn2"):
            if api_working:
                with st.spinner('جاري سؤال الذكاء الاصطناعي...'):
                    try:
                        # هذا الأمر يعمل مع النسخة القياسية
                        response = vision_model.generate_content(["Describe this image in detail for AI image generation prompt", image])
                        st.success("✅ تم التحليل بنجاح! انسخ الوصف التالي:")
                        st.write(response.text)
                        st.code(f"{response.text}, 8k resolution, highly detailed", language="text")
                    except Exception as e:
                        st.error("حدث خطأ تقني. يرجى المحاولة مرة أخرى.")
                        st.error(e)
            else:
                st.error("⚠️ لم يتم العثور على مفتاح API Key في الإعدادات.")
