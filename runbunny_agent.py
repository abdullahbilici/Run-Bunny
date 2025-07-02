"""
    ########################################################
    DO NOT CHANGE ANYTHING IN THIS FILE OTHER THAN THE AGENT
    ########################################################
"""

from src.game import Forest
from random import choice
from agent.agents import *

MAX_RUN = 10
BUNNY_WINS = 0
SETUP = {"size":[5,5],"hunters":7}
ACTIONS = ["UP", "RIGHT", "DOWN", "LEFT"]
AVG_NODE_COUNT = 0

print("RUNNING BUNNY AGENT")
print("-------------------")

game = Forest(size=SETUP["size"],hunters=SETUP["hunters"],render=False, benchmark=False)
for e in range(MAX_RUN):
    
    agent = AlphaBetaAgent(game) # Change this to your agent
    bunny_moves = []
    hunter_moves = agent.hunterMoves
    for i in range(len(agent.bunnyMoves)):
        bunny_moves.append(ACTIONS[agent.bunnyMoves[i]])
    b += len(bunny_moves)
    while not game.getWinner():

        if len(bunny_moves) == 0:
            break

        if len(hunter_moves) != 0:
            bunny_move = bunny_moves.pop(0)
            hunter_move = hunter_moves.pop(0)
            hunter_move = [hunter_move[0] - 1, hunter_move[1] - 1]
            action_valid = game.action(bunny_move, spawn=hunter_move)
        else:
            bunny_move = bunny_moves.pop(0)
            action_valid = game.action(bunny_move)
    print("Episode:",e,"/",end=" ")

    if game.getWinner() == 1:
        print("Bunny Wins")
        BUNNY_WINS += 1
    else:
        print("Hunters Wins")
    print("Number of Nodes Generated:",agent.number_of_nodes_generated)
    AVG_NODE_COUNT += agent.number_of_nodes_generated
    print("-------------------")
    if  e != MAX_RUN - 1:
        game.reset()
        
print("Bunny Win Rate:",BUNNY_WINS/MAX_RUN)
print("Average Number of Nodes Generated:",AVG_NODE_COUNT/MAX_RUN)