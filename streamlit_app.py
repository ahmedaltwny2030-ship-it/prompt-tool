import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

st.set_page_config(page_title="Nano Banana Pro", page_icon="🍌")

st.title("🍌 Nano Banana Pro | المصحح التلقائي")
st.write("---")

# 1. إعداد الاتصال
api_status = False
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    api_status = True
else:
    st.error("⚠️ لم يتم العثور على مفتاح API. تأكد من وضعه في Secrets.")

# 2. الدالة الذكية لتجربة الموديلات (نظام الطوارئ)
def try_generate_content(image_input, prompt):
    # قائمة الموديلات التي سنحاول استخدامها بالترتيب
    models_to_try = ["gemini-1.5-flash", "gemini-1.5-flash-latest", "gemini-pro-vision"]
    
    errors = []
    
    # حلقة تكرار لتجربة الموديلات واحداً تلو الآخر
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            # محاولة التوليد
            response = model.generate_content([prompt, image_input])
            return response.text, model_name # نجح! نرجع النتيجة واسم الموديل
        except Exception as e:
            errors.append(f"{model_name}: {str(e)}")
            continue # فشل هذا الموديل، جرب التالي
            
    # إذا وصلنا هنا، فكل الموديلات فشلت
    return None, errors

# 3. واجهة التطبيق
uploaded_file = st.file_uploader("ارفع الصورة هنا", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, width=300)
    
    if st.button("🚀 تحليل الصورة (محاولة ذكية)"):
        if api_status:
            with st.spinner('جاري البحث عن موديل يعمل...'):
                # استدعاء الدالة الذكية
                result, model_used = try_generate_content(image, "Describe this image in detail for AI prompt generation")
                
                if result:
                    st.success(f"✅ تم النجاح باستخدام الموديل: {model_used}")
                    st.write(result)
                    st.code(result, language="text")
                else:
                    st.error("❌ فشلت جميع المحاولات. تفاصيل الخطأ التقني:")
                    st.write(model_used) # هنا سنطبع قائمة الأخطاء لنعرف السبب الحقيقي
