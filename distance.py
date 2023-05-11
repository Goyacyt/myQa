from sentence_transformers import SentenceTransformer,util
import re
from datasets import load_dataset
import sys

#model = SentenceTransformer('all-MiniLM-L6-v2')
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def sentenceTransformerRun(oriContext,question,topk):
    """sentence_embeddings=model.encode(context)
    question_embeddings=model.encode(question)

    cos_sim=util.cos_sim(sentence_embeddings,question_embeddings)
    sentence_distance=[]
    for i in range(len(cos_sim)):
        if not sentence_context[i]:
            continue
        sentence_distance.append([question,sentence_context[i],cos_sim[i][0].item()])
    return cos_sim[0][0]"""
    return 

def semanticMatch(oriContext,question):
    context=oriContext.split('.')
    context=context[:-1]
    # Context embeddings
    context_embeddings = model.encode(context)

    # Question embeddings
    question_embeddings = model.encode(question)

    # Find the top k context sentence matching the question
    hits = util.semantic_search(question_embeddings,context_embeddings,top_k=len(context))
    hits=hits[0]
    # Print and save results
    results=[]
    #print(f"Question: {question}")
    for hit in hits:
        #print(hit['corpus_id'],type(hit['corpus_id']))
        #print(context[hit['corpus_id']], "(Score: {:.4f})".format(hit['score']))
        results.append([hit['corpus_id'],hit['score']])
    
    return results


import spacy
nlp = spacy.load("en_core_web_lg")

def spacyRun(context,question):

    doc_question=nlp(question)
    doc_sentence=nlp(context)
    sim=doc_question.similarity(doc_sentence)

    return sim

def low(value):
    value=value*100
    res=round(value)-(round(value))%10
    res=(int)(res/10)
    #print(f"value  {value},res  {res}")
    return res 

def threshold():
    dataset=load_dataset('squad')['validation']
    max_max=0
    max_min=sys.maxsize
    min_max=0
    min_min=sys.maxsize
    max_avg=0
    min_avg=0
    num=0
    sen_num=0
    distribute=[0 for __ in range(10)]
    for _,data in enumerate(dataset):
        """if _>50:
            break"""
        context=data['context']
        question=data['question']
        num+=1

        #Get distance imformation
        distance=semanticMatch(oriContext=context,question=question)
        for i in range(len(distance)):
            v=distance[i][1]
            n=low(v)
            distribute[n]=distribute[n]+1
            sen_num=sen_num+1
        if(len(distance)>1):
            ma=0
            mi=len(distance)-1
            if(distance[ma][1]>max_max):
                max_max=distance[ma][1]
            if(distance[ma][1]<max_min):
                max_min=distance[ma][1]
            max_avg=max_avg+distance[ma][1]

            if(distance[mi][1]<min_min):
                min_min=distance[mi][1]
            if(distance[mi][1]>min_max):
                min_max=distance[mi][1]
            min_avg=min_avg+distance[mi][1]

    min_avg=min_avg/num
    max_avg=max_avg/num
    print("max from %d to %d and average is %d",max_min,max_max,max_avg)
    print("min from %d to %d and average is %d",min_min,min_max,min_avg)
    #distribute.sort()
    print(f"total sentence number:{sen_num}")
    ver=0
    for i in range(len(distribute)):
        ver+=distribute[i]
        print(f"between {i*10}% and {(i+1)*10}%     amount:{distribute[i]}    proportion\
              :{distribute[i]/sen_num}")
    if ver==sen_num:
        print("right")
    return distribute,sen_num


if __name__=='__main__':
    threshold()
