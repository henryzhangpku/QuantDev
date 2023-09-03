from timeit import default_timer
import datetime
import time
import sys
import pandas as pd


ROOT = './'
inpath = ROOT + 'data/in/'
outpath = ROOT + 'data/out/'
coinbasepath = ROOT + 'coinbase/'
scorepath = outpath + 'score/'


timenow = datetime.datetime.now().strftime('%Y%m%d')

coinbase_url = "https://pro.coinbase.com/trade/"


instrument_config_coinbase = pd.read_csv(
    coinbasepath + 'instrumentconfig.csv', index_col='Instrument')


lhs_window_len = 10
