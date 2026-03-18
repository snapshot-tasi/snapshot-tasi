import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. إعدادات التصميم (Advanced UI/UX) ---
st.set_page_config(page_title="Snapshot-Tasi | Aramco 2222", layout="wide")

def apply_style():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    html, body, [class*="css"] { font-family: 'Noto Kufi Arabic', sans-serif; text-align: right; direction: rtl; }
    .main { background-color: #f0f4f8; }
    .section-header {
        background: linear-gradient(90deg, #1e3a8a, #3b82f6);
        color: white; padding: 15px; border-radius: 10px; margin: 30px 0 15px 0; font-size: 20px; font-weight: bold;
    }
    .card {
        background: white; padding: 20px; border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-right: 5px solid #1e3a8a; height: 100%;
    }
    .card-title { color: #1e3a8a; font-weight: bold; font-size: 16px; margin-bottom: 8px; }
    .card-value { color: #10b981; font-size: 18px; font-weight: bold; }
    .card-desc { color: #64748b; font-size: 12px; line-height: 1.4; }
    </style>
    """, unsafe_allow_html=True)

apply_style()

st.title("🛡️ Snapshot-Tasi: تقرير أرامكو السعودية (2222)")
st.caption("تحليل مالي معمق لعام 2025/2026 | إعداد: محلل مالي معتمد (CFA3)")

# --- الخطوة 1: الـ Snapshot (10 نقاط) ---
st.markdown("<div class='section-header'>1. الـ Snapshot (10 نقاط استراتيجية)</div>", unsafe_allow_html=True)
snap_data = [
    ("نموذج العمل", "طاقة متكاملة", "أكبر شركة طاقة عالمياً (تنقيب، إنتاج، تكرير)."),
    ("مصدر الإيرادات", "النفط والغاز", "المحرك الرئيسي: النفط الخام، الغاز، والكيميائيات."),
    ("الهوامش الربحية", "19.8% (ROACE)", "هوامش قوية جداً لعام 2025 تعكس كفاءة التشغيل."),
    ("مستوى الدين", "3.8% (Gearing)", "مديونية منخفضة جداً توفر أماناً مالياً عالياً."),
    ("التدفقات النقدية", "320.4B (FCF)", "تدفقات نقدية حرة قوية تدعم التوزيعات المستمرة."),
    ("جودة الأرباح", "عالية جداً", "التدفق التشغيلي يفوق الربح المحاسبي بشكل ملموس."),
    ("المخاطر", "تقلبات النفط", "تأثر بأسعار الطاقة والتوترات الجيوسياسية العالمية."),
    ("المحفزات", "مشروع الجافورة", "التوسع في الغاز وبرامج إعادة شراء الأسهم."),
    ("التقييم الحالي", "18.8x (P/E)", "تقييم عادل يعكس جودة الأصول واستقرار العوائد."),
    ("قرار مبدئي", "شراء (Buy)", "خيار استراتيجي لمستثمري العوائد والنمو الطويل.")
]

for i in range(0, 10, 5):
    cols = st.columns(5)
    for j in range(5):
        title, val, desc = snap_data[i+j]
        with cols[j]:
            st.markdown(f"<div class='card'><div class='card-title'>{title}</div><div class='card-value'>{val}</div><div class='card-desc'>{desc}</div></div>", unsafe_allow_html=True)

# --- الخطوة 2: تحليل الأداء ---
st.markdown("<div class='section-header'>2. تحليل الأداء (آخر 12 ربعاً)</div>", unsafe_allow_html=True)
c2_1, c2_2 = st.columns([2, 1])
with c2_1:
    fig = go.Figure()
    fig.add_trace(go.Bar(x=['2024', '2025'], y=[393, 348], name="صافي الربح (مليار ريال)", marker_color='#1e3a8a'))
    fig.update_layout(title="مقارنة صافي الربح السنوي", height=300)
    st.plotly_chart(fig, use_container_width=True)
with c2_2:
    st.info("**أسباب هبوط الربح (2025 vs 2024):**\n1. انخفاض أسعار النفط والمنتجات.\n2. تراجع مبيعات الكيميائيات.\n3. انخفاض EBIT المعدل لـ 199B$.")

# --- الخطوة 3 & 4: جودة الأرباح والمنافسين ---
st.markdown("<div class='section-header'>3 & 4. جودة الأرباح والمقارنة المحلية</div>", unsafe_allow_html=True)
c3, c4 = st.columns(2)
with c3:
    st.markdown("**إشارات جودة الأرباح:**\n* التدفق التشغيلي (136.2B$) > صافي الربح (93.4B$).\n* تحسن رأس المال العامل في الربع الرابع.\n* خسائر تقييم أصول سابك (غير نقدية).")
with c4:
    comp_df = pd.DataFrame({
        "المعيار": ["صافي الربح", "ROACE", "المديونية", "عائد التوزيعات"],
        "أرامكو": ["348B", "19.8%", "3.8%", "4.9%"],
        "أديس": ["760M", "11%", "عالية", "2.5%"],
        "الدريس": ["421M", "16%", "متوسطة", "1.3%"]
    })
    st.table(comp_df)

# --- الخطوة 5 & 6: السيناريوهات والحساسية ---
st.markdown("<div class='section-header'>5 & 6. السيناريوهات وتحليل الحساسية</div>", unsafe_allow_html=True)
s1, s2, s3 = st.columns(3)
with s1: st.success("**متفائل (Bull):** نفط 90$ | سعر عادل: 32-35 ريال")
with s2: st.info("**أساسي (Base):** نفط 75-80$ | سعر عادل: 27-29 ريال")
with s3: st.error("**تشاؤمي (Bear):** نفط < 65$ | سعر عادل: 22-24 ريال")

st.warning("**نقطة الحساسية الحرجة:** سعر برنت تحت **60$** يهدد التوزيعات الإضافية.")

# --- الخطوة 7: التوصية ---
st.markdown("<div class='section-header'>7. توصية مدير المحفظة (CFA Strategy)</div>", unsafe_allow_html=True)
rec1, rec2 = st.columns(2)
with rec1:
    st.markdown("🎯 **استراتيجية التجميع:** الشراء التدريجي بين **25-27 ريال**.\n\n🛑 **إلغاء الفكرة:** كسر مستوى **23 ريال** مع تدهور النفط.")
with rec2:
    st.markdown("🚀 **محفز زيادة المركز:** بدء إنتاج **حقل الجافورة**.\n\n📉 **محفز الخروج:** وصول السهم لـ **35 ريال** مع تباطؤ الطلب.")
