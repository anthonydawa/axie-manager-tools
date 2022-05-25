
# Python program to read
# json file
 
 
import json
 
# Opening JSON file
f = open('slp_total.json')
 
# returns JSON object as
# a dictionary
data = json.load(f)
 
# Iterating through the json
# # list
# for i in data["held_amt"]:
#     print(i)
total = 0
for i in data:
    total += int(i['held_amt'])
print(total * 0.4)

# Closing file
f.close()