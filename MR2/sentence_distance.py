from sentence_transformers import SentenceTransformer,util
import re
from datasets import load_dataset

def sentence_transformer_run():
    model = SentenceTransformer('all-MiniLM-L6-v2')

    dataset=load_dataset("squad")

    distance=[]
    for j in range(50):
        context=dataset['validation'][j]['context']
        question=dataset['validation'][j]['question']
        sentence_context=context.split('.')
        sentence_embeddings=model.encode(sentence_context)
        question_embeddings=model.encode(question)

        cos_sim=util.cos_sim(sentence_embeddings,question_embeddings)
        sentence_distance=[]
        for i in range(len(cos_sim)):
            if not sentence_context[i]:
                continue
            sentence_distance.append([question,sentence_context[i],cos_sim[i][0].item()])

        distance.append(sentence_distance)
    return distance

import spacy

def spacy_run():
    nlp = spacy.load("en_core_web_lg")

    dataset=load_dataset("squad")
    distance=[]
    for j in range(50):
        context=dataset['validation'][j]['context']
        question=dataset['validation'][j]['question']
        sentence_context=context.split('.')
        doc_question=nlp(question)
        sentence_distance=[]
        for i in range(len(sentence_context)):
            if not sentence_context[i]:
                continue
            doc_sentence=nlp(sentence_context[i])
            sim=doc_question.similarity(doc_sentence)
            sentence_distance.append([question,sentence_context[i],sim])
        distance.append(sentence_distance)

    return distance

if __name__== "__main__":
    filename='./MR2/transformer_spacy_distance.txt'
    file=open(filename,"w",encoding='utf-8')
    print("The first number is from transformers.The second is from spacy",file=file)
    distance1=sentence_transformer_run()
    distance2=spacy_run()
    for i in range(len(distance1)):
        print("test case:",i,file=file)
        sentence_distance1=distance1[i]
        sentence_distance2=distance2[i]
        for j in range(len(sentence_distance1)):
            sentence_distance1[j].append(sentence_distance2[j][2])
            print(sentence_distance1[j],file=file)
        print("",file=file)