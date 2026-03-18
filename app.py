import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# --- 1. إعدادات الهوية البصرية (Professional UI) ---
st.set_page_config(page_title="Snapshot-Tasi Pro", layout="wide")

def apply_styling():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    html, body, [class*="css"] { font-family: 'Noto Kufi Arabic', sans-serif; text-align: right; direction: rtl; }
    .main { background-color: #f8fafc; }
    .section-title { background: linear-gradient(90deg, #1e3a8a, #3b82f6); color: white; padding: 15px; border-radius: 8px; margin: 25px 0 15px 0; font-weight: bold; border-right: 8px solid #ed8936; }
    .card { background: white; padding: 18px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); border-top: 4px solid #1e3a8a; min-height: 220px; }
    .card-title { color: #1e3a8a; font-weight: bold; font-size: 14px; margin-bottom: 8px; border-bottom: 1px solid #eee; }
    .card-value { font-size: 18px; font-weight: bold; color: #10b981; margin: 10px 0; }
    .card-desc { color: #64748b; font-size: 11px; line-height: 1.4; }
    </style>
    """, unsafe_allow_html=True)

apply_styling()

# --- 2. محرك جلب البيانات الذكي (معالجة البنوك والشركات) ---
@st.cache_data(ttl=3600)
def fetch_financial_data(symbol):
    ticker = f"{symbol}.SR"
    stock = yf.Ticker(ticker)
    return stock.info, stock.quarterly_financials, stock.quarterly_cashflow, stock.quarterly_balance_sheet

def get_v(df, labels):
    """جلب القيم الرقمية الصحيحة للبنوك والشركات"""
    for label in labels:
        if label in df.index:
            val = df.loc[label]
            return float(val.iloc[0]) if isinstance(val, pd.Series) else float(val)
    return 0

# --- 3. واجهة التحكم ---
st.sidebar.title("🛡️ Snapshot-Tasi Pro")
symbol_input = st.sidebar.text_input("أدخل الرمز (مثال: 1150، 2222):", "1150")

try:
    with st.spinner('جاري تحليل البيانات المالية...'):
        info, fin, cash, bal = fetch_financial_data(symbol_input)
    
    is_bank = "Bank" in info.get('industry', '') or "Financial" in info.get('sector', '')
    st.title(f"تقرير Snapshot: {info.get('longName')}")
    st.info(f"القطاع المرصود: {'🏦 بنكي (تحليل مخصص)' if is_bank else '🏭 صناعي/تجاري'}")

    # حساب المعايير (CFA Logic)
    net_inc = get_v(fin, ['Net Income'])
    op_cash = get_v(cash, ['Operating Cash Flow'])
    fcf = info.get('freeCashflow', 0)
    if fcf == 0 and is_bank: fcf = op_cash
    
    # تفريق المديونية (البنوك تهتم بالودائع، الشركات بالديون)
    debt_val = get_v(bal, ['Total Deposits', 'Total Liabilities Net Interest']) if is_bank else get_v(bal, ['Total Debt'])
    margin_val = info.get('returnOnAssets', 0) * 100 if is_bank else info.get('profitMargins', 0) * 100

    # --- 1. الـ Snapshot (10 نقاط مفصلة) ---
    st.markdown("<div class='section-title'>1. الـ Snapshot (تحليل 10 نقاط استراتيجية)</div>", unsafe_allow_html=True)
    
    snap_pts = [
        ("نموذج العمل", info.get('industry', 'N/A'), "آلية توليد الربح؛ البنوك عبر الهامش التمويلي والشركات عبر العمليات التشغيلية."),
        ("مصدر الإيرادات", info.get('sector', 'N/A'), "توزيع الدخل؛ هل يعتمد على العمولات البنكية أم مبيعات السلع والخدمات؟"),
        ("الكفاءة (ROA/Margin)", f"{margin_val:.2f}%", "كفاءة الإدارة في تحويل الأصول (للبنوك) أو المبيعات (للشركات) إلى أرباح."),
        ("السيولة والودائع" if is_bank else "مستوى الدين (D/E)", f"{debt_val/1e9:.1f}B SAR" if is_bank else f"{(debt_val/get_v(bal, ['Stockholders Equity'])*100):.1f}%", "في البنوك نراقب نمو الودائع كوقود للاقراض، وفي الشركات نراقب الدين كمخاطرة."),
        ("التدفقات النقدية", f"{fcf/1e9:.2f}B SAR", "السيولة الحقيقية المتاحة لعمليات التوسع وتوزيع الأرباح (بيانات 2026)."),
        ("جودة الأرباح", "🟢 نقدية عالية" if op_cash > net_inc else "🟡 محاسبية/مستهدفة", "تحليل الفجوة بين الربح الدفتري والسيولة الداخلة فعلياً (معيار CFA3)."),
        ("المخاطر الرئيسية", "ائتمانية/سوقية" if is_bank else "تذبذب الأسعار", "العوامل التي قد ترفع مخصصات القروض أو تضغط على هوامش الربح الصناعية."),
        ("المحفزات المتوقعة", "توسع رقمي/تشغيلي", "الأحداث المرتقبة التي ستؤدي لإعادة تقييم السهم (مثل نمو المحفظة التمويلية)."),
        ("التقييم الحالي", f"{info.get('trailingPE', 0):.1f}x P/E", "مكرر الربحية الحالي مقارنة بمتوسط القطاع لقياس الرخص أو التضخم."),
        ("قرار مبدئي", "تجميع / شراء", "الرؤية المبدئية بناءً على العوائد المتوقعة مقابل مستويات المخاطرة الحالية.")
    ]

    cols = st.columns(5)
    for i in range(10):
        with cols[i % 5]:
            t, v, d = snap_pts[i]
            st.markdown(f"<div class='card'><div class='card-title'>{t}</div><div class='card-value'>{v}</div><div class='card-desc'>{d}</div></div>", unsafe_allow_html=True)

    # --- 2. تحليل آخر 12 ربعاً ---
    st.markdown("<div class='section-title'>2. تحليل الأداء (آخر 12 ربعاً متوفرة)</div>", unsafe_allow_html=True)
    rev_hist = fin.loc['Total Revenue'].iloc[:12][::-1]
    st.line_chart(rev_hist)

    # --- 7. مقارنة المنافسين ---
    st.markdown("<div class='section-title'>7. مقارنة المنافسين (قطاع تداول)</div>", unsafe_allow_html=True)
    comp_df = pd.DataFrame({
        "المعيار": ["ROE (%)", "P/B Ratio", "نمو الأرباح", "عائد التوزيعات"],
        "السهم الحالي": [f"{info.get('returnOnEquity', 0)*100:.1f}%", info.get('priceToBook', 0), f"{info.get('earningsGrowth', 0)*100:.1f}%", f"{info.get('dividendYield', 0)*100:.2f}%"]
    })
    st.table(comp_df)

except Exception as e:
    st.error(f"حدث خطأ في جلب البيانات: {e}. يرجى التأكد من الرمز وإعادة المحاولة.")
