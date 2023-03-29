（模型：
    1.bert-large-uncased-whole-word-masking-finetuned-squad\  bert_large_uncased_whole_word.py
    2.longformer-base-4096-finetuned-squadv1\  longformer.py
    3.minilm-uncased-squad2\  minilm.py
    4.roberta-base-squad2\  roberta_base_squad2.py
    1.2.3.4.分别是4个从hugging face上下载的模型 对应的.py文件主要包含一个接收一对{context,question}输出一个answer的函数
）

dataset_modify.py是主函数，其中4个模型分别take原训练集的{context,question}和手动修改过的{context,question}分别得到
ori_answer和rev_answer，两个answer不完全相同时，输出：
    原context
    ----------------------------------------------
    context修改过的地方
    ----------------------------------------------
    原问题
    正确answer
    原context对应的answer
    修改过的context对应的answer
到summary.txt里面

squad2_valid_qc_x.txt是手动修改过的数据