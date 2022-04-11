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


from math import dist, inf
from util import manhattanDistance, raiseNotDefined
from game import Actions, Directions
import random, util

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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
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

        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        food_list = newFood.asList()
        # FOOD DISTANCE FACTOR
        food_distance = sum([manhattanDistance(newPos, food) for food in food_list])                
        # TOTAL SCORE    
        total_score = childGameState.getScore()
        total_score -= (food_distance/(len(food_list)+1))
        # GHOST DISTANCE FACTOR
        for ghost  in newGhostStates:
            distance = manhattanDistance(newPos, ghost.getPosition())
            if  distance <= 3:
                total_score -= 2
        return total_score


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

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        """
            A single level of the search is considered to be one Pacman move and all the ghosts’ responses.
            That is why the depth is being increased only once when the minimizer calls the maximizer.
        """
        inf = 1000000000
        PACMAN_AGENT_INDEX = 0
        LAST_AGENT_INDEX = gameState.getNumAgents()-1

        def minimax(gameState, agent_index, depth):
            # TERMINAL STATE
            if depth==self.depth or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            actions = gameState.getLegalActions(agent_index)
            # MAXIMIZER/PACMAN
            if agent_index == PACMAN_AGENT_INDEX:
                max_score = -inf
                for action in actions:
                    new_state = gameState.getNextState(agent_index, action)
                    max_score = max(max_score, minimax(new_state, PACMAN_AGENT_INDEX+1, depth))
                return max_score
            # MINIMIZER/GHOST
            else:   
                min_score = inf
                for action in actions:
                    new_state = gameState.getNextState(agent_index, action)
                    if agent_index == LAST_AGENT_INDEX:
                        min_score = min(min_score, minimax(new_state, PACMAN_AGENT_INDEX, depth+1))
                    else:
                        min_score = min(min_score, minimax(new_state, agent_index+1, depth))
                return min_score

        def root_search():
            best_root_action = None
            root_score = -inf
            root_actions = gameState.getLegalActions(PACMAN_AGENT_INDEX)
            for root_action in root_actions:
                new_state = gameState.getNextState(PACMAN_AGENT_INDEX, root_action)
                new_score = minimax(new_state, PACMAN_AGENT_INDEX+1, 0)
                if new_score > root_score:
                    root_score = new_score
                    best_root_action = root_action
            return best_root_action

        return root_search()
        """
        For some reason, when i was trying to do minimax for the last ghost to the first ghost the last test case failed,
        although the resut in the end was the same (pacmans actions where the same).
        """


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        inf = 1000000000
        PACMAN_AGENT_INDEX = 0
        LAST_AGENT_INDEX = gameState.getNumAgents()-1
        def minimax(gameState, agent_index, depth, A, B):
            # TERMINAL STATE
            if depth==self.depth or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            actions = gameState.getLegalActions(agent_index)
            # MAXIMIZER/PACMAN
            if agent_index == PACMAN_AGENT_INDEX:
                max_score = -inf
                for action in actions:
                    new_state = gameState.getNextState(agent_index, action)
                    max_score = max(max_score, minimax(new_state, PACMAN_AGENT_INDEX+1, depth, A, B))
                    if max_score > B:
                        return max_score
                    A = max(A, max_score)
                return max_score
            # MINIMIZER/GHOSTS
            else:   
                min_score = inf
                for action in actions:
                    new_state = gameState.getNextState(agent_index, action)
                    if agent_index == LAST_AGENT_INDEX:
                        min_score = min(min_score, minimax(new_state, PACMAN_AGENT_INDEX, depth+1, A, B))
                    else:
                        min_score = min(min_score, minimax(new_state, agent_index+1, depth, A, B))
                    if min_score < A:
                        return min_score
                    B = min(B, min_score)
                return min_score

        def root_search():
            A = -inf
            B = inf
            best_root_action = None
            best_score = -inf
            root_actions = gameState.getLegalActions(PACMAN_AGENT_INDEX)
            for root_action in root_actions:
                new_state = gameState.getNextState(PACMAN_AGENT_INDEX, root_action)
                new_score = minimax(new_state, PACMAN_AGENT_INDEX+1, 0, A, B)
                if new_score > best_score:
                    best_score = new_score
                    best_root_action = root_action
                A = max(A, new_score)
            return best_root_action

        return root_search()
        util.raiseNotDefined()

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
        inf = 1000000000
        PACMAN_AGENT_INDEX = 0
        LAST_AGENT_INDEX = gameState.getNumAgents()-1

        def expectimax(gameState, agent_index, depth):
            # TERMINAL STATE
            if depth==self.depth or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            actions = gameState.getLegalActions(agent_index)
            # MAXIMIZER/PACMAN
            if agent_index == PACMAN_AGENT_INDEX:
                max_score = -inf
                for action in actions:
                    new_state = gameState.getNextState(agent_index, action)
                    max_score = max(max_score, expectimax(new_state, PACMAN_AGENT_INDEX+1, depth))
                return max_score
            # MINIMIZER/GHOST
            else:   
                total = 0
                for action in actions:
                    new_state = gameState.getNextState(agent_index, action)
                    if agent_index == LAST_AGENT_INDEX:
                        new_score = expectimax(new_state, PACMAN_AGENT_INDEX, depth+1)
                    else:
                        new_score = expectimax(new_state, agent_index+1, depth)
                    total += new_score  # average of score of every move
                return total/len(actions)

        def root_search():
            best_root_action = None
            root_score = -inf
            root_actions = gameState.getLegalActions(PACMAN_AGENT_INDEX)
            for root_action in root_actions:
                new_state = gameState.getNextState(PACMAN_AGENT_INDEX, root_action)
                new_score = expectimax(new_state, PACMAN_AGENT_INDEX+1, 0)
                if new_score > root_score:
                    root_score = new_score
                    best_root_action = root_action
            return best_root_action

        return root_search()

import math

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """

    "*** YOUR CODE HERE ***"
    # average distance from food is ~ 7
    # average distance from ghosts is ~3.7
    position = currentGameState.getPacmanPosition()
    food_list = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()
    capsule_positions = currentGameState.getCapsules()
    # FOOD DISTANCE FACTOR
    food_distance = sum([manhattanDistance(position, food) for food in food_list])
    # GHOST DISTANCE FACTOR
    ghost_positions = [ghost.getPosition() for ghost in ghostStates]
    ghost_distance = sum([manhattanDistance(position, pos) for pos in ghost_positions])
    # CAPSULES FACTOR
    close_capsules = 0 # close to pacman
    for pos in capsule_positions:
       close_capsules += manhattanDistance(position, pos) == 1
    # TOTAL SCORE    
    total_score = currentGameState.getScore()
    total_score += close_capsules/(len(capsule_positions)+1)
    total_score -= (food_distance/(len(food_list)+1))
    total_score -= (ghost_distance/(len(ghost_positions)))  
    return total_score
    #util.raiseNotDefined()    

# Abbreviation
better = betterEvaluationFunction
