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
        background: white; padding: 1.5rem; border-radius: 15px; height: 280px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-top: 4px solid #3182ce;
        transition: transform 0.3s ease; display: flex; flex-direction: column;
    }
    .snap-card:hover { transform: translateY(-5px); box-shadow: 0 12px 20px rgba(0,0,0,0.1); }
    .snap-title { color: #2c5282; font-weight: bold; font-size: 1.1rem; margin-bottom: 0.5rem; }
    .snap-value { color: #2f855a; font-size: 1.3rem; font-weight: 700; margin-bottom: 0.5rem; }
    .snap-desc { color: #4a5568; font-size: 0.85rem; line-height: 1.5; flex-grow: 1; }
    .scenario-card { padding: 1.5rem; border-radius: 15px; color: white; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
    .section-title { color: #1a365d; border-right: 6px solid #ed8936; padding-right: 1rem; margin: 3rem 0 1.5rem 0; font-size: 1.8rem; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

apply_pro_styling()

st.markdown("""<div class='header-box'><h1>🛡️ Snapshot-Tasi: أرامكو السعودية (2222)</h1><p>تقرير استراتيجي معمق لعام 2025/2026 | معايير CFA Level III</p></div>""", unsafe_allow_html=True)

# --- 1. الـ Snapshot (10 نقاط) ---
st.markdown("<div class='section-title'>1. الـ Snapshot (تحليل المعايير الاستراتيجية)</div>", unsafe_allow_html=True)

snap_items = [
    ("نموذج العمل", "طاقة متكاملة عمودياً", "أكبر شركة طاقة عالمية تسيطر على كامل سلاسل القيمة من التنقيب حتى بيع المنتجات النهائية."),
    ("مصدر الإيرادات", "مزيج الهيدروكربونات", "تعتمد على الزيت الخام كقاعدة صلبة، مع توسع حاد في الغاز الطبيعي والبتروكيماويات لتقليل الاعتماد على مبيعات الخام."),
    ("الهوامش الربحية", "19.8% (ROACE)", "العائد على متوسط رأس المال المستثمر؛ يعكس كفاءة الإدارة في استغلال الأصول لتوليد أرباح استثنائية."),
    ("مستوى الدين", "3.8% (Gearing)", "نسبة المديونية لصافي رأس المال؛ تعكس ملاءة مالية فائقة وقدرة عالية على مواجهة الصدمات."),
    ("التدفقات النقدية", "320.4B (FCF)", "التدفق النقدي الحر؛ السيولة المتبقية بعد كافة المصاريف الرأسمالية، وهي المصدر الحقيقي للتوزيعات المستدامة."),
    ("جودة الأرباح", "نقدية بامتياز", "مقارنة الربح المحاسبي بالتدفق التشغيلي؛ تفوق النقد يعني غياب الحيل المحاسبية وأن الأرباح نابعة من عمليات تشغيلية حقيقية."),
    ("المخاطر الرئيسية", "تقلبات السلع", "حساسية عالية لأسعار برنت العالمية والتوترات الجيوسياسية التي قد ترفع تكاليف التأمين."),
    ("المحفزات", "حقل الجافورة", "مشروع الغاز غير التقليدي؛ سيغير قواعد اللعبة بجعل الشركة لاعباً عالمياً في الغاز الأزرق والهيدروجين."),
    ("التقييم الحالي", "18.8x (P/E)", "مكرر الربحية؛ يعكس السعر الذي يدفعه المستثمر لكل ريال ربح، ويعتبر عادلاً بالنظر إلى علاوة الأمان في السهم."),
    ("قرار مبدئي", "شراء استراتيجي", "توصية مبنية على نموذج 'الدخل والنمو'؛ حيث يجمع السهم بين توزيعات نقدية سخية ونمو في مشاريع الطاقة.")
]

# تم تصحيح الخطأ هنا في حلقة التكرار
for row in range(2):
    cols = st.columns(5)
    for i in range(5):
        idx = row * 5 + i
        if idx < len(snap_items):
            title, val, desc = snap_items[idx]
            with cols[i]:
                st.markdown(f"<div class='snap-card'><div class='snap-title'>{title}</div><div class='snap-value'>{val}</div><div class='snap-desc'>{desc}</div></div>", unsafe_allow_html=True)

# --- 2. تحليل الأداء وتفكيك الإيرادات ---
st.markdown("<div class='section-title'>2. تحليل الأداء (عزو الأرباح - Profit Attribution)</div>", unsafe_allow_html=True)
c2_left, c2_right = st.columns(2)
with c2_left:
    fig = go.Figure(data=[go.Bar(x=['2024', '2025'], y=[393, 348], marker_color='#2b6cb0', text=['393B', '348B'], textposition='auto')])
    fig.update_layout(title="تراجع الربح المحاسبي (مليار ريال)", height=400)
    st.plotly_chart(fig, use_container_width=True)
with c2_right:
    st.markdown("### 📝 لماذا تراجع الربح بـ 11%؟\n- **عامل السعر:** انخفاض أسعار البيع بنسبة 14%.\n- **مبيعات الكيميائيات:** ضعف الطلب العالمي ضغط على أداء سابيك.\n- **الأداء التشغيلي (EBIT):** تراجع لـ 199B$ بسبب ظروف السوق.")

# --- 4. المقارنة المحلية ---
st.markdown("<div class='section-title'>4. المقارنة مع قطاع الطاقة والخدمات المحلي</div>", unsafe_allow_html=True)
comp_df = pd.DataFrame({"المعيار": ["صافي الربح", "ROACE", "المديونية", "عائد التوزيعات"], "أرامكو (2222)": ["348B ريال", "19.8%", "3.8%", "4.9%"], "أديس (2382)": ["760M ريال", "11.2%", "مرتفعة", "2.8%"], "الدريس (4200)": ["421.8M ريال", "16.4%", "متوسطة", "1.26%"]})
st.table(comp_df.set_index("المعيار"))

# --- 5 & 6. السيناريوهات ---
st.markdown("<div class='section-title'>5 & 6. استشراف المستقبل وتحليل الحساسية</div>", unsafe_allow_html=True)
sc1, sc2, sc3 = st.columns(3)
with sc1: st.markdown("<div class='scenario-card' style='background-color:#2f855a;'><h3>📈 المتفائل</h3><p>نفط 90$ | سعر عادل: 32-35 ريال</p></div>", unsafe_allow_html=True)
with sc2: st.markdown("<div class='scenario-card' style='background-color:#2b6cb0;'><h3>⚖️ الأساسي</h3><p>نفط 75-80$ | سعر عادل: 27-29 ريال</p></div>", unsafe_allow_html=True)
with sc3: st.markdown("<div class='scenario-card' style='background-color:#c53030;'><h3>📉 التشاؤمي</h3><p>نفط < 65$ | سعر عادل: 22-24 ريال</p></div>", unsafe_allow_html=True)

# --- 7. التوصية النهائية ---
st.markdown("<div class='section-title'>7. استراتيجية مدير المحفظة (CFA3 Strategy)</div>", unsafe_allow_html=True)
rec_l, rec_r = st.columns(2)
with rec_l: st.success("🎯 **خطة التجميع:** شراء تدريجي بين **25-27 ريال** للاستفادة من التوزيعات والنمو القادم.")
with rec_r: st.error("🛑 **إدارة المخاطر:** وقف الخسارة عند كسر **23 ريال** مع تدهور أساسيات سوق النفط.")
