# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class Node:
	def __init__(self, state, parent, dir_from_parent, cost_from_start):
		self.state = state
		self.parent = parent
		self.dir_from_parent = dir_from_parent
		self.cost_from_start = cost_from_start

	def __hash__(self):
		return hash(self.state)

	def getHash (self):
		return hash(self.state)

	def __eq__(self, other):
		return isinstance(other, Node) and self.state == other.state

class SearchProblem:
	"""
	This class outlines the structure of a search problem, but doesn't implement
	any of the methods (in object-oriented terminology: an abstract class).

	You do not need to change anything in this class, ever.
	"""

	def getStartState(self):
		"""
		Returns the start state for the search problem.
		"""
		util.raiseNotDefined()

	def isGoalState(self, state):
		"""
		  state: Search state

		Returns True if and only if the state is a valid goal state.
		"""
		util.raiseNotDefined()

	def getSuccessors(self, state):
		"""
		  state: Search state

		For a given state, this should return a list of triples, (successor,
		action, stepCost), where 'successor' is a successor to the current
		state, 'action' is the action required to get there, and 'stepCost' is
		the incremental cost of expanding to that successor.
		"""
		util.raiseNotDefined()

	def getCostOfActions(self, actions):
		"""
		 actions: A list of actions to take

		This method returns the total cost of a particular sequence of actions.
		The sequence must be composed of legal moves.
		"""
		util.raiseNotDefined()


def tinyMazeSearch(problem):
	"""
	Returns a sequence of moves that solves tinyMaze.  For any other maze, the
	sequence of moves will be incorrect, so only use this for tinyMaze.
	"""
	from game import Directions
	s = Directions.SOUTH
	w = Directions.WEST
	return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
	"""
	Search the deepest nodes in the search tree first.

	Your search algorithm needs to return a list of actions that reaches the
	goal. Make sure to implement a graph search algorithm.

	To get started, you might want to try some of these simple commands to
	understand the search problem that is being passed in:

	print "Start:", problem.getStartState()
	print "Is the start a goal?", problem.isGoalState(problem.getStartState())
	print "Start's successors:", problem.getSuccessors(problem.getStartState())
	"""
	# get the start state
	start_state = problem.getStartState()

	# create visited list to maintain explored nodes of a graph
	visited = set()

	# create path_to_goal stack to store the most optimum path from start to goal
	path_from_start = []

	# check if the start_state is the goal state
	if problem.isGoalState(start_state):
		return []

	# Initialize stack for DFS
	stack = util.Stack()

	"""
		store the information in `node` data structure
		Node:
				state, tuple
				parent, tuple
				dir_from_parent, game.Directions
				cost_from_start, int
	"""
	start_node = Node(start_state, None, None, 0)
	stack.push(start_node)

	# loop through the successors and push them to stack if not visited
	# core of DFS
	while not stack.isEmpty():
		cur_node = stack.pop()
		# check if this node has been visited
		if cur_node not in visited:
			visited.add(cur_node)
			if problem.isGoalState(cur_node.state):
				break
			# recursiverly add node's successor
			for successor_state in problem.getSuccessors(cur_node.state):
				successor_node = Node(successor_state[0], cur_node, successor_state[1], 0)
				stack.push(successor_node)

	# navigate the parent pointers to get the path from start
	while cur_node.dir_from_parent != None:
		path_from_start.append(cur_node.dir_from_parent)
		cur_node = cur_node.parent

	path_from_start.reverse()

	return path_from_start

