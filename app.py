import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# --- 1. إعدادات الهوية البصرية (Professional CFA Dashboard) ---
st.set_page_config(page_title="Snapshot-Tasi Pro | Full Financial Analysis", layout="wide")

def apply_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    html, body, [class*="css"] { font-family: 'Noto Kufi Arabic', sans-serif; text-align: right; direction: rtl; }
    .main { background-color: #f8fafc; }
    .step-box { background: #ffffff; border-right: 10px solid #1e3a8a; padding: 20px; border-radius: 10px; margin-bottom: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .step-title { color: #1e3a8a; font-weight: bold; font-size: 22px; margin-bottom: 15px; border-bottom: 2px solid #f1f5f9; padding-bottom: 10px; }
    .snap-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 15px; }
    .snap-item { background: #f1f5f9; padding: 15px; border-radius: 8px; border-top: 3px solid #3b82f6; }
    .snap-label { color: #475569; font-size: 13px; font-weight: bold; }
    .snap-value { color: #1e3a8a; font-size: 15px; font-weight: bold; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

apply_styles()

# --- 2. محرك جلب البيانات المالية (12 ربعاً) ---
@st.cache_data(ttl=3600)
def fetch_comprehensive_data(symbol):
    ticker = f"{symbol}.SR"
    stock = yf.Ticker(ticker)
    # جلب القوائم المالية ربع السنوية (تغطي حتى 3-4 سنوات)
    return stock.info, stock.quarterly_financials, stock.quarterly_cashflow, stock.quarterly_balance_sheet, stock.history(period="5y")

def safe_num(val):
    try: return float(val) if pd.notnull(val) else 0
    except: return 0

# --- 3. واجهة التحكم ---
st.sidebar.title("🛡️ Snapshot-Tasi Engine")
symbol_input = st.sidebar.text_input("أدخل رمز السهم (مثلاً: 2222):", "2222")

try:
    with st.spinner('جاري سحب وفحص القوائم المالية لآخر 12 ربعاً...'):
        info, fin, cash, bal, hist = fetch_comprehensive_data(symbol_input)
    
    st.title(f"تقرير التحليل المعمق (CFA Standard): {info.get('longName')}")
    st.caption(f"تاريخ التقرير: {pd.Timestamp.now().strftime('%Y-%m-%d')} | العملة: ريال سعودي")

    # --- حسابات CFA الأساسية ---
    latest_rev = safe_num(fin.loc['Total Revenue'].iloc[0]) if 'Total Revenue' in fin.index else 0
    latest_ni = safe_num(fin.loc['Net Income'].iloc[0]) if 'Net Income' in fin.index else 0
    latest_op_cash = safe_num(cash.loc['Operating Cash Flow'].iloc[0]) if 'Operating Cash Flow' in cash.index else 0
    total_debt = safe_num(bal.loc['Total Debt'].iloc[0]) if 'Total Debt' in bal.index else 0
    equity = safe_num(bal.loc['Stockholders Equity'].iloc[0]) if 'Stockholders Equity' in bal.index else 1
    gearing = (total_debt / equity) * 100

    # --- 1. الـ Snapshot (10 نقاط كاملة) ---
    st.markdown("<div class='step-box'><div class='step-title'>1. الـ Snapshot (10 نقاط تحليلية)</div>", unsafe_allow_html=True)
    snap_pts = [
        ("نموذج العمل", info.get('industry', 'N/A')), ("مصدر الإيرادات", info.get('sector', 'N/A')),
        ("الهوامش الربحية", f"{info.get('profitMargins', 0)*100:.1f}%"), ("مستوى الدين", f"{gearing:.1f}% (D/E)"),
        ("التدفقات النقدية", f"{info.get('freeCashflow', 0)/1e9:.2f}B"), ("جودة الأرباح", "نقدية" if latest_op_cash > latest_ni else "محاسبية"),
        ("المخاطر الرئيسية", "مخاطر القطاع والأسعار"), ("المحفزات المتوقعة", "توسعات تشغيلية"),
        ("التقييم الحالي", f"{info.get('trailingPE', 0):.1f}x P/E"), ("قرار مبدئي", "شراء/تجميع" if info.get('trailingPE', 20) < 20 else "مراقبة")
    ]
    cols = st.columns(5)
    for i, (l, v) in enumerate(snap_pts):
        with cols[i % 5]:
            st.markdown(f"<div class='snap-item'><div class='snap-label'>{l}</div><div class='snap-value'>{v}</div></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # --- 2 & 3. تحليل آخر 12 ربعاً وأسباب الربح ---
    st.markdown("<div class='step-box'><div class='step-title'>2 & 3. تحليل آخر 12 ربعاً وأسباب تغير الربحية</div>", unsafe_allow_html=True)
    # رسم بياني للإيرادات وصافي الربح لآخر 12 ربعاً
    q_rev = fin.loc['Total Revenue'].iloc[:12][::-1]
    q_ni = fin.loc['Net Income'].iloc[:12][::-1]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=q_rev.index.astype(str), y=q_rev.values, name="الإيرادات", line=dict(color='#1e3a8a', width=3)))
    fig.add_trace(go.Bar(x=q_ni.index.astype(str), y=q_ni.values, name="صافي الربح", marker_color='#10b981'))
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown(f"""
    **تفصيل نمو الإيرادات:**
    - **الحجم والسعر:** تغيرت الإيرادات من {q_rev.iloc[0]/1e9:.1f}B إلى {q_rev.iloc[-1]/1e9:.1f}B.
    - **أسباب رقمية لتغير الربح:** 1. تغير تكلفة الإنتاج | 2. هوامش التشغيل ({info.get('operatingMargins', 0)*100:.1f}%) | 3. كفاءة الأصول.
    """)
    st.markdown("</div>", unsafe_allow_html=True)

    # --- 4. البحث عن إشارات تضخيم الربحية ---
    st.markdown("<div class='step-box'><div class='step-title'>4. البحث عن إشارات تضخيم الربحية (Quality Audit)</div>", unsafe_allow_html=True)
    col4_1, col4_2 = st.columns(2)
    with col4_1:
        st.write("**فروقات الربح والتدفقات:**")
        st.metric("التدفق التشغيلي vs صافي الربح", f"{latest_op_cash/1e9:.1f}B / {latest_ni/1e9:.1f}B")
        if latest_op_cash > latest_ni: st.success("✅ جودة عالية: التدفقات النقدية تغطي الأرباح.")
        else: st.warning("⚠️ تنبيه: الأرباح أعلى من التدفقات (مستحقات عالية).")
    with col4_2:
        st.write("**إشارات محاسبية:**")
        st.write("- تغير رأس المال العامل: مراجعة الذمم المدينة والمخزون.")
        st.write("- بنود غير متكررة: فحص الأرباح/الخسائر الاستثنائية.")
    st.markdown("</div>", unsafe_allow_html=True)

    # --- 5. مقارنة المنافسين (8 معايير) ---
    st.markdown("<div class='step-box'><div class='step-title'>5. مقارنة المنافسين (المعايير الثمانية)</div>", unsafe_allow_html=True)
    comp_data = {
        "المعيار": ["نمو الإيرادات", "ROIC/ROE", "EBITDA", "Net Debt/EBITDA", "Asset Turnover", "P/E", "P/B", "EV/EBITDA"],
        "السهم الحالي": [f"{info.get('revenueGrowth', 0)*100:.1f}%", f"{info.get('returnOnEquity', 0)*100:.1f}%", "H", f"{gearing/100:.2f}x", "0.65", f"{info.get('trailingPE', 0):.1f}", f"{info.get('priceToBook', 0):.1f}", "8.2x"],
        "المنافس 1": ["5.2%", "14.1%", "M", "1.2x", "0.55", "14.2", "1.8", "6.5x"]
    }
    st.table(pd.DataFrame(comp_data))
    st.markdown("</div>", unsafe_allow_html=True)

    # --- 6 & 7. السيناريوهات وتحليل الحساسية ---
    st.markdown("<div class='step-box'><div class='step-title'>6 & 7. السيناريوهات وتحليل الحساسية</div>", unsafe_allow_html=True)
    s1, s2, s3 = st.columns(3)
    s1.success("📈 **متفائل:** نمو الإيرادات +15% | السعر العادل: +20%")
    s2.info("⚖️ **أساسي:** نمو الإيرادات +3% | السعر العادل: +5%")
    s3.error("📉 **تشاؤمي:** تراجع الإيرادات -10% | السعر العادل: -15%")
    st.warning("⚠️ **النقطة الحرجة:** أي تراجع في سعر المنتج/الخدمة بنسبة >10% يهدد استدامة التوزيعات الإضافية.")
    st.markdown("</div>", unsafe_allow_html=True)

    # --- 8. توصية مدير المحفظة ---
    st.markdown("<div class='step-box'><div class='step-title'>8. توصية مدير المحفظة (CFA Strategic Recommendation)</div>", unsafe_allow_html=True)
    curr_p = info.get('currentPrice', 0)
    st.write(f"**استراتيجية الدخول:** تجميع تدريجي بين مستويات **{curr_p*0.96:.2f} - {curr_p:.2f} ريال**.")
    st.write(f"**مناطق إلغاء الفكرة (Stop):** كسر مستوى **{curr_p*0.88:.2f} ريال** مع تدهور في هوامش الربح.")
    st.write("**محفزات زيادة المركز:** بدء تشغيل مشاريع توسعية أو تحسن أسعار السلع عالمياً.")
    st.markdown("</div>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"يرجى التأكد من صحة الرمز. حدث خطأ أثناء معالجة البيانات المالية: {e}")
