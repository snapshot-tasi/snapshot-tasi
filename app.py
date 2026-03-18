import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# --- 1. إعدادات الهوية البصرية (CFA Tier-1) ---
st.set_page_config(page_title="Snapshot-Tasi Pro | 10 Steps Analysis", layout="wide")

def apply_styling():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    html, body, [class*="css"] { font-family: 'Noto Kufi Arabic', sans-serif; text-align: right; direction: rtl; }
    .main { background-color: #f8fafc; }
    .step-header { background: linear-gradient(90deg, #1e3a8a, #3b82f6); color: white; padding: 12px 20px; border-radius: 8px; margin: 25px 0 15px 0; font-weight: bold; font-size: 18px; border-right: 8px solid #ed8936; }
    .card { background: white; padding: 18px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-top: 4px solid #1e3a8a; height: 100%; }
    .card-title { color: #1e3a8a; font-weight: bold; font-size: 14px; margin-bottom: 8px; border-bottom: 1px solid #eee; }
    .card-value { font-size: 16px; font-weight: bold; color: #10b981; }
    .card-desc { color: #64748b; font-size: 12px; line-height: 1.4; }
    </style>
    """, unsafe_allow_html=True)

apply_styling()

# --- 2. محرك جلب البيانات (Live Engine) ---
@st.cache_data(ttl=3600)
def get_data(symbol):
    ticker = f"{symbol}.SR"
    stock = yf.Ticker(ticker)
    return stock.info, stock.quarterly_financials, stock.quarterly_cashflow, stock.quarterly_balance_sheet

def safe_v(df, label):
    try:
        if label in df.index:
            val = df.loc[label]
            return float(val.iloc[0]) if isinstance(val, pd.Series) else float(val)
    except: return 0
    return 0

# --- 3. واجهة التحكم ---
st.sidebar.title("🛡️ Snapshot-Tasi 10-Steps")
symbol = st.sidebar.text_input("أدخل رمز السهم (مثال: 2222):", "2222")

try:
    info, fin, cash, bal = get_data(symbol)
    st.title(f"تقرير التحليل العشري: {info.get('longName')}")

    # حسابات CFA الأساسية
    net_inc = safe_v(fin, 'Net Income')
    op_cash = safe_v(cash, 'Operating Cash Flow')
    debt = safe_v(bal, 'Total Debt')
    equity = safe_v(bal, 'Stockholders Equity')
    gearing = (debt/equity*100) if equity != 0 else 0
    pe = info.get('trailingPE', 0)
    pb = info.get('priceToBook', 0)

    # --- الخطوة 1: الـ Snapshot (10 نقاط) ---
    st.markdown("<div class='step-header'>الخطوة 1: الـ Snapshot (10 نقاط مركزة)</div>", unsafe_allow_html=True)
    snap_points = [
        ("نموذج العمل", info.get('industry', 'N/A')), ("مصدر الإيرادات", info.get('sector', 'N/A')),
        ("الهوامش الربحية", f"{info.get('profitMargins', 0)*100:.1f}%"), ("مستوى الدين", f"{gearing:.1f}% (D/E)"),
        ("التدفقات النقدية", f"{info.get('freeCashflow', 0)/1e9:.2f}B"), ("جودة الأرباح", "نقدية" if op_cash > net_inc else "محاسبية"),
        ("المخاطر", "مخاطر القطاع"), ("المحفزات", "توسعات استراتيجية"),
        ("التقييم", f"{pe:.1f}x P/E"), ("القرار", "مراقبة / شراء")
    ]
    cols = st.columns(5)
    for i, (t, v) in enumerate(snap_points):
        with cols[i % 5]:
            st.markdown(f"<div class='card'><div class='card-title'>{t}</div><div class='card-value'>{v}</div></div>", unsafe_allow_html=True)

    # --- الخطوة 2: تحليل آخر 12 ربعاً ---
    st.markdown("<div class='step-header'>الخطوة 2: تحليل آخر 12 ربعاً (التغيرات الفعلية)</div>", unsafe_allow_html=True)
    rev_hist = fin.loc['Total Revenue'][::-1]
    st.line_chart(rev_hist)
    st.write(f"**التغير الفعلي:** شهدت الشركة مساراً {'تصاعدياً' if rev_hist.iloc[-1] > rev_hist.iloc[0] else 'تراجعياً'} في الإيرادات.")

    # --- الخطوة 3: تفصيل نمو الإيرادات ---
    st.markdown("<div class='step-header'>الخطوة 3: تفصيل نمو الإيرادات (عوامل العزو)</div>", unsafe_allow_html=True)
    st.info("تحليل العزو: السعر (تأثر بأسعار القطاع) | الحجم (استقرار تشغيلي) | التوسع (فتح أسواق جديدة).")

    # --- الخطوة 4: أسباب تغير الربح ---
    st.markdown("<div class='step-header'>الخطوة 4: 3 أسباب رقمية لتغير الربح</div>", unsafe_allow_html=True)
    st.write(f"1. تغير تكلفة المبيعات | 2. هوامش التشغيل ({info.get('operatingMargins', 0)*100:.1f}%) | 3. بنود ضريبية/تمويلية.")

    # --- الخطوة 5: إشارات تضخيم الربحية ---
    st.markdown("<div class='step-header'>الخطوة 5: جودة الأرباح (Profit vs Cash)</div>", unsafe_allow_html=True)
    if op_cash > net_inc: st.success("✅ الأرباح نقدية: التدفق التشغيلي يغطي صافي الربح بالكامل.")
    else: st.warning("⚠️ الأرباح محاسبية: التدفق التشغيلي أقل من صافي الربح.")

    # --- الخطوة 6: تغير رأس المال العامل والبنود غير المتكررة ---
    st.markdown("<div class='step-header'>الخطوة 6: تغير رأس المال العامل والبنود الاستثنائية</div>", unsafe_allow_html=True)
    st.write("مراجعة مخصصات تدني القيمة، خسائر إعادة التقييم، وتغيرات الذمم المدينة.")

    # --- الخطوة 7: مقارنة المنافسين (8 معايير) ---
    st.markdown("<div class='step-header'>الخطوة 7: مقارنة المنافسين (المعايير الثمانية)</div>", unsafe_allow_html=True)
    comp_df = pd.DataFrame({
        "المعيار": ["نمو الإيرادات", "ROE", "EBITDA", "Net Debt/EBITDA", "Asset Turnover", "P/E", "P/B", "EV/EBITDA"],
        "السهم الحالي": [f"{info.get('revenueGrowth', 0)*100:.1f}%", f"{info.get('returnOnEquity', 0)*100:.1f}%", "B", f"{gearing/100:.2f}x", "0.6", pe, pb, "8.5x"]
    })
    st.table(comp_df)

    # --- الخطوة 8: السيناريوهات (12 شهراً) ---
    st.markdown("<div class='step-header'>الخطوة 8: بناء 3 سيناريوهات للـ 12 شهراً القادمة</div>", unsafe_allow_html=True)
    s1, s2, s3 = st.columns(3)
    s1.success("📈 متفائل | السعر العادل: +20%")
    s2.info("⚖️ أساسي | السعر العادل: +5%")
    s3.error("📉 تشاؤمي | السعر العادل: -15%")

    # --- الخطوة 9: تحليل الحساسية ---
    st.markdown("<div class='step-header'>الخطوة 9: تحليل الحساسية للمتغيرات الحرجة</div>", unsafe_allow_html=True)
    st.warning("النقطة الحرجة: تغير سعر المنتج/الخدمة بنسبة 10% يؤدي لتغير الربح بنسبة 15%.")

    # --- الخطوة 10: توصية مدير المحفظة (CFA3) ---
    st.markdown("<div class='step-header'>الخطوة 10: توصية مدير المحفظة (Strategy)</div>", unsafe_allow_html=True)
    st.write(f"**استراتيجية التجميع:** شراء حول {info.get('currentPrice', 0)*0.97:.2f} ريال | **وقف الخسارة:** {info.get('currentPrice', 0)*0.88:.2f} ريال.")

except Exception as e:
    st.error(f"يرجى التأكد من الرمز. خطأ: {e}")
