from FiinQuantX import FiinSession, RealTimeData
import pandas as pd
import numpy as np
import talib
from dotenv import load_dotenv
import os
import json 


load_dotenv('.env')

username = os.getenv('username_h')
password = os.getenv('password')

client = FiinSession(username=username, password=password).login()

tickers = ['HPG']

fs_dict = client.FundamentalAnalysis().get_financeStatement(
    tickers=tickers,
    statement="balancesheet",
    years=[2024],
    quarters=[4],
    audited=True,
    type="consolidated",
    fields=["Assets"]
)

print(json.dumps(fs_dict, indent=4))
