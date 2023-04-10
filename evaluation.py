import torch
from transformers import AutoTokenizer
from datasets import load_dataset,load_metric
import roberta_base_squad2,longformer,minilm,bert_large_uncased_whole_word
import unified_t5
def predict(context,query):

  inputs = tokenizer.encode_plus(query, context, return_tensors='pt')

  outputs = model(**inputs)
  answer_start = torch.argmax(outputs[0])  # get the most likely beginning of answer with the argmax of the score
  answer_end = torch.argmax(outputs[1]) + 1 

  answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs['input_ids'][0][answer_start:answer_end]))

  return answer

def normalize_text(s):
  """Removing articles and punctuation, and standardizing whitespace are all typical text processing steps."""
  import string, re

  def remove_articles(text):
    regex = re.compile(r"\b(a|an|the)\b", re.UNICODE)
    return re.sub(regex, " ", text)

  def white_space_fix(text):
    return " ".join(text.split())

  def remove_punc(text):
    exclude = set(string.punctuation)
    return "".join(ch for ch in text if ch not in exclude)

  def lower(text):
    return text.lower()

  return white_space_fix(remove_articles(remove_punc(lower(s))))

def compute_exact_match(prediction, truth):
    return int(normalize_text(prediction) == normalize_text(truth))

def compute_f1(prediction, truth):
  pred_tokens = normalize_text(prediction).split()
  truth_tokens = normalize_text(truth).split()
  
  # if either the prediction or the truth is no-answer then f1 = 1 if they agree, 0 otherwise
  if len(pred_tokens) == 0 or len(truth_tokens) == 0:
    return int(pred_tokens == truth_tokens)
  
  common_tokens = set(pred_tokens) & set(truth_tokens)
  
  # if there are no common tokens then f1 = 0
  if len(common_tokens) == 0:
    return 0
  
  prec = len(common_tokens) / len(pred_tokens)
  rec = len(common_tokens) / len(truth_tokens)
  
  return 2 * (prec * rec) / (prec + rec)
     

def give_an_answer(context,query,answer):

  prediction = predict(context,query)
  em_score = compute_exact_match(prediction, answer)
  f1_score = compute_f1(prediction, answer)

  """print(f"Question: {query}")
  print(f"Prediction: {prediction}")
  print(f"True Answer: {answer}")
  print(f"EM: {em_score}")
  print(f"F1: {f1_score}")
  print("\n")"""
  return em_score,f1_score

def main():
  datasets=load_dataset("squad")
  em_score1=em_score2=em_score3=em_score4=0
  f1_score1=f1_score2=f1_score3=f1_score4=0
  total=0
  for i,example in enumerate(datasets['validation']):
    if(i>100): break
    question=example['question']
    context=example['context']
    if not example['answers']['text']:
      truthset=['']
    else:
      truthset=example['answers']['text']
    answer1=unified_t5.output_answer(question,context)
    """answer2=longformer.output_answer(question,context)['answer']
    answer3=minilm.output_answer(question,context)['answer']
    answer4=bert_large_uncased_whole_word.output_answer(question,context)['answer']"""
    total+=1
    em_score1+=max(compute_exact_match(answer1,truth) for truth in truthset)
    """em_score2+=max(compute_exact_match(answer2,truth) for truth in truthset)
    em_score3+=max(compute_exact_match(answer3,truth) for truth in truthset)
    em_score4+=max(compute_exact_match(answer4,truth) for truth in truthset)"""
    f1_score1+=max(compute_f1(answer1,truth) for truth in truthset)
    """f1_score2+=max(compute_f1(answer2,truth) for truth in truthset)
    f1_score3+=max(compute_f1(answer3,truth) for truth in truthset)
    f1_score4+=max(compute_f1(answer4,truth) for truth in truthset)"""
    print("evaluate example",i,em_score1,f1_score1)

  roberta_em_score=em_score1*100/total
  """longformer_em_score=em_score2*100/total
  minilm_em_score=em_score3*100/total
  bert_em_score=em_score4*100/total"""
  roberta_f1=f1_score1*100/total
  """longformer_f1=f1_score2*100/total
  minilm_f1=f1_score3*100/total
  bert_f1=f1_score4*100/total"""
  print("roberta:",roberta_em_score,roberta_f1)
  """print("longformer:",longformer_em_score,longformer_f1)
  print("minilm:",minilm_em_score,minilm_f1)
  print("bert:",bert_em_score,bert_f1)"""


if __name__ == "__main__":
    main()