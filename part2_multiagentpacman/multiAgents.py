# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util, sys

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        oldFood = currentGameState.getFood();

        score = 0.0

        scaredGhosts = []
        killerGhosts = []
        for ghost in newGhostStates:
            if ghost.scaredTimer == 0:
                killerGhosts.append(ghost)
            else:
                scaredGhosts.append(ghost)

        for ghost in scaredGhosts:
            dist = util.manhattanDistance(ghost.getPosition(), newPos)
            if dist <= 1:
                score += 2000

        for ghost in killerGhosts:
            dist = util.manhattanDistance(ghost.getPosition(), newPos)
            if dist <= 1:
                score -= 200

        capsuleList = currentGameState.getCapsules()
        for capsule in capsuleList:
            dist = util.manhattanDistance(capsule, newPos)
            if dist == 0:
                score += 100
            else:
                score += 10. / dist
                
        foodList = oldFood.asList()
        for food in foodList:
            dist = util.manhattanDistance(food, newPos)
            if dist == 0:
                score += 100
            else:
                score += 1. / (dist * dist)

        return score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        # number of ghosts
        numGhosts = gameState.getNumAgents() - 1

        score, action = self.maximizerFunction(gameState, 0, 0)

        return action

    def maximizerFunction(self, gameState, currentDepth, agentIndex):
        if currentDepth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), "Stop"

        legalActions = gameState.getLegalActions(agentIndex)
        score = [self.minimizeFunction(gameState.generateSuccessor(agentIndex, action), currentDepth, agentIndex+1) for action in legalActions]
        maxScore = max(score)
        maxScoreAction = [idx for idx in range(len(score)) if score[idx] == maxScore][0]

        return maxScore, legalActions[maxScoreAction]

    def minimizeFunction(self, gameState, currentDepth, agentIndex):
        if currentDepth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), "Stop"

        legalActions = gameState.getLegalActions(agentIndex)
        scores = []
        if agentIndex != gameState.getNumAgents()-1:
            scores = [self.minimizeFunction(gameState.generateSuccessor(agentIndex, action), currentDepth, agentIndex+1) for action in legalActions]
        else:
            scores = [self.maximizerFunction(gameState.generateSuccessor(agentIndex, action), currentDepth+1, 0) for action in legalActions]

        minScore = min(scores)
        minScoreAction = [idx for idx in range(len(scores)) if scores[idx] == minScore][0]

        return minScore, legalActions[minScoreAction]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        numGhosts = gameState.getNumAgents() - 1

        alpha = -sys.maxint-1
        beta = sys.maxint
        score, action = self.maximizerFunction(gameState, 0, 0, alpha, beta)

        return action

    def maximizerFunction(self, gameState, currentDepth, agentIndex, alpha, beta):
        if currentDepth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), "Stop"

        legalActions = gameState.getLegalActions(agentIndex)

        scores = []
        maxScore = -sys.maxint - 1
        for idx in range(len(legalActions)):
            action = legalActions[idx]
            score = self.minimizeFunction(gameState.generateSuccessor(agentIndex, action), currentDepth, agentIndex+1, alpha, beta)[0]
            maxScore = max(maxScore, score)
            if maxScore > beta:
                return maxScore, action
            alpha = max(alpha, maxScore)
            scores.append(score)

        maxScoreAction = [idx for idx in range(len(scores)) if scores[idx] == maxScore][0]

        return maxScore, legalActions[maxScoreAction]

    def minimizeFunction(self, gameState, currentDepth, agentIndex, alpha, beta):
        if currentDepth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), "Stop"

        legalActions = gameState.getLegalActions(agentIndex)
        scores = []

        minScore = sys.maxint
        for idx in range(len(legalActions)):
            action = legalActions[idx]
            score = minScore
            if agentIndex != gameState.getNumAgents() - 1:
                score = self.minimizeFunction(gameState.generateSuccessor(agentIndex, action), currentDepth, agentIndex+1, alpha, beta)[0]
            else:
                score = self.maximizerFunction(gameState.generateSuccessor(agentIndex, action), currentDepth+1, 0, alpha, beta)[0]
            scores.append(score)
            minScore = min(minScore, score)
            if minScore < alpha:
                return minScore, action
            beta = min(beta, minScore)

        minScoreAction = [idx for idx in range(len(scores)) if scores[idx] == minScore][0]

        return minScore, legalActions[minScoreAction]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        score, action = self.maximizerFunction(gameState, 0, 0)

        return action

    def maximizerFunction(self, gameState, currentDepth, agentIndex):
        if currentDepth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), "Stop"

        legalActions = gameState.getLegalActions(agentIndex)
        scores = [self.minimizeFunction(gameState.generateSuccessor(agentIndex, action), currentDepth, agentIndex+1) for action in legalActions]
        maxScore = max(scores)
        maxScoreAction = [idx for idx in range(len(scores)) if scores[idx] == maxScore][0]

        return maxScore, legalActions[maxScoreAction]

    def minimizeFunction(self, gameState, currentDepth, agentIndex):
        if currentDepth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        legalActions = gameState.getLegalActions(agentIndex)
        scores = []
        if agentIndex != gameState.getNumAgents()-1:
            scores = [self.minimizeFunction(gameState.generateSuccessor(agentIndex, action), currentDepth, agentIndex+1) for action in legalActions]
        else:
            scores = [self.maximizerFunction(gameState.generateSuccessor(agentIndex, action), currentDepth+1, 0)[0] for action in legalActions]

        randomScore = sum(scores) / len(scores)

        return randomScore

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

