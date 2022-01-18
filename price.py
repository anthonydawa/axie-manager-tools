from binance.client import Client
client = Client()

axs_price = round(float(client.get_avg_price(symbol='AXSUSDT')['price']),2)
slp_price = round(float(client.get_avg_price(symbol='SLPUSDT')['price']),2)

import sys

print(round(float(sys.argv[1])),'AXS',round(float(sys.argv[2])), 'SLP')
print(f'1 SLP = {slp_price}$ 1 AXS = {axs_price}$')
print(f'1 SLP = {slp_price*47}PHP 1 AXS = {axs_price*47}PHP')
print(float(sys.argv[1])*axs_price, '$', 'worth of AXS')
print(float(sys.argv[2])*slp_price, '$', 'worth of SLP')
print(float(sys.argv[1])*axs_price*49, 'PHP','worth of AXS')
print(float(sys.argv[2])*slp_price*49, 'PHP','worth of SLP')
print(float(sys.argv[1])*axs_price+float(sys.argv[2])*slp_price)