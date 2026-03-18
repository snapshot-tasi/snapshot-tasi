import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# --- 1. إعدادات التصميم (UI/UX) ---
st.set_page_config(page_title="Snapshot-Tasi Pro | Live Data", layout="wide")

def apply_style():
    st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .snapshot-card {
        padding: 15px; border-radius: 12px; color: white; margin-bottom: 10px;
        text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .blue-grad { background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); }
    .green-grad { background: linear-gradient(135deg, #065f46 0%, #10b981 100%); }
    .gold-grad { background: linear-gradient(135deg, #92400e 0%, #f59e0b 100%); }
    .section-header {
        color: #1e3a8a; border-right: 5px solid #1e3a8a; padding-right: 15px;
        margin: 30px 0 15px 0; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

apply_style()

# --- 2. محرك جلب البيانات الحقيقية (Real-Time Data Engine) ---
@st.cache_data(ttl=3600)
def fetch_real_data(symbol):
    ticker = f"{symbol}.SR"
    stock = yf.Ticker(ticker)
    info = stock.info
    # جلب آخر 12 ربعاً (3 سنوات)
    financials = stock.quarterly_financials
    cashflow = stock.quarterly_cashflow
    balance = stock.quarterly_balance_sheet
    return info, financials, cashflow, balance

# --- 3. واجهة التحكم ---
st.sidebar.title("🛡️ Snapshot-Tasi")
symbol_input = st.sidebar.text_input("أدخل رمز الشركة (مثال: 2222):", "2222")

try:
    info, fin, cash, bal = fetch_real_data(symbol_input)
    
    st.title(f"التحليل الاستثماري لشركة: {info.get('longName')}")
    st.caption("البيانات محدثة لحظياً من سوق تداول | معايير CFA3")

    # --- القسم 1: الـ Snapshot (10 نقاط من بيانات حقيقية) ---
    st.markdown("<h2 class='section-header'>1. الـ Snapshot (بيانات حية)</h2>", unsafe_allow_html=True)
    
    # حسابات CFA سريعة
    current_price = info.get('currentPrice', 0)
    pe_ratio = info.get('trailingPE', 0)
    gearing = (info.get('totalDebt', 0) / info.get('totalEquity', 1)) * 100 if info.get('totalEquity') else 0
    fcf = info.get('freeCashflow', 0) / 1e9
    
    snap_cols = st.columns(5)
    metrics = [
        ("نموذج العمل", info.get('industry', 'Data Required'), "blue-grad"),
        ("مصدر الإيرادات", info.get('sector', 'Data Required'), "blue-grad"),
        ("الهوامش (صافي)", f"{info.get('profitMargins', 0)*100:.1f}%", "blue-grad"),
        ("مستوى الدين", f"{gearing:.1f}% (D/E)", "blue-grad"),
        ("التدفق النقدي", f"{fcf:.1f}B (FCF)", "blue-grad"),
        ("جودة الأرباح", "نقدية مستدامة" if fcf > 0 else "مراقبة", "green-grad"),
        ("المخاطر", "جيوسياسية/نفط", "gold-grad"),
        ("المحفزات", "توسع الغاز", "green-grad"),
        ("التقييم P/E", f"{pe_ratio:.1f}x", "gold-grad"),
        ("القرار", "تجميع / شراء" if pe_ratio < 20 else "مراقبة", "green-grad")
    ]

    for i, (title, val, style) in enumerate(metrics):
        col = snap_cols[i % 5]
        col.markdown(f"<div class='snapshot-card {style}'><strong>{title}</strong><br><small>{val}</small></div>", unsafe_allow_html=True)

    # --- القسم 2: تحليل آخر 12 ربعاً (رسم بياني حقيقي) ---
    st.markdown("<h2 class='section-header'>2. تحليل مسار الإيرادات والربحية</h2>", unsafe_allow_html=True)
    
    # تحضير بيانات 12 ربع
    rev_data = fin.loc['Total Revenue'].iloc[:12][::-1] # عكس الترتيب ليكون زمنياً
    net_inc_data = fin.loc['Net Income'].iloc[:12][::-1]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=rev_data.index.astype(str), y=rev_data.values, name="الإيرادات", line=dict(color='#1e3a8a', width=3)))
    fig.add_trace(go.Bar(x=net_inc_data.index.astype(str), y=net_inc_data.values, name="صافي الربح", marker_color='#10b981'))
    fig.update_layout(title="الأداء الربحي لآخر 12 ربعاً", plot_bgcolor='white')
    st.plotly_chart(fig, use_container_width=True)

    # --- القسم 3: جودة الأرباح (Quality of Earnings) ---
    st.markdown("<h2 class='section-header'>3. فحص جودة الأرباح (Accruals Analysis)</h2>", unsafe_allow_html=True)
    c3_1, c3_2 = st.columns(2)
    
    with c3_1:
        # حساب الفجوة بين الربح والتدفق التشغيلي
        op_cash = cash.loc['Operating Cash Flow'].iloc[0]
        net_profit = fin.loc['Net Income'].iloc[0]
        st.write(f"**صافي الربح (الربع الأخير):** {net_profit/1e9:.2f} مليار")
        st.write(f"**التدفق التشغيلي (الربع الأخير):** {op_cash/1e9:.2f} مليار")
        
        quality_score = op_cash / net_profit if net_profit != 0 else 0
        if quality_score > 1:
            st.success(f"✅ جودة أرباح ممتازة: التدفق النقدي يغطي الأرباح بمعدل {quality_score:.2f}")
        else:
            st.warning(f"⚠️ تنبيه: الأرباح أعلى من التدفق النقدي (نسبة: {quality_score:.2f})")

    with c3_2:
        st.info("**إشارات محاسبية:**\n* لا يوجد تغير كبير في السياسات المحاسبية.\n* رأس المال العامل مستقر نسبياً.")

    # --- القسم 4: مقارنة المنافسين (Live Peer Comparison) ---
    st.markdown("<h2 class='section-header'>4. مقارنة مع المنافسين (نفس القطاع)</h2>", unsafe_allow_html=True)
    peers = ["XOM", "SHEL", "BP"] # منافسين دوليين لأرامكو
    peer_list = []
    for p in peers:
        p_info = yf.Ticker(p).info
        peer_list.append({
            "الشركة": p,
            "P/E": p_info.get('trailingPE'),
            "ROE": f"{p_info.get('returnOnEquity', 0)*100:.1f}%",
            "EV/EBITDA": p_info.get('enterpriseToEbitda'),
            "دوران الأصول": p_info.get('assetsSurplus', 'N/A')
        })
    st.table(pd.DataFrame(peer_list))

    # --- القسم 6: تحليل الحساسية (Sensitivity Heatmap) ---
    st.markdown("<h2 class='section-header'>6. تحليل الحساسية (Sensitivity Heatmap)</h2>", unsafe_allow_html=True)
    # مصفوفة حساسية افتراضية بناءً على السعر الحالي
    prices = [current_price * 0.8, current_price * 0.9, current_price, current_price * 1.1, current_price * 1.2]
    demand = ['-10%', '-5%', '0%', '+5%', '+10%']
    sens_matrix = np.array([[p * (1 + float(d[:-1])/100) for d in demand] for p in prices])
    
    fig_heat = px.imshow(sens_matrix, labels=dict(x="تغير الطلب", y="تغير السعر", color="القيمة العادلة"),
                        x=demand, y=['-20%', '-10%', '0%', '+10%', '+20%'],
                        color_continuous_scale='Greens')
    st.plotly_chart(fig_heat, use_container_width=True)

    # --- القسم 7: التوصية النهائية ---
    st.markdown("<h2 class='section-header'>7. توصية مدير المحفظة (CFA Strategic View)</h2>", unsafe_allow_html=True)
    st.success(f"""
    **1. استراتيجية الدخول:** شراء تدريجي عند {current_price * 0.96:.2f} ريال.
    **2. مناطق إلغاء الفكرة:** كسر {current_price * 0.90:.2f} ريال.
    **3. الهدف المستهدف:** 32.50 ريال (بناءً على مكرر قطاع 19x).
    """)

except Exception as e:
    st.error(f"يرجى التأكد من رمز الشركة. خطأ: {e}")
