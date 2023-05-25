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

def merge(args):
    f=open ('MR1.txt','r',encoding='utf-8')
    s=f.read()
    ff=open ('infopro_03_381.json','r',encoding='utf-8')
    ss=ff.read()
    fff=open ('infopro_03_1230.json','r',encoding='utf-8')
    sss=fff.read()
    result=s+ss+sss
    wf=open ('infoproportion_03_50.json','w+',encoding='utf-8')
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

def answerAnalysis(args):

    whWord=[['what','which'],['what year','what month','what day','when','in what year','in which year'],['how many'],['how'],['who'],['where'],['why'],['if'],['other wh']]
    whWordNum=[0 for i in range(len(whWord))]
    whWordNumBug=[0 for i in range(len(whWord))]
    whWordNumBugRate=[0 for i in range(len(whWord))]

    thisresfile=args.filename[:-5]+'result_'+'threshold_'+str(args.simThreshold)[-2:]+'.json'
    f=open(args.filename,'r',encoding='utf-8')
    logfilename=thisresfile[:-5]+'_'+args.matchlogfile
    logfile=open(logfilename,'w+',encoding='utf-8')
    bugfilename=thisresfile[:-5]+'_'+args.buglogfile
    bugfile=open(bugfilename,'w+',encoding='utf-8')
    resultList=f.read()
    resultList=ast.literal_eval(resultList)
    simThreshold=(float)(args.simThreshold)
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
    bugfpRateofContext=[]
    lastContext=''
    for i in range(len(resultList)):
        thisResult=resultList[i]
        caseNum=thisResult['test case number']
        context=thisResult['context']
        modContext=thisResult['modContext']
        question=thisResult['question'].strip().lower()
        groundTruth=thisResult['groundTruth']
        answer=thisResult['answer']
        modAnswer=thisResult['modAnswer']
        dsn=thisResult['delete sentence number']
        dv=thisResult['distance value']
        
        findwh=0
        whtype=-1
        for i in range(len(whWord)-1):
            wh=whWord[i]
            for j in range(len(wh)):
                w=wh[j]
                if question.startswith(w):
                    whWordNum[i]+=1
                    findwh=1
                    whtype=i
                    break
            if findwh:
                break

        if not findwh:
            #print(question)
            whWordNum[len(whWord)-1]+=1
            whtype=len(whWord)-1
        
        totalNum+=1
        if context!=lastContext:
            if contextNum>=0:
                temp_dict={}
                temp_dict['End case number']=caseNum
                temp_dict['context number']=contextNum
                temp_dict['Bug rate']=0
                temp_dict['FP Rate']=0
                if questionNumPerContext[contextNum]!=0:
                    temp_dict['Bug rate']=bugPerContext[contextNum]/questionNumPerContext[contextNum]
                    bugRateofContext.append(bugPerContext[contextNum]/questionNumPerContext[contextNum])
                if bugPerContext[contextNum]!=0:
                    temp_dict['FP Rate']=fpPerContext[contextNum]/bugPerContext[contextNum]
                    fpRateofContext.append(fpPerContext[contextNum]/bugPerContext[contextNum])
                bugfpRateofContext.append(temp_dict)
            
            lastContext=context
            contextNum+=1
            questionPerContext.append([])
            questionNumPerContext.append(0)
            bugPerContext.append(0)
            fpPerContext.append(0)
            contextList.append([caseNum,context])
        
        questionNumPerContext[contextNum]+=1
        questionPerContext[contextNum].append([caseNum,question,modContext])

        if not answerMatch(answer,modAnswer,args.compare,simThreshold,logfile,caseNum):
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

            whWordNumBug[whtype]+=1


            text=groundTruth['text']
            for t in range(len(text)):
                if text[t] not in modContext:
                    fp+=1
                    fpPerContext[contextNum]+=1
                    break
            #TODO:not sure
            
            for t in range(len(text)):
                if answerMatch(text[t],modAnswer,args.compare,simThreshold,logfile,caseNum):
                    mEqualg+=1
                    break

            
            for t in range(len(text)):
                if answerMatch(answer,text[t],args.compare,simThreshold,logfile,caseNum):
                    oEqualg+=1
                    break

    bugRate=bugNum/totalNum
    fpRate=fp/bugNum
    for i in range(len(whWord)):
        if whWordNum[i]!=0:
            whWordNumBugRate[i]=whWordNumBug[i]/whWordNum[i]

    whBug=[]
    for i in range(len(whWord)):
        tem_dict={}
        tem_dict['wh-word']=whWord[i]
        tem_dict['total number']=whWordNum[i]
        tem_dict['bug number']=whWordNumBug[i]
        tem_dict['bug rate']=whWordNumBugRate[i]
        whBug.append(tem_dict)

    wf=open(thisresfile,'w+',encoding='utf-8')
    info_dict={}
    info_dict['Total Number']=totalNum
    info_dict['Bug Number']=bugNum
    info_dict['Bug Rate']=bugRate
    info_dict['False Positive Number']=fp
    info_dict['FP Rate']=fpRate
    info_dict['original answer=standard answer']=oEqualg
    info_dict['modified answer=standard answer']=mEqualg
    info_dict['original answer!=standard answer && modified answer!=standard answer']=bugNum-oEqualg-mEqualg

    whBugs=''
    for i in range(len(whBug)):
        whBugs=whBugs+str(whBug[i])+'\n'

    info_dict['bug rate related to the wh-word of a question']=whBugs

    info_dict['Bug Rate of Context']=bugRateofContext
    info_dict['FP Rate of Context']=fpRateofContext
    info_dict['Bug Rate and FP Rate of Context']=bugfpRateofContext
    info_dict['Context list']=contextList
    info_dict['Question and ModContext']=questionPerContext
    json.dump(info_dict,wf)
    wf.close()
    logfile.close()
    bugfile.close()
    beauty(logfilename)
    beauty(bugfilename)
    otherbeauty(thisresfile)

def beauty(file):
    f=open(file,'r',encoding='utf-8')
    result=f.read()
    result=result.split('}{')
    wf=open(file,'w',encoding='utf-8')
    for i in range(len(result)):
        if i==0:
            result[i]=result[i]+'}\n'
        elif i==len(result)-1:
            result[i]='{'+result[i]
        else:
            result[i]='{'+result[i]+'}\n'
        print(result[i],file=wf)
        #result[i]=ast.literal_eval(result[i])
    #print(result[0]['groundTruth'],result[0]['answer'])
    print(result,file=wf)

def otherbeauty(file):
    f=open(file,'r',encoding='utf-8')
    result=f.read()
    result=ast.literal_eval(result)
    wf=open(file,'w',encoding='utf-8')
    for key in result:
        print(key+':'+str(result[key]),file=wf)

if __name__=='__main__':
    merge(args)
    #answerAnalysis(args)
    
