from FiinQuantX import FiinSession, RealTimeData
import pandas as pd
import numpy as np
import talib
from dotenv import load_dotenv
import os


load_dotenv('.env')

username = os.getenv('username_h')
password = os.getenv('password')

client = FiinSession(username=username, password=password).login()


fi = client.FiinIndicator()


data = client.Fetch_Trading_Data(
    realtime = False,
    tickers=['ACB', 'HPG', 'SSI', 'VN30F1M', 'UPCOMINDEX'],    
    fields = ['open', 'high', 'low', 'close', 'volume', 'bu', 'sd', 'fb', 'fs', 'fn'],
    adjusted=True, # Thị trường ck hay có giá điều chỉnh True để lấy
    by = '1m',
    # from_date='2021-01-01 09:00',
    # to_date='2024-11-28 15:00'       
    period=10 # 10 phiên giao dịch gần nhất
).get_data()


data['rsi'] = fi.rsi(data['close'], window = 14) #length=20, momentum=5)
data['atr'] = fi.atr(data['high'], data['low'], data['close'])
data['sma'] = fi.sma(data['close'], window=30)
data['ema'] = fi.ema(data['close'], window=30)
data['wma'] = fi.wma(data['close'], window=30)
data['macd'] = fi.macd(data['close'])
data['psar'] = fi.psar(data['high'], data['low'], data['close'], step = 0.02, max_step = 0.2)
data['cci'] = fi.cci(data['high'], data['low'], data['close'])
data['aroon'] = fi.aroon(data['high'], data['low'], window=14)
data['zigzag'] = fi.zigzag(data['high'], data['low'], dev_threshold=5, depth=10)
data['Stochastic'] = fi.stoch(data['high'], data['low'], data['close'])
data['atr'] = fi.atr(data['high'], data['low'], data['close'], window=14)
data['mfi'] = fi.mfi(data['high'], data['low'], data['close'], data['volume'], window=14)
data['obv'] = fi.obv(data['close'], data['volume'])
data['vwap'] = fi.vwap(data['high'], data['low'], data['close'], data['volume'])
data['fvg'] = fi.fvg(data['high'], data['low'], data['close'], data['volume'])
data['swing_HL'] = fi.swing_HL(data['open'],data['high'], data['low'], data['close'], swing_length = 50)
data['break_of_structure'] = fi.break_of_structure(data['open'],data['high'], data['low'],data['close'],swing_length=50)
data['chage_of_charactor'] = fi.chage_of_charactor(data['open'],data['high'], data['low'],data['close'])
data['ob'] = fi.ob(data['open'],data['high'], data['low'],data['close'],data['volume'], close_mitigation = False, swing_length = 40)
data['ob_volume'] = fi.ob_volume(data['open'],data['high'], data['low'],data['close'],data['volume'])
data['liquidity'] = fi.liquidity(data['open'],data['high'], data['low'],data['close'])
data['swing_HL'] = fi.swing_HL(data['open'],data['high'], data['low'], data['close'], swing_length = 50)
data['stoch'] = fi.stoch(data['high'], data['low'], data['close'], window=14)
data['stoch_signal'] = fi.stoch_signal(data['high'], data['low'], data['close'], window=14, smooth_window=3)
data['adx'] = fi.adx(data['high'], data['low'], data['close'], window=14)
data['supertrend'] = fi.supertrend(data['high'], data['low'], data['close'], window=14)
data['supertrend_hband'] = fi.supertrend_hband(data['high'], data['low'], data['close'], window=14)
data['supertrend_lband'] = fi.supertrend_lband(data['high'], data['low'], data['close'], window=14)




print(data)     