import json

with open("infothreshold.json",'r') as load_f:
    load_dict = json.load(load_f)
    print(load_dict)