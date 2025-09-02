from FiinQuantX import FiinSession, FiinIndicator
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import pandas as pd

# Đăng nhập
load_dotenv(dotenv_path=".env")
username = os.getenv("username_h")
password = os.getenv("password")

client = FiinSession(username=username, password=password).login()
fi = client.FiinIndicator()

# Tính ngày bắt đầu và kết thúc
to_date = datetime.now().strftime("%Y-%m-%d")
from_date = (datetime.now() - timedelta(days=3 * 365)).strftime("%Y-%m-%d")

# ==== LẤY DANH SÁCH TẤT CẢ MÃ TRÊN 3 SÀN ====
tickers_hose = client.TickerList(ticker="VNINDEX")._get_data()
tickers_hnx = client.TickerList(ticker="HNXINDEX")._get_data()
tickers_upcom = client.TickerList(ticker="UPCOMINDEX")._get_data()

# Lọc mã có độ dài <= 3 ký tự (loại chỉ số, ETF...)
all_tickers = list(set(filter(lambda item: len(item) <= 3, tickers_hose + tickers_hnx + tickers_upcom)))

print(f"Total tickers fetched: {len(all_tickers)}")

all_data = []  # để gộp tất cả dữ liệu

for ticker in all_tickers:
    try:
        event = client.Fetch_Trading_Data(
            realtime=False,
            tickers=[ticker],
            fields=["open", "high", "low", "close", "volume"],
            adjusted=True,
            by="1d",
            from_date=from_date,
            to_date=to_date
        )
        data = event.get_data()
        df = pd.DataFrame(data)

        if df.empty:
            continue

        df['ticker'] = ticker
        df['year'] = pd.to_datetime(df['timestamp']).dt.year
        df['quarter'] = pd.to_datetime(df['timestamp']).dt.quarter

        # ==== Các chỉ báo kỹ thuật ====
        df['ema20'] = fi.ema(df['close'], window=20)
        df['macd_signal'] = fi.macd_signal(df['close'], window_fast=12, window_slow=26, window_sign=9)
        df['macd'] = fi.macd(df['close'], window_fast=12, window_slow=26)
        df['macd_cross'] = 'neutral'
        df.loc[(df['macd'] > df['macd_signal']) & (df['macd'].shift(1) <= df['macd_signal'].shift(1)), 'macd_cross'] = 'goldencross'
        df.loc[(df['macd'] < df['macd_signal']) & (df['macd'].shift(1) >= df['macd_signal'].shift(1)), 'macd_cross'] = 'deathcross'

        df['ema_strat'] = df["close"] > df["ema20"]
        df['rsi30'] = fi.rsi(df['close'], window=30)
        df['rsi_signal'] = df['rsi30'].apply(lambda x: 'overbought' if x > 70 else ('oversold' if x < 30 else 'neutral'))
        df['sma20'] = fi.sma(df['close'], window=20)
        df['bollinger_hband'] = fi.bollinger_hband(df['close'], window=20, window_dev=2)
        df['bollinger_lband'] = fi.bollinger_lband(df['close'], window=20, window_dev=2)
        df['atr'] = fi.atr(df['high'], df['low'], df['close'], window=14)

        # ==== Các chỉ báo bổ sung ====
        df['rsi'] = fi.rsi(df['close'], window=14)
        df['sma'] = fi.sma(df['close'], window=30)
        df['ema'] = fi.ema(df['close'], window=30)
        df['wma'] = fi.wma(df['close'], window=30)
        df['psar'] = fi.psar(df['high'], df['low'], df['close'], step=0.02, max_step=0.2)
        df['cci'] = fi.cci(df['high'], df['low'], df['close'])
        df['aroon'] = fi.aroon(df['high'], df['low'], window=14)
        df['zigzag'] = fi.zigzag(df['high'], df['low'], dev_threshold=5, depth=10)
        df['stochastic'] = fi.stoch(df['high'], df['low'], df['close'])
        df['mfi'] = fi.mfi(df['high'], df['low'], df['close'], df['volume'], window=14)
        df['obv'] = fi.obv(df['close'], df['volume'])
        df['vwap'] = fi.vwap(df['high'], df['low'], df['close'], df['volume'])
        df['fvg'] = fi.fvg(df['high'], df['low'], df['close'], df['volume'])
        df['swing_HL'] = fi.swing_HL(df['open'], df['high'], df['low'], df['close'], swing_length=50)
        df['break_of_structure'] = fi.break_of_structure(df['open'], df['high'], df['low'], df['close'], swing_length=50)
        df['chage_of_charactor'] = fi.chage_of_charactor(df['open'], df['high'], df['low'], df['close'])
        df['ob'] = fi.ob(df['open'], df['high'], df['low'], df['close'], df['volume'], close_mitigation=False, swing_length=40)
        df['ob_volume'] = fi.ob_volume(df['open'], df['high'], df['low'], df['close'], df['volume'])
        df['liquidity'] = fi.liquidity(df['open'], df['high'], df['low'], df['close'])
        df['stoch'] = fi.stoch(df['high'], df['low'], df['close'], window=14)
        df['stoch_signal'] = fi.stoch_signal(df['high'], df['low'], df['close'], window=14, smooth_window=3)
        df['adx'] = fi.adx(df['high'], df['low'], df['close'], window=14)
        df['supertrend'] = fi.supertrend(df['high'], df['low'], df['close'], window=14)
        df['supertrend_hband'] = fi.supertrend_hband(df['high'], df['low'], df['close'], window=14)
        df['supertrend_lband'] = fi.supertrend_lband(df['high'], df['low'], df['close'], window=14)

        all_data.append(df)

    except Exception as e:
        print(f"⚠️ Lỗi khi lấy dữ liệu cho {ticker}: {e}")
        continue

