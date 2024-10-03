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
import random, util

from game import Agent
from pacman import GameState
import sys
from time import sleep

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

    def evaluationFunction(self, currentGameState: GameState, action):
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
        sys.stdout.write(f"\rNEW POS: {newPos} - NEW FOOD: {newFood} - NEW GHOST STATES: {newGhostStates[0]} - NEW SCARED TIMES: {newScaredTimes}")
        # print("NEW FOOD", newFood)
        sys.stdout.flush()
        # print("NEW GHOST STATES", newGhostStates)
        # print("NEW SCARED TIMES", newScaredTimes)

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState: GameState):
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
        self._temp_depth = 0


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        
        actions = gameState.getLegalActions()
        self._temp_depth += 1
        self.__index = 0

        val = -4_000_000
        bestAction = ""
        for action in actions:
            successorGameState = gameState.generateSuccessor(agentIndex=self.__index, action=action)
            score = self.eval(successorGameState)
            if score > val:
                print(score)
                val = score
                bestAction = action
        return bestAction
    
        util.raiseNotDefined()
    
    def eval(self, currentGameState: GameState):
        newPos = currentGameState.getPacmanPosition()
        newFood = currentGameState.getFood()
        numFood = currentGameState.getNumFood()
        newGhostStates = currentGameState.getGhostStates()
        # print(newGhostStates[0].configuration, newGhostStates[1])
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
        self.__index += 1
        if self.__index >= currentGameState.getNumAgents():
            self.__index = 0
        
        if self.__index == 0:
            self._temp_depth += 1

        if self._temp_depth == self.depth:
            distanceFromGhosts = sum(map(lambda loc: ((10 - newPos[0]) ** 2 + (20 - newPos[1]) ** 2) ** 0.5, newGhostStates))
            return -numFood + distanceFromGhosts
            # return currentGameState.getScore()
        
        if self.__index == 0:
            return self.max_value(currentGameState)
        return self.min_value(currentGameState)


        
        # return successorGameState.getScore()
    
    def max_value(self, currentGameState: GameState):
        v = -4_000_000_000
        successors = [currentGameState.generatePacmanSuccessor(action) for action in currentGameState.getLegalActions(agentIndex=self.__index)]
        for successor in successors:
            v = max(v, self.eval(successor))
        return v
    
    def min_value(self, currentGameState: GameState):
        v = +4_000_000_000
        successors = [currentGameState.generatePacmanSuccessor(action) for action in currentGameState.getLegalActions(agentIndex=self.__index)]
        for successor in successors:
            v = min(v, self.eval(successor))
        return v

class MinimaxAgent2(MultiAgentSearchAgent):
    def getAction(self, gameState: GameState):
        legalMoves = gameState.getLegalActions()
        scores = [self.minimax(gameState.generateSuccessor(0, action), 0, 0) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)
        return legalMoves[chosenIndex]

    def minimax(self, gameState: GameState, agentIndex: int, depth: int):
        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.eval(gameState)

        if agentIndex == 0:  # Pacman's turn (Maximizing player)
            return max(self.minimax(gameState.generateSuccessor(agentIndex, action), agentIndex + 1, depth) for action in gameState.getLegalActions(agentIndex))

        else:  # Ghosts' turn (Minimizing players)
            nextAgentIndex = agentIndex + 1
            if nextAgentIndex == gameState.getNumAgents():
                nextAgentIndex = 0  # Reset to Pacman's turn
            if nextAgentIndex == 0:
                depth += 1  # Increment depth when all ghosts have moved
            return min(self.minimax(gameState.generateSuccessor(agentIndex, action), nextAgentIndex, depth) for action in gameState.getLegalActions(agentIndex))

    def eval(self, currentGameState: GameState):
        # Your evaluation function implementation goes here
        newGhostStates = currentGameState.getGhostStates()
        newPos = currentGameState.getPacmanPosition()
        foodCount = currentGameState.getNumFood()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        if currentGameState.isWin():
            return 100000
        sc = currentGameState.getScore()
        foods = currentGameState.getFood()
        nearestFood = 10000000
        nearestFoodLoc = ()
        for i, f1 in enumerate(foods):
            for j, f2 in enumerate(f1):
                if not f2:
                    continue
                if manhattanDistance((i, j), newPos) < nearestFood:
                    nearestFood = manhattanDistance((i, j), newPos)
                    nearestFoodLoc = (i, j)
        sys.stdout.write(f"\rPACMAN: {newPos} -- FOOD: {nearestFoodLoc} -- DIS: {nearestFood}\n")
        
        for i, w in enumerate(currentGameState.getWalls()):
            for j, ww in enumerate(w):
                if not ww:
                    continue
                sc -= 100
        # print("PACMAN: ", newPos)
        # print(nearestFoodLoc)
        # print(nearestFood)
        sys.stdout.flush()

        if nearestFood != 10000000:
            sc -= nearestFood

        distanceFromNearestGhost = 10000000
        for i, ghostState in enumerate(newGhostStates):
            if newScaredTimes[i] not in (0, '0'):
                continue
            distanceFromNearestGhost = min(distanceFromNearestGhost, manhattanDistance(ghostState.getPosition(), newPos))
        
        # if distanceFromNearestGhost != 10000000:
        #     sc += distanceFromNearestGhost

        if distanceFromNearestGhost < 6:
            sc += distanceFromNearestGhost * 2
        # print("SC", sc)
        # if foodCount < 5:
        #     sc -= nearestFood

        return sc

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
