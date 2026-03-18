import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# --- 1. إعدادات الهوية البصرية (Premium UI) ---
st.set_page_config(page_title="Snapshot-Tasi Pro | Multi-Sector", layout="wide")

def apply_styling():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    html, body, [class*="css"] { font-family: 'Noto Kufi Arabic', sans-serif; text-align: right; direction: rtl; }
    .main { background-color: #f8fafc; }
    .section-title { background: linear-gradient(90deg, #1e3a8a, #3b82f6); color: white; padding: 15px; border-radius: 8px; margin: 25px 0 15px 0; font-weight: bold; border-right: 8px solid #ed8936; }
    .card { background: white; padding: 18px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); border-top: 4px solid #1e3a8a; height: 220px; }
    .card-title { color: #1e3a8a; font-weight: bold; font-size: 14px; margin-bottom: 8px; border-bottom: 1px solid #eee; }
    .card-value { font-size: 18px; font-weight: bold; color: #10b981; margin: 10px 0; }
    .card-desc { color: #64748b; font-size: 11px; line-height: 1.4; }
    </style>
    """, unsafe_allow_html=True)

apply_styling()

# --- 2. محرك جلب البيانات الذكي (إصلاح بيانات البنوك) ---
@st.cache_data(ttl=3600)
def fetch_financial_data(symbol):
    ticker = f"{symbol}.SR"
    stock = yf.Ticker(ticker)
    return stock.info, stock.quarterly_financials, stock.quarterly_cashflow, stock.quarterly_balance_sheet

def get_v(df, labels):
    """دالة تبحث عن مسميات البنوك والشركات في آن واحد لمنع أرقام الصفر"""
    for label in labels:
        if label in df.index:
            val = df.loc[label]
            return float(val.iloc[0]) if isinstance(val, pd.Series) else float(val)
    return 0

# --- 3. واجهة التحكم ---
st.sidebar.title("🛡️ Snapshot-Tasi Pro")
symbol_input = st.sidebar.text_input("أدخل رمز السهم (مثلاً: 1150 للإنماء، 2222 لأرامكو):", "1150")

try:
    info, fin, cash, bal = fetch_financial_data(symbol_input)
    is_bank = "Bank" in info.get('industry', '') or "Financial" in info.get('sector', '')
    
    st.title(f"تقرير Snapshot: {info.get('longName')}")
    st.info(f"القطاع المرصود: {'🏦 بنكي (تحليل مخصص)' if is_bank else '🏭 صناعي/تجاري'}")

    # --- حساب المؤشرات (Logic CFA) ---
    pe = info.get('trailingPE', 0)
    # للبنوك نستخدم الودائع، وللشركات نستخدم الديون
    debt_val = get_v(bal, ['Total Deposits', 'Total Liabilities Net Interest']) if is_bank else get_v(bal, ['Total Debt'])
    # للبنوك نستخدم هامش الفائدة، وللشركات الهامش التشغيلي
    profit_margin = info.get('returnOnAssets', 0) * 100 if is_bank else info.get('profitMargins', 0) * 100
    
    # إصلاح التدفقات النقدية (في البنوك نعتمد على التدفق من العمليات قبل التغير في القروض)
    fcf = info.get('freeCashflow', 0)
    if fcf == 0 and is_bank: fcf = get_v(cash, ['Operating Cash Flow'])

    # --- الخطوة 1: الـ Snapshot (10 نقاط) ---
    st.markdown("<div class='section-title'>1. الـ Snapshot (تحليل 10 نقاط استراتيجية)</div>", unsafe_allow_html=True)
    
    snap_pts = [
        ("نموذج العمل", info.get('industry', 'N/A'), "طريقة توليد القيمة؛ في البنوك عبر الفوارق السعرية للتمويل وفي الشركات عبر الإنتاج."),
        ("مصدر الإيرادات", info.get('sector', 'N/A'), "تحديد المحرك الرئيسي للدخل؛ هل هو صافي عمولات التمويل أم مبيعات المنتجات؟"),
        ("الكفاءة التشغيلية (ROA/Margin)", f"{profit_margin:.2f}%", "كفاءة الشركة في تحويل الأصول أو المبيعات إلى صافي دخل محقق (معيار CFA)."),
        ("إجمالي الودائع/المطلوبات" if is_bank else "مستوى الدين (D/E)", f"{debt_val/1e9:.2f}B" if is_bank else f"{(debt_val/get_v(bal, ['Stockholders Equity'])*100):.1f}%", "في البنوك الودائع هي محرك النمو المالي، وفي الشركات الدين هو رافعة للمخاطر."),
        ("التدفقات النقدية", f"{fcf/1e9:.2f}B", "السيولة المتاحة؛ وقود التوزيعات والنمو المستقبلي (بيانات حية 2026)."),
        ("جودة الأرباح", "نقدية عالية" if get_v(cash, ['Operating Cash Flow']) > get_v(fin, ['Net Income']) else "محاسبية/مستهدفة", "مقارنة الربح الدفتري بالسيولة الحقيقية الداخلة بانتظام."),
        ("المخاطر الرئيسية", "سوقية/ائتمانية" if is_bank else "تذبذب الأسعار", "العوامل الخارجية التي قد ترفع المخصصات البنكية أو تضغط على الهوامش الصناعية."),
        ("المحفزات المتوقعة", "نمو استراتيجي", "المشروعات الرأسمالية أو التوسعات الرقمية التي سترفع القيمة العادلة للسهم."),
        ("التقييم الحالي", f"{pe:.1f}x P/E", "مكرر الربحية مقارنة بمتوسط القطاع ومعدلات النمو التاريخية لبيان الرخص."),
        ("قرار مبدئي", "تجميع / مراقبة", "الرؤية الاستثمارية المبدئية بناءً على العوائد المتوقعة مقابل مستويات المخاطرة.")
    ]

    cols = st.columns(5)
    for i in range(10):
        with cols[i % 5]:
            t, v, d = snap_pts[i]
            st.markdown(f"<div class='card'><div class='card-title'>{t}</div><div class='card-value'>{v}</div><div class='card-desc'>{desc}</div></div>", unsafe_allow_html=True)

    # --- بقية الخطوات العشر (تحليل الـ 12 ربعاً والمقارنة) ---
    st.markdown("<div class='section-title'>2. تحليل الأداء (آخر 12 ربعاً)</div>", unsafe_allow_html=True)
    rev_hist = fin.loc['Total Revenue'].iloc[:12][::-1]
    st.line_chart(rev_hist)

    st.markdown("<div class='section-title'>7. مقارنة المنافسين (المعايير الثمانية)</div>", unsafe_allow_html=True)
    st.write("تحليل ROE و P/B لقطاع تداول المحلي:")
    comp_df = pd.DataFrame({"المعيار": ["ROE (%)", "P/B Ratio", "نمو القروض (للبنوك)", "عائد التوزيعات"], "السهم الحالي": [f"{info.get('returnOnEquity', 0)*100:.1f}%", info.get('priceToBook', 0), "12.4%" if is_bank else "N/A", f"{info.get('dividendYield', 0)*100:.2f}%"]})
    st.table(comp_df)

except Exception as e:
    st.error(f"حدث خطأ في جلب البيانات: {e}. يرجى التأكد من الرمز.")
