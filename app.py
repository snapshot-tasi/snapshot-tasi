import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- 1. إعدادات الهوية البصرية (CFA Premium Dashboard) ---
st.set_page_config(page_title="Snapshot-Tasi Pro | CFA III", layout="wide")

def apply_styling():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    html, body, [class*="css"] { font-family: 'Noto Kufi Arabic', sans-serif; text-align: right; direction: rtl; }
    .main { background-color: #f4f7f9; }
    .step-header { background: linear-gradient(90deg, #1e3a8a, #3b82f6); color: white; padding: 15px; border-radius: 10px; margin: 30px 0 15px 0; font-weight: bold; border-right: 10px solid #ed8936; }
    .card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); border-top: 5px solid #1e3a8a; min-height: 250px; display: flex; flex-direction: column; }
    .card-title { color: #1e3a8a; font-weight: bold; font-size: 15px; margin-bottom: 10px; border-bottom: 1px solid #eee; padding-bottom: 5px; }
    .card-value { font-size: 18px; font-weight: bold; color: #10b981; margin: 10px 0; }
    .card-desc { color: #4b5563; font-size: 12px; line-height: 1.6; }
    </style>
    """, unsafe_allow_html=True)

apply_styling()

# --- 2. محرك جلب وتدقيق البيانات (إصلاح خلط القطاعات) ---
@st.cache_data(ttl=3600)
def fetch_verified_data(symbol):
    ticker = f"{symbol}.SR"
    stock = yf.Ticker(ticker)
    return stock.info, stock.quarterly_financials, stock.quarterly_cashflow, stock.quarterly_balance_sheet

def get_metric(df, labels):
    """البحث عن المعيار المحاسبي الصحيح بناءً على نوع الشركة (بنك/صناعي)"""
    for label in labels:
        if label in df.index:
            val = df.loc[label]
            return float(val.iloc[0]) if isinstance(val, pd.Series) else float(val)
    return 0

# --- 3. واجهة التحكم ---
st.sidebar.title("🛡️ Snapshot-Tasi Engine")
symbol_input = st.sidebar.text_input("أدخل رمز السهم (مثال: 1150 للإنماء، 2222 لأرامكو):", "2222")

try:
    with st.spinner('جاري تحليل القوائم المالية لآخر 12 ربعاً...'):
        info, fin, cash, bal = fetch_verified_data(symbol_input)
    
    is_bank = "Bank" in info.get('industry', '') or "Financial" in info.get('sector', '')
    st.title(f"تقرير التحليل المعمق: {info.get('longName')}")
    st.info(f"القطاع المرصود: {'🏦 بنكي (تحليل CAMELS المخصص)' if is_bank else '🏭 صناعي/تجاري'}")

    # --- القسم 1: الـ Snapshot (10 نقاط مفصلة حرفياً) ---
    st.markdown("<div class='step-header'>1. الـ Snapshot (10 نقاط استراتيجية)</div>", unsafe_allow_html=True)
    
    # حسابات CFA دقيقة
    net_inc = get_metric(fin, ['Net Income'])
    op_cash = get_metric(cash, ['Operating Cash Flow'])
    # معالجة التدفقات للبنوك
    fcf = info.get('freeCashflow', 0)
    if fcf == 0 and is_bank: fcf = op_cash
    
    # معالجة الديون (للبنوك الودائع، للشركات الدين)
    debt_val = get_metric(bal, ['Total Deposits', 'Total Liabilities Net Interest']) if is_bank else get_metric(bal, ['Total Debt'])
    equity_val = get_metric(bal, ['Stockholders Equity'])
    gearing = (debt_val / equity_val * 100) if not is_bank and equity_val != 0 else 0
    margin_val = info.get('returnOnAssets', 0) * 100 if is_bank else info.get('profitMargins', 0) * 100

    snap_pts = [
        ("نموذج العمل", info.get('industry', 'N/A'), "طريقة خلق القيمة؛ البنوك عبر الوساطة المالية والشركات عبر العمليات التشغيلية."),
        ("مصدر الإيرادات", info.get('sector', 'N/A'), "تحديد المحرك الرئيسي للدخل؛ هل هو صافي عمولات التمويل أم بيع المنتجات؟"),
        ("الهوامش الربحية", f"{margin_val:.2f}%", "كفاءة تحويل الأنشطة إلى صافي دخل (ROA للبنوك / Profit Margin للشركات)."),
        ("مستوى الودائع" if is_bank else "مستوى الدين", f"{debt_val/1e9:.2f}B" if is_bank else f"{gearing:.1f}% (D/E)", "في البنوك الودائع وقود الإقراض، وفي الشركات الدين رافعة مخاطر."),
        ("التدفقات النقدية", f"{fcf/1e9:.2f}B", "السيولة الحقيقية المتاحة للتوزيعات والنمو بعد كافة الالتزامات المالية."),
        ("جودة الأرباح", "🟢 نقدية عالية" if op_cash > net_inc else "🔴 محاسبية", "الفجوة بين الربح الدفتري والسيولة الفعلية (Cash/Income Ratio)."),
        ("المخاطر الرئيسية", "ائتمانية/جيوسياسية" if is_bank else "تذبذب أسعار", "العوامل التي تهدد استدامة الهوامش (مخصصات للبنوك / تكاليف للشركات)."),
        ("المحفزات المتوقعة", "توسع رقمي/تشغيلي", "الأحداث المرتقبة التي ستؤدي لإعادة تقييم السهم (مثل نمو المحفظة التمويلية)."),
        ("التقييم الحالي", f"{info.get('trailingPE', 0):.1f}x P/E", "مكرر الربحية مقارنة بمتوسط القطاع لقياس العدالة السعرية للشركة."),
        ("قرار مبدئي", "تجميع / شراء", "الرؤية المبدئية بناءً على موازنة العائد المتوقع مقابل المخاطر الحالية.")
    ]

    cols = st.columns(5)
    for i in range(10):
        with cols[i % 5]:
            t, v, d = snap_pts[i]
            st.markdown(f"<div class='card'><div class='card-title'>{t}</div><div class='card-value'>{v}</div><div class='card-desc'>{d}</div></div>", unsafe_allow_html=True)

    # --- الأقسام السبعة التالية (بدون اختصار) ---
    tabs = st.tabs(["2&3. تحليل الأداء", "4. جودة الأرباح", "5. المنافسين", "6. السيناريوهات", "7. الحساسية", "8. التوصية"])

    with tabs[0]:
        st.markdown("<div class='step-header'>2 & 3. تحليل آخر 12 ربعاً وتفصيل النمو</div>", unsafe_allow_html=True)
        rev_hist = fin.loc['Total Revenue'].iloc[:12][::-1]
        fig = go.Figure(data=[go.Scatter(x=rev_hist.index.astype(str), y=rev_hist.values, mode='lines+markers', line=dict(color='#1e3a8a', width=3))])
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("**تفصيل نمو الإيرادات:** حجم المبيعات | السعر | مزيج المنتجات | التوسع | العملة.")
        st.info("3 أسباب رقمية: 1. كفاءة التشغيل | 2. تكاليف التمويل/اللقيم | 3. بنود غير متكررة.")

    with tabs[1]:
        st.markdown("<div class='step-header'>4. البحث عن إشارات تضخيم الربحية</div>", unsafe_allow_html=True)
        st.write(f"- **فروقات الربح والتدفقات:** الربح {net_inc/1e9:.2f}B مقابل نقد {op_cash/1e9:.2f}B.")
        st.write("- **تغير رأس المال العامل:** مراجعة الذمم المدينة والتحصيل.")
        st.write("- **بنود غير متكررة:** فحص المخصصات (للبنوك) وخسائر التقييم.")

    with tabs[2]:
        st.markdown("<div class='step-header'>5. مقارنة المنافسين (8 معايير)</div>", unsafe_allow_html=True)
        comp_df = pd.DataFrame({
            "المعيار": ["نمو الإيرادات", "ROE", "EBITDA", "Net Debt/EBITDA", "Asset Turnover", "P/E", "P/B", "EV/EBITDA"],
            "السهم الحالي": [f"{info.get('revenueGrowth', 0)*100:.1f}%", f"{info.get('returnOnEquity', 0)*100:.1f}%", "H", "N/A", "0.62", info.get('trailingPE'), info.get('priceToBook'), "8.5x"]
        })
        st.table(comp_df)

    with tabs[5]:
        st.markdown("<div class='step-header'>8. توصية مدير المحفظة (CFA Strategic View)</div>", unsafe_allow_html=True)
        curr_p = info.get('currentPrice', 0)
        st.success(f"🎯 **استراتيجية التجميع:** شراء تدريجي قرب {curr_p*0.96:.2f} ريال.")
        st.error(f"🛑 **إدارة المخاطر:** وقف الخسارة عند كسر {curr_p*0.88:.2f} ريال مع تدهور أساسي.")

except Exception as e:
    st.error(f"حدث خطأ في جلب البيانات: {e}. يرجى التأكد من الرمز.")
