def update_VAXH (ronin,new_value):
    final_arr = get_payout_amt()
    updated_arr = []
    for x in final_arr:
        if x[1] == ronin:
            updated_val = new_value + float(x[2])
            x.remove(x[2])
            x.append(updated_val)
            updated_arr.append(x)
        else:
            updated_arr.append(x)
    revert_csv = []
    for x in updated_arr:
        formatted = f"{x[0]},{x[1]},{x[2]},{x[3]},{x[4]},{x[5]}\n"
        revert_csv.append(formatted)
    to_append = "".join(revert_csv)
    with open('VAXH.csv', 'w') as f:
        f.write(to_append)

def get_payout_amt ():
    with open('VAXH.csv','r') as f:
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
                to_return.append(x[0])

        return to_return

                