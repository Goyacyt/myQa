from tabulate import tabulate


modelname1="minilm"
accuracy_rate1=66.12207252068575
mis11=1
mis21=8
mis31=1
modelname2="longformer"
accuracy_rate2=35.928893017015625
mis12=0
mis22=2
mis32=0
modelname3="bert"
accuracy_rate3=38.51851851851852
mis13=0
mis23=2
mis33=1
modelname4="roberta"
accuracy_rate4=69.64810615604266
mis14=0
mis24=8
mis34=1
modelname5="allenai/unifiedqa-t5-large"
accuracy_rate5=92.57142857142857
mis15=0
mis25=8
mis35=1
modelname6="allenai/unifiedqa-t5-base"
accuracy_rate6=80.33333333333331
mis16=0
mis26=8
mis36=1
table=[["squad2 dataset"],
    ["","mistake_1","mistake_2","mistake_3","f1_score"],
       [modelname1,1,8,1,"66.12207252068575%"],
       [modelname2,0,2,0,"35.928893017015625%"],
       [modelname3,0,2,1,"38.51851851851852%"],
       [modelname4,0,8,1,"69.64810615604266%"],
       [modelname5,mis15,mis25,mis35,accuracy_rate5],
       [modelname6,mis16,mis26,mis36,accuracy_rate6]]
print(tabulate(table,headers="firstrow"))
modelname5="allenai/unifiedqa-t5-large"
accuracy_rate5=92.57142857142857
mis15=0
mis25=8
mis35=1
modelname6="allenai/unifiedqa-t5-base"
accuracy_rate6=80.33333333333331
mis16=0
mis26=8
mis36=1
table=[["squad dataset"],
    ["","mistake_1","mistake_2","mistake_3","f1_score"],
       [modelname5,mis15,mis25,mis35,accuracy_rate5],
       [modelname6,mis16,mis26,mis36,accuracy_rate6]]
