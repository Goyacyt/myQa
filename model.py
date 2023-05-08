from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import os
os.environ['CURL_CA_BUNDLE'] = ''

def output_answer(question,context,model_name):
    model=AutoModelForSeq2SeqLM.from_pretrained(model_name)
    tokenizer=AutoTokenizer.from_pretrained(model_name)
    device = torch.device("cuda")
    inputs = tokenizer(question, context, return_tensors="pt").input_ids.to(device)
    model.to(device)
    with torch.no_grad():
        outputs = model.generate(inputs)
    #print(outputs)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)