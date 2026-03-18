import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# --- 1. إعدادات الهوية البصرية ---
st.set_page_config(page_title="Snapshot-Tasi Engine", layout="wide")

def apply_pro_styling():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    html, body, [class*="css"] { font-family: 'Noto Kufi Arabic', sans-serif; text-align: right; direction: rtl; }
    .main { background-color: #f0f2f5; }
    .header-box { background: linear-gradient(135deg, #1a365d 0%, #2b6cb0 100%); color: white; padding: 2rem; border-radius: 20px; margin-bottom: 2rem; border-right: 8px solid #ed8936; }
    .snap-card { background: white; padding: 1.5rem; border-radius: 15px; height: 320px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-top: 5px solid #3182ce; display: flex; flex-direction: column; }
    .snap-title { color: #2c5282; font-weight: bold; font-size: 1.1rem; margin-bottom: 0.5rem; }
    .snap-value { font-size: 1.2rem; font-weight: 700; margin-bottom: 0.5rem; }
    .status-pos { color: #2f855a; } .status-neu { color: #d69e2e; } .status-neg { color: #c53030; }
    .section-title { color: #1a365d; border-right: 6px solid #ed8936; padding-right: 1rem; margin: 3rem 0 1.5rem 0; font-size: 1.8rem; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

apply_pro_styling()

# --- 2. محرك جلب وتحليل البيانات الحية ---
@st.cache_data(ttl=3600)
def fetch_and_analyze(symbol):
    ticker = f"{symbol}.SR"
    stock = yf.Ticker(ticker)
    info = stock.info
    fin = stock.quarterly_financials
    cash = stock.quarterly_cashflow
    hist = stock.history(period="2y")
    return info, fin, cash, hist

# --- 3. واجهة التحكم ---
st.sidebar.title("🛡️ محرك Snapshot-Tasi")
symbol_input = st.sidebar.text_input("أدخل رمز السهم (مثلاً: 1120 لـ الراجحي):", "2222")

try:
    info, fin, cash, hist = fetch_and_analyze(symbol_input)
    st.markdown(f"<div class='header-box'><h1>🛡️ Snapshot-Tasi: {info.get('longName')} ({symbol_input})</h1><p>تحليل استراتيجي آلي بناءً على معايير CFA3 | بيانات حية</p></div>", unsafe_allow_html=True)

    # --- حساب المؤشرات المالية ديناميكياً ---
    pe = info.get('trailingPE', 0)
    gearing = (info.get('totalDebt', 0) / info.get('totalEquity', 1)) * 100 if info.get('totalEquity') else 0
    margin = info.get('profitMargins', 0) * 100
    fcf = info.get('freeCashflow', 0) / 1e6 # بالمليون
    
    # تحديد الجودة (صافي الربح vs تدفق تشغيلي)
    net_inc = fin.loc['Net Income'].iloc[0] if 'Net Income' in fin.index else 1
    op_cash = cash.loc['Operating Cash Flow'].iloc[0] if 'Operating Cash Flow' in cash.index else 0
    quality_status = 1 if op_cash > net_inc else 3

    # --- 1. الـ Snapshot الديناميكي ---
    st.markdown("<div class='section-title'>1. الـ Snapshot (تحليل آلي للمؤشرات)</div>", unsafe_allow_html=True)
    
    snap_items = [
        ("نموذج العمل", f"🟢 {info.get('industry', 'N/A')}", "طريقة توليد القيمة في القطاع الذي تعمل فيه الشركة.", 1),
        ("مصدر الإيرادات", f"🟢 {info.get('sector', 'N/A')}", "القطاع الرئيسي المحرك للمبيعات والنمو.", 1),
        ("الهوامش الربحية", f"{'🟢' if margin > 15 else '🟡'} {margin:.1f}%", "كفاءة الإدارة في تحويل المبيعات إلى أرباح صافية.", 1 if margin > 15 else 2),
        ("مستوى الدين", f"{'🟢' if gearing < 50 else '🔴'} {gearing:.1f}% (D/E)", "قدرة الشركة على تغطية التزاماتها ومخاطر الرفع المالي.", 1 if gearing < 50 else 3),
        ("التدفقات النقدية", f"{'🟢' if fcf > 0 else '🔴'} {fcf:.1f}M", "السيولة المتاحة بعد النفقات الرأسمالية (وقود التوزيعات).", 1 if fcf > 0 else 3),
        ("جودة الأرباح", f"{'🟢 نقدية' if quality_status==1 else '🔴 محاسبية'}", "مدى تطابق الأرباح الدفترية مع السيولة النقدية الفعلية.", quality_status),
        ("المخاطر الرئيسية", "🟡 مخاطر القطاع", "تأثر الشركة بالدورة الاقتصادية وتغير أسعار الفائدة واللقيم.", 2),
        ("المحفزات", "🟢 نمو تشغيلي", "التوسعات المرتقبة وخطط الشركة الاستراتيجية لزيادة الحصة السوقية.", 1),
        ("التقييم الحالي", f"{'🟢' if pe < 15 else '🟡'} {pe:.1f}x (P/E)", "مقارنة السعر بالربحية؛ هل يتداول السهم بخصم أم علاوة؟", 1 if pe < 15 else 2),
        ("قرار مبدئي", f"{'🟢 شراء/تجميع' if pe < 20 else '🟡 مراقبة'}", "رؤية المحرك المبدئية بناءً على مكررات الربحية والتدفقات.", 1 if pe < 20 else 2)
    ]

    for row in range(2):
        cols = st.columns(5)
        for i in range(5):
            idx = row * 5 + i
            title, val, desc, status = snap_items[idx]
            val_class = "status-pos" if status == 1 else ("status-neu" if status == 2 else "status-neg")
            with cols[i]:
                st.markdown(f"<div class='snap-card'><div class='snap-title'>{title}</div><div class='snap-value {val_class}'>{val}</div><p style='font-size:0.8rem; color:#64748b;'>{desc}</p></div>", unsafe_allow_html=True)

    # --- 2. تحليل الأداء (12 ربعاً - ديناميكي) ---
    st.markdown("<div class='section-title'>2. تحليل الأداء (آخر 8-12 ربعاً متوفرة)</div>", unsafe_allow_html=True)
    c2_l, c2_r = st.columns([2, 1])
    with c2_l:
        rev_hist = fin.loc['Total Revenue'][::-1]
        fig = go.Figure(data=[go.Scatter(x=rev_hist.index.astype(str), y=rev_hist.values, mode='lines+markers', line=dict(color='#2b6cb0', width=3))])
        fig.update_layout(title="مسار الإيرادات الربعية", height=400, plot_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)
    with c2_r:
        st.info(f"**تحليل النمو:**\nالإيرادات الحالية بلغت {rev_hist.iloc[-1]/1e6:.1f}M.\nبناءً على الاتجاه، الشركة تمر بمرحلة {'نمو' if rev_hist.iloc[-1] > rev_hist.iloc[0] else 'انكماش'} تشغيلي.")

    # --- 7. التوصية (بناءً على البيانات الحية) ---
    st.markdown("<div class='section-title'>7. توصية مدير المحفظة الاستراتيجية</div>", unsafe_allow_html=True)
    curr_p = info.get('currentPrice', 0)
    rec_l, rec_r = st.columns(2)
    with rec_l:
        st.success(f"🎯 **استراتيجية التجميع:** شراء تدريجي قرب مستويات **{curr_p*0.95:.2f} ريال** (بناءً على التقييم الحالي).")
    with rec_r:
        st.error(f"🛑 **إدارة المخاطر:** وقف الخسارة عند كسر **{curr_p*0.88:.2f} ريال** (تراجع بنسبة 12% من السعر الحالي).")

except Exception as e:
    st.error(f"يرجى التأكد من الرمز. خطأ في البيانات: {e}")
