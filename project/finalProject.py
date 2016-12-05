import random, getData, unidecode, nltk, util, submission
from nltk.corpus import cmudict
d = cmudict.dict()

def nsyl(word):
  return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]] 

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
	songLyrics = getData.getData(artistName)
	totalSyllables = 0
	numLines = 0
	for lyrics in songLyrics:
		if lyrics == None: continue
		lyrics = unidecode.unidecode(lyrics)
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
				if prevWords in ngramMap:
					ngramMap[prevWords].append(words[i])
				else:
					ngramMap[prevWords] = [words[i]]
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
	return ngramMap, rhymeMap, reverseNgramMap, avgSyllables


n = 3
ngrams, rhyme, reverseNgramMap = getMap("Kendrick Lamar", n)
print rhyme
# genRap(ngrams, rhyme, reverseNgramMap)
mdp = rapMDP.RapMDP(rhyme, ngrams, n)
viAlgorithm = submission.QLearningAlgorithm(mdp.actions(), mdp.discount())
print "hello", viAlgorithm.actions()
viAlgorithm.solve(originalMDP)
util.simulate(mdp, viAlgorithm)