import json
import time
from claims import AxieClaimsManager
from my_helper import generate_pay_json, update_VAXH
from payments import AxiePaymentsManager
import logging
import os
import sys
from binance.client import Client
import credentials
from payout import send_ltc
from datetime import date
client = Client(credentials.API_KEY,credentials.SECRET_KEY)



from helper import check_address

class Scholar:

    def __init__(self, ign, ronin, address, cut, held_amt):
        self.ign = ign
        self.ronin = ronin
        self.address = address
        self.cut = cut
        self.held_amt = held_amt

class PayoutManager:

    def __init__(self, new_data_path, old_data_path, hold_users_path, payments_path ):
        self.new_data_path = new_data_path
        self.old_data_path = old_data_path
        self.hold_users_path = hold_users_path
        self.new_scholar_data = []
        self.old_scholar_data = []
        self.payments_path = payments_path
        self.init_scholar_data()

    def generate_payments(self):     

        scholar_list = self.new_scholar_data
        full_json = {}
        array_dict_scholars = []

        for scholar in scholar_list:
    
            addresee = check_address(scholar.address)
  
            if 'ronin' == addresee:
    
                payout_val = float(scholar.held_amt)

                if payout_val > 0:

                    scholar_d = dict({
                        "Name":scholar.ign,
                        "AccountAddress":scholar.ronin,
                        "ScholarPayoutAddress":scholar.address,
                        "ScholarPayout":round(payout_val * float(scholar.cut)),
                        "ManagerPayout":round(payout_val * (1 - float(scholar.cut)))
                    })
                    array_dict_scholars.append(scholar_d)

                elif payout_val == 0:
                    pass

            elif 'ronin' != addresee:

                payout_val = float(scholar.held_amt)

                if payout_val > 0:

                    scholar_d = dict({
                        "Name":scholar.ign,
                        "AccountAddress":scholar.ronin,
                        "ScholarPayoutAddress":"ronin:f99fe48ff09f72023acfee37b878711842af71f9",
                        "ScholarPayout":round(payout_val * float(scholar.cut)),
                        "ManagerPayout":round(payout_val * (1 - float(scholar.cut)))
                    })

                    array_dict_scholars.append(scholar_d)

                elif payout_val == 0:
                    pass           

        full_json = {
            "Manager": "ronin:f99fe48ff09f72023acfee37b878711842af71f9",
            "Scholars": array_dict_scholars
        }

        with open('payments.json', 'w', encoding='utf-8') as f:
            json.dump(full_json, f, ensure_ascii=False, indent=4)


    def init_scholar_data(self):

        isko_list_new = self.get_scholar_from_csv(self.new_data_path)
        isko_list_old = self.get_scholar_from_csv(self.old_data_path)

        isko1 = []
        isko2 = []

        for isko in isko_list_new:

            try:
                isko_obj = Scholar(isko[0],isko[1],isko[2],isko[4],isko[5])
                isko1.append(isko_obj)

            except Exception as e:
                print(e)

        for isko in isko_list_old:

            try:
                isko_obj = Scholar(isko[0],isko[1],isko[2],isko[4],isko[5])
                isko2.append(isko_obj)

            except Exception as e:
                print(e)

        self.new_scholar_data = isko1
        self.old_scholar_data = isko2


    def get_payouts_true(self):
        
        with open(self.hold_users_path, 'r') as f:

            data = f.readlines()
            cleaned = []
            final_arr = []
            to_return = []
            for x in data:
                newx = x.replace('\n','')
                cleaned.append(newx)
            for x in cleaned:
                final_arr.append(x.split(','))
            for x in final_arr:
                if 'True' in x :
                    to_return.append(x[1])

            return to_return
        

    def get_scholar_from_csv(self,path):

        with open(path,'r') as f:

            data = f.readlines()
            cleaned = []
            final_arr = []
            for x in data:
                newx = x.replace('\n','')
                cleaned.append(newx)
            for x in cleaned:
                final_arr.append(x.split(','))
            return final_arr[1:]

    def update_old_data(self):

        just_claimed = self.get_scholar_from_csv(self.new_data_path)
        binance = self.get_scholar_from_csv(self.old_data_path)
        new_csv = 'name,ronin,address,isManager,cut,held_amt\n'
        for idx,_ in enumerate(just_claimed):
            added_val = str( int(just_claimed[idx][-1]) + int(binance[idx][-1]))
            my_str = f'{just_claimed[idx][0]},{just_claimed[idx][1]},{just_claimed[idx][2]},{just_claimed[idx][3]},{just_claimed[idx][4]},{added_val}\n'
            new_csv = new_csv + my_str

        with open('vaxh-binance.csv','w') as f:
            f.write(new_csv)

    def get_payout_info(self):

        total_new_slp = 0

        total_hold_slp = 0
        total_manager_slp = 0
        total_scholar_slp = 0
        total_takers_slp = 0
        payout_takers = []

        for isko in self.new_scholar_data:
            total_new_slp += int(isko.held_amt)
            total_scholar_slp += int(isko.held_amt) * float(isko.cut)
            total_manager_slp += int(isko.held_amt) * (1 - float(isko.cut))

        for isko in self.old_scholar_data:
            total_hold_slp += int(isko.held_amt) * float(isko.cut)

        true_payouts = self.get_payouts_true()
        isko_data = self.new_scholar_data

        for x in true_payouts:
            print(x)

        for x in isko_data:
            if x.ronin in true_payouts:
                payout_takers.append(x)

        for x in payout_takers:
            total_takers_slp += (int(x.held_amt) * float(x.cut))

        slp_keep = total_scholar_slp - total_takers_slp

        payout_dict = {
            "hold_wallet_slp" : slp_keep,
            "total_manager_slp": total_manager_slp,
            "total_scholar_slp_init": total_scholar_slp,
            "total_takers_slp": total_takers_slp,
            "scholar_takers" : payout_takers
        }

        return payout_dict


    def claim_scholar_slp(self):

        os.makedirs('logs', exist_ok=True)
        log = logging.getLogger()
        log.setLevel(logging.INFO)
        ch = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
        ch.setFormatter(formatter)
        log.addHandler(ch)

        acm = AxieClaimsManager('payments.json','secrets_files.json')
        acm.verify_inputs()
        acm.prepare_claims()

    def run_scholar_payout(self):

        os.makedirs('logs', exist_ok=True)
        log = logging.getLogger()
        log.setLevel(logging.INFO)
        ch = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
        ch.setFormatter(formatter)
        log.addHandler(ch)

                        
        apm = AxiePaymentsManager('payments.json', 'secrets_files.json', auto='--yes')
        apm.verify_inputs()
        apm.prepare_payout()

    def run_vaxh_payouts(self,isko_arr):

        ## send slp of hold slp to ronin hold wallet

        for isko in isko_arr:

            slp_trades = float(client.get_recent_trades(symbol='SLPUSDT')[0]['price'])
            dollar_value = slp_trades * (float(isko.cut) * float(isko.held_amt))
            print(dollar_value)
            recent_trades = float(client.get_recent_trades(symbol='LTCUSDT')[0]['price'])
            computed_value = float(round((dollar_value / recent_trades),7))
            print('sending',isko.ign,isko.held_amt,computed_value)
            time.sleep(15)
            send_ltc(isko.address,computed_value)
            update_VAXH(isko.ronin,0,self.old_data_path)
            


