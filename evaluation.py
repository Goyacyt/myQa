import torch
from transformers import AutoTokenizer
from datasets import load_dataset,load_metric
import roberta_base_squad2,longformer,minilm,bert_large_uncased_whole_word
import model_output

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
     

def main():
  datasets=load_dataset("squad_v2")
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
    model_name1="allenai/unifiedqa-t5-large"
    model_name2="allenai/unifiedqa-t5-base"
    answer1=model_output.output_answer(question,context,model_name1)
    answer2=model_output.output_answer(question,context,model_name2)
    """answer3=minilm.output_answer(question,context)['answer']
    answer4=bert_large_uncased_whole_word.output_answer(question,context)['answer']"""
    total+=1
    em_score1+=max(compute_exact_match(answer1,truth) for truth in truthset)
    em_score2+=max(compute_exact_match(answer2,truth) for truth in truthset)
    """em_score3+=max(compute_exact_match(answer3,truth) for truth in truthset)
    em_score4+=max(compute_exact_match(answer4,truth) for truth in truthset)"""
    f1_score1+=max(compute_f1(answer1,truth) for truth in truthset)
    f1_score2+=max(compute_f1(answer2,truth) for truth in truthset)
    """f1_score3+=max(compute_f1(answer3,truth) for truth in truthset)
    f1_score4+=max(compute_f1(answer4,truth) for truth in truthset)"""
    print(model_name1,"evaluating example ",i,em_score1,f1_score1)
    print(model_name2,"evaluating example ",i,em_score2,f1_score2)

  large_em_score=em_score1*100/total
  base_em_score=em_score2*100/total
  """minilm_em_score=em_score3*100/total
  bert_em_score=em_score4*100/total"""
  large_f1=f1_score1*100/total
  base_f1=f1_score2*100/total
  """minilm_f1=f1_score3*100/total
  bert_f1=f1_score4*100/total"""
  print(model_name1,large_em_score,large_f1)
  print(model_name2,base_em_score,base_f1)
  """print("minilm:",minilm_em_score,minilm_f1)
  print("bert:",bert_em_score,bert_f1)"""

def evaluate(truthset,answer):
  em_score=0
  f1_score=0
  em_score+=max(compute_exact_match(answer,truth) for truth in truthset)
  f1_score+=max(compute_f1(answer,truth) for truth in truthset)
  return em_score,f1_score

if __name__=="__main__":
    main()