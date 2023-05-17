import ast
import argparse
from answerCompare import *
import json

parser=argparse.ArgumentParser(description="input MR type")
parser.add_argument("-f","--filename",default="output.txt",help="file to record the bugs")
parser.add_argument("-t","--simThreshold",default=0.8,help="thethreshold to dicide whether two answers are the same")
parser.add_argument("-cmp","--compare",default="complicate",help="the type of comparing two answers two pattern : complicate and simple")
parser.add_argument("-bl","--buglogfile",default="buglogfile.json")
parser.add_argument("-ml","--matchlogfile",default="matchlog.json")
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
    f=open(args.filename,'r',encoding='utf-8')
    logfile=open(args.matchlogfile,'w+',encoding='utf-8')
    bugfile=open(args.buglogfile,'w+',encoding='utf-8')
    resultList=f.read()
    resultList=ast.literal_eval(resultList)
    simthreshold=args.simThreshold
    totalNum=0
    bugNum=0#modified answer is different from original answer
    oEqualg=0
    mEqualg=0
    bugRate=0
    fp=0#the number of false positive
    fpRate=0
    contextNum=-1#the number of different context
    contextList=[]#different cotext
    questionNumPerContext=[]#the number of question asking each context
    questionPerContext=[]#the question list of each context
    bugPerContext=[]#the number of each context bugs
    fpPerContext=[]
    bugRateofContext=[]#the rate
    fpRateofContext=[]
    lastContext=''
    for i in range(len(resultList)):
        thisResult=resultList[i]
        caseNum=thisResult['test case number']
        context=thisResult['context']
        modContext=thisResult['modContext']
        question=thisResult['question']
        groundTruth=thisResult['groundTruth']
        answer=thisResult['answer']
        modAnswer=thisResult['modAnswer']
        dsn=thisResult['delete sentence number']
        dv=thisResult['distance value']

        
        totalNum+=1
        if context!=lastContext:
            bugRateofContext.append(bugPerContext[contextNum]/questionNumPerContext[contextNum])
            fpRateofContext.append(fpPerContext[contextNum]/bugPerContext[contextNum])
            lastContext=context
            contextNum+=1
            questionPerContext.append([])
            questionNumPerContext.append(0)
            bugPerContext.append(0)
            fpPerContext.append(0)
            contextList.append([caseNum,context])
        
        questionNumPerContext[contextNum]+=1
        questionPerContext[contextNum].append([caseNum,question,modContext])

        if not answerMatch(answer,modAnswer,args.compare,args.simThreshold,logfile):
            bug_dict={}
            bug_dict['test case number']=caseNum
            bug_dict['context']=context
            bug_dict['modContext']=modContext
            bug_dict['question']=question
            bug_dict['groundTruth']=groundTruth
            bug_dict['answer']=answer
            bug_dict['modAnswer']=modAnswer
            bug_dict['delete sentence number']=dsn
            bug_dict["distance value"]=dv
            json.dump(bug_dict,bugfile)

            #discover a bug
            bugNum+=1
            bugPerContext[contextNum]+=1
            if groundTruth not in modContext:
                fp+=1
                fpPerContext[contextNum]+=1
            text=groundTruth['text']
            for t in range(len(text)):
                if answerMatch(text[t],modAnswer,args.compare,args.simThreshold,logfile):
                    mEqualg+=1
                    break
            for t in range(len(text)):
                if answerMatch(answer,text[t],args.compare,args.simThreshold,logfile):
                    oEqualg+=1
                    break

    bugRate=bugNum/totalNum
    fpRate=fp/bugNum

    wf=open(args.filename[:-5]+'res.json','w+',encoding='utf-8')
    info_dict={}
    info_dict['Total Number']=totalNum
    info_dict['Bug Number']=bugNum
    info_dict['Bug Rate']=bugRate
    info_dict['False Positive Number']=fp
    info_dict['FP Rate']=fpRate

    info_dict['Bug Rate of Context']=bugRateofContext
    info_dict['FP Rate of Context']=fpRateofContext
    info_dict['Context list']=contextList
    info_dict['Question and ModContext']=questionPerContext
    json.dump(info_dict,wf)



if __name__=='__main__':
    answerAnalysis(args)