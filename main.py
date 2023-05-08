import argparse
from datasets import load_dataset
from distance import *
from transformer import *
from model import output_answer
from answerCompare import answerMatch
import difflib
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser=argparse.ArgumentParser(description="input MR type")

parser.add_argument("--mr",default=2,help="MR type")
parser.add_argument("--module",default="t5-base",help="choose between t5-large or\
                    t5-base or t5-3b")
parser.add_argument("--dataset",default="squad",help="choose between squad2|squad|boolq")
parser.add_argument("--lowk",default=True,help="true if you want to delete the least associated sentence")
parser.add_argument("-f","--filename",default="output.txt",help="file to record the bugs")
parser.add_argument("-de","--deleteextent",default="least",help="the pattern of deleting unrelated message,you can\
                    choose between least|proportion|threshold")
parser.add_argument("-p","--proportion",default=0.3,help="the proportion of sentences being deleted")
parser.add_argument("-t","--threshold",default=0.4,help="delete the sentence whose distance is below this value")

args=parser.parse_args()
#case=0

def record(context,modContext,question,answer,modAnswer,groundTruth,fn,_):
    print(f"------------test case{_}------------",file=fn)
    print("Original Context:\n",context,file=fn)
    print("Modified Context:\n",modContext,file=fn)
    print("Question:\n",question,file=fn)
    print("Standard Answer:     ",groundTruth,file=fn)
    print("Original Answer:     ",answer,'\n',"Modified Answer:     ",modAnswer,file=fn)
    print('',file=fn)


def main(args):
    dataset=load_dataset(args.dataset)['validation']
    fileName=open(args.filename,'w+',encoding='utf-8')
    for _,data in enumerate(dataset):
        context=data['context']
        question=data['question']
        groundTruth=data['answers']

        print("starting processing data  ......",_)
        #Get distance imformation
        modContext=''
        distance=semanticMatch(oriContext=context,question=question)
        print("finish semanticMatch......")
        if args.mr==2:
            modContext=MR2(context=context,distance=distance,pattern='leastone')
            print("finish MR2......")
        elif args.mr==1:
            modContext=MR1(context=context,pattern="")

        model_name='allenai/unifiedqa-'+args.module
        answer=output_answer(question=question,context=context,model_name=model_name)
        print("finish original answer......")
        modAnswer=output_answer(question=question,context=modContext,model_name=model_name)
        print("finish modified answer......")

        if not answerMatch(answer=answer,modAnswer=modAnswer):
            record(context,modContext,question,answer,modAnswer,groundTruth,fileName,_)
        print("finish recording......")



if __name__=='__main__':
    main(args=args)