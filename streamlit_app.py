import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Nano Banana Pro", page_icon="🍌")
st.title("🍌 Nano Banana Pro | المختار الآلي")
st.caption("اختر الموديل من القائمة وجرب حتى يعمل معك")
st.markdown("---")

# 1. إعداد الاتصال
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ يجب وضع مفتاح API Key في الـ Secrets")
    st.stop()

# 2. جلب الموديلات المتاحة لك فعلياً
try:
    # نطلب من جوجل القائمة الخاصة بك
    my_models = []
    for m in genai.list_models():
        # نأخذ فقط الموديلات التي تدعم الصور (Vision)
        if 'vision' in m.supported_generation_methods or 'generateContent' in m.supported_generation_methods:
            my_models.append(m.name)
    # نرتبها لتظهر الموديلات الجديدة (Flash) في البداية
    my_models.sort(reverse=True)
except Exception as e:
    st.error(f"لم أتمكن من جلب القائمة: {e}")
    my_models = ["models/gemini-1.5-flash", "models/gemini-pro-vision"]

# 3. واجهة التطبيق
# === القائمة المنسدلة (الحل السحري) ===
selected_model = st.selectbox("⬇️ اختر الموديل من هنا (جرب الأول، إذا فشل جرب الثاني):", my_models)

uploaded_file = st.file_uploader("ارفع الصورة هنا", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, width=200)
    
    if st.button("🚀 تحليل الصورة"):
        with st.spinner(f'جاري التحليل باستخدام {selected_model}...'):
            try:
                # نستخدم الموديل الذي اخترته أنت بيدك
                model = genai.GenerativeModel(selected_model)
                response = model.generate_content(["Describe this image in detail for AI prompt generation", image])
                
                st.success(f"✅ تم النجاح بالموديل: {selected_model}")
                st.write(response.text)
                st.code(response.text)
                
            except Exception as e:
                st.error("❌ فشل هذا الموديل، جرب اختيار موديل آخر من القائمة في الأعلى.")
                st.error(e)