def breadthFirstSearch(problem):
	"""Search the node of least total cost first."""

	# get the start state
	start_state = problem.getStartState()

	# create visited list to maintain explored nodes of a graph
	visited = set()

	# create path_to_goal stack to store the most optimum path from start to goal
	path_from_start = []

	# check if the start_state is the goal state
	if problem.isGoalState(start_state):
		return []

	# initialize a queue for BFS
	queue = util.Queue()

	"""
		store the information in `node` data structure
		Node:
				state, tuple
				parent, tuple
				dir_from_parent, game.Directions
				cost_from_start, int
	"""
	start_node = Node(start_state, None, None, 0)
	queue.push(start_node)

	# core of Uniform Cost Search
	while not queue.isEmpty():
		cur_node = queue.pop()
		# check if this node has been visited
		if cur_node not in visited:
			visited.add(cur_node)
			if problem.isGoalState(cur_node.state):
				break
			# recursiverly add node's successor
			for successor_state in problem.getSuccessors(cur_node.state):
				successor_node = Node(successor_state[0], cur_node, successor_state[1], cur_node.cost_from_start + successor_state[2])
				queue.push(successor_node)

	# navigate the parent pointers to get the path from start
	while cur_node.dir_from_parent != None:
		path_from_start.append(cur_node.dir_from_parent)
		cur_node = cur_node.parent

	path_from_start.reverse()

	return path_from_start

def uniformCostSearch(problem):
	"""Search the node of least total cost first."""

	# get the start state
	start_state = problem.getStartState()

	# create visited list to maintain explored nodes of a graph
	visited = set()

	# create path_to_goal stack to store the most optimum path from start to goal
	path_from_start = []

	# check if the start_state is the goal state
	if problem.isGoalState(start_state):
		return []

	# initialize a queue for BFS
	priority_queue = util.PriorityQueue()

	"""
		store the information in `node` data structure
		Node:
				state, tuple
				parent, tuple
				dir_from_parent, game.Directions
				cost_from_start, int
	"""
	start_node = Node(start_state, None, None, 0)
	priority_queue.push(start_node, start_node.cost_from_start)

	# core of Uniform Cost Search
	while not priority_queue.isEmpty():
		cur_node = priority_queue.pop()
		# check if this node has been visited
		if cur_node not in visited:
			visited.add(cur_node)
			if problem.isGoalState(cur_node.state):
				break
			# recursiverly add node's successor
			for successor_state in problem.getSuccessors(cur_node.state):
				successor_node = Node(successor_state[0], cur_node, successor_state[1], cur_node.cost_from_start + successor_state[2])
				priority_queue.push(successor_node, successor_node.cost_from_start)

	# navigate the parent pointers to get the path from start
	while cur_node.dir_from_parent != None:
		path_from_start.append(cur_node.dir_from_parent)
		cur_node = cur_node.parent

	path_from_start.reverse()

	return path_from_start

def nullHeuristic(state, problem=None):
	"""
	A heuristic function estimates the cost from the current state to the nearest
	goal in the provided SearchProblem.  This heuristic is trivial.
	"""
	return 0

def aStarSearch(problem, heuristic=nullHeuristic):
	"""Search the node of least total cost first."""

	# get the start state
	start_state = problem.getStartState()

	# create visited list to maintain explored nodes of a graph
	visited = set()

	# create path_to_goal stack to store the most optimum path from start to goal
	path_from_start = []

	# check if the start_state is the goal state
	if problem.isGoalState(start_state):
		return []

	# initialize a queue for BFS
	priority_queue = util.PriorityQueue()

	"""
		store the information in `node` data structure
		Node:
				state, tuple
				parent, tuple
				dir_from_parent, game.Directions
				cost_from_start, int
	"""
	start_node = Node(start_state, None, None, 0)
	priority_queue.push(start_node, start_node.cost_from_start  + heuristic (start_node.state, problem))

	# core of A* Search
	while not priority_queue.isEmpty():
		cur_node = priority_queue.pop()
		# check if this node has been visited
		if cur_node not in visited:
			visited.add(cur_node)
			if problem.isGoalState(cur_node.state):
				break
			# recursiverly add node's successor
			for successor_state in problem.getSuccessors(cur_node.state):
				successor_node = Node(successor_state[0], cur_node, successor_state[1], cur_node.cost_from_start + successor_state[2])
				priority_queue.push(successor_node, successor_node.cost_from_start + heuristic (successor_node.state, problem))

	# navigate the parent pointers to get the path from start
	while cur_node.dir_from_parent != None:
		path_from_start.append(cur_node.dir_from_parent)
		cur_node = cur_node.parent

	path_from_start.reverse()

	return path_from_start


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
