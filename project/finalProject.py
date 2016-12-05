import random, getData, unidecode, nltk, util, submission, rapMDP
from nltk.corpus import cmudict
d = cmudict.dict()

def nsyl(word):
	if word.lower() in d:
		return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]] 
	return [0]

def rhyme(inp, level):
     entries = nltk.corpus.cmudict.entries()
     syllables = [(word, syl) for word, syl in entries if word == inp]
     rhymes = []
     for (word, syllable) in syllables:
             rhymes += [word for word, pron in entries if pron[-level:] == syllable[-level:]]
     return set(rhymes)

def getMap(artistName, n):
	ngramMap = {}
	rhymeMap = {}
	lyrics = getData.getData(artistName)
	totalSyllables = 0
	numLines = 0
	rhymeWord = "not chosen yet"
	lines = lyrics.split('\n')
	numLines +=  len(lines)
	for line in lines:
		line += '\n'
		#line = unidecode.unidecode(line)
		words = line.split()
		if len(words) == 0: continue
		for i in range(0, len(words)):
			prevWords = [None for x in range(0, n)]
			for j in range(1, n+1):
				if i-j >= 0:
					prevWords[j-1] = words[j-1]
			totalSyllables += nsyl(words[i])[0]
			ngram = tuple(prevWords)
			if ngram in ngramMap:
				ngramMap[ngram].append(words[i])
			else:
				ngramMap[ngram] = [words[i]]
		if rhymeWord == "not chosen yet":
			rhymeWord = words[-1]
		else:
			if rhymeWord in rhymeMap:
				rhymeMap[rhymeWord].append(words[-1])
			else:
				rhymeMap[rhymeWord] = [words[-1]]
			if words[-1] in rhymeMap:
				rhymeMap[words[-1]].append(rhymeWord)
			else:
				rhymeMap[words[-1]] = [rhymeWord]
			rhymeWord = "not chosen yet"
	avgSyllables = totalSyllables/float(numLines)
	return ngramMap, rhymeMap, avgSyllables


n = 3
ngrams, rhyme, avgSyllables = getMap("Kendrick Lamar", n)
print ngrams
# genRap(ngrams, rhyme, reverseNgramMap)
mdp = rapMDP.RapMDP(rhyme, ngrams, avgSyllables, n)
alg = util.ValueIteration()
alg.solve(mdp, .0001)
util.simulate(mdp, alg)