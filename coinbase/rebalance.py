from coinbase.monitor import show_holding
from coinbase.trade import tradeCB
from global_config import *
if __name__ == '__main__':
    signalname = 'trend'
    pm = pd.read_csv(outpath + '/coinbase/' + signalname + '_signals.csv')


    signals = set(pm['Asset'].apply(lambda x: x.split('-')[0]))

    print(signals)
    positions = show_holding()

    assets_to_exit = set(positions.index.values).difference(
        signals)
    print("Exiting Trade:")
    print(assets_to_exit)
    for instrument_code in assets_to_exit:
        order_amount = -1
        close_ratio = 1
        USD = 25
        tradeCB(instrument_code, order_amount, close_ratio, USD)

    assets_to_enter = signals.difference(
        set(positions.index.values))
    print("Entering Trade :")
    print(assets_to_enter)
    for instrument_code in assets_to_enter:
        order_amount = 1
        close_ratio = 1
        USD = 25
        tradeCB(instrument_code, order_amount, close_ratio, USD)

    assets_to_check = set(positions.index.values).intersection(
        signals)  # .remove('USD')
    for instrument_code in assets_to_check:
        order_amount = 1
        close_ratio = 0.5
        USD = 2
        if float(positions.loc[instrument_code]['MarketValue']) < float(USD) - 1:
            print(positions.loc[instrument_code])
            tradeCB(instrument_code, order_amount, close_ratio, USD)


