from sentence_transformers import SentenceTransformer,util
import re
from datasets import load_dataset
model = SentenceTransformer('all-MiniLM-L6-v2')

def sentenceTransformerRun(context,question):

    sentence_embeddings=model.encode(context)
    question_embeddings=model.encode(question)

    cos_sim=util.cos_sim(sentence_embeddings,question_embeddings)
    """sentence_distance=[]
    for i in range(len(cos_sim)):
        if not sentence_context[i]:
            continue
        sentence_distance.append([question,sentence_context[i],cos_sim[i][0].item()])"""
    return cos_sim[0][0]



import spacy
nlp = spacy.load("en_core_web_lg")

def spacyRun(context,question):

    doc_question=nlp(question)
    doc_sentence=nlp(context)
    sim=doc_question.similarity(doc_sentence)

    return sim
