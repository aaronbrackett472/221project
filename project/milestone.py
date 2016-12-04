import random, getData, unidecode, nltk, util
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

def getMap(artistName):
	ngramMap = {}
	rhymeMap = {}
	reverseNgramMap = {}
	songLyrics = getData.getData(artistName)
	totalSyllables = 0
	numLines = 0
	for lyrics in songLyrics:
		if lyrics == None: continue
		lyrics = unidecode.unidecode(lyrics)
		prevWord = "not chosen yet"
		lines = lyrics.split('\n')
		numLines +=  len(lines)
		for line in lines:
			line += '\n'
			#line = unidecode.unidecode(line)
			words = line.split()
			if len(words) == 0: continue
			if 'START_LINE' in ngramMap:
				ngramMap['START_LINE'].append(words[0])
			else:
				ngramMap['START_LINE'] = [words[0]]
			if words[0] in reverseNgramMap:
				reverseNgramMap[words[0]].append('START_LINE')
			else:
				reverseNgramMap[words[0]] = ['START_LINE']
			for i in range(0, len(words)-1):
				if words[i] in ngramMap:
					ngramMap[words[i]].append(words[i+1])
				else:
					ngramMap[words[i]] = [words[i+1]]
				if i-1 >= 0:
						if words[i] in reverseNgramMap:
							reverseNgramMap[words[i]].append(words[i-1])
						else:
							reverseNgramMap[words[i]] =[words[i-1]]
				totalSyllables += nsyl(words[i])
			totalSyllables += nsyl(words[-1])
			if len(words) >= 2:
				if words[-1] in reverseNgramMap:
					reverseNgramMap[words[-1]].append(words[-2])
				else:
					reverseNgramMap[words[-1]] = [words[-2]]
			else:
				if words[-1] in reverseNgramMap:
					reverseNgramMap[words[-1]].append('START_LINE')
				else:
					reverseNgramMap[words[-1]] = ['START_LINE']
			if words[-1] in ngramMap:
				ngramMap[words[-1]].append('END_LINE')
			else:
				ngramMap[words[-1]] = ['END_LINE']
			if 'END_LINE' in ngramMap:
				ngramMap['END_LINE'].append(words[-1])
			else:
				ngramMap['END_LINE'] = [words[-1]]
			if prevWord == "not chosen yet":
				prevWord = words[-1]
			else:
				if prevWord in rhymeMap:
					rhymeMap[prevWord].append(words[-1])
				else:
					rhymeMap[prevWord] = [words[-1]]
				if words[-1] in rhymeMap:
					rhymeMap[words[-1]].append(prevWord)
				else:
					rhymeMap[words[-1]] = [prevWord]
				prevWord = "not chosen yet"
				# if prevWord in rhyme(words[-1], 1):
				# 	print "rhyme"
				# 	print prevWord, words[-1]
				# prevWord = "not chosen yet"
	avgSyllables = totalSyllables/float(numLines)
	return ngramMap, rhymeMap, reverseNgramMap, avgSyllables

def genRap(ngramMap, rhymeMap, reverseNgramMap):
	rhymeWord = None
	for i in range(0,16):
		line = ''
		if i % 2 == 0:
			randomStartIndex = random.randint(0, len(ngramMap['START_LINE'])-1)
			curToken = ngramMap['START_LINE'][randomStartIndex]
			line += curToken
			prevToken = None
			while curToken != 'END_LINE':
				randomIndex =random.randint(0, len(ngramMap[curToken])-1)
				prevToken = curToken
				curToken = ngramMap[curToken][randomIndex]
				while  curToken == 'START_LINE':
					curToken = ngramMap[curToken][randomIndex]
				line += ' ' + curToken
			rhymeWord = prevToken
			line = line[:-8]
			print line
		else:
			randomStartIndex = random.randint(0, len(rhymeMap[rhymeWord])-1)
			curToken = rhymeMap[rhymeWord][randomStartIndex]
			line = curToken + line
			while curToken != 'START_LINE':
				randomIndex =random.randint(0, len(reverseNgramMap[curToken])-1)
				curToken = reverseNgramMap[curToken][randomIndex]
				line = curToken + ' ' + line
			line = line[11:]
			print line

ngrams, rhyme, reverseNgramMap = getMap("Kendrick Lamar")
# genRap(ngrams, rhyme, reverseNgramMap)
mdp = rapMDP.RapMDP(rhyme, ngrams)