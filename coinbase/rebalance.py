from coinbase.monitor import show_holding
from coinbase.trade import tradeCB
from global_config import *
if __name__ == '__main__':
    signalname = 'trend'
    USD = 10
    pm = pd.read_csv(outpath + '/coinbase/' + signalname + '_signals.csv')
    print(pm)
    pm = pm[pm[pm.columns[1]]>0] # enter long only signals , or exit
    signals = set(pm['Asset'].apply(lambda x: x.split('-')[0]))
    positions = show_holding()

    assets_to_exit = set(positions.index.values).difference(
        signals).difference(set(['USD']))
    print("Exiting Trade:")
    print(assets_to_exit)
    for instrument_code in assets_to_exit:
        order_amount = -1
        close_ratio = 1
        tradeCB(instrument_code, order_amount, close_ratio, USD)

    assets_to_enter = signals.difference(
        set(positions.index.values))
    print("Entering Trade :")
    print(assets_to_enter)
    for instrument_code in assets_to_enter:
        order_amount = 1
        close_ratio = 1
        
        tradeCB(instrument_code, order_amount, close_ratio, USD)



