import spacy

def manually():
    nlp = spacy.load('en_core_web_md')
    sentence="The Super Bowl 50 halftime show was headlined by the British rock group Coldplay with special guest perfrmers Beyoncé and Bruno Mars, who headlined the Super Bowl XLVII and Super Bowl XLVIII halftime shows, respectively. It was the third-most watched U.S."
    doc = nlp(sentence)
    for token in doc:
        print('{0}({1}) <-- {2} -- {3}({4})'.format(token.text, token.tag_, token.dep_, token.head.text, token.head.tag_))

from parrot import Parrot

parrot = Parrot()
phrases = [
  "CBS broadcast Super Bowl 50 in the U.S., and charged an average of $5 million for a 30-second commercial during the game."
]

for phrase in phrases:
  print("-"*100)
  print("Input_phrase: ", phrase)
  print("-"*100)
  paraphrases = parrot.augment(input_phrase=phrase)
  if paraphrases:
    for paraphrase in paraphrases:
      print(paraphrase)