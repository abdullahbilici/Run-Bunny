"""
    ###################################
    DO NOT CHANGE ANYTHING IN THIS FILE
    ###################################
"""

class Agent():
    def __init__(self,game):
        self.moves = [[-1, 0, 0], [0, 1, 1], [1, 0, 2], [0, -1, 3]]  # UP, RIGHT, DOWN, LEFT (x, y, action)
        self.grid = game.grid                                        # Game grid
        self.bunny = game.bunny                                      # Bunny position
        self.hunters = game.hunters                                  # Hunters position                              
        self.sizes = game.sizes                                      # Size of the grid
        self.map = None                                              # Game state                     
        self.val = None                                              # Value of the game state
        self.bunnyMoves = None                                       # Bunny moves
        self.hunterMoves = None                                      # Hunters moves                                  
        self.generateMap()                                           # Generate the game state                             
        self.number_of_nodes_generated = 1                           # Number of nodes generated
    
    def generateMap(self):
        """
            Generates a map of the game state

            0 - Empty,
            1 - Wall,
            2 - Hunter,
            3 - Bunny,

        Returns:
            map (list): A list of lists representing the game state
        """
        self.map = [[0 for x in range(self.sizes[0] + 2)] for y in range(self.sizes[1] + 2)]

        for i in range(self.sizes[0] + 2):
            self.map[i][0] = 1
            self.map[i][self.sizes[0] + 1] = 1

        for i in range(self.sizes[1] + 2):
            self.map[0][i] = 1
            self.map[self.sizes[1] + 1][i] = 1

        for i in range(len(self.hunters)):
            self.map[self.hunters[i][0] + 1][self.hunters[i][1] + 1] = 2

        self.map[self.bunny[0] + 1][self.bunny[1] + 1] = 3

    def checkTerminal(self, map, pos):
        """
            Checks if the game is over

            Args:
                map (list): A list of lists representing the game state
                pos (list): A list of the current position of the agent

            Returns:
                bool: True if the game is over, False otherwise
        """
        surrounded = 0
        for i in range(len(self.moves)):

            if map[pos[0] - self.moves[i][0]][pos[1] - self.moves[i][1]] == 1:
                return True

            if map[pos[0] - self.moves[i][0]][pos[1] - self.moves[i][1]] == 2:
                surrounded += 1
                if surrounded == 4:
                    return True
                
        return False
    
    def returnScore(self, map, pos):
        """
            Returns the score of the game state

            Args:
                map (list): A list of lists representing the game state
                pos (list): A list of the current position of the agent
            
            Returns:
                int: 1 if the bunny wins, -1 if the hunters win, 0 otherwise
        """
        surrounded = 0
        for i in range(len(self.moves)):
            if map[pos[0] - self.moves[i][0]][pos[1] - self.moves[i][1]] == 1:
                return 1
            if map[pos[0] - self.moves[i][0]][pos[1] - self.moves[i][1]] == 2:
                surrounded += 1
                if surrounded == 4:
                    return -1
        return 0
    
    def emptySpace(self, map):
        """
            Returns a list of empty spaces

            Args:
                map (list): A list of lists representing the game state

            Returns:
                empty (list): A list of empty spaces
        """
        empty = []
        for i in range(len(map)):
            for j in range(len(map[i])):
                if map[i][j] == 0:
                    for k in range(len(self.moves)):
                        if map[i - self.moves[k][0]][j - self.moves[k][1]] == 3:
                            empty.append([i, j])
        
        return empty