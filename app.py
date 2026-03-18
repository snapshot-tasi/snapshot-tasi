import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# --- 1. إعدادات التصميم المتطور (Custom CSS) ---
st.set_page_config(page_title="Snapshot-Tasi Pro", layout="wide")

def local_css():
    st.markdown("""
    <style>
    /* خلفية التطبيق */
    .main { background-color: #f8f9fa; }
    
    /* تصميم البطاقات (Cards) */
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #007bff;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    
    .snapshot-box {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        font-weight: bold;
        min-height: 100px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
    }
    
    .section-header {
        color: #1e3a8a;
        border-bottom: 2px solid #e5e7eb;
        padding-bottom: 10px;
        margin-top: 30px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

# --- 2. محرك البيانات (Data Engine) ---
# سنفترض هنا أنك ستدخل البيانات يدوياً أو سيتم سحبها تلقائياً
st.title("🛡️ منصة Snapshot-Tasi للتحليل المعمق")
st.sidebar.header("إعدادات التقرير")
company_name = st.sidebar.selectbox("اختر الشركة", ["أرامكو السعودية (2222)", "سابيك (2010)", "الراجحي (1120)"])

# --- القسم 1: الـ Snapshot (10 نقاط في Grid) ---
st.markdown("<h2 class='section-header'>1. الـ Snapshot (العرض السريع)</h2>", unsafe_allow_html=True)

# توزيع الـ 10 نقاط في صفين
row1 = st.columns(5)
row2 = st.columns(5)

snapshot_points = [
    ("نموذج العمل", "متكامل (طاقة وكيميائيات)"),
    ("مصدر الإيرادات", "مبيعات الزيت الخام والغاز"),
    ("الهوامش الربحية", "45% هامش تشغيلي"),
    ("مستوى الدين", "منخفض جداً (Gearing 3.8%)"),
    ("التدفقات النقدية", "85 مليار دولار FCF"),
    ("جودة الأرباح", "عالية (مدعومة نقدياً)"),
    ("المخاطر الرئيسية", "تذبذب الأسعار الجيوسياسي"),
    ("المحفزات", "مشروع الجافورة للغاز"),
    ("التقييم الحالي", "17.3x P/E"),
    ("قرار مبدئي", "شراء / تجميع")
]

for i, (title, val) in enumerate(snapshot_points[:5]):
    with row1[i]:
        st.markdown(f"<div class='snapshot-box'>{title}<br><span style='font-size:12px; font-weight:normal;'>{val}</span></div>", unsafe_allow_html=True)

for i, (title, val) in enumerate(snapshot_points[5:]):
    with row2[i]:
        st.markdown(f"<div class='snapshot-box' style='background: linear-gradient(135deg, #10b981 0%, #059669 100%);'>{title}<br><span style='font-size:12px; font-weight:normal;'>{val}</span></div>", unsafe_allow_html=True)

# --- القسم 2: تحليل آخر 12 ربعاً (جرافيك متطور) ---
st.markdown("<h2 class='section-header'>2. تحليل آخر 12 ربعاً</h2>", unsafe_allow_html=True)
c1, c2 = st.columns([2, 1])

with c1:
    # رسم بياني تفصيلي لنمو الإيرادات (Waterfall أو Grouped Bar)
    quarters = ['Q1-23', 'Q2-23', 'Q3-23', 'Q4-23', 'Q1-24', 'Q2-24', 'Q3-24', 'Q4-24', 'Q1-25', 'Q2-25', 'Q3-25', 'Q4-25']
    revenue = [100, 110, 105, 120, 115, 125, 130, 128, 135, 140, 145, 150]
    fig = px.area(x=quarters, y=revenue, title="مسار الإيرادات التاريخي", markers=True)
    fig.update_traces(line_color='#1e3a8a', fillcolor='rgba(59, 130, 246, 0.2)')
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.info("**تفصيل نمو الإيرادات:**\n* حجم الإنتاج: +2%\n* السعر: -5%\n* العملة: مستقر")
    st.write("**3 أسباب للربحية:**\n1. كفاءة التكاليف\n2. هوامش التكرير\n3. انخفاض مخصصات")

# --- القسم 4: مقارنة المنافسين (جدول ملون) ---
st.markdown("<h2 class='section-header'>4. مقارنة المنافسين</h2>", unsafe_allow_html=True)
comparison_data = pd.DataFrame({
    'المعيار': ['P/E', 'ROE', 'EV/EBITDA', 'Net Debt/EBITDA'],
    'أرامكو': [17.3, '28%', 8.2, '0.04x'],
    'إكسون': [12.5, '18%', 6.5, '0.15x'],
    'شل': [10.2, '14%', 5.1, '0.22x']
})
st.table(comparison_data.style.background_gradient(cmap='Blues', subset=['أرامكو']))

# --- القسم 5: السيناريوهات (تصميم البطاقات الثلاث) ---
st.markdown("<h2 class='section-header'>5. سيناريوهات الـ 12 شهراً القادمة</h2>", unsafe_allow_html=True)
sc1, sc2, sc3 = st.columns(3)

with sc1:
    st.markdown("<div style='border:1px solid #ddd; padding:15px; border-radius:10px;'><h4>📈 السيناريو المتفائل</h4><p>نمو الإيرادات: 10%<br>السعر العادل: 34 ريال</p></div>", unsafe_allow_html=True)
with sc2:
    st.markdown("<div style='border:1px solid #3b82f6; padding:15px; border-radius:10px; background-color:#f0f7ff;'><h4>⚖️ السيناريو الأساسي</h4><p>نمو الإيرادات: 2%<br>السعر العادل: 30 ريال</p></div>", unsafe_allow_html=True)
with sc3:
    st.markdown("<div style='border:1px solid #ef4444; padding:15px; border-radius:10px;'><h4>📉 السيناريو التشاؤمي</h4><p>نمو الإيرادات: -5%<br>السعر العادل: 26 ريال</p></div>", unsafe_allow_html=True)

# --- القسم 7: توصية مدير المحفظة (CFA3) ---
st.markdown("<h2 class='section-header'>7. توصية مدير المحفظة</h2>", unsafe_allow_html=True)
st.success("""
**استراتيجية الدخول:** تجميع تدريجي (Scale-in) بين مستويات 27-28 ريال.
**مناطق إلغاء الفكرة:** كسر مستوى 25 ريال مع ارتفاع في الرفع المالي.
**محفزات الخروج:** وصول مكرر الربحية إلى 22x أو تراجع حاد في هوامش الكيميائيات.
""")
