import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# --- 1. إعدادات التصميم المتطور (UI/UX) ---
st.set_page_config(page_title="Snapshot-Tasi Pro | CFA Analysis", layout="wide")

def apply_ultra_style():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    html, body, [class*="css"] { font-family: 'Noto Kufi Arabic', sans-serif; text-align: right; direction: rtl; }
    .main { background-color: #f8fafc; }
    
    /* تصميم البطاقة الذكية */
    .card {
        background: white; padding: 20px; border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05); border-right: 6px solid #1e3a8a;
        margin-bottom: 20px; min-height: 180px;
    }
    .card-title { color: #1e3a8a; font-weight: bold; font-size: 18px; margin-bottom: 10px; }
    .card-value { color: #10b981; font-size: 20px; font-weight: bold; }
    .card-desc { color: #64748b; font-size: 13px; line-height: 1.5; margin-top: 10px; }
    
    .section-header {
        background: linear-gradient(90deg, #1e3a8a, #3b82f6);
        color: white; padding: 15px 25px; border-radius: 10px;
        margin: 40px 0 20px 0; font-size: 22px; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

apply_ultra_style()

# --- 2. محرك البيانات الحقيقي ---
@st.cache_data(ttl=3600)
def get_data(symbol):
    ticker = f"{symbol}.SR"
    stock = yf.Ticker(ticker)
    return stock.info, stock.quarterly_financials, stock.quarterly_cashflow

# --- 3. واجهة التحكم والمدخلات ---
st.sidebar.title("🛡️ Snapshot-Tasi Pro")
symbol = st.sidebar.text_input("أدخل رمز الشركة (مثال: 2222):", "2222")

try:
    info, fin, cash = get_data(symbol)
    st.title(f"التحليل الاستثماري المعمق: {info.get('longName')}")

    # --- 1. الـ Snapshot (10 نقاط منظمة ومطورة جرافيكياً) ---
    st.markdown("<div class='section-header'>1. الـ Snapshot (10 نقاط تحليلية محورية)</div>", unsafe_allow_html=True)
    
    # تعريف النقاط العشر مع قيمها وشروحاتها
    snapshot_items = [
        ("نموذج العمل", info.get('industry', 'Data Required'), "تحليل كيفية خلق القيمة؛ هل تعتمد الشركة على الأصول الثقيلة أم التكنولوجيا؟"),
        ("مصدر الإيرادات", info.get('sector', 'Data Required'), "تحديد القطاع المشغل؛ لفهم مدى الحساسية للدورات الاقتصادية."),
        ("الهوامش الربحية", f"{info.get('profitMargins', 0)*100:.1f}%", "هامش صافي الربح؛ يقيس قدرة الإدارة على التحكم في التكاليف التشغيلية."),
        ("مستوى الدين", f"{info.get('debtToEquity', 0):.2f} (D/E)", "نسبة الرافعة المالية؛ تشير إلى قدرة الشركة على الوفاء بالالتزامات طويلة الأجل."),
        ("التدفقات النقدية", f"{info.get('freeCashflow', 0)/1e9:.1f}B", "التدفق النقدي الحر (FCF)؛ الوقود الحقيقي للتوزيعات والنمو المستقبلي."),
        ("جودة الأرباح", "نقدية" if (cash.loc['Operating Cash Flow'].iloc > fin.loc['Net Income'].iloc) else "محاسبية", "مقارنة الربح الدفتري بالسيولة الداخلة فعلياً (مؤشر CFA الحرج)."),
        ("المخاطر الرئيسية", "سوقية/تشغيلية", "تحديد العوامل التي قد تؤدي إلى تآكل الهوامش (مثل أسعار الفائدة أو اللقيم)."),
        ("المحفزات المتوقعة", "نمو مستقبلي", "أحداث مرتقبة (توسعات، اندماج، فتح أسواق) قد تعيد تقييم السهم."),
        ("التقييم الحالي", f"{info.get('trailingPE', 0):.1f}x P/E", "مقارنة السعر بالأرباح؛ هل يتداول السهم بخصم أم علاوة مقارنة بتاريخه؟"),
        ("قرار مبدئي", "مراقبة / تجميع", "رؤية استثمارية أولية بناءً على العائد المتوقع مقابل المخاطرة.")
    ]

    # عرض النقاط في شبكة (Grid) 5x2
    for row_idx in :
        cols = st.columns(5)
        for col_idx in range(5):
            item_idx = row_idx * 5 + col_idx
            title, val, desc = snapshot_items
            with cols[col_idx]:
                st.markdown(f"""
                <div class='card'>
                    <div class='card-title'>{title}</div>
                    <div class='card-value'>{val}</div>
                    <div class='card-desc'>{desc}</div>
                </div>
                """, unsafe_allow_html=True)

    # --- 2. تحليل آخر 12 ربعاً (أسباب رقمية وشرح) ---
    st.markdown("<div class='section-header'>2. تحليل الـ 12 ربعاً الماضية (أين التغيير؟)</div>", unsafe_allow_html=True)
    c2_1, c2_2 = st.columns([2, 1])
    with c2_1:
        rev = fin.loc['Total Revenue'].iloc[:12][::-1]
        fig = px.line(rev, markers=True, title="مسار الإيرادات الربعية", color_discrete_sequence=['#1e3a8a'])
        st.plotly_chart(fig, use_container_width=True)
    with c2_2:
        st.markdown("""
        **لماذا تغير الربح؟ (تحليل CFA):**
        1. **مزيج المنتجات:** تحول نحو المنتجات ذات الهوامش الأعلى.
        2. **كفاءة السعر:** القدرة على تمرير التكاليف للمستهلك النهائي.
        3. **توسع النطاق:** انخفاض التكلفة الثابتة للوحدة مع زيادة الإنتاج.
        """)

    # --- 4. مقارنة المنافسين (السوق السعودي) ---
    st.markdown("<div class='section-header'>4. المقارنة مع المنافسين (القطاع المحلي)</div>", unsafe_allow_html=True)
    st.markdown("<div style='background:white; padding:20px; border-radius:10px;'>تحليل ROE و ROIC يوضح جودة استخدام رأس المال مقارنة بالمنافسين المباشرين في تداول.</div>", unsafe_allow_html=True)
    
    # بيانات مقارنة افتراضية (يمكنك ربطها بـ Ticker آخر)
    comp_data = pd.DataFrame({
        "المعيار": ["ROE (%)", "P/E Ratio", "Net Debt/EBITDA", "Asset Turnover"],
        "الشركة الحالية": [f"{info.get('returnOnEquity', 0)*100:.1f}", info.get('trailingPE'), "0.05x", "0.62"],
        "المنافس 1": ["18.2", "14.5", "0.18x", "0.55"],
        "المنافس 2": ["15.5", "12.2", "0.25x", "0.48"]
    })
    st.table(comp_data)

    # --- 7. توصية مدير المحفظة (CFA3 Strategy) ---
    st.markdown("<div class='section-header'>7. توصية مدير المحفظة الاستثمارية</div>", unsafe_allow_html=True)
    t1, t2 = st.columns(2)
    with t1:
        st.success("**استراتيجية التجميع:** الشراء التدريجي عند مستويات الدعم الفني بناءً على مكررات ربحية عادلة.")
        st.info("**محفزات زيادة المركز:** إعلان نتائج ربعية تتجاوز توقعات المحللين بنسبة >5%.")
    with t2:
        st.error("**مناطق إلغاء الفكرة:** كسر مستويات وقف الخسارة أو تدهور هوامش الربح التشغيلية.")
        st.warning("**محفزات الخروج:** وصول التقييم لمستويات مبالغ فيها (P/E > 25x) مع تباطؤ النمو.")

except Exception as e:
    st.error(f"خطأ: يرجى التأكد من الرمز. تفاصيل: {e}")
