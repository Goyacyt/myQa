from sentence_transformers import SentenceTransformer
import torch
from torch import nn

model_path='whaleloops/phrase-bert'
phrase_sim_model=SentenceTransformer(model_path)

cos_sim=nn.CosineSimilarity(dim=0)

def answerMatch(answer,modAnswer,pattern,threshold,logfile):
    answer=answer.strip().lower()
    modAnswer=modAnswer.strip().lower()
    #simple == match:
    if pattern=="sim":
        if (answer==modAnswer) or (answer in modAnswer) or (modAnswer in answer):
            return True
        else:
            return False
    
    elif pattern=="com":
        if (answer==modAnswer) or (answer in modAnswer) or (modAnswer in answer):
            return True
        
        res=phrase_sim_model.encode([answer,modAnswer])
        [e1,e2]=res
        sim=cos_sim(torch.tensor(e1),torch.tensor(e2))
        print(f"{answer} | {modAnswer} | {sim}",file=logfile)
        print(f"similarity of {answer} and {modAnswer} : {sim}")
        if sim>threshold:
            return True
        else:
            return False
        
    else:
        print("answerMatch not realized or wrongly spelled")
        exit(0)


if __name__=="__main__":
    if(answerMatch('Denver Broncos',' the denver broncos defeated the national football conference (NFC) champion Carolina Panthers',"com",0.75)):
        print("match!")