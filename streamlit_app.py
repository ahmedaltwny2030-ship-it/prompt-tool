import streamlit as st

# إعداد الصفحة
st.set_page_config(page_title="مساعد التصميم الاحترافي", layout="centered")

# العنوان الرئيسي
st.title("🎨 مساعد توليد البرومبت الاحترافي")
st.markdown("---")

# تقسيم الصفحة لعمودين
col1, col2 = st.columns(2)

with col1:
    # قائمة اختيار النمط
    style = st.selectbox(
        "اختر النمط (Style)", 
        ["تصوير واقعي (Cinematic)", "تصوير منتجات (Product)", "ثلاثي الأبعاد (3D Render)", "رسم رقمي (Digital Art)"]
    )

with col2:
    # مربع كتابة النص
    subject = st.text_input("ماذا تريد أن تصمم؟", placeholder="مثال: علبة عطر فاخرة، رجل ببدلة...")

# خيارات إضافية للإضاءة
lighting = st.select_slider("اختر نوع الإضاءة", options=["إضاءة نهارية", "إضاءة استوديو", "إضاءة درامية", "إضاءة نيون"])

# دالة التوليد (العقل المدبر)
def generate_prompt(sub, sty, lig):
    # قاموس الأنماط
    styles_map = {
        "تصوير واقعي (Cinematic)": "cinematic shot, 35mm lens, depth of field, hyperrealistic, 8k",
        "تصوير منتجات (Product)": "professional product photography, studio lighting, clean background, advertising standard, 8k",
        "ثلاثي الأبعاد (3D Render)": "3D render, Unreal Engine 5, octane render, c4d, hyper-detailed",
        "رسم رقمي (Digital Art)": "digital art, concept art, detailed illustration, masterpiece"
    }
    
    # قاموس الإضاءة
    light_map = {
        "إضاءة نهارية": "natural sunlight, golden hour, bright, soft shadows",
        "إضاءة استوديو": "soft studio lighting, softbox, professional setup, evenly lit",
        "إضاءة درامية": "dramatic lighting, rim light, volumetric fog, moody",
        "إضاءة نيون": "neon lighting, cyberpunk atmosphere, colorful, glowing"
    }
    
    # تجميع البرومبت النهائي
    final_prompt = f"{sub}, {styles_map[sty]}, {light_map[lig]}, 8k resolution, masterpiece, sharp focus, HDR, high fidelity"
    return final_prompt

# زر التشغيل
if st.button("✨ توليد البرومبت", use_container_width=True):
    if subject:
        # استدعاء الدالة
        prompt = generate_prompt(subject, style, lighting)
        
        # عرض النتيجة
        st.success("تم التوليد بنجاح! انسخ النص أدناه:")
        st.code(prompt, language="text")
        st.info("نصيحة: خذ هذا النص وضعه في Midjourney أو Leonardo للحصول على أفضل نتيجة.")
    else:
        st.warning("يرجى كتابة اسم الشيء الذي تريد تصميمه أولاً.")
