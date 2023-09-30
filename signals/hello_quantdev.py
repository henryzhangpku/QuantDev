import matplotlib
from global_config import *
matplotlib.use("TkAgg")
"""

Work up a minimum example of a trend following system

"""

"""
Let's create a simple trading rule

No capping or scaling
"""

from sysquant.estimators.vol import robust_vol_calc
from syscore.pandas.pdutils import pd_readcsv


def calc_ewmac_forecast(price, Lfast, Lslow=None):
    """
    Calculate the ewmac trading rule forecast, given a price and EWMA speeds
    Lfast, Lslow and vol_lookback

    """


    price = price.resample("1B").last()

    if Lslow is None:
        Lslow = 4 * Lfast

    # We don't need to calculate the decay parameter, just use the span
    # directly
    fast_ewma = price.ewm(span=Lfast).mean()
    slow_ewma = price.ewm(span=Lslow).mean()
    raw_ewmac = fast_ewma - slow_ewma

    vol = robust_vol_calc(price.diff())
    return raw_ewmac / vol


if __name__ == '__main__':
    inpath = 'data/in/'
    outpath = 'data/out/'
    signals = [ ]
    for instrument_code in instrument_config_coinbase.index.values:
        data = pd_readcsv(inpath +"/coinbase/" + instrument_code + '_raw.csv', date_index_name='Date')
        price = data['Close']
        score = calc_ewmac_forecast(price, 32, 128)
        score.to_csv(outpath +"/coinbase/" + instrument_code + '_signal.csv')
        signals.append(score.rename(instrument_code))

    signals = pd.concat(signals, axis=1)
    pm = signals.iloc[-1]
    pm.index.rename("Asset", inplace=True)
    pm.to_csv(outpath +"/coinbase/trend_signals.csv")