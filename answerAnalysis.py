import ast
import argparse

parser=argparse.ArgumentParser(description="input MR type")
parser.add_argument("-f","--filename",default="output.txt",help="file to record the bugs")
args=parser.parse_args()

def answerAnalysis(args):
    """f=open ('infopro0.json','r',encoding='utf-8')
    s=f.read()
    ff=open ('infopro172.json','r',encoding='utf-8')
    ss=ff.read()
    fff=open ('infopro253.json','r',encoding='utf-8')
    sss=fff.read()
    ffff=open ('infopro1001.json','r',encoding='utf-8')
    ssss=ffff.read()
    fffff=open ('infopro1465.json','r',encoding='utf-8')
    sssss=fffff.read()
    result=s+ss+sss+ssss+sssss
    wf=open ('infoproportion_04_50.json','w+',encoding='utf-8')
    result=result.split('}{')
    for i in range(len(result)):
        if i==0:
            result[i]=result[i]+'}'
        elif i==len(result)-1:
            result[i]='{'+result[i]
        else:
            result[i]='{'+result[i]+'}'
        result[i]=ast.literal_eval(result[i])
    #print(result[0]['groundTruth'],result[0]['answer'])
    print(result,file=wf)"""
    

if __name__=='__main__':
    answerAnalysis(args)