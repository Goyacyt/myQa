import re
import json
import ast

if __name__=="__main__":
    f=open("output5.txt","r",encoding='utf-8')
    st=f.read()
    js=re.split(r'------------test\scase[0-9]*------------\n',st)
    js_dict=ast.literal_eval(js)
    print(js_dict)
    """nf=open("result.json","w",encoding='utf-8')
    json.dump(js,nf)"""
