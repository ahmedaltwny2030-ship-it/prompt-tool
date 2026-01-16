import streamlit as st

# إعداد الصفحة
st.set_page_config(page_title="Nano Banana Pro Generator", layout="centered", page_icon="🍌")

# العنوان والشعار
st.title("🍌 Nano Banana Pro | مولد البرومبت")
st.caption("أداة متخصصة لنموذج Gemini 3 Pro Image")
st.markdown("---")

# 1. العمود الأيمن: إعدادات الصورة الأساسية
col1, col2 = st.columns(2)

with col1:
    style = st.selectbox(
        "نط الصورة (Style)", 
        ["فوتوغرافية (Photography)", "إعلان تجاري (Advertising)", "انفوجرافيك (Infographic)", "ثلاثي الأبعاد (3D Render)", "تصميم واجهة (UI Design)"]
    )
    
    aspect_ratio = st.selectbox(
        "الأبعاد (Aspect Ratio)",
        ["16:9 (عريض - يوتيوب/شاشات)", "9:16 (طولي - تيك توك/ريلز)", "1:1 (مربع - انستجرام)", "21:9 (سينمائي)"]
    )

# 2. العمود الأيسر: الدقة والنصوص
with col2:
    resolution = st.selectbox("الدقة (Resolution)", ["4K (Ultra HD)", "2K (Standard)", "8K (Upscaled)"])
    
    # ميزة حصرية لـ Nano Banana: كتابة النصوص
    text_on_image = st.text_input("نص يكتب داخل الصورة (اختياري)", placeholder="مثال: Special Offer")

# 3. وصف المشهد (الأساس)
st.markdown("### 📝 وصف المشهد")
subject = st.text_area("اشرح فكرتك بالتفصيل", placeholder="مثال: زجاجة عطر فاخرة من الكريستال الأزرق موضوعة على صخرة سوداء في وسط البحر...", height=100)

# دالة التوليد المتخصصة لـ Nano Banana
def generate_nano_prompt(sub, sty, ar, res, txt):
    # تحويل الأبعاد لصيغة يفهمها الموديل
    ar_map = {
        "16:9 (عريض - يوتيوب/شاشات)": "--ar 16:9",
        "9:16 (طولي - تيك توك/ريلز)": "--ar 9:16",
        "1:1 (مربع - انستجرام)": "--ar 1:1",
        "21:9 (سينمائي)": "--ar 21:9"
    }
    
    # تحسينات الأنماط الخاصة بـ Nano Banana
    style_prompts = {
        "فوتوغرافية (Photography)": "shot on Sony A7R IV, 85mm lens, photorealistic, depth of field",
        "إعلان تجاري (Advertising)": "professional product photography, studio lighting, advertising standard, clean background, commercial look",
        "انفوجرافيك (Infographic)": "clean infographic style, vector graphics, educational layout, minimalist design, clear typography",
        "ثلاثي الأبعاد (3D Render)": "3D render, Unreal Engine 5 style, octane render, hyper-detailed textures, volumetric lighting",
        "تصميم واجهة (UI Design)": "modern UI/UX design, glassmorphism, clean interface, figma style, high fidelity mockup"
    }

    # بناء البرومبت
    base_prompt = f"{sub}"
    
    # إضافة النص إذا وجد (ميزة Nano القوية)
    text_instruction = ""
    if txt:
        text_instruction = f", render the text '{txt}' clearly and elegantly in a matching font"
    
    # تجميع الأجزاء
    full_prompt = (
        f"Generate a {resolution} image of {base_prompt}. "
        f"Style: {style_prompts[sty]}{text_instruction}. "
        f"Lighting: Cinematic lighting with soft shadows. "
        f"Quality: Masterpiece, highly detailed, sharp focus. "
        f"{ar_map[ar]}"
    )
    
    return full_prompt

# زر التنفيذ
if st.button("🚀 توليد كود Nano Banana", use_container_width=True):
    if subject:
        final_prompt = generate_nano_prompt(subject, style, aspect_ratio, resolution, text_on_image)
        
        st.success("تم تجهيز البرومبت! انسخه للنموذج:")
        st.code(final_prompt, language="text")
        
        # نصائح إضافية تظهر بعد التوليد
        st.info("💡 نصيحة للمحترفين: نموذج Nano Banana Pro يحب التفاصيل الطبيعية، لا تتردد في وصف الإضاءة (مثلاً: Sunset, Neon light).")
    else:
        st.warning("⚠️ يرجى كتابة وصف المشهد أولاً")