####   TO FINISH
       
    def binance_payout_list(self):
        # get all True @payouts-hold and return array of True
        list_of_payouts = self.get_payouts_true()
        list_of_members = self.get_scholar_from_csv(self.old_data_path)
        final_list = []
        for x in list_of_payouts:
            for y in list_of_members:

                if x == y[1]: 
                    if 'ltc' == check_address(y[2]):       
                        final_list.append(Scholar(y[0],y[1],y[2],y[-2],y[-1]))
                
        return final_list 


    def gcash_payout(self):
        # get all True @payouts-hold and return array of True
        list_of_payouts = self.get_payouts_true()
        list_of_members = self.get_scholar_from_csv(self.old_data_path)
        today = date.today()
        d1 = str(today.strftime("%d_%m_%Y"))
        file_str = f'gcash_payout{d1}'
        payout_str = 'ign,address,cut,amt\n'
        total_gcash_scholar = 0
        total_gcash_manager = 0
        for x in list_of_payouts:
            for y in list_of_members:
                
                if x == y[1]: 
                    if 'gcash' == check_address(y[2]):
                        payout_str += f'{y[0]},{y[2]},{y[-2]},{y[-1],{float(y[-1])*float(y[-2])}}\n'
                        total_gcash_scholar += (float(y[-1]) * float(y[-2]))
                        total_gcash_manager += (float(y[-1]) * (1 - float(y[-2])))
                        update_VAXH(y[1],0,'vaxh-binance.csv')

        slp_trades = float(client.get_recent_trades(symbol='SLPUSDT')[0]['price'])
        dollar_value = slp_trades * (float(total_gcash_scholar+total_gcash_manager))
        recent_trades = float(client.get_recent_trades(symbol='LTCUSDT')[0]['price'])
        computed_value = float(round((dollar_value / recent_trades),7)) 
        send_ltc('MX6JQX6reLvWMNdjJh7nBfRmrKUHVkqni4', computed_value)

        with open(file_str, 'a+') as f:
            f.write(payout_str)

    


## main profit from 

if __name__ == "__main__":
    x = PayoutManager('vaxh.csv','vaxh-binance.csv','payout_hold.csv','payments.json')
    ### ran generate_pay_json(True) last time
    # generate_pay_json(True)
    # x.claim_scholar_slp()
    ### create @generate payments
    # x.update_old_data()
    ### create payout cut if payout is true and has hold amt
    # x.generate_payments()
    ## x.generate payments does not work with hold payouts
    x.run_scholar_payout()
    # print(x.binance_payout_list())
    # print(x.gcash_payout())
    # x.binance_payout()
    # print(x.get_payout_info())
    # print(x.binance_payout_list())



    ### vaxh binance update