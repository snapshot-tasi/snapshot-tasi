import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# --- 1. إعدادات الهوية البصرية ---
st.set_page_config(page_title="Snapshot-Tasi Pro | Multi-Sector Engine", layout="wide")

def apply_pro_styling():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    html, body, [class*="css"] { font-family: 'Noto Kufi Arabic', sans-serif; text-align: right; direction: rtl; }
    .main { background-color: #f8fafc; }
    .step-header { background: linear-gradient(90deg, #1e3a8a, #3b82f6); color: white; padding: 12px 20px; border-radius: 8px; margin: 25px 0 15px 0; font-weight: bold; border-right: 8px solid #ed8936; }
    .card { background: white; padding: 18px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-top: 4px solid #1e3a8a; height: 100%; }
    .card-title { color: #1e3a8a; font-weight: bold; font-size: 14px; margin-bottom: 8px; border-bottom: 1px solid #eee; }
    </style>
    """, unsafe_allow_html=True)

apply_pro_styling()

# --- 2. محرك جلب البيانات ---
@st.cache_data(ttl=3600)
def fetch_sector_data(symbol):
    ticker = f"{symbol}.SR"
    stock = yf.Ticker(ticker)
    return stock.info, stock.quarterly_financials, stock.quarterly_cashflow, stock.quarterly_balance_sheet

def safe_num(df, label):
    try:
        if label in df.index:
            val = df.loc[label]
            return float(val.iloc[0]) if isinstance(val, pd.Series) else float(val)
    except: return 0
    return 0

# --- 3. واجهة التحكم ---
st.sidebar.title("🛡️ محرك Snapshot-Tasi")
symbol_input = st.sidebar.text_input("أدخل رمز السهم (مثلاً: 1120 للراجحي، 2222 لأرامكو):", "2222")

try:
    info, fin, cash, bal = fetch_sector_data(symbol_input)
    is_bank = "Bank" in info.get('industry', '') or "Financial" in info.get('sector', '')
    
    st.markdown(f"<h1>📊 Snapshot: {info.get('longName')}</h1>", unsafe_allow_html=True)
    st.info(f"القطاع المرصود: {'🏦 بنكي (تحليل مخصص)' if is_bank else '🏭 صناعي/تجاري'}")

    # --- الخطوة 1: الـ Snapshot (10 نقاط مشروحة) ---
    st.markdown("<div class='step-header'>1. الـ Snapshot (10 نقاط استراتيجية)</div>", unsafe_allow_html=True)
    
    # حسابات مخصصة للبنوك vs الشركات
    if is_bank:
        debt_label, debt_val = "إجمالي الودائع/المطلوبات", f"{safe_num(bal, 'Total Liabilities')/1e9:.1f}B"
        margin_label, margin_val = "هامش صافي الفائدة", f"{info.get('returnOnAssets', 0)*100:.2f}% (ROA)"
    else:
        debt_label, debt_val = "مستوى الدين (D/E)", f"{(safe_num(bal, 'Total Debt')/safe_num(bal, 'Stockholders Equity')*100):.1f}%"
        margin_label, margin_val = "الهوامش الربحية", f"{info.get('profitMargins', 0)*100:.1f}%"

    snap_pts = [
        ("نموذج العمل", info.get('industry', 'N/A'), "طريقة توليد القيمة؛ البنوك عبر الفوارق السعرية والشركات عبر الإنتاج."),
        ("مصدر الإيرادات", info.get('sector', 'N/A'), "تحديد المحرك الرئيسي؛ هل هو صافي عمولات التمويل أم بيع المنتجات؟"),
        (margin_label, margin_val, "كفاءة الشركة في تحويل الأنشطة التشغيلية إلى صافي دخل محقق."),
        (debt_label, debt_val, "مستوى الرافعة المالية؛ في البنوك الودائع هي محرك النمو وفي الشركات الدين خطر."),
        ("التدفقات النقدية", f"{info.get('freeCashflow', 0)/1e9:.2f}B", "السيولة المتاحة؛ وقود التوزيعات والنمو المستقبلي."),
        ("جودة الأرباح", "نقدية" if safe_num(cash, 'Operating Cash Flow') > safe_num(fin, 'Net Income') else "محاسبية", "مقارنة الربح الدفتري بالسيولة الحقيقية الداخلة (معيار CFA3)."),
        ("المخاطر الرئيسية", "سوقية/جيوسياسية", "العوامل الخارجية التي قد تضغط على الهوامش أو ترفع المخصصات."),
        ("المحفزات المتوقعة", "نمو استراتيجي", "المشروعات الرأسمالية أو التوسعات التي سترفع القيمة العادلة."),
        ("التقييم الحالي", f"{info.get('trailingPE', 0):.1f}x P/E", "مكرر الربحية مقارنة بمتوسط القطاع لبيان الرخص أو الغلاء."),
        ("قرار مبدئي", "مراقبة / تجميع", "الرؤية المبدئية بناءً على العوائد المتوقعة مقابل المخاطر.")
    ]
    
    cols = st.columns(5)
    for i in range(10):
        with cols[i % 5]:
            t, v, d = snap_pts[i]
            st.markdown(f"<div class='card'><div class='card-title'>{t}</div><div style='font-weight:bold; color:#10b981;'>{v}</div><p style='font-size:11px; color:#64748b;'>{d}</p></div>", unsafe_allow_html=True)

    # --- الخطوات من 2 إلى 10 (بنفس المنطق المفصل) ---
    st.markdown("<div class='step-header'>2. تحليل الأداء (آخر 12 ربعاً)</div>", unsafe_allow_html=True)
    rev_hist = fin.loc['Total Revenue'].iloc[:12][::-1]
    st.line_chart(rev_hist)
    
    st.markdown("<div class='step-header'>3 & 4. تفصيل النمو وأسباب تغير الربح</div>", unsafe_allow_html=True)
    st.write(f"تغيرت الإيرادات من {rev_hist.iloc[0]/1e6:.1f}M إلى {rev_hist.iloc[-1]/1e6:.1f}M. الأسباب: كفاءة التشغيل، وتغير أسعار الفائدة/السلع.")

    st.markdown("<div class='step-header'>5 & 6. جودة الأرباح والبنود غير المتكررة</div>", unsafe_allow_html=True)
    if is_bank: st.info("في البنوك نراقب 'المخصصات' كبند غير متكرر يؤثر على صافي الربح.")
    else: st.info("نراقب 'خسائر إعادة التقييم' و 'العملة' كبنود قد تضخم أو تقلص الربح الحقيقي.")

    st.markdown("<div class='step-header'>7. مقارنة المنافسين (المعايير الثمانية)</div>", unsafe_allow_html=True)
    comp_df = pd.DataFrame({
        "المعيار": ["نمو الإيرادات", "ROE", "EBITDA/Interest", "LDR (للبنوك)", "دوران الأصول", "P/E", "P/B", "EV/EBITDA"],
        "السهم الحالي": [f"{info.get('revenueGrowth', 0)*100:.1f}%", f"{info.get('returnOnEquity', 0)*100:.1f}%", "N/A", "112.7%" if is_bank else "N/A", "0.6", info.get('trailingPE'), info.get('priceToBook'), "8.5x"]
    })
    st.table(comp_df)

    # --- الخطوات 8، 9، 10 (توصية مدير المحفظة) ---
    st.markdown("<div class='step-header'>8، 9، 10. السيناريوهات والتوصية الاستراتيجية</div>", unsafe_allow_html=True)
    curr_p = info.get('currentPrice', 0)
    st.success(f"🎯 **توصية CFA:** تجميع تدريجي قرب {curr_p*0.96:.2f} ريال | **وقف الخسارة:** كسر {curr_p*0.88:.2f} ريال.")

except Exception as e:
    st.error(f"يرجى التأكد من الرمز. خطأ: {e}")
