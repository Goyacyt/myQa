from MR2.sentence_distance import *
import ast
from datasets import load_dataset
import numpy as np

def compare():
    wr=open('compare/output_50.txt',"w",encoding='utf-8')
    fileDir='squad_modify'
    filenum=0
    fileName=fileDir+'/'+'squad_valid_qc_'+str(filenum)+'.txt'
    with open(fileName,"r",encoding='utf-8') as f:
        s=f.read()
    s=s.replace('\n','').replace('\r','')
    s=s.split('}{')
    data_dict=[]
    for i in range(len(s)):
        if i==0:
            data_dict.append(ast.literal_eval(s[i]+'}'))
        elif i==len(s)-1:
            data_dict.append(ast.literal_eval('{'+s[i]))
        else:
            data_dict.append(ast.literal_eval('{'+s[i]+'}'))
    dataset=load_dataset('squad')
    myDistance=[]
    transformerDistance=[]
    spacyDistance=[]
    for i in range(31,50):
        #处理数据集里面的第i个数据
        lmyDistance=[]
        ltransformerDistance=[]
        lspacyDistance=[]
        """context=data_dict[i]['context']
        question=data_dict[i]['question']"""
        context=dataset['validation'][i]['context']
        question=dataset['validation'][i]['question']
        print(question)
        print(question,file=wr)
        contextSentence=context.split('.')
        for k in range(len(contextSentence)):
            if not contextSentence[k]:
                continue
            print(k,":",contextSentence[k])
            print(k,":",contextSentence[k],file=wr)
            lmyDistance.append(input("mydistance:"))
            ltransformerDistance.append(sentenceTransformerRun(contextSentence[k],question))
            lspacyDistance.append(spacyRun(contextSentence[k],question))

            #print(contextSentence[k],"\nmydistance:",lmyDistance[k],"transformerDistance",\
            #      ltransformerDistance[k],"spacyDistance",lspacyDistance[k],file=wr)
        myIdx=np.argsort(lmyDistance)
        print("myDistance:",file=wr)
        for k in range(len(myIdx)):
            print(myIdx[k],":",format(float(lmyDistance[myIdx[k]]),'.6f'),file=wr)
        transformerIdx=np.argsort(ltransformerDistance)
        print("transformerDistance:",file=wr)
        for k in range(len(transformerIdx)):
            if myIdx[k]==transformerIdx[k]:
                t='right'
            else:
                t='false'
            print(transformerIdx[k],":",format(float(ltransformerDistance[transformerIdx[k]]),'.6f'),'    ',t,file=wr)
        spacyIdx=np.argsort(lspacyDistance)
        print("spacyDistance:",file=wr)
        for k in range(len(spacyIdx)):
            if myIdx[k]==spacyIdx[k]:
                t='right'
            else:
                t='false'
            print(spacyIdx[k],":",format(float(lspacyDistance[spacyIdx[k]]),'6f'),'    ',t,file=wr)

        print('',file=wr)
        myDistance.append(lmyDistance)
        transformerDistance.append(ltransformerDistance)
        spacyDistance.append(lspacyDistance)


if __name__=='__main__':
    compare()