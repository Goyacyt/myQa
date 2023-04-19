import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk import pos_tag, word_tokenize, RegexpParser

# String to parse
to_parse = "This tree is illustrating the constituency relation"

# Find all parts of speech in above sentence
tagged_parts = pos_tag(word_tokenize(to_parse))

# Defining grammar on basis of which we 've to extract
grammar = r'''
NP: {<DT>?<JJ>*<NN>}
P: {<IN>}
V: {<V.*>}
PP: {<p> <NP>}
VP: {<V> <NP|PP>*}'''

 #Extracting all parts of speech
parser = RegexpParser(grammar)

 # Print all parts of speech in above sentence
output = parser.parse(tagged_parts)
print("\nAfter Extracting the parts\n\n", output,"\n")

import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("Apple is looking at buying U.K. startup for $1 billion")

for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
            token.shape_, token.is_alpha, token.is_stop)