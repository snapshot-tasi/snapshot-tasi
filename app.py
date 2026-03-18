import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# --- 1. إعدادات الهوية البصرية ---
st.set_page_config(page_title="Snapshot-Tasi Live Engine", layout="wide")

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

# --- 2. محرك جلب البيانات اللحظية (Real-Time API) ---
@st.cache_data(ttl=3600) # التحديث كل ساعة لضمان دقة البيانات
def fetch_live_data(symbol):
    ticker = f"{symbol}.SR"
    stock = yf.Ticker(ticker)
    
    # جلب البيانات الأساسية، القوائم المالية، والتدفقات النقدية
    info = stock.info
    fin = stock.quarterly_financials
    cash = stock.quarterly_cashflow
    bal = stock.quarterly_balance_sheet
    hist = stock.history(period="2y") # تاريخ السهم لآخر سنتين
    
    return info, fin, cash, bal, hist

# --- 3. واجهة التحكم ---
st.sidebar.title("🛡️ محرك Snapshot-Tasi المباشر")
symbol_input = st.sidebar.text_input("أدخل رمز السهم (مثلاً: 2222 لأرامكو):", "2222")
current_date = datetime.now().strftime("%Y-%m-%d")

try:
    with st.spinner('جاري سحب أحدث البيانات المالية من تداول...'):
        info, fin, cash, bal, hist = fetch_live_data(symbol_input)

    st.markdown(f"""
    <div class='header-box'>
        <h1>🛡️ Snapshot-Tasi: {info.get('longName')} ({symbol_input})</h1>
        <p>تحليل استراتيجي آلي بناءً على بيانات حقيقية بتاريخ: {current_date}</p>
    </div>
    """, unsafe_allow_html=True)

    # --- الحسابات المالية اللحظية (CFA Formulas) ---
    curr_price = info.get('currentPrice', 0)
    pe_ratio = info.get('trailingPE', 0)
    # حساب نسبة الدين (D/E) من الميزانية العمومية الحقيقية
    total_debt = bal.loc['Total Debt'].iloc if 'Total Debt' in bal.index else 0
    total_equity = bal.loc['Stockholders Equity'].iloc if 'Stockholders Equity' in bal.index else 1
    gearing = (total_debt / total_equity) * 100
    
    # جودة الأرباح: التدفق التشغيلي مقابل صافي الربح
    latest_net_inc = fin.loc['Net Income'].iloc if 'Net Income' in fin.index else 0
    latest_op_cash = cash.loc['Operating Cash Flow'].iloc if 'Operating Cash Flow' in cash.index else 0
    quality_status = 1 if latest_op_cash > latest_net_inc else 3

    # --- 1. الـ Snapshot المحدث ---
    st.markdown("<div class='section-title'>1. الـ Snapshot (آخر تحديث متاح)</div>", unsafe_allow_html=True)
    
    snap_items = [
        ("نموذج العمل", f"🟢 {info.get('industry', 'Data Required')}", "تحليل الأنشطة التشغيلية الحالية للشركة.", 1),
        ("مصدر الإيرادات", f"🟢 {info.get('sector', 'Data Required')}", "القطاع الرئيسي الذي يولد الدخل التشغيلي.", 1),
        ("الهوامش الربحية", f"{'🟢' if info.get('profitMargins', 0) > 0.15 else '🟡'} {info.get('profitMargins', 0)*100:.1f}%", "كفاءة تحويل المبيعات لأرباح (بيانات حية).", 1 if info.get('profitMargins', 0) > 0.15 else 2),
        ("مستوى الدين", f"{'🟢' if gearing < 40 else '🔴'} {gearing:.1f}% (D/E)", "نسبة المديونية الحقيقية بناءً على آخر ميزانية عمومية.", 1 if gearing < 40 else 3),
        ("التدفقات النقدية", f"🟢 {info.get('freeCashflow', 0)/1e9:.2f}B", "التدفق النقدي الحر السنوي (FCF) المحقق.", 1),
        ("جودة الأرباح", f"{'🟢 نقدية عالية' if quality_status==1 else '🔴 محاسبية/مستحقات'}", "مقارنة السيولة بالربح الدفتري لآخر ربع مالي.", quality_status),
        ("المخاطر", "🟡 مخاطر السوق", "تأثر الشركة بأسعار السلع أو تكلفة التمويل الحالية.", 2),
        ("المحفزات", "🟢 نمو استراتيجي", "المشروعات الرأسمالية والتوسعية المعلنة.", 1),
        ("التقييم P/E", f"{'🟢 جذاب' if pe_ratio < 15 else '🟡 عادل'} {pe_ratio:.2f}x", "تقييم السهم بناءً على سعر السوق الحالي وأرباح آخر 12 شهر.", 1 if pe_ratio < 15 else 2),
        ("قرار مبدئي", f"{'🟢 شراء/تجميع' if pe_ratio < 20 else '🟡 مراقبة'}", "رؤية استثمارية مبدئية بناءً على المعايير الحالية.", 1 if pe_ratio < 20 else 2)
    ]

    # عرض البطاقات (2 صفوف × 5 أعمدة)
    for row in range(2):
        cols = st.columns(5)
        for i in range(5):
            idx = row * 5 + i
            title, val, desc, status = snap_items[idx]
            val_class = "status-pos" if status == 1 else ("status-neu" if status == 2 else "status-neg")
            with cols[i]:
                st.markdown(f"<div class='snap-card'><div class='snap-title'>{title}</div><div class='snap-value {val_class}'>{val}</div><p style='font-size:0.8rem; color:#64748b;'>{desc}</p></div>", unsafe_allow_html=True)

    # --- 2. تحليل الأداء الحقيقي (12 ربعاً) ---
    st.markdown("<div class='section-title'>2. تحليل الأداء (مسار الإيرادات التاريخي)</div>", unsafe_allow_html=True)
    c2_l, c2_r = st.columns([2, 1])
    with c2_l:
        # رسم بياني للإيرادات لآخر 12 ربعاً (أو المتوفر)
        rev_history = fin.loc['Total Revenue'][::-1]
        fig = go.Figure(data=[go.Bar(x=rev_history.index.astype(str), y=rev_history.values, marker_color='#2b6cb0')])
        fig.update_layout(title="تطور الإيرادات الربعية الحقيقي", height=400, plot_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)
    with c2_r:
        growth_rate = ((rev_history.iloc[-1] / rev_history.iloc) - 1) * 100
        st.info(f"**ملخص النمو الربع سنوي:**\nتغيرت الإيرادات بنسبة **{growth_rate:.1f}%** بين أول ربع وآخر ربع في السلسلة الزمنية المتاحة.")

    # --- 7. التوصية الاستراتيجية ---
    st.markdown("<div class='section-title'>7. توصية مدير المحفظة (CFA3 Strategy)</div>", unsafe_allow_html=True)
    rec_l, rec_r = st.columns(2)
    with rec_l:
        st.success(f"🎯 **استراتيجية التجميع:** الشراء التدريجي قرب مستويات **{curr_price*0.95:.2f} ريال** (بناءً على سعر إغلاق اليوم).")
    with rec_r:
        st.error(f"🛑 **إدارة المخاطر:** وقف الخسارة عند كسر **{curr_price*0.88:.2f} ريال** (تحليل الحساسية بنسبة 12%).")

except Exception as e:
    st.error(f"حدث خطأ أثناء جلب البيانات لـ {symbol_input}. يرجى التأكد من الرمز. (الخطأ: {e})")
