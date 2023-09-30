from global_config import  *
from private.credential import *
import cbpro
auth_client = cbpro.AuthenticatedClient(cb_key, cb_b64secret, cb_passphrase)
public_client = cbpro.PublicClient()
pd.set_option('display.max_rows', None)


def show_holding(smart_sorting=True):
    instrument_list = []
    acs = auth_client.get_accounts()
    for ac in acs:
        if ac['available'] != '0':
            cbid = ac['currency']
            instrument_list.append(cbid)
    report = pd.DataFrame( 
        0, index=instrument_list, columns=['Return', 'MarketValue', 'Price', 'Holding', 'Benchmark']) 

    print("#####################################################################")

    for ac in acs:
        if ac['available'] != '0':
            cbid = ac['currency']
            h = float(ac['available'])
            if cbid != 'USD':
                #print(cbid)
                ticker = public_client.get_product_ticker(
                    product_id=cbid + "-USD")
                # print(ticker)
                if "price" not in ticker:
                    continue
                price = float(ticker['price'])
                md = public_client.get_product_24hr_stats(cbid + "-USD")
     
                if ('last' not in md) or ('open' not in md):
                    continue
                net_change = float(md['last']) - float(md['open'])
                ret = round(net_change / float(md['open']) * 100, 3)
            else:
                price = 1
                ret = 0

            report.loc[cbid] = [ret, h * price, price, h, '']
            if cbid == 'APE':
                report.loc[cbid] = [ret, h * price, price, h, '*****']
            if cbid == 'USD':
                report.loc[cbid] = [ret, h * price, price, h, '-----']

    report.index.names = ['Asset']
    report = report[report['MarketValue'] > 1]
    if smart_sorting:
        report = report.sort_values(
            ['Return', 'MarketValue'], ascending=[False, False])
    else:
        report = report.sort_index(ascending=True)


    return report


if __name__ == '__main__':
    smart_sorting = True
    if len(sys.argv) > 1:
        smart_sorting = bool(sys.argv[1])
    while True:
        report = show_holding(smart_sorting=smart_sorting)
        print(report)
        print("NAV = " + str(round(report['MarketValue'].sum(), 3)))
        if "USD" in report.index.values:
            print("USD = " + str(round(report.loc['USD']['MarketValue'].sum(), 3)))
        time.sleep(30)
