import nltk
import random
from nltk.corpus import wordnet as wn

def polysemy(word):
        return len(wn.synsets(word))

clues = ["TALK", "STICK"]
word1 = random.choice(clues)
clues.remove(word1)
word2 = clues[0]


sense1 = "0" + str(random.randint(1, polysemy(word1)))
sense2 = "0" + str(random.randint(1, polysemy(word2)))
try:
	synset1 = wn.synset(word1+".n." + sense1)
except:
	synset1 = wn.synset(word1+".v." + sense1)
try:
	synset2 = wn.synset(word2 +".n." + sense2)
except:
	synset2 = wn.synset(word2 +".v." + sense2)
hypernyms = synset1.hypernyms()
hyponyms = synset1.hyponyms()

related = hypernyms + hyponyms
print("related", related)
maxSimilarity = 0
mostSimilar = None
for item in related:

	mySimilarity = synset2.wup_similarity(synset1)
	if mySimilarity > maxSimilarity:
		maxSimilarity = mySimilarity
		mostSimilar = item
print("Clue from "+ word1+ " and "+word2+" is...")
print(str(mostSimilar)[8:-7])
