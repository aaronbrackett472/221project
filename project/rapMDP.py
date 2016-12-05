from nltk.corpus import cmudict
import nltk, util
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




class RapMDP(util.MDP):
    def __init__(self, rhymeMap, wordMap, idealSyllCount, n):
        """
        cardValues: array of card values for each card type
        multiplicity: number of each card type
        threshold: maximum total before going bust
        peekCost: how much it costs to peek at the next card
        """
        self.rhymeMap = rhymeMap
        self.wordMap = wordMap
        self.idealSyllCount = idealSyllCount
        self.n = n

    # Return the start state.
    # Look at this function to learn about the state representation.
    # The first element of the tuple is the sum of the cards in the player's
    # hand.
    # The second element is the index (not the value) of the next card, if the player peeked in the
    # last action.  If they didn't peek, this will be None.
    # The final element is the current deck.
    def startState(self):
        #current line
        #previous words
        #last word of previous line
        #lyrics
        return (0, [None for x in range(0,self.n)], None, "")  # total, next card (if any), multiplicity for each card

    # Return set of actions possible from |state|.
    # You do not need to modify this function.
    # All logic for dealing with end states should be done in succAndProbReward
    def actions(self, state):
        ["Keep Going", "Finish Line"]



    # Return a list of (newState, prob, reward) tuples corresponding to edges
    # coming out of |state|.  Indicate a terminal state (after quitting or
    # busting) by setting the deck to None. 
    # When the probability is 0 for a particular transition, don't include that 
    # in the list returned by succAndProbReward.
    def succAndProbReward(self, state, action):
        # BEGIN_YOUR_CODE (our solution is 53 lines of code, but don't worry if you deviate from this)
        #raise Exception("Not implemented yet")
        edges = []
        if state[0] >= 16:
            return edges
        if action == "Keep Going":
            possWords = set(self.wordMap[state[1]])
            numPossWords = float(len(self.wordMap[state[1]]))
            for word in possWords:
                syllables = nsyl(word)
                newState = (state[0], shiftWords(state[1], word), state[2], lyrics+word)
                edges.append(newState, self.wordMap[state[1]].count(word)/numPossWords, 0)
        elif action == "Finish Line":
            nextWords = set(self.wordMap[state[1]])
            rhymes = set(self.rhymeMap[state[2]])
            possWords = nextWords.intersection(rhymes)
            numPossWords = 0
            for word in possWords:
                numPossWords += self.wordMap[state[1]].count(word)
                numPossWords += self.rhymeMap[state[2]].count(word)
            for word in possWords:
                newState = (state[0]+1, shiftWords(state[1], word), word, state[4]+word+'\n')
                wordCount = self.wordMap[state[1]].count(word) + self.rhymeMap[state[2]].count(word)  
                if state[0] == 15:
                    score = self.reward(state[3], self.idealSyllCount)
                    edges.append(newState, float(wordCount)/numPossWords, score)
                else:
                    edges.append(newState, float(wordCount)/numPossWords, 0)
        # END_YOUR_CODE

    def shiftWords(words, newWord):
        newWords = []
        for i in range(1, len(words)):
            newWords.append(words[i])
        newWords.append(newWord)
        return newWords

    def discount(self):
        return 1

    def reward(lyrics, idealSyllCount):
        reward = 0
        prevWord = None
        for line in lyrics:
            words = line.split()
            numSylls = 0
            for word in words:
               numSylls += nsyl(word)[0]
            reward += abs(1./idealSyllCount-numSylls)
            if prevWord != None:
                lastWord = words[-1]
                rhymes = rhyme(prevWord, 2)
                if lastWord in rhymes:
                    reward += 1
            prevWord = words[-1]
