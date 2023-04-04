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
table=[["","mistake_1","mistake_2","mistake_3","accuracy_rate"],
       [modelname1,1,8,1,"66.12207252068575%"],
       [modelname2,0,2,0,"35.928893017015625%"],
       [modelname3,0,2,1,"38.51851851851852%"],
       [modelname4,0,8,1,"69.64810615604266%"]]
print(tabulate(table,headers="firstrow"))
