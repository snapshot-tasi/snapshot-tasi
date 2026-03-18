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

# --- 2. محرك جلب البيانات اللحظية ---
@st.cache_data(ttl=3600)
def fetch_live_data(symbol):
    ticker = f"{symbol}.SR"
    stock = yf.Ticker(ticker)
    return stock.info, stock.quarterly_financials, stock.quarterly_cashflow, stock.quarterly_balance_sheet, stock.history(period="2y")

# --- 3. واجهة التحكم ---
st.sidebar.title("🛡️ محرك Snapshot-Tasi المباشر")
symbol_input = st.sidebar.text_input("أدخل رمز السهم (مثلاً: 2222 لأرامكو):", "2222")
current_date = datetime.now().strftime("%Y-%m-%d")

try:
    with st.spinner('جاري سحب أحدث البيانات المالية وتدقيقها...'):
        info, fin, cash, bal, hist = fetch_live_data(symbol_input)

    st.markdown(f"<div class='header-box'><h1>🛡️ Snapshot-Tasi: {info.get('longName')} ({symbol_input})</h1><p>تحليل استراتيجي بناءً على بيانات حقيقية بتاريخ اليوم: {current_date}</p></div>", unsafe_allow_html=True)

    # --- تصحيح الحسابات المالية (ضمان قيم رقمية) ---
    curr_price = info.get('currentPrice', 0)
    pe_ratio = info.get('trailingPE', 0)
    
    # حساب نسبة الدين (D/E) - تم إصلاح الفهرسة هنا
    debt = bal.loc['Total Debt'].iloc[0] if 'Total Debt' in bal.index else 0
    equity = bal.loc['Stockholders Equity'].iloc[0] if 'Stockholders Equity' in bal.index else 1
    gearing = (debt / equity) * 100 if equity != 0 else 0
    
    # جودة الأرباح - تم إصلاح الفهرسة هنا
    latest_net_inc = fin.loc['Net Income'].iloc[0] if 'Net Income' in fin.index else 0
    latest_op_cash = cash.loc['Operating Cash Flow'].iloc[0] if 'Operating Cash Flow' in cash.index else 0
    quality_status = 1 if latest_op_cash > latest_net_inc else 3

    # --- 1. الـ Snapshot المحدث ---
    st.markdown("<div class='section-title'>1. الـ Snapshot (تحليل الأرقام الفعلية)</div>", unsafe_allow_html=True)
    
    snap_items = [
        ("نموذج العمل", f"🟢 {info.get('industry', 'N/A')}", "تحليل الأنشطة التشغيلية الحالية للشركة."),
        ("مصدر الإيرادات", f"🟢 {info.get('sector', 'N/A')}", "القطاع الرئيسي الذي يولد الدخل التشغيلي."),
        ("الهوامش الربحية", f"{'🟢' if info.get('profitMargins', 0) > 0.15 else '🟡'} {info.get('profitMargins', 0)*100:.1f}%", "كفاءة تحويل المبيعات لأرباح."),
        ("مستوى الدين", f"{'🟢' if gearing < 40 else '🔴'} {gearing:.1f}% (D/E)", "نسبة المديونية الحقيقية بناءً على الميزانية."),
        ("التدفقات النقدية", f"🟢 {info.get('freeCashflow', 0)/1e9:.2f}B", "التدفق النقدي الحر السنوي المحقق (بالمليار)."),
        ("جودة الأرباح", f"{'🟢 نقدية' if quality_status==1 else '🔴 محاسبية'}", "مقارنة السيولة بالربح لآخر ربع مالي."),
        ("المخاطر", "🟡 مخاطر السوق", "تأثر الشركة بأسعار السلع أو تكلفة التمويل."),
        ("المحفزات", "🟢 نمو استراتيجي", "المشروعات الرأسمالية والتوسعية المعلنة."),
        ("التقييم P/E", f"{'🟢 جذاب' if pe_ratio < 15 else '🟡 عادل'} {pe_ratio:.2f}x", "تقييم السهم بناءً على السعر الحالي والأرباح."),
        ("قرار مبدئي", f"{'🟢 شراء' if pe_ratio < 20 else '🟡 مراقبة'}", "رؤية استثمارية مبدئية بناءً على المعايير.")
    ]

    for row in range(2):
        cols = st.columns(5)
        for i in range(5):
            idx = row * 5 + i
            title, val, desc, status = snap_items[idx]
            val_class = "status-pos" if status == 1 else ("status-neu" if status == 2 else "status-neg")
            with cols[i]:
                st.markdown(f"<div class='snap-card'><div class='snap-title'>{title}</div><div class='snap-value {val_class}'>{val}</div><p style='font-size:0.8rem; color:#64748b;'>{desc}</p></div>", unsafe_allow_html=True)

    # --- 2. تحليل الأداء (12 ربعاً) ---
    st.markdown("<div class='section-title'>2. تحليل الأداء (مسار الإيرادات الحقيقي)</div>", unsafe_allow_html=True)
    rev_hist = fin.loc['Total Revenue'][::-1]
    fig = go.Figure(data=[go.Bar(x=rev_hist.index.astype(str), y=rev_hist.values, marker_color='#2b6cb0')])
    fig.update_layout(title="تطور الإيرادات الربعية", height=400, plot_bgcolor='white')
    st.plotly_chart(fig, use_container_width=True)

    # --- 7. التوصية ---
    st.markdown("<div class='section-title'>7. توصية مدير المحفظة (CFA3 Strategy)</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.success(f"🎯 **استراتيجية التجميع:** شراء قرب مستويات **{curr_price*0.95:.2f} ريال**.")
    c2.error(f"🛑 **إدارة المخاطر:** وقف الخسارة عند كسر **{curr_price*0.88:.2f} ريال**.")

except Exception as e:
    st.error(f"يرجى التأكد من الرمز. حدث خطأ أثناء معالجة البيانات: {e}")
