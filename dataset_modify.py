import re
import ast
from datasets import load_dataset,load_metric
#from qa_testing import question_answerer_0,question_answerer_1,question_answerer_2,question_answerer_3,question_answerer_4
import roberta_base_squad2,longformer,minilm,bert_large_uncased_whole_word
import difflib
d=difflib.Differ()
num=10
epoch=3
datasets=load_dataset("squad_v2")
for e in range(5,7):
    refileName="squad2_valid_qc_"+str(e)+".txt"
    with open(refileName,"r",encoding='utf-8') as f:
        s=f.read()
    s=s.replace('\n','').replace('\r','')
    #print(s)
    wrfileName="squad2_valid_qc_"+str(e)+"_result.txt"
    write_file=open(wrfileName,"w",encoding='utf-8')
    rev_datasets=s.split('}{')
    for i in range(num):
        print(f"------------test case{i}------------",file=write_file)
        q=datasets['validation'][10*e+i]['question']
        ori_c=datasets['validation'][10*e+i]['context']
        answer=datasets['validation'][10*e+i]['answers']['text']
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
        print(pri_c,file=write_file)
        diff=d.compare(ori_list,rev_list)
        print (",\n".join(list(diff)),file=write_file)
        print("question:",q,file=write_file)
        print("right answer:--------",answer,file=write_file)
        ori_result=roberta_base_squad2.output_answer(q,ori_c)
        rev_result=roberta_base_squad2.output_answer(q,rev_c)
        print("model roberta:\noriginal result:-----",ori_result['answer'],"\nmodified result:-----",rev_result['answer'],\
              file=write_file)
        
        ori_result=longformer.output_answer(q,ori_c)
        rev_result=longformer.output_answer(q,rev_c)
        print("model longformer:\noriginal result:-----",ori_result['answer'],"\nmodified result:-----",rev_result['answer'],\
              file=write_file)
        ori_result=minilm.output_answer(q,ori_c)
        rev_result=minilm.output_answer(q,rev_c)
        print("model minilm:\noriginal result:-----",ori_result['answer'],"\nmodified result:-----",rev_result['answer'],\
              file=write_file)
        ori_result=bert_large_uncased_whole_word.output_answer(q,ori_c)
        rev_result=bert_large_uncased_whole_word.output_answer(q,rev_c)
        print("model bert_large:\noriginal result:-----",ori_result['answer'],"\nmodified result:-----",rev_result['answer'],\
              file=write_file)
        """ori_result=albert_xxlarge.output_answer(q,ori_c)
        rev_result=albert_xxlarge.output_answer(q,rev_c)
        print("model albert_xxlarge:\noriginal result:-----",ori_result['answer'],"modified result:-----",rev_result['answer'],\
              file=write_file)"""
        print("\n\n\n",file=write_file)

