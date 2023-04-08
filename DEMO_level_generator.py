################################################
#                                              #
#     LEVEL GENERATOR FOR SOKOBAN FRAMEWORK    #
#                Written by Milk               #
#                                              #
################################################


# import libraries
import random
from agent import DoNothingAgent, RandomAgent, BFSAgent, DFSAgent, AStarAgent, HillClimberAgent, GeneticAgent, MCTSAgent
from helper import *
import os

# COMMAND LINE ARGS
EVAL_AGENT = "Random"			#sokoban master agent to use as evaluator
SOLVE_ITERATIONS = 500			#number of iterations to run agent for

MIN_SOL_LEN = 3					#minimum length of solution
MAX_SOL_LEN = 20				#maximum length of solution

NUM_LEVELS = 5					#number of levels to generate
OUT_DIR = "assets/gen_levels"	#directory to output generated levels
LEVEL_PREFIX = "Level"			#prefix for the filename of the generated levels


# SOKOBAN ASCII CHARS KEY #
_player = "@"  #1 per game
_crate = "$"
_wall = "#"
_floor = " "
_emptyGoal = "."
_filledGoal = "*"


#turns 2d array of a level into an ascii string
def lev2Str(l):
	s = ""
	for r in l:
		s += ("".join(r) + "\n")
	return s


# creates an empty base sokoban level
def makeEmptyLevel(w=9,h=9):
	l = []

	tbw = [] #top/bottom walls
	lrw = [] #left/right walls

	#initialize row setup
	for i in range(w):
		tbw.append(_wall)
	for i in range(w):
		if i == 0 or i == (w-1):
			lrw.append(_wall)
		else:
			lrw.append(_floor)

	#make level
	for i in range(h):
		if i == 0 or i == (h-1):
			l.append(tbw[:])
		else:
			l.append(lrw[:])

	return l



#get a position inside the map
def randPos(W,H):
	x=random.randint(1,W-2)
	y=random.randint(1,H-2)
	return x,y
	

#generates a level at random
def buildALevel():
	W = 6
	H = 6
	coinFlip = 0.3

	#create a blank level with the dimensions set
	l = makeEmptyLevel(W,H)

	#place extra walls
	while(random.random() < coinFlip):
		x,y = randPos(W,H)

		l[y][x]=_wall

	#place 1 crate
	x,y = randPos(W,H)
	l[y][x]=_crate

	#place 1 goal
	x,y = randPos(W,H)
	l[y][x]=_emptyGoal

	#place the player (only 1)
	x,y = randPos(W,H)
	l[y][x]=_player

	return lev2Str(l)


#use the agent to attempt to solve the level
def solveLevel(l,bot):
	#create new state from level
	state = State()
	state.stringInitialize(l.split("\n"))

	#evaluate level
	sol = bot.getSolution(state, maxIterations=SOLVE_ITERATIONS)
	for s in sol:
		state.update(s['x'],s['y'])
	return state.checkWin(), len(sol)

	
#generate and export levels using the PCG level builder and agent evaluator
def generateLevels():
	#set the agent
	solver = None
	if EVAL_AGENT == 'DoNothing':
		solver = DoNothingAgent()
	elif EVAL_AGENT == 'Random':
		solver = RandomAgent()
	elif EVAL_AGENT == 'BFS':
		solver = BFSAgent()
	elif EVAL_AGENT == 'DFS':
		solver = DFSAgent()
	elif EVAL_AGENT == 'AStar':
		solver = AStarAgent()
	elif EVAL_AGENT == 'HillClimber':
		solver = HillClimberAgent()
	elif EVAL_AGENT == 'Genetic':
		solver = GeneticAgent()
	elif EVAL_AGENT == 'MCTS':
		solver = MCTSAgent()

	#create the directory if it doesn't exist
	if not os.path.exists(OUT_DIR):
		os.makedirs(OUT_DIR)

	#create levels
	totLevels = 0
	while totLevels < NUM_LEVELS:
		lvl = buildALevel()

		solvable, solLen = solveLevel(lvl,solver)

		#uncomment these lines if you want to see all the generated levels (including the failed ones)
		'''
		print(f"{lvl}solvable: {solvable}")
		if solvable:
			print(f"  -> solution len: {solLen}\n")
		else:
			print("")
		'''

		#export the level if solvable
		if solvable and solLen >= MIN_SOL_LEN and solLen <= MAX_SOL_LEN:
			with open(f"{OUT_DIR}/{LEVEL_PREFIX}_{totLevels}.txt",'w') as f:
				f.write(lvl)
			totLevels+=1

			#show the level exported
			print(f"LEVEL #{totLevels}/{NUM_LEVELS} -> {solLen} MOVES\n{lvl}")



#run whole script to generate 
if __name__ == "__main__":
	generateLevels()



