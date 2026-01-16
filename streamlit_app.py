import streamlit as st
import subprocess
import sys
import os

# --- أداة الإصلاح الذاتي (Force Update) ---
# هذا الجزء يجبر السيرفر على تحميل أحدث نسخة رغماً عنه
try:
    import google.generativeai as genai
    # نتأكد هل النسخة قديمة؟
    if genai.__version__ < "0.8.3":
        st.toast("⚠️ جاري تحديث النظام تلقائياً... انتظر لحظة", icon="🔄")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "google-generativeai"])
        import google.generativeai as genai
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "google-generativeai"])
    import google.generativeai as genai

from PIL import Image

# إعداد الصفحة
st.set_page_config(page_title="Nano Banana Pro", page_icon="🍌")

# --- واجهة التطبيق ---
st.title("🍌 Nano Banana Pro | الإصدار المحدث")

# طباعة رقم النسخة للتأكد (ستظهر لك في أعلى التطبيق)
st.caption(f"System Version: {genai.__version__} (Correct ✅)")
st.markdown("---")

# إعداد المفتاح
api_working = False
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    api_working = True
else:
    st.error("⚠️ لم يتم العثور على مفتاح API Key.")

# تبويبات التطبيق
tab1, tab2 = st.tabs(["📝 توليد نصي", "🖼️ تحليل صورة"])

# التبويب 1
with tab1:
    txt = st.text_input("ماذا تريد أن تصمم؟")
    if st.button("توليد"):
        st.code(f"Imagine {txt}, 8k resolution", language="text")

# التبويب 2 (المشكلة كانت هنا)
with tab2:
    st.write("ارفع الصورة وسأقوم بتحليلها بالموديل الجديد:")
    uploaded_file = st.file_uploader("اختر صورة", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, width=200)
        
        if st.button("🚀 تحليل الصورة"):
            if api_working:
                with st.spinner('جاري الاتصال بـ Gemini 1.5 Flash...'):
                    try:
                        # نستخدم الموديل السريع والمدعوم
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        response = model.generate_content(["Describe this image for AI prompt", image])
                        st.success("تم التحليل بنجاح! 🎉")
                        st.write(response.text)
                    except Exception as e:
                        st.error("حدث خطأ تقني:")
                        st.write(e)
            else:
                st.error("تحقق من المفتاح السري (Secrets).")
