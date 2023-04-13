import re
import ast
from datasets import load_dataset
import roberta_base_squad2,longformer,minilm,bert_large_uncased_whole_word
import model_output
import difflib
import torch
from evaluation import evaluate
d=difflib.Differ()
num=10
epoch=3
datasets=load_dataset("squad_v2")
model_name1="allenai/unifiedqa-t5-large"
model_name2="allenai/unifiedqa-t5-base"
model_name3="allenai/unifiedqa-t5-3b"
file_name="t5-large.txt"

def main():
    total=0
    em_score_large=f1_score_large=0
    em_score_base=f1_score_base=0
    em_score_3b=f1_score_3b=0
    for e in range(5,8):
        refileName="squad2_valid_qc_"+str(e)+".txt"
        with open(refileName,"r",encoding='utf-8') as f:
            s=f.read()
        s=s.replace('\n','').replace('\r','')
        #print(s)
        wrfileName="./new/squad2_valid_qc_"+str(e)+"_result.txt"
        write_file=open(wrfileName,"w",encoding='utf-8')
        rev_datasets=s.split('}{')
        for i in range(num):
            total+=1
            q=datasets['validation'][10*e+i]['question']
            ori_c=datasets['validation'][10*e+i]['context']
            answer=datasets['validation'][10*e+i]['answers']['text']
            if(not answer):
                answer=['']
            if i==0:
                data_dict=ast.literal_eval(rev_datasets[i]+'}')
            elif i==num-1:
                data_dict=ast.literal_eval('{'+rev_datasets[i])
            else:
                data_dict=ast.literal_eval('{'+rev_datasets[i]+'}')
            rev_c=data_dict['context']
            #ori_list = re.sub(r"(.{100})", "\\1\n", ori_c)
            ori_list = re.split(r'[,.]', ori_c)
            #rev_list = re.sub(r"(.{100})", "\\1\n", rev_c)
            rev_list = re.split(r'[,.]', rev_c)
            pri_c = re.sub(r"(.{100})", "\\1\n", ori_c)
            print(f"------------test case{10*e+i}------------",file=write_file)
            print("primary context:",file=write_file)
            print(pri_c,file=write_file)
            diff=d.compare(ori_list,rev_list)
            print("----------------------------------------------",file=write_file)
            print("context after modification:",file=write_file)
            print (",\n".join(list(diff)),file=write_file)
            print("----------------------------------------------",file=write_file)
            print("question:",q,file=write_file)
            print("right answer:--------",answer,file=write_file)
            ori_result=model_output.output_answer(q,ori_c,model_name1)
            rev_result=model_output.output_answer(q,rev_c,model_name1)
            em,f1=evaluate(answer,ori_result)
            if ori_result!=rev_result:
                print(model_name1,":\noriginal result:-----",ori_result,"\nmodified result:-----",rev_result,\
                file=write_file)
            em_score_large+=em
            f1_score_large+=f1
            ori_result=model_output.output_answer(q,ori_c,model_name2)
            rev_result=model_output.output_answer(q,rev_c,model_name2)
            em,f1=evaluate(answer,ori_result)
            if ori_result!=rev_result:
                print(model_name2,":\noriginal result:-----",ori_result,"\nmodified result:-----",rev_result,\
                file=write_file)
            em_score_base+=em
            f1_score_base+=f1
            """ori_result=model_output.output_answer(q,ori_c,model_name3)
            rev_result=model_output.output_answer(q,rev_c,model_name3)
            em,f1=evaluate(answer,ori_result)
            if ori_result!=rev_result:
                print(model_name3,":\noriginal result:-----",ori_result,"\nmodified result:-----",rev_result,\
                file=write_file)
            em_score_3b+=em
            f1_score_3b+=f1"""

    output=open('output.txt','w',encoding='utf-8')
    print(model_name1,":\nem score: ",em_score_large*100/total,"f1 score: ",f1_score_large*100/total,file=output)
    print(model_name2,":\nem score: ",em_score_base*100/total,"f1 score: ",f1_score_base*100/total,file=output)
    #print(model_name3,":\nem score: ",em_score_3b*100/total,"f1 score: ",f1_score_3b*100/total)

if __name__=="__main__":
    main()