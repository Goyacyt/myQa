import sys
import numpy as np

def MR2(context,distance,pattern,threshold,proportion):
    context=context.split('.')
    context=context[:-1]
    delnum=[]
    if pattern=="leastone":
        if len(distance)>1:
            del context[distance[len(distance)-1][0]]
    elif pattern=="threshold":
        for i in range(len(distance)):
            if distance[i][1]<threshold:
                delnum.append(distance[i][0])
                #del context[distance[i][0]]
        delnum.sort(reverse=True)
        for i in range(len(delnum)):
            del context[delnum[i]]
    elif pattern=="proportion":
        for i in range(len(distance)):
            if distance[i][1]<threshold:
                v=np.random.rand()
                #print(f"v:{v}")
                if v<proportion:
                    delnum.append(distance[i][0])
        delnum.sort(reverse=True)
        for i in range(len(delnum)):
            del context[delnum[i]]
    else:
        print("MR type not realized or wrong spelled")
        sys.exit()
    str='.'
    context=str.join(context)
    context=context+'.'
    return context,delnum

from parrot import Parrot
from transformers import *

parrot = Parrot()

model = PegasusForConditionalGeneration.from_pretrained("tuner007/pegasus_paraphrase")
tokenizer = PegasusTokenizerFast.from_pretrained("tuner007/pegasus_paraphrase")

def get_paraphrased_sentences(model, tokenizer, sentence, num_return_sequences=5, num_beams=5):
    inputs = tokenizer([sentence], truncation=True, padding="longest", return_tensors="pt")
    outputs = model.generate(
        **inputs,
        num_beams=num_beams,
        num_return_sequences=num_return_sequences,
    )
    return tokenizer.batch_decode(outputs, skip_special_tokens=True)

def MR1(context,pattern,distance,reThreshold):
    
    context=context.split('.')
    context=context[:-1]
    rewriteContext=[]
    change=False
    if pattern=='all':
        for sentence in context:
            #print(sentence)
            paraphrases=parrot.augment(input_phrase=sentence)
            #print(paraphrases)
            if not paraphrases:
                rewriteContext.append(sentence)
            else:
                rewriteContext.append(paraphrases[0][0])
                if paraphrases[0][1]!=0:
                    change=True
    elif pattern=='proportion':
        sorted(distance,key=(lambda x:x[0]))
        for i in range(len(context)):
            if distance[i][1]>reThreshold:
                rewriteContext.append(context[i])
            else:
                paraphrases=get_paraphrased_sentences(model,tokenizer,context[i])
                if not paraphrases:
                    rewriteContext.append(context[i])
                else:
                    rewriteContext.append(paraphrases[0])
                    change=True
        
    else:
        print("MR type not realized or wrong spelled")
        sys.exit()
    str='.'
    rewriteContext=str.join(rewriteContext)
    rewriteContext=rewriteContext+'.'
    return rewriteContext,change

if __name__=='__main__':
    context="The Broncos took an early lead in Super Bowl 50 and never trailed. Newton was limited by Denver's defense, which sacked him seven times and forced him into three turnovers, including a fumble which they recovered for a touchdown. Denver linebacker Von Miller was named Super Bowl MVP, recording five solo tackles, 2½ sacks, and two forced fumbles."
    res,change=MR1(context,"all",1,1,1)
    if change:
        print(res)

