import util, math, random, sys
from collections import defaultdict
from util import ValueIteration

############################################################
# Problem 2a

# If you decide 2a is true, prove it in blackjack.pdf and put "return None" for
# the code blocks below.  If you decide that 2a is false, construct a counterexample.
class CounterexampleMDP(util.MDP):
    def startState(self):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return None 
        # END_YOUR_CODE

    # Return set of actions possible from |state|.
    def actions(self, state):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return None 
        # END_YOUR_CODE

    # Return a list of (newState, prob, reward) tuples corresponding to edges
    # coming out of |state|.
    def succAndProbReward(self, state, action):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return None 
        # END_YOUR_CODE

    def discount(self):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return None 
        # END_YOUR_CODE

############################################################
# Problem 3a

class BlackjackMDP(util.MDP):
    def __init__(self, cardValues, multiplicity, threshold, peekCost):
        """
        cardValues: array of card values for each card type
        multiplicity: number of each card type
        threshold: maximum total before going bust
        peekCost: how much it costs to peek at the next card
        """
        self.cardValues = cardValues
        self.multiplicity = multiplicity
        self.threshold = threshold
        self.peekCost = peekCost

    # Return the start state.
    # Look at this function to learn about the state representation.
    # The first element of the tuple is the sum of the cards in the player's
    # hand.
    # The second element is the index (not the value) of the next card, if the player peeked in the
    # last action.  If they didn't peek, this will be None.
    # The final element is the current deck.
    def startState(self):
        return (0, None, (self.multiplicity,) * len(self.cardValues))  # total, next card (if any), multiplicity for each card

    # Return set of actions possible from |state|.
    # You do not need to modify this function.
    # All logic for dealing with end states should be done in succAndProbReward
    def actions(self, state):
        return ['Take', 'Peek', 'Quit']

    # Return a list of (newState, prob, reward) tuples corresponding to edges
    # coming out of |state|.  Indicate a terminal state (after quitting or
    # busting) by setting the deck to None. 
    # When the probability is 0 for a particular transition, don't include that 
    # in the list returned by succAndProbReward.
    def succAndProbReward(self, state, action):
        # BEGIN_YOUR_CODE (our solution is 53 lines of code, but don't worry if you deviate from this)
        #raise Exception("Not implemented yet")
        if state[2] == None:
            return []
        if action == 'Quit':
            newState = (state[0], None, None)
            return [(newState, 1, state[0])]
        if action == 'Take':
            if state[2] == None:
                newState = (state[0], None, None)
                return [(newState, 1, state[0])]
            if state[1] != None:
                reward = state[0]+self.cardValues[state[1]]
                if reward > self.threshold:
                    return [((reward, None, None), 1, 0)]
                deck = list(state[2])
                deck[state[1]] -= 1
                numCards = sum(deck)
                if numCards == 0:
                    newState = (reward, None, None)
                    return [(newState, 1, reward)]
                else:
                    newState = (reward, None, tuple(deck))
                    return [(newState, 1, 0)]
            returnTuples = []
            deck = state[2]
            numCards = float(sum(deck))
            for i in range(0, len(deck)):
                count = deck[i]
                if count > 0:
                    prob = count/numCards
                    newHand = state[0] + self.cardValues[i]
                    if newHand > self.threshold:
                        newState = (newHand, None, None)
                        returnTuples.append((newState, prob, 0))
                    else:
                        newDeck = list(deck)
                        newDeck[i] -= 1
                        if numCards == 1:#last state had one card left, drew last  card
                            newState = (newHand, None, None)
                            returnTuples.append((newState, prob, newHand))
                        else:
                            newState = (newHand, None, tuple(newDeck))
                            returnTuples.append((newState, prob, 0))
            return returnTuples
        if action == 'Peek':
            if state[1] != None:
                return []
            returnTuples = []
            deck = state[2]
            if deck == None:
                newState = (state[0], None, None)
                return [(newState, 1, state[0])]
            numCards = float(sum(deck))
            for i in range(0, len(deck)):
                count = deck[i]
                if count > 0:
                    prob = count/numCards
                    newState = (state[0], i, tuple(deck))
                    returnTuples.append((newState, prob, -self.peekCost))
            return returnTuples


        # END_YOUR_CODE

    def discount(self):
        return 1

############################################################
# Problem 3b

def peekingMDP():
    """
    Return an instance of BlackjackMDP where peeking is the optimal action at
    least 10% of the time.
    """
    # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)
    #raise Exception("Not implemented yet")
    return BlackjackMDP([5, 15], 4, 20, 1)
    # END_YOUR_CODE

############################################################
# Problem 4a: Q learning

