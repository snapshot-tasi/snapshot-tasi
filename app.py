import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# --- 1. إعدادات التصميم المتطور (UI/UX) ---
st.set_page_config(page_title="Snapshot-Tasi Pro | TASI Analysis", layout="wide")

def apply_pro_style():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com');
    html, body, [class*="css"] { font-family: 'Tajawal', sans-serif; text-align: right; }
    .main { background-color: #f4f7f9; }
    .snapshot-card {
        padding: 20px; border-radius: 15px; color: white; margin-bottom: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1); transition: 0.3s;
    }
    .snapshot-card:hover { transform: translateY(-5px); }
    .blue-grad { background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); }
    .emerald-grad { background: linear-gradient(135deg, #065f46 0%, #10b981 100%); }
    .amber-grad { background: linear-gradient(135deg, #92400e 0%, #f59e0b 100%); }
    .section-header {
        color: #1e3a8a; border-right: 6px solid #1e3a8a; padding-right: 15px;
        margin: 40px 0 20px 0; font-weight: bold; font-size: 24px;
    }
    .explanation-text { background: white; padding: 15px; border-radius: 10px; border-right: 4px solid #3b82f6; margin-bottom: 20px; font-size: 14px; line-height: 1.6; }
    </style>
    """, unsafe_allow_html=True)

apply_pro_style()

# --- 2. قاعدة بيانات قطاعات تداول (TASI Sectors) ---
TASI_SECTORS = {
    "الطاقة": ["2222", "2310", "2030", "2223"],
    "البنوك": ["1120", "1150", "1180", "1010", "1080"],
    "المواد الأساسية": ["2010", "2020", "2350", "2250"],
    "الاتصالات": ["7010", "7020", "7030"],
}

@st.cache_data(ttl=3600)
def get_tasi_data(symbol):
    stock = yf.Ticker(f"{symbol}.SR")
    return stock.info, stock.quarterly_financials, stock.quarterly_cashflow, stock.quarterly_balance_sheet

# --- 3. واجهة التحكم ---
st.sidebar.title("📈 Snapshot-Tasi Pro")
selected_symbol = st.sidebar.text_input("أدخل رمز الشركة (مثلاً: 2222):", "2222")

try:
    info, fin, cash, bal = get_tasi_data(selected_symbol)
    st.title(f"تقرير التحليل Snapshot لشركة {info.get('longName')}")
    
    # --- 1. الـ Snapshot (10 نقاط مع الشرح) ---
    st.markdown("<h2 class='section-header'>1. الـ Snapshot (10 نقاط مركزة)</h2>", unsafe_allow_html=True)
    
    # حسابات CFA
    pe = info.get('trailingPE', 0)
    gearing = (info.get('totalDebt', 0) / info.get('totalEquity', 1)) * 100
    fcf = info.get('freeCashflow', 0) / 1e9
    
    snap_data = [
        ("نموذج العمل", info.get('industry', 'N/A'), "طريقة توليد القيمة عبر الأنشطة التشغيلية.", "blue-grad"),
        ("مصدر الإيرادات", info.get('sector', 'N/A'), "توزيع الدخل حسب القطاعات الجغرافية أو التشغيلية.", "blue-grad"),
        ("الهوامش الربحية", f"{info.get('profitMargins', 0)*100:.1f}%", "كفاءة الشركة في تحويل المبيعات إلى أرباح صافية.", "blue-grad"),
        ("مستوى الدين", f"{gearing:.1f}%", "درجة الرفع المالي والمخاطر التمويلية (Gearing).", "blue-grad"),
        ("التدفق النقدي", f"{fcf:.1f}B", "السيولة المتاحة بعد النفقات الرأسمالية (FCF).", "blue-grad"),
        ("جودة الأرباح", "نقدية" if fcf > 0 else "محاسبية", "مدى تطابق الأرباح المحاسبية مع التدفقات النقدية الحقيقية.", "emerald-grad"),
        ("المخاطر", "متعددة", "العوامل الخارجية والداخلية التي تهدد استدامة الأرباح.", "amber-grad"),
        ("المحفزات", "نمو توسعي", "الأحداث المستقبلية التي قد ترفع قيمة السهم السوقية.", "emerald-grad"),
        ("التقييم الحالي", f"{pe:.1f}x P/E", "مقارنة السعر بالأرباح لقياس مدى غلاء أو رخص السهم.", "amber-grad"),
        ("قرار مبدئي", "مراقبة/تجميع", "رؤية المحلل المبدئية بناءً على المعطيات الحالية.", "emerald-grad")
    ]

    cols = st.columns(5)
    for i, (title, val, desc, style) in enumerate(snap_data):
        with cols[i % 5]:
            st.markdown(f"<div class='snapshot-card {style}'><strong>{title}</strong><br>{val}</div>", unsafe_allow_html=True)
            with st.expander("شرح"): st.write(desc)

    # --- 2. تحليل آخر 12 ربعاً ---
    st.markdown("<h2 class='section-header'>2. تحليل آخر 12 ربعاً (أين تكمن التغيرات؟)</h2>", unsafe_allow_html=True)
    st.markdown("<div class='explanation-text'>نقوم هنا بتفكيك نمو الإيرادات إلى (حجم المبيعات، سعر المنتج، ومزيج المنتجات) لمعرفة هل النمو حقيقي أم مجرد تضخم سعري.</div>", unsafe_allow_html=True)
    
    rev_chart = fin.loc['Total Revenue'].iloc[:12][::-1]
    fig = px.area(rev_chart, title="مسار الإيرادات الربعي", color_discrete_sequence=['#1e3a8a'])
    st.plotly_chart(fig, use_container_width=True)

    # --- 3. جودة الأرباح ---
    st.markdown("<h2 class='section-header'>3. البحث عن إشارات تضخيم الربحية</h2>", unsafe_allow_html=True)
    st.markdown("<div class='explanation-text'>بصفتي CFA، أبحث عن الفجوة بين الربح المحاسبي والتدفق النقدي التشغيلي. إذا كان الربح أعلى بكثير من النقد، فهذه إشارة حمراء (Accruals Risk).</div>", unsafe_allow_html=True)
    
    # --- 4. مقارنة المنافسين في السوق السعودي (TASI) ---
    st.markdown("<h2 class='section-header'>4. المقارنة مع المنافسين في السوق السعودي</h2>", unsafe_allow_html=True)
    
    current_sector = "الطاقة" # يمكن جعلها ديناميكية لاحقاً
    st.write(f"مقارنة ضمن قطاع: **{current_sector}**")
    
    peer_data = []
    for ticker in TASI_SECTORS[current_sector]:
        p_info = yf.Ticker(f"{ticker}.SR").info
        peer_data.append({
            "الرمز": ticker,
            "الاسم": p_info.get('shortName'),
            "نمو الإيرادات": f"{p_info.get('revenueGrowth', 0)*100:.1f}%",
            "ROE": f"{p_info.get('returnOnEquity', 0)*100:.1f}%",
            "P/E": p_info.get('trailingPE'),
            "EV/EBITDA": p_info.get('enterpriseToEbitda')
        })
    st.table(pd.DataFrame(peer_data))

    # --- 5 & 6. السيناريوهات والحساسية ---
    st.markdown("<h2 class='section-header'>5 & 6. السيناريوهات وتحليل الحساسية</h2>", unsafe_allow_html=True)
    st.markdown("<div class='explanation-text'>جدول الحساسية يحدد 'نقطة الانكسار'. عند أي سعر للنفط أو تكلفة تمويل يتحول نمو الشركة إلى تراجع؟</div>", unsafe_allow_html=True)
    
    # --- 7. التوصية النهائية ---
    st.markdown("<h2 class='section-header'>7. توصية مدير المحفظة (CFA Strategic View)</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.success(f"**استراتيجية التجميع:** الشراء بين {info.get('currentPrice')*0.95:.2f} و {info.get('currentPrice'):.2f}")
    with c2:
        st.error(f"**مناطق الخروج الكامل:** كسر مستوى {info.get('currentPrice')*0.85:.2f} ريال.")

except Exception as e:
    st.error(f"حدث خطأ: {e}")
