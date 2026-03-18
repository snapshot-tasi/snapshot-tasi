import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. إعدادات الهوية البصرية المتقدمة (CFA Premium UI) ---
st.set_page_config(page_title="Snapshot-Tasi Pro | Aramco Analysis", layout="wide")

def apply_pro_styling():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    html, body, [class*="css"] { font-family: 'Noto Kufi Arabic', sans-serif; text-align: right; direction: rtl; }
    .main { background-color: #f0f2f5; }
    .header-box {
        background: linear-gradient(135deg, #1a365d 0%, #2b6cb0 100%);
        color: white; padding: 2rem; border-radius: 20px; margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1); border-right: 8px solid #ed8936;
    }
    .snap-card {
        background: white; padding: 1.5rem; border-radius: 15px; height: 300px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-top: 5px solid #3182ce;
        transition: transform 0.3s ease; display: flex; flex-direction: column;
    }
    .snap-card:hover { transform: translateY(-5px); box-shadow: 0 12px 20px rgba(0,0,0,0.1); }
    .snap-title { color: #2c5282; font-weight: bold; font-size: 1.1rem; margin-bottom: 0.5rem; }
    .snap-value { font-size: 1.3rem; font-weight: 700; margin-bottom: 0.5rem; }
    .snap-desc { color: #4a5568; font-size: 0.85rem; line-height: 1.5; flex-grow: 1; }
    .status-pos { color: #2f855a; } /* أخضر إيجابي */
    .status-neu { color: #d69e2e; } /* أصفر محايد */
    .status-neg { color: #c53030; } /* أحمر سلبي */
    .section-title { color: #1a365d; border-right: 6px solid #ed8936; padding-right: 1rem; margin: 3rem 0 1.5rem 0; font-size: 1.8rem; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

apply_pro_styling()

st.markdown("""<div class='header-box'><h1>🛡️ Snapshot-Tasi: أرامكو السعودية (2222)</h1><p>تقرير استراتيجي معمق لعام 2025/2026 | معايير CFA Level III</p></div>""", unsafe_allow_html=True)

# --- 1. الـ Snapshot (10 نقاط مع علامات الحالة) ---
st.markdown("<div class='section-title'>1. الـ Snapshot (تحليل المعايير الاستراتيجية)</div>", unsafe_allow_html=True)

# الحالة: 1=إيجابي، 2=محايد، 3=سلبي
snap_items = [
    ("نموذج العمل", "🟢 طاقة متكاملة", "أكبر شركة طاقة عالمية تسيطر على كامل سلاسل القيمة من التنقيب حتى بيع المنتجات النهائية.", 1),
    ("مصدر الإيرادات", "🟢 مزيج الهيدروكربونات", "تعتمد على الزيت الخام كقاعدة صلبة، مع توسع حاد في الغاز الطبيعي لتقليل المخاطر.", 1),
    ("الهوامش الربحية", "🟢 19.8% (ROACE)", "كفاءة استثنائية في استغلال الأصول لتوليد أرباح تفوق تكلفة رأس المال.", 1),
    ("مستوى الدين", "🟢 3.8% (Gearing)", "ملاءة مالية فائقة وقدرة عالية على مواجهة الصدمات العالمية.", 1),
    ("التدفقات النقدية", "🟢 320.4B (FCF)", "تدفق نقدي حر قوي جداً؛ وهو المصدر الحقيقي للاستدامة المالية والتوزيعات.", 1),
    ("جودة الأرباح", "🟢 نقدية بامتياز", "تفوق النقد على الربح المحاسبي يؤكد غياب الحيل المحاسبية وجودة التشغيل.", 1),
    ("المخاطر الرئيسية", "🔴 تقلبات السلع", "حساسية عالية لأسعار برنت العالمية والتوترات الجيوسياسية التي تهدد الهوامش.", 3),
    ("المحفزات", "🟢 حقل الجافورة", "مشروع الغاز غير التقليدي سيخلق مصادر دخل ضخمة ومستدامة بعيداً عن النفط.", 1),
    ("التقييم الحالي", "🟡 18.8x (P/E)", "مكرر ربحية يعكس علاوة أمان، لكنه يتطلب نمواً موازياً للحفاظ على جاذبيته.", 2),
    ("قرار مبدئي", "🟢 شراء استراتيجي", "توصية مبنية على قوة التوزيعات والنمو القادم في مشاريع الطاقة النظيفة والغاز.", 1)
]

for row in range(2):
    cols = st.columns(5)
    for i in range(5):
        idx = row * 5 + i
        if idx < len(snap_items):
            title, val, desc, status = snap_items[idx]
            val_class = "status-pos" if status == 1 else ("status-neu" if status == 2 else "status-neg")
            with cols[i]:
                st.markdown(f"""
                <div class='snap-card'>
                    <div class='snap-title'>{title}</div>
                    <div class='snap-value {val_class}'>{val}</div>
                    <div class='snap-desc'>{desc}</div>
                </div>
                """, unsafe_allow_html=True)

# --- 2. تحليل الأداء (مع علامات الحالة) ---
st.markdown("<div class='section-title'>2. تحليل الأداء وتفكيك الإيرادات</div>", unsafe_allow_html=True)
c2_l, c2_r = st.columns(2)
with c2_l:
    fig = go.Figure(data=[go.Bar(x=['2024', '2025'], y=[393, 348], marker_color=['#2b6cb0', '#c53030'], text=['393B', '348B'], textposition='auto')])
    fig.update_layout(title="تراجع الربح السنوي (مليار ريال)", height=350)
    st.plotly_chart(fig, use_container_width=True)
with c2_r:
    st.markdown("""
    ### 📊 لماذا تراجع الربح؟
    - 🔴 **عامل السعر:** انخفاض أسعار البيع بنسبة 14% (تأثير سلبي حاد).
    - 🔴 **الطلب الكيميائي:** ضعف السوق العالمي ضغط على هوامش سابيك.
    - 🟢 **عامل الحجم:** استقرار الإنتاج عند 12.9M برميل يومياً (نقطة قوة).
    """)

# --- 5 & 6. السيناريوهات وتحليل الحساسية ---
st.markdown("<div class='section-title'>5 & 6. استشراف المستقبل والحساسية</div>", unsafe_allow_html=True)
sc1, sc2, sc3 = st.columns(3)
with sc1: st.markdown("<div style='background-color:#2f855a; color:white; padding:15px; border-radius:15px; text-align:center;'>🟢 <strong>المتفائل:</strong> نفط 90$ | سعر عادل: 32-35 ريال</div>", unsafe_allow_html=True)
with sc2: st.markdown("<div style='background-color:#2b6cb0; color:white; padding:15px; border-radius:15px; text-align:center;'>🔵 <strong>الأساسي:</strong> نفط 75-80$ | سعر عادل: 27-29 ريال</div>", unsafe_allow_html=True)
with sc3: st.markdown("<div style='background-color:#c53030; color:white; padding:15px; border-radius:15px; text-align:center;'>🔴 <strong>التشاؤمي:</strong> نفط < 65$ | سعر عادل: 22-24 ريال</div>", unsafe_allow_html=True)

st.warning("⚠️ **تحليل الحساسية:** سعر برنت تحت **60 دولار** يمثل نقطة الخطر على التوزيعات الإضافية.")

# --- 7. التوصية النهائية ---
st.markdown("<div class='section-title'>7. توصية مدير المحفظة (CFA3 Strategy)</div>", unsafe_allow_html=True)
rec_l, rec_r = st.columns(2)
with rec_l:
    st.success("🎯 **خطة التجميع:** شراء تدريجي بين **25-27 ريال** (🟢 إيجابية العائد).")
with rec_r:
    st.error("🛑 **إدارة المخاطر:** وقف الخسارة عند كسر **23 ريال** (🔴 إشارة خروج).")
