##############################################################
#                                                            #
#     LEVEL GENERATOR FOR SOKOBAN FRAMEWORK                  #
#         Written by Dasari Sri Sai Abhishake Gopal          #
#                                                            #
##############################################################


# import libraries
import random
from agent import DoNothingAgent, RandomAgent, BFSAgent, DFSAgent, AStarAgent, HillClimberAgent, GeneticAgent, MCTSAgent
from helper import *
import os
import numpy as np

# COMMAND LINE ARGS
EVAL_AGENT = "AStar"			#sokoban master agent to use as evaluator
SOLVE_ITERATIONS = 3000			#number of iterations to run agent for

MIN_SOL_LEN = 5					#minimum length of solution
MAX_SOL_LEN = 30				#maximum length of solution

NUM_LEVELS = 40					#number of levels to generate
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






###############################
##                           ##
##      ADD YOUR HELPER      ##
##      FUNCTIONS HERE       ##
##                           ##
###############################

def randPos(W,H):
	x=random.randint(1,W-2)
	y=random.randint(1,H-2)
	return x,y
def randPos_crate(W,H):
	x=random.randint(2,W-3)
	y=random.randint(2,H-3)
	return x,y
#generates a level
def buildALevel(bot):
	# WRITE YOUR OWN CODE HERE
	W= np.random.randint(7,15)
	H= np.random.randint(7,15)
	l=makeEmptyLevel(W,H)
	coinFlip = 0.5
	#print("New Game")
	crates=[]
	k=random.choice([1,2])
	for i in range(k):
		crate=[]
		x, y = randPos_crate(len(l),len(l[0]))
		while(l[x][y]!=" "):
				x, y = randPos_crate(len(l), len(l[0]))
		l[x][y] = _crate

		#print(l[x][y])
		crate.append(x)
		crate.append(y)
		crates.append(crate)
	#print(crates)

	goals=[]
	for i in range(k):
		goal=[]
		x, y = randPos(len(l), len(l[0]))
		while (l[x][y] != " "):
			x, y = randPos(len(l), len(l[0]))
		l[x][y] = _emptyGoal
		goal.append(x)
		goal.append(y)
		goals.append(goal)
	#print(goals)
	bot1=AStarAgent()
	player=[]
	x, y = randPos(len(l[0]), len(l))
	while (l[y][x] != " "):
		x, y = randPos(len(l[0]), len(l))
	l[y][x] = _player
	player_x=x
	player_y=y

	player.append(x)
	player.append(y)
	#print(player)
	s=lev2Str(l)
	state = State()
	state.stringInitialize(s.split("\n"))
	#print(state)
	sol = bot1.getSolution(state, maxIterations=SOLVE_ITERATIONS)
	path=[]
	for step in sol:
		path_x=player[0]+step['x']
		player[0]+=step['x']
		path_y=player[1]+step['y']
		player[1]+=step['y']
		#print(player)
		path.append([path_x,path_y])
	#print(path)
	path_xs=[]
	path_ys=[]
	for tile in path:
		path_xs.append(tile[0])
		path_ys.append(tile[1])

	# WRITE YOUR CODE HERE #
	for i in range(len(l)):
		for j in range(len(l[0])):
			if random.random() < coinFlip:
				l[i][j]=_wall
	#print(goal)
	for tile in path:
		l[tile[1]][tile[0]]=_floor
		if(tile[0]-1!=0):
			l[tile[1]][tile[0]-1] = _floor
		if (tile[1] - 1 != 0):
			l[tile[1]-1][tile[0]] = _floor
	for goal in goals:
		l[goal[0]][goal[1]]=_emptyGoal
	l[player_y][player_x] = _player
	for crate in crates:
		l[crate[0]][crate[1]] = _crate
	s=lev2Str(l)
	state.stringInitialize(s.split("\n"))
	return lev2Str(l)  #returns as a string










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
		lvl = buildALevel(solver)

		solvable, solLen = solveLevel(lvl,solver)

		#uncomment these lines if you want to see all the generated levels (including the failed ones)

		print(f"{lvl}solvable: {solvable}")
		if solvable:
			print(f"  -> solution len: {solLen}\n")
		else:
			print("")



		#export the level if solvable 
		if solvable and solLen >= MIN_SOL_LEN and solLen <= MAX_SOL_LEN:
			with open(f"{OUT_DIR}/{LEVEL_PREFIX}_{totLevels}.txt",'w') as f:
				f.write(lvl)
				#print(lvl)
		totLevels+=1



	print(f"LEVEL #{totLevels}/{NUM_LEVELS} -> {solLen} MOVES\n{lvl}")




#run whole script to generate 
if __name__ == "__main__":
	generateLevels()



