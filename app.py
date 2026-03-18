import streamlit as st
import yfinance as yf
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="Snapshot-Tasi", layout="wide", page_icon="📊")

# 2. تصميم الواجهة
st.title("🔍 Snapshot-Tasi")
st.subheader("منصة تحليل الأسهم السعودية (TASI)")

# 3. اختيار الشركة
symbol = st.sidebar.text_input("أدخل رمز الشركة (مثال: 2222):", "2222")
ticker_symbol = f"{symbol}.SR"

# 4. جلب البيانات
@st.cache_data(ttl=3600)
def load_data(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    # جلب القوائم المالية
    fin = stock.quarterly_financials
    cash = stock.quarterly_cashflow
    return info, fin, cash

try:
    info, fin, cash = load_data(ticker_symbol)
    
    # 5. عرض المقاييس الرئيسية
    st.header(f"شركة: {info.get('longName', 'المختارة')}")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("السعر الحالي", f"{info.get('currentPrice')} ريال")
    m2.metric("P/E Ratio", f"{round(info.get('trailingPE', 0), 2)}")
    m3.metric("مضاعف القيمة الدفترية", f"{round(info.get('priceToBook', 0), 2)}")
    m4.metric("العائد على التوزيعات", f"{info.get('dividendYield', 0)*100:.2f}%")

    # 6. تحليل جودة الأرباح (CFA Insight)
    st.divider()
    st.subheader("💡 جودة الأرباح (Earnings Quality)")
    
    # مقارنة صافي الربح بالتدفق النقدي
    net_income = fin.loc['Net Income'].iloc[0]
    op_cash = cash.loc['Operating Cash Flow'].iloc[0]
    
    col_a, col_b = st.columns(2)
    col_a.info(f"صافي الربح المعلن: {net_income:,.0f}")
    col_b.success(f"التدفق النقدي التشغيلي: {op_cash:,.0f}")
    
    if op_cash > net_income:
        st.write("✅ **الأرباح ذات جودة عالية:** الشركة تحول أرباحها المحاسبية إلى سيولة حقيقية.")
    else:
        st.warning("⚠️ **تنبيه:** التدفق النقدي أقل من الربح المحاسبي، قد توجد مستحقات غير محصلة.")

except Exception as e:
    st.error("يرجى إدخال رمز شركة صحيح من تداول (مثل 2222، 1120).")
