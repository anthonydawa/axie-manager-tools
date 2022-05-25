def check_address(address):
    if 'ronin' in address:
        return 'ronin'
    elif len(address) == 34:
        return 'ltc'
    elif address.isdecimal():
        return 'gcash'
    else:
        return None

