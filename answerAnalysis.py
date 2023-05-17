import ast
import argparse

parser=argparse.ArgumentParser(description="input MR type")
parser.add_argument("-f","--filename",default="output.txt",help="file to record the bugs")
args=parser.parse_args()

def answerAnalysis(args):
    f=open ('infothreshold.json','r',encoding='utf-8')
    s=f.read()
    ff=open ('infothreshold1500.json','r',encoding='utf-8')
    ss=ff.read()
    result=s+ss
    """f=open (args.filename,'r',encoding='utf-8')
    result=f.read()
    f.close()
    """
    wf=open ('infothreshold_03.json','w+',encoding='utf-8')
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
    print(result,file=wf)

if __name__=='__main__':
    answerAnalysis(args)