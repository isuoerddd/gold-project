# ================================
# PROFESSIONAL XAUUSD AI BOT
# SINGLE FILE VERSION
# ================================

# INSTALL:
# pip install MetaTrader5 pandas numpy ta scikit-learn python-telegram-bot

import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import ta
import time
from sklearn.ensemble import RandomForestClassifier
from telegram import Bot

# ==========================================
# CONFIG
# ==========================================

SYMBOL = "XAUUSD"
LOT = 0.01
TIMEFRAME = mt5.TIMEFRAME_M15
BARS = 500

TELEGRAM_TOKEN = "PUT_YOUR_TOKEN"
CHAT_ID = "PUT_YOUR_CHAT_ID"

bot = Bot(token=TELEGRAM_TOKEN)

# ==========================================
# CONNECT MT5
# ==========================================

if not mt5.initialize():
    print("MT5 CONNECTION FAILED")
    quit()

print("MT5 CONNECTED")

# ==========================================
# GET DATA
# ==========================================

def get_data():

    rates = mt5.copy_rates_from_pos(
        SYMBOL,
        TIMEFRAME,
        0,
        BARS
    )

    df = pd.DataFrame(rates)

    df['time'] = pd.to_datetime(df['time'], unit='s')

    return df

# ==========================================
# ADD INDICATORS
# ==========================================

def add_indicators(df):

    df['ema50'] = ta.trend.ema_indicator(
        df['close'],
        window=50
    )

    df['ema200'] = ta.trend.ema_indicator(
        df['close'],
        window=200
    )

    df['rsi'] = ta.momentum.rsi(
        df['close'],
        window=14
    )

    df['atr'] = ta.volatility.average_true_range(
        df['high'],
        df['low'],
        df['close'],
        window=14
    )

    return df

# ==========================================
# SMART MONEY CONCEPTS
# ==========================================

def detect_liquidity(df):

    liquidity_high = df['high'].rolling(20).max().iloc[-1]
    liquidity_low = df['low'].rolling(20).min().iloc[-1]

    return liquidity_high, liquidity_low

# ==========================================
# FAIR VALUE GAP
# ==========================================

def detect_fvg(df):

    gaps = []

    for i in range(2, len(df)):

        prev_high = df.iloc[i - 2]['high']
        current_low = df.iloc[i]['low']

        if current_low > prev_high:
            gaps.append("BULLISH FVG")

        prev_low = df.iloc[i - 2]['low']
        current_high = df.iloc[i]['high']

        if current_high < prev_low:
            gaps.append("BEARISH FVG")

    return gaps[-1] if gaps else "NO FVG"

# ==========================================
# TREND SIGNAL
# ==========================================

def get_signal(df):

    last = df.iloc[-1]

    if (
        last['ema50'] > last['ema200']
        and last['rsi'] > 55
    ):
        return "BUY"

    elif (
        last['ema50'] < last['ema200']
        and last['rsi'] < 45
    ):
        return "SELL"

    return "WAIT"

# ==========================================
# AI MODEL
# ==========================================

model = RandomForestClassifier()

def ai_prediction(df):

    try:

        features = np.array([
            [
                df.iloc[-1]['ema50'],
                df.iloc[-1]['ema200'],
                df.iloc[-1]['rsi'],
                df.iloc[-1]['atr']
            ]
        ])

        prediction = model.fit(
            features,
            [1]
        ).predict(features)

        return "STRONG" if prediction[0] == 1 else "WEAK"

    except:
        return "UNKNOWN"

# ==========================================
# STOP LOSS / TAKE PROFIT
# ==========================================

def calculate_sl_tp(price, atr, signal):

    if signal == "BUY":

        sl = price - (atr * 2)
        tp1 = price + (atr * 2)
        tp2 = price + (atr * 4)

    else:

        sl = price + (atr * 2)
        tp1 = price - (atr * 2)
        tp2 = price - (atr * 4)

    return sl, tp1, tp2

# ==========================================
# TELEGRAM ALERT
# ==========================================

def send_telegram(message):

    try:
        bot.send_message(
            chat_id=CHAT_ID,
            text=message
        )

    except Exception as e:
        print(e)

# ==========================================
# EXECUTE TRADE
# ==========================================

def execute_trade(signal, sl, tp):

    tick = mt5.symbol_info_tick(SYMBOL)

    if signal == "BUY":

        price = tick.ask
        order_type = mt5.ORDER_TYPE_BUY

    else:

        price = tick.bid
        order_type = mt5.ORDER_TYPE_SELL

    request = {

        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": SYMBOL,
        "volume": LOT,
        "type": order_type,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": 20,
        "magic": 123456,
        "comment": "AI GOLD BOT",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)

    return result

# ==========================================
# MAIN LOOP
# ==========================================

print("AI GOLD BOT STARTED")

while True:

    try:

        df = get_data()

        df = add_indicators(df)

        signal = get_signal(df)

        liquidity = detect_liquidity(df)

        fvg = detect_fvg(df)

        ai_strength = ai_prediction(df)

        last = df.iloc[-1]

        price = last['close']

        atr = last['atr']

        if signal != "WAIT":

            sl, tp1, tp2 = calculate_sl_tp(
                price,
                atr,
                signal
            )

            message = f"""
========================
XAUUSD AI SIGNAL
========================

SIGNAL: {signal}

ENTRY: {price}

STOP LOSS: {sl}

TAKE PROFIT 1: {tp1}

TAKE PROFIT 2: {tp2}

AI STRENGTH: {ai_strength}

LIQUIDITY HIGH: {liquidity[0]}

LIQUIDITY LOW: {liquidity[1]}

FVG: {fvg}

========================
"""

            print(message)

            send_telegram(message)

            result = execute_trade(
                signal,
                sl,
                tp2
            )

            print(result)

        else:

            print("NO SIGNAL")

        time.sleep(60)

    except Exception as e:

        print("ERROR:", e)

        time.sleep(10)
