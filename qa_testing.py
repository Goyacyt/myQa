from transformers import pipeline
question_answerer_0 = pipeline("question-answering", model='distilbert-base-cased-distilled-squad')
question_answerer_1= pipeline("question-answering", model='bert-large-uncased-whole-word-masking-finetuned-squad')
question_answerer_2= pipeline("question-answering", model='deepset/roberta-base-squad2')
question_answerer_3= pipeline("question-answering", model='deepset/minilm-uncased-squad2')
question_answerer_4= pipeline("question-answering", model='Rakib/roberta-base-on-cuad')