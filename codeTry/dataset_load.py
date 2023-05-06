from datasets import load_dataset,load_metric
import re
datasets=load_dataset("squad")
print(datasets)
epoch=10
num=10
for i in range(epoch):
    f=open("./squad_modify/squad_valid_qc_"+str(i)+".txt","w",encoding='utf-8')
    for j in range(num):
        s=str(datasets['validation'][i*num+j])
        s = re.sub(r"(.{100})", "\\1\n", s)
        print(s,file=f)