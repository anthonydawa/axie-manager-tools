from binance.client import Client
import credentials
from my_helper import generate_pay_json, get_payouts_true, get_payout_amt, update_VAXH, update_VAXH_binance
client = Client(credentials.API_KEY,credentials.SECRET_KEY)

from binance.exceptions import BinanceAPIException
import market_order
import time
import vaxe as VAXH
from run_payout import run_payout
from run_claims import run_claims

def send_xrp(address,tag,amt):
    try:
        result = client.withdraw(coin='XRP',address=address,addressTag=tag,amount=amt)
        print(result)
    except BinanceAPIException as e:
        print(e)
    else:
        print("Success")
        
def send_ltc(address,amt):
    try:
        result = client.withdraw(coin='LTC',address=address,amount=amt)
        print(result)
    except BinanceAPIException as e:
        print(e)
    else:
        print("Success")

def send_slp(address,amt):
    try:
        result = client.withdraw(coin='SLP',address=address,network='ronin',amount=amt)
        print(result)
    except BinanceAPIException as e:
        print(e)
    else:
        print("Success")

def send_scholar_payout(scholars):

    for scholar in scholars:
        if scholar['amt'] != 0:
            # slp_trades = float(client.get_recent_trades(symbol='SLPUSDT')[0]['price'])
            slp_trades = float(0.0310)
            dollar_value = slp_trades * (scholar['amt'] * scholar['share'])
            recent_trades = float(client.get_recent_trades(symbol='LTCUSDT')[0]['price'])
            computed_value = float(round((dollar_value / recent_trades),7))
            print('sending',scholar['name'],scholar['address'],computed_value)
            time.sleep(12)
            send_ltc(scholar['address'],computed_value)
        else:
            print(scholar['name'],'is holding')


def send_manager_payout(managers):

    balance = float(client.get_asset_balance(asset='LTC')['free']) * 0.998
    manager_share = float(round((balance * 0.33),7))

    
    for manager in managers:


        print('sending',manager['name'],manager['address'],manager_share)
        time.sleep(5)
        send_ltc(manager['address'],manager_share)



def send_test_manager_payout(managers):

    for manager in managers:
        
        manager_share = float(25.55)

        print('sending',manager['name'],manager['address'],manager['tag'],manager_share)
        time.sleep(15)
        send_xrp(manager['address'],manager['tag'],manager_share)


def send_test_scholar_payout(scholars):

    for scholar in scholars:
        computed_value = float(25.55)
        print('sending',scholar['name'],scholar['address'],scholar['tag'],computed_value)
        time.sleep(1)
        send_xrp(scholar['address'],scholar['tag'],computed_value)


def compute_reqd():
    # get all True @payouts-hold and return array of True
    list_of_payouts = get_payouts_true()
    list_of_members = get_payout_amt('vaxh-binance.csv')
    final_list = []
    for x in list_of_payouts:
        for y in list_of_members:

            if x == y[1]:   
                print(y)            
                # do something with matched here
                member_pay = {
                    "name":y[0],
                    "address":y[2],
                    "amt":y[-1],
                    "cut":y[-2],
                    "ronin":y[1]
                }
                final_list.append(member_pay)
    return final_list

    # show amt to be taken from slp staking 
    # get total balance and compute cut needed

    

def run_vaxh_payouts(arr):
    ## convert slp to ltc
    ##get total amt frm from x in arr 

    for x in arr:
        # slp_trades = float(0.0310)
        slp_trades = float(client.get_recent_trades(symbol='SLPUSDT')[0]['price'])
        dollar_value = slp_trades * (float(x["cut"]) * float(x["amt"]))
        print(dollar_value)
        recent_trades = float(client.get_recent_trades(symbol='LTCUSDT')[0]['price'])
        computed_value = float(round((dollar_value / recent_trades),7))
        print('sending',x["name"],x["amt"],computed_value)
        print(x)
        time.sleep(15)
        send_ltc(x['address'],computed_value)
        update_VAXH(x['ronin'],0,'vaxh-binance.csv')

def get_managers_share():
    balance = float(client.get_asset_balance(asset='SLP')['free']) * 0.999
    return balance

def record_total(x):
    with open('manager_total','a') as f :
        txt = f'{x}\n'
        f.writelines(txt)



if __name__ == "__main__":
######### check tracker for total and confirm with inventory get total claimed current
    # generate_pay_json(True)
    # run_claims()
    # generate_pay_json(False)
    ### create at payout json if 0 dont include
    # run_payout()
    # manager_total = get_managers_share()
    # record_total(manager_total)
    ### must be same array #
    update_VAXH_binance()
    ### create total hold current slp total  
    # to_pay = compute_reqd()
    # print(to_pay)
    # run_vaxh_payouts(to_pay)
    # send_manager_payout(VAXH.managers)

    # manager_total = get_managers_share()
    # to_pay = compute_reqd()
    # run_vaxh_payouts(to_pay)
#     market_order.sell_market_order('SLPUSDT',market_order.get_lot_size('SLPUSDT'))
#     time.sleep(10)
#     market_order.buy_market_order('XRPUSDT',market_order.get_lot_size('XRPUSDT'))
    # send_scholar_payout(VAXH.scholars)
    # send_slp('ronin:2534339890f04477211b94069c4fb5514c6611e5',160)
    
    # send_test_manager_payout(VAXH.managers)
    # send_xrp('rKvAtitwmaYVFG8GwDmUSyqo71YMbeBSwn','229549852',519)
    # send_xrp('rKvAtitwmaYVFG8GwDmUSyqo71YMbeBSwn','600888575',396)
    # send_xrp('rKvAtitwmaYVFG8GwDmUSyqo71YMbeBSwn','229549852',396)
    # send_ltc('MX6JQX6reLvWMNdjJh7nBfRmrKUHVkqni4', round(0.07800000,7))