# Performs Q-learning.  Read util.RLAlgorithm for more information.
# actions: a function that takes a state and returns a list of actions.
# discount: a number between 0 and 1, which determines the discount factor
# featureExtractor: a function that takes a state and action and returns a list of (feature name, feature value) pairs.
# explorationProb: the epsilon value indicating how frequently the policy
# returns a random action
class QLearningAlgorithm(util.RLAlgorithm):
    def __init__(self, actions, discount, featureExtractor, explorationProb=0.2):
        self.actions = actions
        self.discount = discount
        self.featureExtractor = featureExtractor
        self.explorationProb = explorationProb
        self.weights = defaultdict(float)
        self.numIters = 0

    # Return the Q function associated with the weights and features
    def getQ(self, state, action):
        score = 0
        for f, v in self.featureExtractor(state, action):
            score += self.weights[f] * v
        return score

    # This algorithm will produce an action given a state.
    # Here we use the epsilon-greedy algorithm: with probability
    # |explorationProb|, take a random action.
    def getAction(self, state):
        self.numIters += 1
        if random.random() < self.explorationProb:
            return random.choice(self.actions(state))
        else:
            return max((self.getQ(state, action), action) for action in self.actions(state))[1]

    # Call this function to get the step size to update the weights.
    def getStepSize(self):
        return 1.0 / math.sqrt(self.numIters)

    # We will call this function with (s, a, r, s'), which you should use to update |weights|.
    # Note that if s is a terminal state, then s' will be None.  Remember to check for this.
    # You should update the weights using self.getStepSize(); use
    # self.getQ() to compute the current estimate of the parameters.
    def incorporateFeedback(self, state, action, reward, newState):
        # BEGIN_YOUR_CODE (our solution is 12 lines of code, but don't worry if you deviate from this)
        #raise Exception("Not implemented yet")
        if newState == None:
            qOpt = 0
            vOpt = 0
        else:
            qOpt = float(self.getQ(state, action))
            vOpt = -sys.maxint - 1
            for act in self.actions(newState):
                vOptNext = float(self.getQ(newState, act))
                if vOptNext > vOpt:
                    vOpt = vOptNext
        innerBracket = qOpt - (reward+self.discount*vOpt)
        stepSize = float(self.getStepSize())
        phi = self.featureExtractor(state, action)
        for feature in phi:
            key = feature[0]
            value = feature[1]
            if key not in self.weights:                
                self.weights[key] = 0
            oldWeight = self.weights[key]
            self.weights[key] = oldWeight - stepSize*innerBracket*value

        # END_YOUR_CODE

# Return a singleton list containing indicator feature for the (state, action)
# pair.  Provides no generalization.
def identityFeatureExtractor(state, action):
    featureKey = (state, action)
    featureValue = 1
    return [(featureKey, featureValue)]

############################################################
# Problem 4b: convergence of Q-learning
# Small test case
# smallMDP = BlackjackMDP(cardValues=[1, 5], multiplicity=2, threshold=10, peekCost=1)
# learningAlgorithm = QLearningAlgorithm(smallMDP.actions, 1, identityFeatureExtractor)
# util.simulate(smallMDP, learningAlgorithm, numTrials=30000)
# viAlgorithm = ValueIteration()
# viAlgorithm.solve(smallMDP)
# pi = viAlgorithm.pi
# smallMDP.computeStates()
# sameCount = 0
# for state in smallMDP.states:
#     learningAlgorithm.explorationProb = 0
#     qAction = learningAlgorithm.getAction(state)
#     viAction = pi[state]
#     if  qAction != viAction:
#         print "VI: %s" %(viAction)
#         print "Q: %s" %(qAction)
#     else: sameCount += 1
# print sameCount
# print len(smallMDP.states)
#Large test case
# largeMDP = BlackjackMDP(cardValues=[1, 3, 5, 8, 10], multiplicity=3, threshold=40, peekCost=1)
# learningAlgorithm = QLearningAlgorithm(largeMDP.actions, 1, identityFeatureExtractor)
# util.simulate(largeMDP, learningAlgorithm, numTrials=30000)
# viAlgorithm = ValueIteration()
# viAlgorithm.solve(largeMDP)
# pi = viAlgorithm.pi
# largeMDP.computeStates()
# sameCount = 0
# for state in largeMDP.states:
#     learningAlgorithm.explorationProb = 0
#     qAction = learningAlgorithm.getAction(state)
#     viAction = pi[state]
#     if  qAction != viAction:
#         print "VI: %s" %(viAction)
#         print "Q: %s" %(qAction)
#     else: sameCount += 1
# print sameCount
# print len(largeMDP.states)



############################################################
# Problem 4c: features for Q-learning.

# You should return a list of (feature key, feature value) pairs (see
# identityFeatureExtractor()).
# Implement the following features:
# - indicator on the total and the action (1 feature).
# - indicator on the presence/absence of each card and the action (1 feature).
#       Example: if the deck is (3, 4, 0 , 2), then your indicator on the presence of each card is (1,1,0,1)
#       Only add this feature if the deck != None
# - indicator on the number of cards for each card type and the action (len(counts) features).  Only add these features if the deck != None
def blackjackFeatureExtractor(state, action):
    total, nextCard, counts = state
    # BEGIN_YOUR_CODE (our solution is 9 lines of code, but don't worry if you deviate from this)
    #raise Exception("Not implemented yet")
    featurePairs = []
    featurePairs.append(("A: "+str(total)+';'+str(action), 1))
    if counts != None:
        present = []
        for i in range(0, len(counts)):
            count = counts[i]
            if count > 0:
                present.append(1)
            else:
                present.append(0)
            featurePairs.append(("C: " +str(i)+';'+ str(count)+';'+ str(action), 1 ))
        featurePairs.append(("B: "+ str(present)+';'+str(action), 1))
    print state, action, featurePairs
    return featurePairs
    # END_YOUR_CODE

############################################################
# Problem 4d: What happens when the MDP changes underneath you?!

# Original mdp
originalMDP = BlackjackMDP(cardValues=[1, 5], multiplicity=2, threshold=10, peekCost=1)
viAlgorithm = util.ValueIteration()
viAlgorithm.solve(originalMDP)


# New threshold
newThresholdMDP = BlackjackMDP(cardValues=[1, 5], multiplicity=2, threshold=15, peekCost=1)
fixedAlg = util.FixedRLAlgorithm(viAlgorithm.pi)
rewards = util.simulate(newThresholdMDP, fixedAlg)
averageReward = sum(rewards)/float(len(rewards))
print averageReward

learningAlgorithm = QLearningAlgorithm(originalMDP.actions, 1, identityFeatureExtractor)
rewards = util.simulate(newThresholdMDP, learningAlgorithm)
averageReward = sum(rewards)/float(len(rewards))
print averageReward