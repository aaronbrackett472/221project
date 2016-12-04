import random

def getMap():
	f = open('kendrick.txt', 'r')
	ngramMap = {}
	for line in f:
		print line
		words = line.split()
		if len(words) == 0: continue
		if 'START_LINE' in ngramMap:
			ngramMap['START_LINE'].append(words[0])
		else:
			ngramMap['START_LINE'] = [words[0]]
		for i in range(0, len(words)-1):
			if words[i] in ngramMap:
				ngramMap[words[i]].append(words[i+1])
			else:
				ngramMap[words[i]] = [words[i+1]]
		if words[-1] in ngramMap:
			ngramMap[words[-1]].append('END_LINE')
		else:
			ngramMap[words[-1]] = ['END_LINE']
	return ngramMap

def genRap(ngramMap):
	for i in range(0,16):
		line = ''
		randomStartIndex = random.randint(0, len(ngramMap['START_LINE'])-1)
		curToken = ngramMap['START_LINE'][randomStartIndex]
		line += curToken
		while curToken != 'END_LINE':
			randomIndex =random.randint(0, len(ngramMap[curToken])-1)
			curToken = ngramMap[curToken][randomIndex]
			line += curToken
		print line

myMap = getMap()
print "map: "
print myMap
genRap(myMap)