from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch

tokenizer = AutoTokenizer.from_pretrained("./roberta-base-squad2")

model = AutoModelForQuestionAnswering.from_pretrained("./roberta-base-squad2")
def output_answer(question,context):
    inputs = tokenizer(question, context, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    #print(outputs)
    start_logits = outputs.start_logits
    end_logits = outputs.end_logits

    sequence_ids = inputs.sequence_ids()
    mask = [i != 1 for i in sequence_ids]
    mask[0] = False # Unmask the [CLS] token
    mask = torch.tensor(mask)[None]

    start_logits[mask] = -10000
    end_logits[mask] = -10000

    start_probabilities = torch.nn.functional.softmax(start_logits, dim=-1)[0]
    end_probabilities = torch.nn.functional.softmax(end_logits, dim=-1)[0]
    scores = start_probabilities[:, None] * end_probabilities[None, :]
    scores = torch.triu(scores)
    max_index = scores.argmax().item()
    start_index = max_index // scores.shape[1]
    end_index = max_index % scores.shape[1]

    inputs_with_offsets = tokenizer(question, context, return_offsets_mapping=True)
    offsets = inputs_with_offsets["offset_mapping"]

    start, _ = offsets[start_index]
    _, end = offsets[end_index]

    result = {
        "answer": context[start:end],
        "start": start,
        "end": end,
        "score": float(scores[start_index, end_index]),
    }
    #print(result)
    return result