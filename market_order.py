
from binance.client import Client
import credentials
client = Client(credentials.API_KEY,credentials.SECRET_KEY)
from binance.enums import *


def count_decimal(num):
    str_num = str(num)
    count = 0
    for d in str_num:
        if d == '0':
            count += 1
        elif d == '.':
            pass
        elif d == '1':
            break
    return count


def get_price_filter(symbol):
    details = client.get_symbol_info(str(symbol).upper())
    price_filter = count_decimal(details['filters'][0]['tickSize'])
    return price_filter

def get_lot_size(symbol):
    details = client.get_symbol_info(str(symbol).upper())
    lot_size = count_decimal(details['filters'][2]['stepSize'])
    return lot_size

def buy_limit_order(symbol,TP,lot_size,price_filter,min_trade = 11):

    balance = client.get_asset_balance(asset='USDT')
    balance_amt = float(balance['free'])
    amt_price_str = "{:0.0{}f}".format(TP, price_filter)  
    quantity = balance_amt * 0.999
    amt_str = "{:0.0{}f}".format(quantity, lot_size)
    trades = client.get_recent_trades(symbol=symbol)
    trade_value = float(trades[0]['price'])
    current_amount_avail = balance_amt * trade_value  

    if current_amount_avail < min_trade:
        print('not enough balance', current_amount_avail)
    elif current_amount_avail >= min_trade:
        success = False
        count = 0
        while success == False:
            try:
                client.order_limit_buy(symbol=str(symbol).upper(),quantity=amt_str,price=amt_price_str)
            except:
                if count == 3:
                    success = True
                else:
                    count += 1
                    print('error buy_limit_order',symbol,'trying again..')


def sell_limit_order(symbol,TP,lot_size,price_filter,min_trade = 11): 
    strx = str(symbol).replace('USDT','')

    balance = client.get_asset_balance(asset=strx)
    balance_amt = float(balance['free'])
    quantity = balance_amt * 0.998
    amt_str = "{:0.0{}f}".format(quantity, lot_size)
    amt_price_str = "{:0.0{}f}".format(TP, price_filter)
    trades = client.get_recent_trades(symbol=symbol)
    trade_value = float(trades[0]['price'])
    current_amount_avail = balance_amt * trade_value

    if current_amount_avail < min_trade: 
        
        print('not enough balance', current_amount_avail)

    elif current_amount_avail >= min_trade:
        success = False
        count = 0
        while success == False:
            try:
                order = client.order_limit_sell(symbol=symbol,quantity=amt_str,price=amt_price_str)
                return order
            except:
                if count == 3:
                    success = True
                else:
                    count += 1
                    print('error sell_limit_order',symbol,'trying again..')




def buy_market_order(symbol,lot_size,min_trade = 11):

    balance = client.get_asset_balance(asset='USDT')
    trades = client.get_recent_trades(symbol=symbol)
    current_amt_avail = float(balance['free'])
    price = float(trades[0]['price'])
    quantity = (current_amt_avail/price)*(0.998)
    amt_str = "{:0.0{}f}".format(quantity, lot_size)

    result = client.order_market_buy(symbol=symbol, quantity=amt_str)

    if result['status'] == 'FILLED':
        print(result['status'], result['cummulativeQuoteQty'])
    elif not result['status'] == 'FILLED':
        print(result)




def sell_market_order(symbol,lot_size,min_trade = 11): 

    strx = str(symbol).replace('USDT','')
    balance = client.get_asset_balance(asset=strx)
    balance_amt = float(balance['free'])
    quantity = balance_amt * 0.998
    amt_str = "{:0.0{}f}".format(quantity, lot_size)


    result = client.order_market_sell(symbol=symbol, quantity=amt_str)

    if result['status'] == 'FILLED':
        print(result['status'], result['cummulativeQuoteQty'])
    elif not result['status'] == 'FILLED':
        print(result)






if __name__ == "__main__":
    buy_market_order('BNBUSDT',get_lot_size('BNBUSDT'))