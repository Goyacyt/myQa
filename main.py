import argparse
from datasets import load_dataset
from distance import *
from transformer import *
from model import output_answer
from answerCompare import answerMatch
import difflib
import urllib3
import json
import ast
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser=argparse.ArgumentParser(description="input MR type")

parser.add_argument("--mr",default=2,help="MR type")
parser.add_argument("--module",default="t5-base",help="choose between t5-large or\
                    t5-base or t5-3b")
parser.add_argument("--dataset",default="squad",help="choose between squad2|squad|boolq")
parser.add_argument("--lowk",default=True,help="true if you want to delete the least associated sentence")
parser.add_argument("-f","--filename",default="output.txt",help="file to record the bugs")
parser.add_argument("-de","--deleteextent",default="leastone",help="the pattern of deleting unrelated message,you can\
                    choose between least|proportion|threshold")
parser.add_argument("-p","--proportion",default=0.5,help="the proportion of sentences being deleted")
parser.add_argument("-t","--threshold",default=0.3,help="delete the sentence whose distance is below this value")
parser.add_argument("-cmp","--compare",default="com",help="the type of comparing two answers")
parser.add_argument("-cmpt","--comparethreshold",default=0.75,help="the threshold of answer similarity")
parser.add_argument("-l","--logfile",default="log.txt")
parser.add_argument("-s","--start",default=0,help="dataset start number")
parser.add_argument("-e","--end",default=2000,help="dataset end number")
parser.add_argument("-re","--rewritePattern",default="all",help="rewrite all the sentence or choose some sentence and rewrite them")
parser.add_argument("-tH","--reThreshold",default=0.5)
parser.add_argument("-tL","--thresholdLow",default=15)

args=parser.parse_args()
#case=0

def record(_,context,modContext,question,answer,modAnswer,groundTruth,delsentence,distance,f):
    info_dict={}
    info_dict['test case number']=_
    info_dict['context']=context
    info_dict['modContext']=modContext
    info_dict['question']=question
    info_dict['groundTruth']=groundTruth
    info_dict['answer']=answer
    info_dict['modAnswer']=modAnswer
    info_dict['delete sentence number']=delsentence
    info_dict["distance value"]=distance
    json.dump(info_dict,f)


    """print(f"------------test case{_}------------",file=fn)
    print("Original Context:\n",context,file=fn)
    print("Modified Context:\n",modContext,file=fn)
    print("Question:\n",question,file=fn)
    print("Standard Answer:     ",groundTruth,file=fn)
    print("Original Answer:     ",answer,'\n',"Modified Answer:     ",modAnswer,file=fn)
    print('',file=fn)"""
    #print("Bug")


def main(args):
    dataset=load_dataset(args.dataset)['validation']
    #fileName=open(args.filename,'w+',encoding='utf-8')
    #for _,data in enumerate(dataset):
    f=open (args.filename,'w+',encoding='utf-8')
    l=len(dataset)
    logf=open(args.logfile,'w+',encoding='utf-8')
    lastContext=''
    lastModContext=''
    lastChange=True
    for i in range((int)(args.start),(int)(args.end)):
        _=i
        data=dataset[i]
        context=data['context']
        question=data['question']
        groundTruth=data['answers']

        print("starting processing data  ......",_,file=logf)
        print("starting processing data  ......",_)
        #Get distance imformation
        modContext=''
        distance=semanticMatch(oriContext=context,question=question)
        delsentence=[]
        #print("finish semanticMatch......")
        if (int)(args.mr)==2:
            modContext,delsentence=MR2(context=context,distance=distance,pattern=args.deleteextent,threshold=float(args.threshold),proportion=args.proportion)
            #print("finish MR2......")
        elif (int)(args.mr)==1:
            if context==lastContext:
                modContext=lastModContext
                print("one",file=logf)
                print(lastModContext)
            else:
                lastContext=context
                modContext,change=MR1(context=context,pattern=args.rewritePattern,distance=distance,reThreshold=(float)(args.reThreshold))
                lastModContext=modContext
                lastChange=change
                print("two",file=logf)
                print(lastModContext)
        model_name='allenai/unifiedqa-'+args.module
        answer=output_answer(question=question,context=context,model_name=model_name)
        #print("finish original answer......")
        modAnswer=''
        if (int)(args.mr)==2:
            if delsentence!=[]:
                modAnswer=output_answer(question=question,context=modContext,model_name=model_name)
            else:
                modAnswer=answer
        elif (int)(args.mr)==1:
            if lastChange:
                modAnswer=output_answer(question=question,context=modContext,model_name=model_name)
                print("change",file=logf)
            else:
                print("unchange",file=logf)
                modAnswer=answer
            #print(delsentence,'yes')
        #print("finish modified answer......")

        print(modAnswer)
        #if not answerMatch(answer=answer,modAnswer=modAnswer,pattern=args.compare,threshold=args.comparethreshold,logfile=logf):
        record(_,context,modContext,question,answer,modAnswer,groundTruth,delsentence,distance,f)
        #print("finish recording......")


def answerAnalysis(args):
    f=open (args.filename,'r',encoding='utf-8')
    result=f.read()
    f.close()
    f=open (args.filename,'w+',encoding='utf-8')
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
    print(result,file=f)

if __name__=='__main__':
    main(args=args)
    #answerAnalysis(args=args)