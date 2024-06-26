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

        "*** YOUR CODE HERE ***"
        food_distance = 100000
        for foodPos in newFood.asList():
            food_distance = min(food_distance, manhattanDistance(newPos, foodPos) + 0.00001)

        return 1 / food_distance + successorGameState.getScore()

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

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        super().__init__(evalFn, depth)
        self.maxState = 0
        self.minState = 1
        self.total_enemy = 0
        self.MAX_SCORE = 99999.0
        self.MIN_SCORE = -self.MAX_SCORE

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
        self.total_enemy = gameState.getNumAgents() - 1
        ret_action = None
        max_score = self.MIN_SCORE
        for action in gameState.getLegalActions(0):
            score = self.getValue(gameState.generateSuccessor(0, action), 1, self.minState, 1)
            if score > max_score:
                max_score = score
                ret_action = action

        return ret_action

    def getValue(self, gameState: GameState, depth: int, nowState, enemy: int):
        if depth == self.depth + 1 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if nowState == self.maxState:
            return self.maxValue(gameState, depth)
        if nowState == self.minState:
            return self.minValue(gameState, depth, enemy)

    def maxValue(self, gameState: GameState, depth: int):
        value = self.MIN_SCORE
        for action in gameState.getLegalActions(0):
            value = max(value, self.getValue(gameState.generateSuccessor(0, action), depth, self.minState, 1))
        return value

    def minValue(self, gameState: GameState, depth: int, enemy: int):
        value = self.MAX_SCORE
        nowState = self.minState

        if enemy == self.total_enemy:
            depth = depth + 1
            nowState = self.maxState

        for action in gameState.getLegalActions(enemy):
            value = min(value, self.getValue(gameState.generateSuccessor(enemy, action), depth, nowState, enemy + 1))

        return value







class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        super().__init__(evalFn, depth)
        self.maxState = 0
        self.minState = 1
        self.total_enemy = 0
        self.MAX_SCORE = 99999.0
        self.MIN_SCORE = -self.MAX_SCORE

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        self.total_enemy = gameState.getNumAgents() - 1
        ret_action = None
        max_score = self.MIN_SCORE
        alpha = self.MIN_SCORE
        beta = self.MAX_SCORE
        for action in gameState.getLegalActions(0):
            score = self.getValue(gameState.generateSuccessor(0, action), 1, self.minState, 1, alpha, beta)
            if score > max_score:
                max_score = score
                ret_action = action

            alpha = max(alpha, score)

        return ret_action

    def getValue(self, gameState: GameState, depth: int, nowState, enemy: int, alpha: float, beta: float):
        if depth == self.depth + 1 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if nowState == self.maxState:
            return self.maxValue(gameState, depth, alpha, beta)
        if nowState == self.minState:
            return self.minValue(gameState, depth, enemy, alpha, beta)

    def maxValue(self, gameState: GameState, depth: int, alpha: float, beta: float):
        value = self.MIN_SCORE
        for action in gameState.getLegalActions(0):
            value = max(value, self.getValue(gameState.generateSuccessor(0, action), depth, self.minState, 1, alpha, beta))
            if value > beta:
                return value
            alpha = max(alpha, value)
        return value

    def minValue(self, gameState: GameState, depth: int, enemy: int, alpha: float, beta: float):
        value = self.MAX_SCORE
        nowState = self.minState

        if enemy == self.total_enemy:
            depth = depth + 1
            nowState = self.maxState

        for action in gameState.getLegalActions(enemy):
            value = min(value, self.getValue(gameState.generateSuccessor(enemy, action), depth, nowState, enemy + 1, alpha, beta))
            if value < alpha:
                return value
            beta = min(beta, value)

        return value

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        super().__init__(evalFn, depth)
        self.maxState = 0
        self.expState = 1
        self.total_enemy = 0
        self.MAX_SCORE = 99999.0
        self.MIN_SCORE = -self.MAX_SCORE

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        self.total_enemy = gameState.getNumAgents() - 1

        max_value = self.MIN_SCORE
        ret_action = None

        for action in gameState.getLegalActions(0):
            value = self.getValue(gameState.generateSuccessor(0, action), self.expState, 1, 1)
            if value > max_value:
                max_value = value
                ret_action = action

        return ret_action

    def getValue(self, gameState: GameState, nowState: int, depth: int, enemy: int):
        if depth == self.depth + 1 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if nowState == self.expState:
            return self.expValue(gameState, depth, enemy)
        if nowState == self.maxState:
            return self.maxValue(gameState, depth)

    def maxValue(self, gameState: GameState, depth: int):
        value = self.MIN_SCORE
        for action in gameState.getLegalActions(0):
            value = max(value, self.getValue(gameState.generateSuccessor(0, action), self.expState, depth, 1))
        return value

    def expValue(self, gameState: GameState, depth: int, enemy: int):
        value = 0
        nowState = self.expState

        if enemy == self.total_enemy:
            nowState = self.maxState
            depth += 1

        actions_number = len(gameState.getLegalActions(enemy))
        for action in gameState.getLegalActions(enemy):
            value += 1 / actions_number * self.getValue(gameState.generateSuccessor(enemy, action), nowState, depth, enemy + 1)
        return value

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    nowPos = currentGameState.getPacmanPosition()
    nowFood = currentGameState.getFood()
    food_distance = 100000
    for foodPos in nowFood.asList():
        food_distance = min(food_distance, manhattanDistance(nowPos, foodPos) + 0.00001)

    return 1 / food_distance + currentGameState.getScore()

# Abbreviation
better = betterEvaluationFunction
