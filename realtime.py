from FiinQuantX import FiinSession, RealTimeData
import pandas as pd
import numpy as np
import talib
from dotenv import load_dotenv
import os
import time



load_dotenv('.env')

username = os.getenv('username_h')
password = os.getenv('password')

client = FiinSession(username=username, password=password).login()

def OnTickerEvent(data: RealTimeData):
    print(data.to_dataFrame())


event = client.Trading_Data_Stream(
    tickers=['ACB', 'HPG', 'SSI', 'VN30F1M', 'UPCOMINDEX'],
    callback= OnTickerEvent
)


event.start()

try: 
    while not event._stop:
        time.sleep(1)
except KeyboardInterrupt:
    event.stop()
    print("Stopped by user")