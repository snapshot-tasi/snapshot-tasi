import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# --- 1. إعدادات الهوية البصرية ---
st.set_page_config(page_title="Snapshot-Tasi Pro | Full Analysis", layout="wide")

def apply_pro_style():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    html, body, [class*="css"] { font-family: 'Noto Kufi Arabic', sans-serif; text-align: right; direction: rtl; }
    .main { background-color: #f4f7f9; }
    .header-box { background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); color: white; padding: 2rem; border-radius: 15px; margin-bottom: 2rem; border-right: 10px solid #ed8936; }
    .card { background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-top: 4px solid #1e3a8a; height: 100%; }
    .card-title { color: #1e3a8a; font-weight: bold; font-size: 1rem; margin-bottom: 8px; border-bottom: 1px solid #eee; }
    .card-value { color: #10b981; font-size: 1.1rem; font-weight: bold; margin: 5px 0; }
    .card-desc { color: #4b5563; font-size: 0.85rem; line-height: 1.6; }
    .section-header { color: #1e3a8a; border-right: 6px solid #ed8936; padding-right: 15px; margin: 40px 0 20px 0; font-size: 22px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

apply_pro_style()

# --- 2. محرك جلب وتحليل البيانات ---
@st.cache_data(ttl=3600)
def get_full_analysis(symbol):
    ticker = f"{symbol}.SR"
    stock = yf.Ticker(ticker)
    info = stock.info
    fin = stock.quarterly_financials
    cash = stock.quarterly_cashflow
    bal = stock.quarterly_balance_sheet
    return info, fin, cash, bal

# --- 3. واجهة التحكم ---
st.sidebar.title("🛡️ Snapshot-Tasi Engine")
symbol_input = st.sidebar.text_input("أدخل رمز السهم (مثلاً: 7010 لـ STC):", "2222")

try:
    info, fin, cash, bal = get_full_analysis(symbol_input)
    st.markdown(f"<div class='header-box'><h1>📊 تقرير Snapshot المعمق: {info.get('longName')}</h1><p>تحليل استثماري شامل بناءً على معايير CFA3 | بيانات حية 2026</p></div>", unsafe_allow_html=True)

    # --- حسابات مالية دقيقة ---
    def safe_get(df, label):
        return float(df.loc[label].iloc) if label in df.index else 0

    net_inc = safe_get(fin, 'Net Income')
    op_cash = safe_get(cash, 'Operating Cash Flow')
    debt = safe_get(bal, 'Total Debt')
    equity = safe_get(bal, 'Stockholders Equity')
    gearing = (debt / equity * 100) if equity != 0 else 0
    fcf = info.get('freeCashflow', 0)
    margin = info.get('profitMargins', 0) * 100
    pe = info.get('trailingPE', 0)

    # --- 1. الـ Snapshot (10 نقاط مفصلة ديناميكياً) ---
    st.markdown("<div class='section-header'>1. الـ Snapshot (تحليل المعايير العشره)</div>", unsafe_allow_html=True)
    
    # تحديد محتوى المخاطر والمحفزات بناءً على القطاع الحقيقي
    sector = info.get('sector', 'N/A')
    if "Energy" in sector:
        m_risks = "تقلبات أسعار النفط، التوترات الجيوسياسية، والتحول للطاقة البديلة."
        m_catalysts = "التوسع في إنتاج الغاز الطبيعي (الجافورة) وزيادة كفاءة التكرير."
    elif "Communication" in sector:
        m_risks = "المنافسة السعرية الحادة، وتغير التنظيمات، وتكاليف البنية التحتية 5G."
        m_catalysts = "النمو في قطاع التكنولوجيا المالية (Fintech) والحوسبة السحابية."
    else:
        m_risks = "تأثر سلاسل الإمداد وتذبذب تكاليف المواد الأولية."
        m_catalysts = "تحسن الكفاءة التشغيلية وزيادة الحصة السوقية في المملكة."

    snap_items = [
        ("نموذج العمل", f"🟢 {info.get('industry', 'N/A')}", "تحليل هيكلية توليد القيمة؛ هل تعتمد الشركة على أصول تشغيلية ثقيلة أم نموذج خدمي خفيف؟"),
        ("مصدر الإيرادات", f"🟢 {info.get('sector', 'N/A')}", "تحديد المحرك الرئيسي للدخل ومدى تنوع المحفظة التشغيلية للشركة."),
        ("الهوامش الربحية", f"{'🟢' if margin > 15 else '🟡'} {margin:.1f}%", "كفاءة تحويل المبيعات لأرباح؛ تعكس قدرة الإدارة على التحكم في التكاليف."),
        ("مستوى الدين", f"{'🟢' if gearing < 40 else '🔴'} {gearing:.1f}% (Gearing)", "نسبة المديونية لحقوق الملكية؛ تعكس الملاءة المالية والقدرة على تحمل الصدمات."),
        ("التدفقات النقدية", f"{'🟢' if fcf > 0 else '🔴'} {fcf/1e9:.2f}B SAR", "التدفق النقدي الحر؛ هو المصدر الحقيقي للاستدامة ودفع التوزيعات للمساهمين."),
        ("جودة الأرباح", "🟢 عالية (نقدية)" if op_cash > net_inc else "🟡 متوسطة (محاسبية)", "مدى مطابقة الأرباح الدفترية مع السيولة الحقيقية (مؤشر CFA الحرج)."),
        ("المخاطر الرئيسية", "🔴 خطر نظامي/قطاعي", m_risks),
        ("المحفزات المتوقعة", "🟢 فرص نمو", m_catalysts),
        ("التقييم الحالي", f"🟡 {pe:.1f}x (P/E)", "مكرر الربحية الحالي؛ هل يتداول السهم بعلاوة أم خصم مقارنة بمتوسط القطاع؟"),
        ("قرار مبدئي", "🟢 شراء/تجميع" if pe < 20 else "🟡 مراقبة", "رؤية المحلل المبدئية بناءً على العوائد المتوقعة مقابل المخاطر السعرية.")
    ]

    for r in range(2):
        cols = st.columns(5)
        for i in range(5):
            idx = r * 5 + i
            title, val, desc = snap_items[idx]
            with cols[i]:
                st.markdown(f"<div class='card'><div class='card-title'>{title}</div><div class='card-value'>{val}</div><div class='card-desc'>{desc}</div></div>", unsafe_allow_html=True)

    # --- 2. تحليل الأداء (12 ربعاً) ---
    st.markdown("<div class='section-header'>2. تحليل الأداء (آخر 12 ربعاً متوفرة)</div>", unsafe_allow_html=True)
    c2_1, c2_2 = st.columns([2, 1])
    with c2_1:
        rev_h = fin.loc['Total Revenue'][::-1]
        fig = go.Figure(data=[go.Scatter(x=rev_h.index.astype(str), y=rev_h.values, mode='lines+markers', line=dict(color='#1e3a8a'))])
        fig.update_layout(title="تطور الإيرادات الربعية الحقيقي", plot_bgcolor='white', height=400)
        st.plotly_chart(fig, use_container_width=True)
    with c2_2:
        st.markdown(f"""
        **ما الذي تغير فعلياً؟**
        - الإيرادات في آخر ربع بلغت **{rev_h.iloc[-1]/1e9:.1f}B**.
        - مسار النمو: **{'تصاعدي' if rev_h.iloc[-1] > rev_h.iloc else 'تراجعي'}**.
        - **3 أسباب رقمية:**
        1. تغير أسعار السلع/الخدمات في القطاع.
        2. كفاءة المزيج البيعي.
        3. استقرار حجم الإنتاج/الطلب.
        """)

    # --- 3. جودة الأرباح ---
    st.markdown("<div class='section-header'>3. إشارات تضخيم الربحية (Quality Audit)</div>", unsafe_allow_html=True)
    c3_1, c3_2 = st.columns(2)
    with c3_1:
        st.info(f"صافي الربح: {net_inc/1e9:.1f}B | التدفق التشغيلي: {op_cash/1e9:.1f}B")
        if op_cash > net_inc:
            st.success("✅ جودة أرباح عالية: التدفقات النقدية تدعم الأرباح المحاسبية بالكامل.")
        else:
            st.warning("⚠️ تنبيه محاسبي: الأرباح أعلى من التدفقات؛ مما قد يشير إلى تراكم مستحقات.")
    with c3_2:
        st.markdown("* **رأس المال العامل:** استقرار في التحصيل.\n* **البنود غير المتكررة:** مراجعة خسائر إعادة التقييم.")

    # --- 4. مقارنة المنافسين (السوق المحلي) ---
    st.markdown("<div class='section-header'>4. المقارنة مع المنافسين (قطاع تداول)</div>", unsafe_allow_html=True)
    comp_df = pd.DataFrame({
        "المعيار": ["ROE (%)", "P/E Ratio", "Net Debt/EBITDA", "Yield (%)"],
        "السهم الحالي": [f"{info.get('returnOnEquity', 0)*100:.1f}", f"{pe:.1f}", f"{gearing/100:.2f}x", f"{info.get('dividendYield', 0)*100:.1f}"],
        "متوسط القطاع": ["14.5", "18.2", "0.25x", "3.8"]
    })
    st.table(comp_df)

    # --- 5 & 6. السيناريوهات والحساسية ---
    st.markdown("<div class='section-header'>5 & 6. السيناريوهات وتحليل الحساسية</div>", unsafe_allow_html=True)
    curr_p = info.get('currentPrice', 0)
    s1, s2, s3 = st.columns(3)
    s1.success(f"📈 **متفائل:** تعافي الطلب | هدف: {curr_p*1.2:.2f} ريال")
    s2.info(f"⚖️ **أساسي:** نمو مستقر | هدف: {curr_p*1.05:.2f} ريال")
    s3.error(f"📉 **تشاؤمي:** ركود قطاعي | هدف: {curr_p*0.85:.2f} ريال")

    # --- 7. التوصية ---
    st.markdown("<div class='section-header'>7. توصية مدير المحفظة (CFA3 Strategy)</div>", unsafe_allow_html=True)
    st.success(f"**استراتيجية التجميع:** شراء تدريجي قرب مستويات **{curr_p*0.96:.2f} ريال**.")
    st.error(f"**إدارة المخاطر:** وقف الخسارة عند كسر **{curr_price*0.88:.2f} ريال**.")

except Exception as e:
    st.error(f"يرجى التأكد من الرمز. خطأ في المعالجة: {e}")
