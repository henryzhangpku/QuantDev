from coinbase.monitor import *


def tradeCB(instrument_code, order_amount=1, close_ratio=1, USD=25):
    if instrument_code == 'USD':
        return
    cbid = instrument_code + '-USD'

    ticker = public_client.get_product_ticker(product_id=cbid)
    if ticker is None or 'price' not in ticker:
        print("no " + cbid + " market on Coinbase")
        return
    price = float(ticker['price'])
    size = float(round(USD * order_amount / price, 2))
    if order_amount > 0:
        auth_client.place_market_order(product_id=cbid,
                                       side='buy',
                                       funds=USD * order_amount*close_ratio)
        print("#####################################################################")
        print("bought " + str(size) + " " + cbid + " at " + str(price))

    else:
        h = 0
        for ac in auth_client.get_accounts():
            # print(ac['currency'])
            if ac['currency'] == instrument_code:
                h = float(ac['available'])

        h = h * close_ratio

        auth_client.place_market_order(product_id=cbid,
                                       side='sell',
                                       funds=round(h * price, 1))

        print("#####################################################################")
        print("sold " + str(h) + " " + cbid + " at " + str(price))


if __name__ == '__main__':
    instrument_list = ['BTC']
    NAV = 1000
    USD = NAV * 0.01
    order_amount = 1
    close_ratio = 1
    if len(sys.argv) > 1:
        instrument_list = sys.argv[1]
    if len(sys.argv) > 2:
        order_amount = int(sys.argv[2])
    if len(sys.argv) > 3:
        close_ratio = float(sys.argv[3])
    instrument_list = instrument_list.split(',')
    for instrument_code in instrument_list:
        tradeCB(instrument_code, order_amount, close_ratio, USD)