# Gộp tất cả lại thành 1 DataFrame
if all_data:
    final_df = pd.concat(all_data, ignore_index=True)
    os.makedirs("csv", exist_ok=True)
    final_df.to_csv("csv/data_all_tickers.csv", index=False)
    print(f"✅ Đã lưu dữ liệu cho {len(all_tickers)} mã vào csv/data_all_tickers.csv")
else:
    print("⚠️ Không lấy được dữ liệu cho mã nào!")




# from FiinQuantX import FiinSession, FiinIndicator
# from datetime import datetime, timedelta
# import os
# import json
# from dotenv import load_dotenv
# import time
# import pandas as pd

# # Đăng nhập
# load_dotenv(dotenv_path=".env")
# username = os.getenv("username_h")
# password = os.getenv("password")

# client = FiinSession(
#     username=username,
#     password=password,
# ).login()

# # Tính ngày bắt đầu và kết thúc
# to_date = datetime.now().strftime("%Y-%m-%d")
# from_date = (datetime.now() - timedelta(days=3*365)).strftime("%Y-%m-%d")

# tick = "VN30"

# VN_30 = ['STB', 'VIC', 'DGC', 'SAB', 'ACB', 'BCM', 'MSN', 'CTG', 'GVR', 'MWG', 'VIB', 'VNM', 'HPG', 'VPB', 'VCB', 'LPB', 'TPB', 'MBB', 'HDB', 'FPT', 'VRE', 'TCB', 'BID', 'VHM', 'SHB', 'VJC', 'SSB', 'GAS', 'PLX', 'SSI']

# tickers_hose = client.TickerList(ticker="VNINDEX")._get_data()
# tickers_hnx = client.TickerList(ticker="HNXINDEX")._get_data()
# tickers_upcom = client.TickerList(ticker="UPCOMINDEX")._get_data()

# all_tickers = list(set(filter(lambda item: len(item) <= 3, tickers_hose + tickers_hnx)))

# # Gọi dữ liệu lịch sử
# for i in VN_30:
#     event = client.Fetch_Trading_Data(
#         realtime=False,
#         tickers=[i],
#         fields=["open", "high", "low", "close", "volume"],
#         adjusted=True,
#         by="1d",
#         from_date=from_date,
#         to_date=to_date
#     )
#     data = event.get_data()
#     df = pd.DataFrame(data)
#     # print(i)
#     df['ticker'] = i
#     # df.set_index(['ticker'], inplace=True)
#     df['year'] = pd.to_datetime(df['timestamp']).dt.year
#     df['quarter'] = pd.to_datetime(df['timestamp']).dt.quarter
#     fi = client.FiinIndicator()

#     df['ema20'] =+ fi.ema(df['close'], window=20)
#     df['macd_signal'] = fi.macd_signal(df['close'], window_fast=12, window_slow=26, window_sign=9)
#     df['macd'] = fi.macd(df['close'], window_fast=12, window_slow=26)
#     df['macd_cross'] = 'neutral'

#     # Golden cross (MACD cắt lên Signal)
#     df.loc[(df['macd'] > df['macd_signal']) & (df['macd'].shift(1) <= df['macd_signal'].shift(1)), 'macd_cross'] = 'goldencross'

#     # Death cross (MACD cắt xuống Signal)
#     df.loc[(df['macd'] < df['macd_signal']) & (df['macd'].shift(1) >= df['macd_signal'].shift(1)), 'macd_cross'] = 'deathcross'

#     df['ema_strat'] = df["close"] > df["ema20"]
#     df['rsi30'] = fi.rsi(df['close'], window=30)
#     df['rsi_signal'] = df['rsi30'].apply(lambda x: 'overbought' if x > 70 else ('oversold' if x < 30 else 'neutral'))
#     df['sma20'] = fi.sma(df['close'], window=20)
#     df['bollinger_hband'] = fi.bollinger_hband(df['close'], window=20, window_dev=2)
#     df['bollinger_lband'] = fi.bollinger_lband(df['close'], window=20, window_dev=2)
#     df['atr'] = fi.atr(df['high'], df['low'], df['close'], window=14)
#     df['tp'] = df['high'].rolling(20).max().shift()
#     df['sl'] = df['low'].rolling(20).min().shift()



#     # print(df)
#     df.to_csv(f"csv/data_{i}_1d.csv", index=False)

# # print(f"Total tickers with volume >= 200000: {cnt}")