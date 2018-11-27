import nltk
from nltk.corpus import wordnet as wn
phone = wn.synset("phone.n.01")
france = wn.synset("france.n.01")
hypernyms = phone.hypernyms()
hyponyms = phone.hyponyms()

related = hypernyms + hyponyms

maxSimilarity = 0
mostSimilar = None
for item in related:
    mySimilarity = france.wup_similarity(phone)
    if mySimilarity > maxSimilarity:
        maxSimilarity = mySimilarity
        mostSimilar = item
print("Clue from 'france' and 'phone' is...")
print(str(mostSimilar)[8:-7])
