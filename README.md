模型：

    1.bert-large-uncased-whole-word-masking-finetuned-squad\  bert_large_uncased_whole_word.py
    
    2.longformer-base-4096-finetuned-squadv1\  longformer.py
    
    3.minilm-uncased-squad2\  minilm.py
    
    4.roberta-base-squad2\  roberta_base_squad2.py
    
    1.2.3.4.分别是4个从hugging face上下载的模型 对应的.py文件主要包含一个接收一对{context,question}输出一个answer的函数
    

dataset_modify.py是主函数，其中引用4个模型，分别take原训练集的{context,question}和手动修改过的{context,question}后，分别得到ori_answer和rev_answer，两个answer不完全相同时，输出如下格式的文本块到summary.txt中：

    原context
    
    ------------------------------
    
    context修改过的地方
    
    ------------------------------
    
    原问题
    
    正确answer
    
    model:使用的模型
    
    original answer:原context对应的answer
    
    modified answer:修改过的context对应的answer
    
    model:使用的模型
    
    original answer:原context对应的answer
    
    modified answer:修改过的context对应的answer
    
    ......
 

squad2_valid_qc_x.txt是手动修改过的数据(x=0,1,2,3...)

squad2_valid_qc_x_result.txt是全部的输出，没有经过answer对比的筛选(x=0,1,2,3...)
