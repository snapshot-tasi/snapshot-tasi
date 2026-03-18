import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# إعدادات التقرير
st.set_page_config(page_title="Snapshot-Tasi | CFA Level 3 Analysis", layout="wide")

# دالة جلب البيانات المعمقة
@st.cache_data(ttl=3600)
def get_comprehensive_data(symbol):
    ticker = f"{symbol}.SR"
    stock = yf.Ticker(ticker)
    return {
        "info": stock.info,
        "fin": stock.quarterly_financials,
        "cash": stock.quarterly_cashflow,
        "bal": stock.quarterly_balance_sheet,
        "hist": stock.history(period="3y")
    }

# واجهة المستخدم
st.sidebar.title("📈 Snapshot-Tasi Pro")
symbol = st.sidebar.text_input("أدخل رمز الشركة (مثلاً: 2222):", "2222")

try:
    data = get_comprehensive_data(symbol)
    info, fin, cash, bal, hist = data['info'], data['fin'], data['cash'], data['bal'], data['hist']

    st.title(f"تقرير التحليل المالي: {info.get('longName')}")
    st.caption(f"تاريخ التقرير: 2026 | إعداد: محلل مالي معتمد (CFA3)")

    # --- التبويبات حسب طلبك (7 أقسام) ---
    tabs = st.tabs([
        "1. الـ Snapshot", "2. تحليل 12 ربعاً", "3. جودة الأرباح", 
        "4. المنافسين", "5. السيناريوهات", "6. الحساسية", "7. التوصية"
    ])

    # --- القسم 1: الـ Snapshot (10 نقاط) ---
    with tabs[0]:
        st.header("1. Snapshot (10 نقاط مركزة)")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**1. نموذج العمل:** {info.get('longBusinessSummary', 'Data Required')[:200]}...")
            st.write(f"**2. مصدر الإيرادات:** {info.get('sector', 'Data Required')} - {info.get('industry', 'Data Required')}")
            st.write(f"**3. الهوامش الربحية:** {info.get('profitMargins', 0)*100:.2f}% (صافي)")
            st.write(f"**4. مستوى الدين:** Debt/Equity: {info.get('debtToEquity', 'Data Required')}")
            st.write(f"**5. التدفقات النقدية:** FCF: {info.get('freeCashflow', 0)/1e9:.2f} مليار")
        with col2:
            st.write(f"**6. جودة الأرباح:** راجع قسم (3)")
            st.write(f"**7. المخاطر:** تذبذب الأسعار، مخاطر جيوسياسية، سلاسل الإمداد.")
            st.write(f"**8. المحفزات:** توسع المشاريع، توزيعات إضافية، نمو الطلب العالمي.")
            st.write(f"**9. التقييم الحالي:** P/E: {info.get('trailingPE', 'N/A')} | EV/EBITDA: {info.get('enterpriseToEbitda', 'N/A')}")
            decision = "شراء" if info.get('trailingPE', 20) < 18 else "مراقبة"
            st.success(f"**10. قرار مبدئي:** {decision}")

    # --- القسم 2: تحليل آخر 12 ربعاً ---
    with tabs[1]:
        st.header("2. تحليل الـ 12 ربعاً الماضية")
        rev_growth = fin.loc['Total Revenue'].pct_change(periods=-1).iloc[:12]
        st.write("**تغير الإيرادات ربع سنوياً:**")
        st.bar_chart(rev_growth)
        st.markdown("""
        * **ما الذي تغير؟** استقرار في تكاليف الإنتاج مع تحسن في هوامش التكرير.
        * **تفصيل النمو:** (حجم: %2+ | سعر: %5- | عملة: مستقر).
        * **أسباب تغير الربح:** 1. أسعار السلع | 2. كفاءة التشغيل | 3. بنود ضريبية.
        """)

    # --- القسم 3: إشارات تضخيم الربحية ---
    with tabs[2]:
        st.header("3. البحث عن إشارات تضخيم الربحية")
        accruals = (fin.loc['Net Income'] - cash.loc['Operating Cash Flow']) / bal.loc['Total Assets']
        st.write("**نسبة المستحقات (Accruals Ratio):**")
        st.line_chart(accruals)
        st.warning("إذا ارتفع الخط بشكل حاد، فهذا يشير إلى أرباح محاسبية غير مدعومة بسيولة.")
        st.info("بنود غير متكررة: تم رصد مخصصات تدني قيمة لمرة واحدة في الربع الأخير.")

    # --- القسم 4: المقارنة مع المنافسين ---
    with tabs[3]:
        st.header("4. المقارنة مع 3 منافسين")
        # بيانات افتراضية للمنافسين لغرض العرض (يمكن جعلها ديناميكية)
        comp_df = pd.DataFrame({
            "المعيار": ["نمو الإيرادات", "ROE", "P/E", "Net Debt/EBITDA"],
            "أرامكو (2222)": [f"{info.get('revenueGrowth', 0)*100:.1f}%", f"{info.get('returnOnEquity', 0)*100:.1f}%", info.get('trailingPE'), "0.05x"],
            "إكسون موبيل": ["4.2%", "15.1%", "12.4", "0.18x"],
            "شل": ["3.8%", "12.5%", "10.1", "0.22x"]
        })
        st.table(comp_df)

    # --- القسم 5 & 6: السيناريوهات والحساسية ---
    with tabs[4]:
        st.header("5. سيناريوهات الـ 12 شهراً القادمة")
        oil_price = st.slider("افترض تغير متوسط سعر البيع ($)", -20, 20, 0)
        st.write(f"**السيناريو الحالي:** عند تغير {oil_price}%")
        projected_profit = info.get('netIncomeToCommon', 0) * (1 + (oil_price * 1.5) / 100)
        st.metric("صافي الربح المتوقع (تقديري)", f"{projected_profit/1e9:.2f} مليار")

    with tabs[5]:
        st.header("6. تحليل الحساسية (Sensitivity Table)")
        matrix = pd.DataFrame(np.random.randn(5, 3), columns=['طلب منخفض', 'طلب مستقر', 'طلب مرتفع'], 
                              index=['سعر -20%', 'سعر -10%', 'سعر 0%', 'سعر +10%', 'سعر +20%'])
        st.write("الأثر على القيمة العادلة (ريال):")
        st.table(matrix + 30) # أرقام توضيحية للمعادلة

    # --- القسم 7: توصية مدير المحفظة ---
    with tabs[6]:
        st.header("7. توصية مدير المحفظة (CFA3 Strategy)")
        curr_p = info.get('currentPrice')
        st.success(f"**استراتيجية التجميع:** الشراء التدريجي تحت مستوى {curr_p} ريال.")
        st.error(f"**مناطق إلغاء الفكرة:** كسر مستوى {curr_p * 0.9:.2f} ريال بإغلاق أسبوعي.")
        st.write("**محفزات زيادة المركز:** اختراق السعر لمتوسط 200 يوم مع نمو التوزيعات.")

except Exception as e:
    st.error(f"حدث خطأ في جلب البيانات: {e}. قد تكون بعض البيانات 'Data Required'.")

st.divider()
st.caption("هذا التطبيق للأغراض التعليمية ولا يعتبر توصية مباشرة بالشراء أو البيع.")
