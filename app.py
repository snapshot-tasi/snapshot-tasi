import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# --- 1. إعدادات الهوية البصرية (CFA Premium UI) ---
st.set_page_config(page_title="Snapshot-Tasi Engine Pro", layout="wide")

def apply_pro_style():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    html, body, [class*="css"] { font-family: 'Noto Kufi Arabic', sans-serif; text-align: right; direction: rtl; }
    .main { background-color: #f4f7f9; }
    .header-box { background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); color: white; padding: 2rem; border-radius: 15px; margin-bottom: 2rem; border-right: 10px solid #ed8936; box-shadow: 0 10px 20px rgba(0,0,0,0.1); }
    .card { background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-top: 5px solid #1e3a8a; height: 100%; transition: 0.3s; }
    .card:hover { transform: translateY(-5px); box-shadow: 0 12px 20px rgba(0,0,0,0.1); }
    .card-title { color: #1e3a8a; font-weight: bold; font-size: 1rem; margin-bottom: 8px; border-bottom: 1px solid #eee; }
    .card-value { font-size: 1.1rem; font-weight: bold; margin: 8px 0; }
    .card-desc { color: #4b5563; font-size: 0.82rem; line-height: 1.6; }
    .pos { color: #10b981; } .neu { color: #f59e0b; } .neg { color: #ef4444; }
    .section-header { color: #1e3a8a; border-right: 6px solid #ed8936; padding-right: 15px; margin: 40px 0 20px 0; font-size: 22px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

apply_pro_style()

# --- 2. محرك جلب البيانات الذكي (Data Extraction Fix) ---
@st.cache_data(ttl=3600)
def fetch_full_data(symbol):
    ticker = f"{symbol}.SR"
    stock = yf.Ticker(ticker)
    return stock.info, stock.quarterly_financials, stock.quarterly_cashflow, stock.quarterly_balance_sheet

# دالة لاستخراج الرقم الأول بأمان لمنع خطأ الـ Indexing
def safe_num(df, label):
    try:
        if label in df.index:
            val = df.loc[label]
            # إذا كان الناتج سلسلة (Series)، خذ العنصر الأول
            if isinstance(val, pd.Series): return float(val.iloc)
            return float(val)
    except: return 0
    return 0

# --- 3. واجهة التحكم ---
st.sidebar.title("🛡️ Snapshot-Tasi Engine")
symbol_input = st.sidebar.text_input("أدخل رمز السهم (مثلاً: 2222 أو 7010):", "2222")

try:
    with st.spinner('جاري جلب أحدث البيانات المالية وتدقيقها...'):
        info, fin, cash, bal = fetch_full_data(symbol_input)
    
    st.markdown(f"<div class='header-box'><h1>📊 تقرير Snapshot المعمق: {info.get('longName')}</h1><p>تحليل استثماري شامل بناءً على معايير CFA3 | بيانات حية 18 مارس 2026</p></div>", unsafe_allow_html=True)

    # --- حسابات CFA الديناميكية ---
    net_inc = safe_num(fin, 'Net Income')
    op_cash = safe_num(cash, 'Operating Cash Flow')
    debt = safe_num(bal, 'Total Debt')
    equity = safe_num(bal, 'Stockholders Equity')
    gearing = (debt / equity * 100) if equity != 0 else 0
    fcf = info.get('freeCashflow', 0)
    margin = info.get('profitMargins', 0) * 100
    pe = info.get('trailingPE', 0)

    # --- 1. الـ Snapshot (تحليل الـ 10 نقاط المفصلة) ---
    st.markdown("<div class='section-header'>1. الـ Snapshot (تحليل المعايير العشره)</div>", unsafe_allow_html=True)
    
    # منطق المحفزات والمخاطر حسب القطاع
    sector = info.get('sector', 'N/A')
    m_risks = "تقلبات أسعار السلع الأساسية والتوترات الجيوسياسية." if "Energy" in sector else "المنافسة السعرية وتغير الأنظمة التقنية."
    m_catalysts = "التوسع في مشاريع الغاز والهيدروجين." if "Energy" in sector else "نمو قطاع البيانات والخدمات الرقمية."

    snap_items = [
        ("نموذج العمل", f"🟢 {info.get('industry', 'N/A')}", "طريقة توليد القيمة؛ هل تعتمد الشركة على أصول تشغيلية ثقيلة أم نموذج خدمي خفيف؟"),
        ("مصدر الإيرادات", f"🟢 {info.get('sector', 'N/A')}", "تحديد المحرك الرئيسي للدخل ومدى تنوع المحفظة التشغيلية لضمان الاستدامة."),
        ("الهوامش الربحية", f"{'🟢' if margin > 15 else '🟡'} {margin:.1f}%", "كفاءة تحويل المبيعات لأرباح؛ تعكس قدرة الإدارة على التحكم في التكاليف التشغيلية."),
        ("مستوى الدين", f"{'🟢' if gearing < 40 else '🔴'} {gearing:.1f}% (Gearing)", "نسبة المديونية لحقوق الملكية؛ تعكس الملاءة المالية والقدرة على تحمل الهزات."),
        ("التدفقات النقدية", f"{'🟢' if fcf > 0 else '🔴'} {fcf/1e9:.2f}B SAR", "التدفق النقدي الحر؛ هو المصدر الحقيقي للاستدامة ودفع التوزيعات للمساهمين."),
        ("جودة الأرباح", "🟢 عالية" if op_cash > net_inc else "🔴 محاسبية", "مدى مطابقة الأرباح الدفترية مع السيولة الحقيقية (مؤشر CFA الحرج)."),
        ("المخاطر الرئيسية", "🔴 خطر نظامي", m_risks),
        ("المحفزات المتوقعة", "🟢 فرص نمو", m_catalysts),
        ("التقييم الحالي", f"🟡 {pe:.1f}x (P/E)", "مكرر الربحية الحالي؛ هل يتداول السهم بعلاوة أم خصم مقارنة بمتوسط تاريخه؟"),
        ("قرار مبدئي", "🟢 شراء/تجميع" if pe < 20 else "🟡 مراقبة", "رؤية المحلل المبدئية بناءً على العوائد المتوقعة مقابل المخاطر السعرية.")
    ]

    for row_idx in range(2):
        cols = st.columns(5)
        for i in range(5):
            idx = row_idx * 5 + i
            title, val, desc = snap_items[idx]
            val_color = "pos" if "🟢" in val or "عالية" in val else ("neg" if "🔴" in val else "neu")
            with cols[i]:
                st.markdown(f"<div class='card'><div class='card-title'>{title}</div><div class='card-value {val_color}'>{val}</div><div class='card-desc'>{desc}</div></div>", unsafe_allow_html=True)

    # --- 2. تحليل الأداء (12 ربعاً) ---
    st.markdown("<div class='section-header'>2. تحليل الأداء (آخر 12 ربعاً متوفرة)</div>", unsafe_allow_html=True)
    rev_hist = fin.loc['Total Revenue'][::-1]
    fig = go.Figure(data=[go.Scatter(x=rev_hist.index.astype(str), y=rev_hist.values, mode='lines+markers', line=dict(color='#1e3a8a'))])
    fig.update_layout(title="تطور الإيرادات الربعية", height=350, plot_bgcolor='white')
    st.plotly_chart(fig, use_container_width=True)

    # --- 7. التوصية النهائية ---
    st.markdown("<div class='section-header'>7. توصية مدير المحفظة (CFA3 Strategy)</div>", unsafe_allow_html=True)
    curr_p = info.get('currentPrice', 0)
    c1, c2 = st.columns(2)
    c1.success(f"🎯 **استراتيجية التجميع:** شراء تدريجي قرب مستويات **{curr_p*0.96:.2f} ريال**.")
    c2.error(f"🛑 **إدارة المخاطر:** وقف الخسارة عند كسر **{curr_p*0.88:.2f} ريال**.")

except Exception as e:
    st.error(f"يرجى التأكد من الرمز. خطأ في المعالجة: {e}")
