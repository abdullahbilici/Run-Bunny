########################## 
# Name = Abdullah bilici #
# ID = 150200330         #
########################## 


import copy
import random
from agent.agent import Agent

class Node():
    def __init__(self, parent, val, pos, map, bunnyMoves, hunterMoves):
        self.parent = parent            # Parent Node
        self.val = val                  # Terminal Value (1, -1, 0)
        self.pos = pos                  # Position of the bunny
        self.map = map                  # Map of the game
        self.bunnyMoves = bunnyMoves    # List of bunny moves
        self.hunterMoves = hunterMoves  # List of hunter moves

class ReflexAgent(Agent):
    def __init__(self, game):
        super().__init__(game)
        self.node = Node(None, 0, [self.bunny[0]+1, self.bunny[1]+1], copy.deepcopy(self.map), [], []) #Initial Node
        self.reflex = self.reflexPlayer(self.map, self.node) # Starts the reflex agent
        self.val = self.reflex[0]           # Terminal Value (1, -1, 0)
        self.bunnyMoves = self.reflex[1]    # List of bunny moves
        self.hunterMoves = self.reflex[2]   # List of hunter moves

    def find_move(self, node):
        hunters = list()
        
        normal = lambda p: [p[0]/norm(p)**2, p[1]/norm(p)**2] 
        norm = lambda p: (p[0]**2 + p[1]**2)**(1/2) 
        cos_dist = lambda p1, p2: (p1[0]*p2[0] + p1[1]*p2[1]) / (norm(p1)*norm(p2)) 

        for i in range(len(node.map)):
            for j in range(len(node.map[0])):
                if node.map[i][j] == 2:
                    hunter_vector= [i-node.pos[0], j-node.pos[1]]
                    hunters.append(normal(hunter_vector))
        
        hunter_density = [0,0]
        hunter_density[0] = sum([hunter_norm[0] for hunter_norm in hunters])
        hunter_density[1] = sum([hunter_norm[1] for hunter_norm in hunters])
            
        if hunter_density == [0,0]:
            for action in self.moves:
                if node.map[node.pos[0] + action[0]][node.pos[1] + action[1]] != 2:
                    return action[-1]

        best_distance, best_action = float("inf"), None
        for action in self.moves:
            if node.map[node.pos[0] + action[0]][node.pos[1] + action[1]] == 0:
                if best_distance > cos_dist(action[:2],hunter_density):
                    best_distance, best_action = cos_dist(action[:2],hunter_density), action[-1]

        return best_move

    def reflexPlayer(self, map, node):
        """
            IMPROVE THIS FUNCTION
        """
        if self.checkTerminal(map, node.pos):
            node.val = self.returnScore(map, node.pos)
            return node.val, node.bunnyMoves, node.hunterMoves

        best = self.find_move(node)
        new_pos = [node.pos[0] + self.moves[best][0], node.pos[1] + self.moves[best][1]]
        new_node = Node(node, 0, new_pos, copy.deepcopy(map), copy.deepcopy(node.bunnyMoves), copy.deepcopy(node.hunterMoves))
        new_node.map[new_pos[0]][new_pos[1]] = 3
        new_node.map[node.pos[0]][node.pos[1]] = 0
        new_node.bunnyMoves.append(best)
        self.number_of_nodes_generated += 1

        return self.reflexOpponent(new_node.map, new_node)
    
    def reflexOpponent(self, map, node):    
        """
            DO NOT CHANGE THIS FUNCTION
        """
        if self.checkTerminal(map, node.pos):
            node.val = self.returnScore(map, node.pos)
            return node.val, node.bunnyMoves, node.hunterMoves
        
        empty = self.emptySpace(map)
        rnd = random.randint(0, len(empty) - 1)

        new_node = Node(node, 0, node.pos, copy.deepcopy(map), copy.deepcopy(node.bunnyMoves), copy.deepcopy(node.hunterMoves))
        new_node.map[empty[rnd][0]][empty[rnd][1]] = 2
        new_node.hunterMoves.append([empty[rnd][0], empty[rnd][1]])
        self.number_of_nodes_generated += 1

        return self.reflexPlayer(new_node.map, new_node)

