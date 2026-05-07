import yfinance as yf
import pandas_ta as ta
import pandas as pd
import numpy as np

def analyze_market(symbol="GC=F"): # GC=F هو رمز الذهب، يمكن تغييره لـ EURUSD=X
    print(f"--- جاري تحليل زوج: {symbol} ---")
    
    # 1. جلب البيانات (إطار 15 دقيقة للسكالبينج أو ساعة للتحليل اليومي)
    data = yf.download(symbol, period="5d", interval="15m", progress=False)
    
    if data.empty:
        print("فشل في جلب البيانات.")
        return

    # 2. حساب المؤشرات الفنية القوية
    # مؤشر RSI لمعرفة مناطق التشبع
    data['RSI'] = ta.rsi(data['Close'], length=14)
    # مؤشر ATR لتحديد الأهداف بدقة بناءً على حركة السعر
    data['ATR'] = ta.atr(data['High'], data['Low'], data['Close'], length=14)
    
    # 3. تحديد مستويات SNR (الدعم والمقاومة)
    last_lows = data['Low'].tail(20)
    last_highs = data['High'].tail(20)
    
    support = last_lows.min()
    resistance = last_highs.max()
    current_price = data['Close'].iloc[-1]
    
    # 4. حساب الأهداف (Targets)
    # الهدف الأول: 1.5 ضعف الـ ATR
    # الهدف الثاني: 3 أضعاف الـ ATR
    atr_value = data['ATR'].iloc[-1]
    target_buy = current_price + (atr_value * 2)
    target_sell = current_price - (atr_value * 2)

    # 5. منطق التحليل والقوة
    print(f"السعر الحالي: {current_price:.2f}")
    print(f"دعم قريب (Support): {support:.2f}")
    print(f"مقاومة قريبة (Resistance): {resistance:.2f}")
    print("-" * 30)

    if current_price <= support * 1.001: # قريب من الدعم
        print("إشارة: منطقة شراء محتملة (ارتداد من دعم)")
        print(f"الهدف المقترح (TP): {target_buy:.2f}")
    elif current_price >= resistance * 0.999: # قريب من المقاومة
        print("إشارة: منطقة بيع محتملة (ارتداد من مقاومة)")
        print(f"الهدف المقترح (TP): {target_sell:.2f}")
    else:
        print("الحالة: السعر في منطقة تعادل (انتظر الوصول لمناطق السيولة)")

    print(f"قوة الاتجاه (RSI): {data['RSI'].iloc[-1]:.2f}")
    print("-" * 30)

# تشغيل المحلل
if __name__ == "__main__":
    analyze_market("GC=F") # للذهب
    # analyze_market("EURUSD=X") # للفوركس
