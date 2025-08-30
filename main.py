from FiinQuantX import FiinSession, RealTimeData
import pandas as pd
import numpy as np
import talib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import requests as rq
import time
import os
import urllib3
import logging
from dotenv import load_dotenv
import os
import sys

load_dotenv('.env')

username = os.getenv('username_h')
password = os.getenv('password')

print(username, password)

client = FiinSession(username=username, password=password).login()

tickers = ['HPG', 'SSI', 'VN30F1M', 'UPCOMINDEX']
    
data = client.Fetch_Trading_Data(
    realtime = False,
    tickers = tickers,    
    fields = ['open', 'high', 'low', 'close', 'volume', 'bu', 'sd', 'fb', 'fs', 'fn'],
    adjusted=True,
    by = '1m', 
    from_date='2024-11-28 09:00',
).get_data()

print(data)