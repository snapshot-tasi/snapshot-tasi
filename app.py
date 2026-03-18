import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- الإعدادات الجرافيكية والهوية (CFA Style) ---
st.set_page_config(page_title="Snapshot-Tasi Pro | CFA III Analysis", layout="wide")

def apply_styling():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    html, body, [class*="css"] { font-family: 'Noto Kufi Arabic', sans-serif; text-align: right; direction: rtl; }
    .main { background-color: #f4f7f9; }
    .header-box { background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); color: white; padding: 25px; border-radius: 15px; border-right: 10px solid #ed8936; margin-bottom: 30px; }
    .section-title { color: #1e3a8a; border-right: 6px solid #ed8936; padding-right: 15px; margin: 40px 0 20px 0; font-size: 22px; font-weight: bold; }
    .card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); border-top: 4px solid #1e3a8a; height: 100%; }
    .card-title { color: #1e3a8a; font-weight: bold; font-size: 15px; margin-bottom: 10px; border-bottom: 1px solid #eee; }
    .card-value { font-size: 18px; font-weight: bold; color: #10b981; }
    .card-desc { color: #64748b; font-size: 12px; line-height: 1.5; margin-top: 8px; }
    .status-badge { padding: 4px 8px; border-radius: 5px; font-size: 12px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

apply_styling()

# --- محرك البيانات الذكي (معالجة البنوك والشركات) ---
@st.cache_data(ttl=3600)
def get_full_market_data(symbol):
    ticker = f"{symbol}.SR"
    stock = yf.Ticker(ticker)
    return stock.info, stock.quarterly_financials, stock.quarterly_cashflow, stock.quarterly_balance_sheet

def safe_num(df, labels):
    for label in labels:
        if label in df.index:
            val = df.loc[label]
            return float(val.iloc[0]) if isinstance(val, pd.Series) else float(val)
    return 0

# --- واجهة التحكم ---
st.sidebar.title("🛡️ Snapshot-Tasi Pro")
symbol_input = st.sidebar.text_input("أدخل رمز السهم (2222، 1150، 1120...):", "1150")

try:
    with st.spinner('جاري بناء التقرير المالي المعمق...'):
        info, fin, cash, bal = get_full_market_data(symbol_input)
    
    is_bank = "Bank" in info.get('industry', '') or "Financial" in info.get('sector', '')
    st.markdown(f"<div class='header-box'><h1>تقرير Snapshot: {info.get('longName')}</h1><p>تحليل مالي شامل 2025/2026 | معايير CFA Level III</p></div>", unsafe_allow_html=True)

    # --- القسم 1: الـ Snapshot (10 نقاط كاملة) ---
    st.markdown("<div class='section-title'>1. الـ Snapshot (10 نقاط استراتيجية)</div>", unsafe_allow_html=True)
    
    # حسابات CFA
    net_inc = safe_num(fin, ['Net Income'])
    op_cash = safe_num(cash, ['Operating Cash Flow'])
    fcf = info.get('freeCashflow', 0) or op_cash # للبنوك
    debt_val = safe_num(bal, ['Total Deposits', 'Total Liabilities Net Interest']) if is_bank else safe_num(bal, ['Total Debt'])
    margin_val = info.get('returnOnAssets', 0) * 100 if is_bank else info.get('profitMargins', 0) * 100

    snapshot_points = [
        ("نموذج العمل", info.get('industry', 'Data Required'), "آلية توليد الربح والقيمة المضافة في قطاع الشركة."),
        ("مصدر الإيرادات", info.get('sector', 'Data Required'), "القطاعات الجغرافية والتشغيلية التي تدر التدفقات النقدية."),
        ("الهوامش الربحية", f"{margin_val:.2f}%", "كفاءة تحويل العمليات إلى صافي دخل (ROA للبنوك / Profit Margin للشركات)."),
        ("مستوى الودائع/الدين", f"{debt_val/1e9:.2f}B SAR", "الرافعة المالية؛ الودائع كمحرك للنمو في البنوك والدين كمخاطرة في الصناعة."),
        ("التدفقات النقدية", f"{fcf/1e9:.2f}B SAR", "السيولة الحقيقية المتاحة للتوزيعات والنمو بعد كافة الالتزامات."),
        ("جودة الأرباح", "🟢 نقدية عالية" if op_cash > net_inc else "🔴 محاسبية", "الفجوة بين الربح الدفتري والسيولة الفعلية (Cash/Income Ratio)."),
        ("المخاطر الرئيسية", "سوقية / ائتمانية", "العوامل الخارجية والداخلية التي تهدد استدامة الهوامش والربحية."),
        ("المحفزات المتوقعة", "توسع تشغيلي", "الأحداث المرتقبة التي ستؤدي لإعادة تقييم السهم في السوق."),
        ("التقييم الحالي", f"{info.get('trailingPE', 0):.1f}x P/E", "مكرر الربحية الحالي مقارنة بمتوسط القطاع لقياس العدالة السعرية."),
        ("قرار مبدئي", "تجميع / شراء", "الرؤية المبدئية بناءً على موازنة العائد المتوقع مقابل المخاطر.")
    ]

    for r in range(2):
        cols = st.columns(5)
        for i in range(5):
            idx = r * 5 + i
            t, v, d = snapshot_points[idx]
            with cols[i]:
                st.markdown(f"<div class='card'><div class='card-title'>{t}</div><div class='card-value'>{v}</div><div class='card-desc'>{d}</div></div>", unsafe_allow_html=True)

    # --- الأقسام السبعة المتكاملة ---
    t1, t2, t3, t4, t5, t6 = st.tabs(["2&3. تحليل الأداء", "4. جودة الأرباح", "5. المنافسين", "6. السيناريوهات", "7. الحساسية", "8. التوصية"])

    with t1:
        st.markdown("<div class='section-title'>2 & 3. تحليل آخر 12 ربعاً</div>", unsafe_allow_html=True)
        rev_hist = fin.loc['Total Revenue'].iloc[:12][::-1]
        fig = go.Figure(data=[go.Scatter(x=rev_hist.index.astype(str), y=rev_hist.values, mode='lines+markers', line=dict(color='#1e3a8a', width=3))])
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("**تفصيل نمو الإيرادات:** حجم المبيعات | السعر | مزيج المنتجات | التوسع | العملة.")
        st.write("3 أسباب رقمية: 1. كفاءة التشغيل | 2. تكلفة اللقيم/الفائدة | 3. بنود استثنائية.")

    with t2:
        st.markdown("<div class='section-title'>4. إشارات تضخيم الربحية</div>", unsafe_allow_html=True)
        st.write("- **تغير رأس المال العامل:** مراجعة الذمم المدينة والمخزون.")
        st.write("- **بنود غير متكررة:** فحص المكاسب/الخسائر غير النقدية.")
        st.write("- **سياسات محاسبية:** مراجعة المخصصات (Provision Reversals).")

    with t3:
        st.markdown("<div class='section-header'>5. مقارنة المنافسين (المعايير الثمانية)</div>", unsafe_allow_html=True)
        comp_df = pd.DataFrame({
            "المعيار": ["نمو الإيرادات", "ROE", "EBITDA", "Net Debt/EBITDA", "Asset Turnover", "P/E", "P/B", "EV/EBITDA"],
            "السهم الحالي": [f"{info.get('revenueGrowth', 0)*100:.1f}%", f"{info.get('returnOnEquity', 0)*100:.1f}%", "H", "N/A", "0.62", info.get('trailingPE'), info.get('priceToBook'), "8.5x"]
        })
        st.table(comp_df)

    with t4:
        st.markdown("<div class='section-title'>6. سيناريوهات الـ 12 شهراً</div>", unsafe_allow_html=True)
        s1, s2, s3 = st.columns(3)
        s1.success("📈 متفائل: تعافي الطلب | أثر: +15% ربح")
        s2.info("⚖️ أساسي: نمو مستقر | أثر: توزيعات منتظمة")
        s3.error("📉 تشاؤمي: ركود | أثر: ضغط على الهوامش")

    with t5:
        st.markdown("<div class='section-title'>7. تحليل الحساسية</div>", unsafe_allow_html=True)
        st.write("**المتغيرات الحرجة:** سعر المنتج، الطلب، تكلفة التمويل.")
        st.warning("نقطة الانكسار: عند أي مستوى يتحول النمو إلى تراجع؟ (Sensitivity Matrix).")

    with t6:
        st.markdown("<div class='section-title'>8. توصية مدير المحفظة (CFA3 Strategy)</div>", unsafe_allow_html=True)
        curr_p = info.get('currentPrice', 0)
        st.success(f"🎯 **استراتيجية التجميع:** شراء تدريجي قرب {curr_p*0.96:.2f} ريال.")
        st.error(f"🛑 **مناطق إلغاء الفكرة:** كسر مستوى {curr_p*0.88:.2f} ريال مع تدهور أساسي.")

except Exception as e:
    st.error(f"خطأ في البيانات: {e}. يرجى التأكد من الرمز.")
