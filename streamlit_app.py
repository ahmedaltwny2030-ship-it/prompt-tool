import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Nano Banana Pro", page_icon="🍌")
st.title("🍌 Nano Banana Pro | المكتشف الذكي")

# 1. إعداد الاتصال
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ يجب وضع مفتاح API Key في الـ Secrets")
    st.stop()

# 2. دالة ذكية تجرب كل الموديلات المعروفة حتى ينجح واحد منها
def smart_generate(image_input, prompt_text):
    # قائمة بكل الموديلات المحتملة (الجديد والقديم)
    candidates = [
        "gemini-1.5-flash", 
        "gemini-1.5-pro", 
        "gemini-pro-vision", 
        "models/gemini-1.5-flash-latest",
        "gemini-1.0-pro-vision-latest"
    ]
    
    last_error = ""
    
    # حلقة تكرار تجربهم واحداً تلو الآخر
    for model_name in candidates:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content([prompt_text, image_input])
            return response.text, model_name # نجح! مبروك
        except Exception as e:
            last_error = str(e)
            continue # فشل هذا، جرب اللي بعده فوراً
            
    return None, last_error

# 3. الواجهة
st.write("ارفع الصورة وسأبحث عن الموديل المناسب لحسابك تلقائياً:")
uploaded_file = st.file_uploader("اختر صورة", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, width=200)
    
    if st.button("🚀 تحليل (تجربة الكل)"):
        with st.spinner('جاري تجربة الموديلات المتاحة...'):
            result, model_used = smart_generate(image, "Describe this image in detail")
            
            if result:
                st.success(f"✅ تم النجاح! الموديل الذي اشتغل معك هو: {model_used}")
                st.write(result)
                st.code(result)
            else:
                st.error("❌ للأسف حسابك لا يدعم أي موديل صور حالياً. إليك قائمة الموديلات المتاحة في مفتاحك:")
                # كود تشخيصي لطباعة الموديلات المتاحة فعلياً
                try:
                    for m in genai.list_models():
                        if 'vision' in m.supported_generation_methods or 'generateContent' in m.supported_generation_methods:
                            st.write(f"- {m.name}")
                except:
                    st.write("لم أتمكن من جلب القائمة.")
