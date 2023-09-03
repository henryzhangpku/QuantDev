from global_config import *
from Historic_Crypto import HistoricalData
import cbpro
public_client = cbpro.PublicClient()
pd.set_option('display.max_colwidth', None)


def load_data():
    instrument_list = []
    for product in public_client.get_products():
        #print(product)
        if 'USDT' == product['quote_currency']:
            instrument_list.append(product['id'])

    instrument_list = instrument_config_coinbase.index.values

    report = pd.DataFrame(0, index=instrument_list, columns=['Return'])
    today = datetime.datetime.now().date() 
    startdate = datetime.date(2017, 1, 1)
    datelist = pd.date_range(startdate, today).tolist()
    print("Data start date:" + startdate.strftime('%m/%d/%Y'))
    day_in_seconds = 86400
    extra_list = []
    for product in public_client.get_products():
        
        if product['id'] in instrument_list:
            cbid = product['id']
 
            # EOD
            md = public_client.get_product_24hr_stats(cbid)
            # print(cbid)
            # print(md)
            if ('last' not in md) or ('open' not in md):
                continue
            net_change = float(md['last']) - float(md['open'])
            if float(md['open']) != 0:
                ret = round(net_change / float(md['open']) * 100, 3)
            else:
                ret = 0
            report.loc[cbid] = [ret]
            klines = public_client.get_product_historic_rates(
                cbid, start=startdate.strftime('%m/%d/%Y'), granularity=day_in_seconds)
    
            raw_data = pd.DataFrame(None, index=datelist, columns=[
                                    'Low', 'High', 'Open', 'Close', 'Volume'])  # .dropna()

            if klines is None or len(klines) < 2:
                continue

            for i in range(0, len(klines)):
   
                dateditem = klines[i]
                row = [dateditem[1], dateditem[2],
                       dateditem[3], dateditem[4], dateditem[5]]
                # print(row)
                raw_data.iloc[-i - 1] = row
            raw_data = raw_data.dropna()
            raw_data.index.names = ['Date']
            raw_data.to_csv(inpath +"/coinbase/" +
                            cbid + '_raw.csv')
            raw_price = pd.DataFrame(raw_data['Close'], columns=[
                'Close']).sort_index(axis=0, ascending=True)

            # raw price
            raw_price.index.names = ['DATETIME']
            raw_price.to_csv(inpath +"/coinbase/" + 
                             cbid + '_price.csv')

            if cbid not in instrument_config_coinbase.index.values:
                extra_list.append(cbid)

    # print out new additional assets
    print("##########")
    for cbid in extra_list:
        print(cbid + ",1,Crypto,USDT,FALSE," + cbid + ",Coinbase,Crypto,")

    report = report.sort_values(['Return'], ascending=[False])
    print(report)
    report.to_csv(inpath +"/coinbase/" + "coinbase_returns.csv")


if __name__ == "__main__":

    start_an = default_timer()
    load_data()
    end_an = default_timer()
    print("4.Completed data loading in " +
            str(round(end_an - start_an, 2)) + " seconds")