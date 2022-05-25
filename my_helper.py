from hashlib import new
import json

from payments import Payment


def update_VAXH (ronin,new_value,csv):
    final_arr = get_payout_amt('vaxh.csv')
    updated_arr = []
    for x in final_arr:
        if x[1] == ronin:
            # updated_val = str(new_value + float(x[-1]))
            updated_val = str( int(new_value) - 1 )
            x.remove(x[-1])
            x.append(updated_val)
            updated_arr.append(x)      
        else:
            updated_arr.append(x)
    revert_csv = []
    for x in updated_arr:
        formatted = f"{x[0]},{x[1]},{x[2]},{x[3]},{x[4]},{x[5]}\n"
        revert_csv.append(formatted)
    to_append = "".join(revert_csv)
    with open(csv, 'w') as f:
        f.write(to_append)


def get_payout_amt(csv):
    with open(csv,'r') as f:
        data = f.readlines()
        cleaned = []
        final_arr = []
        for x in data:
            newx = x.replace('\n','')
            cleaned.append(newx)
        for x in cleaned:
            final_arr.append(x.split(','))
        return final_arr
        
def get_payouts_true():
    with open('payout_hold.csv', 'r') as f:
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


def generate_pay_json(bool):
    
    data = get_payout_amt('vaxh.csv')
    full_json = {}
    array_dict_scholars = []

    if bool == True:

        for x in data[1:]:
            payout_val = int(0)
            scholar_d = dict({
                "Name":x[0],
                "AccountAddress":x[1],
                "ScholarPayoutAddress":"ronin:f99fe48ff09f72023acfee37b878711842af71f9",
                "ScholarPayout":payout_val,
                "ManagerPayout":0
            })
            array_dict_scholars.append(scholar_d)
        full_json = {
            "Manager": "ronin:f99fe48ff09f72023acfee37b878711842af71f9",
            "Scholars": array_dict_scholars
        }

        with open('payments.json', 'w', encoding='utf-8') as f:
            json.dump(full_json, f, ensure_ascii=False, indent=4)

    elif bool == False:
        # work on adding scholar payout address if taking payout
        for x in data[1:]:
            payout_val = int(x[-1])
            scholar_cut = x[-2]
            if payout_val >= 0:
                scholar_d = dict({
                    "Name":x[0],
                    "AccountAddress":x[1],
                    "ScholarPayoutAddress":"ronin:f99fe48ff09f72023acfee37b878711842af71f9",
                    "ScholarPayout":int((payout_val * float(scholar_cut))),
                    "ManagerPayout":int((payout_val * (1 - float(scholar_cut)) ))
                })
                array_dict_scholars.append(scholar_d)
        full_json = {
            "Manager": "ronin:f99fe48ff09f72023acfee37b878711842af71f9",
            "Scholars": array_dict_scholars
        }

        with open('payments.json', 'w', encoding='utf-8') as f:
            json.dump(full_json, f, ensure_ascii=False, indent=4)

def update_VAXH_binance():
    just_claimed = get_payout_amt('vaxh.csv')
    binance = get_payout_amt('vaxh-binance.csv')
    new_csv = 'name,ronin,ltc_address,isManager,cut,held_amt\n'

    for idx,_ in enumerate(just_claimed[1:],1):
        added_val = str( int(just_claimed[idx][-1]) + int(binance[idx][-1]))
        my_str = f'{just_claimed[idx][0]},{just_claimed[idx][1]},{just_claimed[idx][2]},{just_claimed[idx][3]},{just_claimed[idx][4]},{added_val}\n'
        new_csv = new_csv + my_str
    with open('vaxh-binance.csv','w') as f:
        f.write(new_csv)


    print('done updating')

        

    # for x in just_claimed[1:]:
    #     for y in binance[1:]:
    #         if x[1] == y[1]:
    #             if int(x[-1]) != 0:
    #                 myron = str(x[1])
    #                 added_val = str(int(x[-1]) + int(y[-1]))
    #                 my_str = f'{x[0]},{x[1]},{x[2]},{x[3]},{x[4]},{added_val}\n'
    #                 new_csv = new_csv + my_str
    #                 print(new_csv)             

# update_VAXH_binance()
    #then generate 0 file
# generate_pay_json(True)


if __name__ == "__main__":
    x = 0.1 * 945
    print(int(x))
