import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# --- 1. إعدادات الهوية البصرية ---
st.set_page_config(page_title="Snapshot-Tasi Pro | Dynamic Engine", layout="wide")

def apply_ultra_style():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    html, body, [class*="css"] { font-family: 'Noto Kufi Arabic', sans-serif; text-align: right; direction: rtl; }
    .main { background-color: #f8fafc; }
    .header-box { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: white; padding: 2rem; border-radius: 20px; margin-bottom: 2rem; border-right: 10px solid #3b82f6; }
    .card { background: white; padding: 18px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-top: 4px solid #3b82f6; height: 100%; }
    .card-title { color: #1e3a8a; font-weight: 700; font-size: 0.95rem; margin-bottom: 8px; border-bottom: 1px solid #f1f5f9; }
    .card-value { font-size: 1.1rem; font-weight: 700; margin: 8px 0; }
    .card-desc { color: #64748b; font-size: 0.75rem; line-height: 1.4; }
    .pos { color: #10b981; } .neu { color: #f59e0b; } .neg { color: #ef4444; }
    </style>
    """, unsafe_allow_html=True)

apply_ultra_style()

# --- 2. محرك جلب البيانات الذكي ---
@st.cache_data(ttl=3600)
def fetch_dynamic_data(symbol):
    ticker = f"{symbol}.SR"
    stock = yf.Ticker(ticker)
    return stock.info, stock.quarterly_financials, stock.quarterly_cashflow, stock.quarterly_balance_sheet

# --- 3. واجهة التحكم ---
st.sidebar.title("🛡️ Snapshot-Tasi Pro")
symbol_input = st.sidebar.text_input("أدخل رمز السهم (مثلاً: 7010):", "2222")

try:
    info, fin, cash, bal = fetch_dynamic_data(symbol_input)
    st.markdown(f"<div class='header-box'><h1>📊 Snapshot: {info.get('longName')} ({symbol_input})</h1><p>تحليل استراتيجي آلي بناءً على بيانات القطاع الحقيقية | {datetime.now().strftime('%d-%m-%Y')}</p></div>", unsafe_allow_html=True)

    # --- 4. الحسابات المالية (إصلاح الـ Indexing) ---
    # جلب القيم مع التأكد من وجودها وتحويلها لأرقام بسيطة
    def get_val(df, label):
        if label in df.index:
            val = df.loc[label].iloc[0]
            return float(val) if pd.notnull(val) else 0
        return 0

    net_inc = get_val(fin, 'Net Income')
    op_cash = get_val(cash, 'Operating Cash Flow')
    total_debt = get_val(bal, 'Total Debt')
    equity = get_val(bal, 'Stockholders Equity')
    gearing = (total_debt / equity * 100) if equity != 0 else 0
    fcf = info.get('freeCashflow', 0)
    pe_ratio = info.get('trailingPE', 0)
    margin = info.get('profitMargins', 0) * 100

    # --- 5. المنطق الوصفي الديناميكي (إصلاح الخلط بين الشركات) ---
    sector = info.get('sector', 'N/A')
    
    # تحديد المخاطر والمحفزات بناءً على القطاع الحقيقي وليس أرامكو فقط
    if "Energy" in sector:
        risks = "تقلبات أسعار السلع (برنت) والتوترات الجيوسياسية."
        catalysts = "التوسع في إنتاج الغاز ومشروعات الطاقة النظيفة."
    elif "Communication" in sector:
        risks = "المنافسة السعرية الحادة، تغير التنظيمات التقنية، وتكاليف الرخص."
        catalysts = "نمو قطاع البيانات (5G)، التوسع في الحوسبة السحابية، والخدمات المالية."
    elif "Financial" in sector:
        risks = "تغير أسعار الفائدة، مخاطر الائتمان، وتباطؤ القروض."
        catalysts = "التحول الرقمي، نمو التمويل العقاري، وارتفاع صافي هامش الفائدة."
    else:
        risks = "التغيرات في سلاسل الإمداد وتكاليف التشغيل."
        catalysts = "تحسن الكفاءة التشغيلية وزيادة الحصة السوقية."

    # --- عرض الـ Snapshot (10 نقاط) ---
    st.subheader("1. الـ Snapshot (تحليل المعايير العشره)")
    
    snap_config = [
        ("نموذج العمل", "🟢" if "Services" in info.get('industry', '') else "🔵", info.get('industry', 'N/A'), "طريقة الشركة في توليد القيمة ضمن تخصصها التشغيلي."),
        ("مصدر الإيرادات", "🟢", info.get('sector', 'N/A'), "القطاع الرئيسي المحرك للدخل ومدى استدامته."),
        ("الهوامش الربحية", "🟢" if margin > 15 else "🟡", f"{margin:.1f}%", "يقيس قدرة الشركة على تحويل المبيعات لصافي ربح بعد كافة التكاليف."),
        ("مستوى الدين", "🟢" if gearing < 40 else "🔴", f"{gearing:.1f}% (Gearing)", "الرافعة المالية؛ نسبة الديون لحقوق الملكية ومدى الأمان المالي."),
        ("التدفقات النقدية", "🟢" if fcf > 0 else "🔴", f"{fcf/1e9:.2f}B SAR", "السيولة الحقيقية المتبقية للتوزيعات بعد المصاريف الرأسمالية."),
        ("جودة الأرباح", "🟢 عالية" if op_cash > net_inc else "🔴 محاسبية", "نقدية" if op_cash > net_inc else "مستحقات", "مقارنة السيولة بالربح؛ التدفق التشغيلي يغطي الربح بامتياز."),
        ("المخاطر", "🔴 خطر", "مخاطر القطاع", risks),
        ("المحفزات", "🟢 إيجابي", "فرص النمو", catalysts),
        ("التقييم الحالي", "🟡 عادل" if pe_ratio > 15 else "🟢 جذاب", f"{pe_ratio:.1f}x (P/E)", "مكرر الربحية مقارنة بمتوسط القطاع وفرص النمو المستقبلي."),
        ("قرار مبدئي", "🟢 شراء/تجميع" if pe_ratio < 20 else "🟡 مراقبة", "استراتيجي", "رؤية المحرك بناءً على العوائد النقدية المحققة ومكررات الربحية.")
    ]

    for row in range(2):
        cols = st.columns(5)
        for i in range(5):
            idx = row * 5 + i
            title, icon, val, desc = snap_config[idx]
            with cols[i]:
                st.markdown(f"<div class='card'><div class='card-title'>{title}</div><div class='card-value'>{icon} {val}</div><div class='card-desc'>{desc}</div></div>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"يرجى التأكد من الرمز. حدث خطأ في البيانات: {e}")
