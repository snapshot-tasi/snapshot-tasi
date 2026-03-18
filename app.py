class UniversalMarketAnalyzer:
    def __init__(self, ticker, sector, financials):
        self.ticker = ticker
        self.sector = sector
        self.data = financials # البيانات: P/E, D/E, ROE, Current_Ratio, etc.

    def analyze_sector_specifics(self):
        """تطبيق قواعد الـ CFA حسب نوع القطاع"""
        
        # 1. قطاع الطاقة والبتروكيماويات (مثل أرامكو، سابك)
        if self.sector == "Energy" or self.sector == "Petrochemicals":
            debt_threshold = 40  # مديونية مقبولة حتى 40%
            key_metric = "Cash_Flow_Stability"
            status = "High" if self.data['D_E'] < debt_threshold else "Warning"
            insight = f"في قطاع الطاقة، مديونية {self.data['D_E']}% تعتبر {status} نظراً لحجم الأصول الرأسمالية."

        # 2. قطاع البنوك والخدمات المالية (مثل الراجحي، الأهلي)
        elif self.sector == "Banking":
            # في البنوك لا نستخدم D/E بل نستخدم معدل كفاية رأس المال (CAR)
            car_ratio = self.data.get('CAR', 15)
            status = "Strong" if car_ratio > 12 else "Weak"
            insight = f"معدل كفاية رأس المال {car_ratio}% يشير إلى ملاءة {status} وقدرة عالية على الإقراض."

        # 3. قطاع التكنولوجيا والنمو (مثل علم، حلول)
        elif self.sector == "Technology":
            # نركز على مكرر الربحية للنمو (PEG) بدلاً من P/E العادي
            peg = self.data['PE'] / self.data.get('Growth_Rate', 1)
            status = "Attractive" if peg < 1.5 else "Expensive"
            insight = f"مكرر PEG عند {peg} يوضح ما إذا كان السعر يسبق النمو المتوقع أم يواكبه."

        # 4. قطاع التجزئة والاستهلاك (مثل جرير)
        else:
            # نركز على العائد على حقوق المساهمين (ROE) وكفاءة التشغيل
            roe = self.data.get('ROE', 0)
            status = "Excellent" if roe > 20 else "Average"
            insight = f"عائد حقوق المساهمين {roe}% يعكس كفاءة الإدارة في استغلال رأس المال."

        return {"Insight": insight, "Status": status}

    def generate_snapshot_report(self):
        """توليد النقاط العشر (Snapshot) بشكل آلي مخصص"""
        sector_analysis = self.analyze_sector_specifics()
        
        report = {
            "Ticker": self.ticker,
            "Sector": self.sector,
            "Financial_Health": sector_analysis['Status'],
            "Strategic_Review": sector_analysis['Insight'],
            "Decision_Support": "تجميع/شراء" if sector_analysis['Status'] in ["High", "Strong", "Attractive"] else "انتظار/مراقبة"
        }
        return report

# --- أمثلة تشغيلية للمحرك ---

# 1. تحليل أرامكو (طاقة)
aramco = UniversalMarketAnalyzer("ARAMCO", "Energy", {"PE": 17.9, "D_E": 23.5})
print(f"تحليل أرامكو: {aramco.generate_snapshot_report()}\n")

# 2. تحليل بنك (بنوك) - لاحظ تغير المنطق
bank_x = UniversalMarketAnalyzer("RAJHI", "Banking", {"CAR": 19.5})
print(f"تحليل الراجحي: {bank_x.generate_snapshot_report()}\n")

# 3. تحليل شركة نمو (تكنولوجيا)
tech_co = UniversalMarketAnalyzer("ELM", "Technology", {"PE": 35, "Growth_Rate": 25})
print(f"تحليل علم: {tech_co.generate_snapshot_report()}")