class MinimaxAgent(Agent):
    def __init__(self, game):
        super().__init__(game)
        self.node = Node(None, 0, [self.bunny[0]+1, self.bunny[1]+1], copy.deepcopy(self.map), [], []) #Initial Node
        self.minimax = self.maxVal(self.map, 50, self.node) # Starts the minimax agent
        self.val = self.minimax[0]          # Terminal Value (1, -1, 0)
        self.bunnyMoves = self.minimax[1]   # List of bunny moves
        self.hunterMoves = self.minimax[2]  # List of hunter moves
        
    def expand(self, node, maxplayer):
        children = list()
        new_bunnyMoves = copy.deepcopy(node.bunnyMoves)
        new_hunterMoves = copy.deepcopy(node.hunterMoves)

        if maxplayer: # generates new nodes for bunny
            for action in self.moves:
                new_pos = [node.pos[0] + action[0], node.pos[1] + action[1]]
                if node.map[new_pos[0]][new_pos[1]] == 0:
                    new_map = copy.deepcopy(node.map)
                    new_bunnyMoves = copy.deepcopy(node.bunnyMoves)
                    new_hunterMoves = copy.deepcopy(node.hunterMoves)
                    new_map[new_pos[0]][new_pos[1]], new_map[node.pos[0]][node.pos[1]] = new_map[node.pos[0]][node.pos[1]], new_map[new_pos[0]][new_pos[1]]
                    new_bunnyMoves.append(action[-1])
                    new_node = Node(node, self.returnScore(new_map, new_pos), new_pos, new_map, new_bunnyMoves, new_hunterMoves)
                    children.append(new_node)

                    self.number_of_nodes_generated += 1

        if not maxplayer: # generates new nodes for hunter
            for space in self.emptySpace(node.map):
                new_map = copy.deepcopy(node.map)
                new_bunnyMoves = copy.deepcopy(node.bunnyMoves)
                new_hunterMoves = copy.deepcopy(node.hunterMoves)
                new_map[space[0]][space[1]] = 2
                new_hunterMoves.append(space)
                new_node = Node(node, self.returnScore(new_map, node.pos), node.pos, new_map, new_bunnyMoves, new_hunterMoves)
                children.append(new_node)

                self.number_of_nodes_generated += 1

        return children

    def maxVal(self, map, depth, node):
        ### YOUR CODE HERE ###
        if depth == 0 or self.checkTerminal(node.map, node.pos): # terminal state
            return node.val, node.bunnyMoves, node.hunterMoves

        # finds the node with higher values
        best = None
        for child in self.expand(node, True):
            val, bunnyMoves, hunterMoves = self.minVal(child.map, depth-1, child)
            if not best:
                best = (val, bunnyMoves, hunterMoves)
            elif val > best[0]:
                best = (val, bunnyMoves, hunterMoves)

        ### YOUR CODE HERE ###
        return best # Example return you can change it if you want

    def minVal(self, map, depth, node):
        ### YOUR CODE HERE ###
        if depth == 0 or self.checkTerminal(node.map, node.pos): # terminal state
            return node.val, node.bunnyMoves, node.hunterMoves

        # finds the node with lower values
        best = None
        for child in self.expand(node, False):
            val, bunnyMoves, hunterMoves = self.maxVal(child.map, depth-1, child)
            if not best:
                best = (val, bunnyMoves, hunterMoves)
            elif val < best[0]:
                best = (val, bunnyMoves, hunterMoves)

        ### YOUR CODE HERE ###
        
        return best # Example return you can change it if you want
        
class AlphaBetaAgent(Agent):
    def __init__(self, game):
        super().__init__(game) 
        self.node = Node(None, 0, [self.bunny[0]+1, self.bunny[1]+1], copy.deepcopy(self.map), [], []) #Initial Node
        self.alphabeta = self.maxVal(self.map, 50, self.node, -1000, 1000) # Starts the alpha-beta agent
        self.val = self.alphabeta[0]            # Terminal Value (1, -1, 0)
        self.bunnyMoves = self.alphabeta[1]     # List of bunny moves
        self.hunterMoves = self.alphabeta[2]    # List of hunter moves

    def expand(self, node, maxplayer):
        children = list()

        if maxplayer: # Creates new nodes for bunny
            for action in self.moves:
                new_pos = [node.pos[0] + action[0], node.pos[1] + action[1]]
                if node.map[new_pos[0]][new_pos[1]] == 0:
                    new_node = copy.deepcopy(node)
                    new_node.parent = node
                    new_node.map[new_pos[0]][new_pos[1]] = 3
                    new_node.map[node.pos[0]][node.pos[1]] = 0
                    new_node.pos = new_pos
                    new_node.bunnyMoves.append(action[-1])
                    new_node.val = self.returnScore(new_node.map, new_node.pos)
                    children.append(new_node)

                    self.number_of_nodes_generated += 1

        if not maxplayer: # creates new nodes for hunter
            for space in self.emptySpace(node.map):
                new_node = copy.deepcopy(node)
                new_node.parent = node
                new_node.map[space[0]][space[1]] = 2
                new_node.hunterMoves.append(space)
                new_node.val = self.returnScore(new_node.map, new_node.pos)
                children.append(new_node)

                self.number_of_nodes_generated += 1

        return children

    def maxVal(self, map, depth, node, alpha, beta):
        ### YOUR CODE HERE ###
        if depth == 0 or self.checkTerminal(node.map, node.pos):# terminal state
            return node.val, node.bunnyMoves, node.hunterMoves

        # finds the node with higher values
        best = None
        for child in self.expand(node, maxplayer=True):
            val, bunnyMoves, hunterMoves = self.minVal(child.map, depth-1, child, alpha, beta)
            if not best:
                best = (val, bunnyMoves, hunterMoves)
            elif val > best[0]:
                best = (val, bunnyMoves, hunterMoves)

            # Prunes the tree
            alpha = max(alpha, val)
            if alpha >= beta:
                break

        ### YOUR CODE HERE ###
        return best
    
    def minVal(self, map, depth, node, alpha, beta):
        ### YOUR CODE HERE ###
        if depth == 0 or self.checkTerminal(node.map, node.pos):# terminal state
            return node.val, node.bunnyMoves, node.hunterMoves

        # finds the node with lower values
        best = list()
        for child in self.expand(node, maxplayer=False):
            val, bunnyMoves, hunterMoves  = self.maxVal(child.map, depth-1, child, alpha, beta)
            if not best:
                best = (val, bunnyMoves, hunterMoves)
            elif val < best[0]:
                best = (val, bunnyMoves, hunterMoves)
                
            # Prunes the tree
            beta = min(beta, val)
            if beta >= alpha: break
        ### YOUR CODE HERE ###
        
        return best # Example return you can change it if you want
