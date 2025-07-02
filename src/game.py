"""
    ###################################
    DO NOT CHANGE ANYTHING IN THIS FILE
    ###################################
"""

import pygame
from pygame.locals import RLEACCEL
import numpy
from random import randint, choice
from copy import deepcopy

class Forest:
    benchmark_game = [[2,2],[[0, 0], [0, 3], [1, 4], [2, 4], [3, 1], [3, 4], [4, 3]]]
    def __init__(self, size=[5,5], hunters=7,intelligent = False, render=True, verbose=False, benchmark=False) -> None:
        
        pygame.init()
        pygame.display.set_caption("Forest")


        self.render = render
        self.verbose = verbose
        self.intelligent = intelligent
        self.start_hunter = hunters
        self.benchmark = benchmark
        self.cell_properties = {"height":100,"width":100,"margin":5}
        self.sizes = (size[0],size[1])
        self.window_size = (self.sizes[1]*(self.cell_properties["width"]+self.cell_properties["margin"])+self.cell_properties["margin"],
                            self.sizes[0]*(self.cell_properties["height"]+self.cell_properties["margin"])+self.cell_properties["margin"])
        
        if render:
            self.screen = pygame.display.set_mode(self.window_size)
        self.clock = pygame.time.Clock()
        self.grid = numpy.zeros(self.sizes)
        if render:
            self.image_size = [self.cell_properties["width"]-10,self.cell_properties["height"]-10]
            self.BUNNY_IMG = pygame.transform.scale(pygame.image.load('images/bunny.png'), self.image_size)
            self.BUNNY_IMG.set_colorkey((255, 255, 255), RLEACCEL)
            self.BUNNY_IMG = self.BUNNY_IMG.convert_alpha()
            self.HUNTER_IMG = pygame.transform.scale(pygame.image.load('images/hunter.png'), self.image_size)
            self.HUNTER_IMG.set_colorkey((255, 255, 255), RLEACCEL)
            self.HUNTER_IMG = self.HUNTER_IMG.convert_alpha()
        
        self.reset()
        if render:
            self.drawingLoop()

    def __del__(self) -> None:
        pygame.quit()

    def loadGame(self,state):
        self.bunny,hunters = state
        self.hunters = []
        for h in hunters:
            self.hunters.append(h)

    def spawnHunter(self,rnd=True, spawn=None):

        if spawn is not None:
            r = spawn
            r = self.hunters.append(r)
            return r
            

        if rnd:
            r = [randint(0,self.sizes[0]-1),randint(0,self.sizes[1]-1)]
            while r in self.hunters or r == self.bunny:
                r = [randint(0,self.sizes[0]-1),randint(0,self.sizes[1]-1)]
            self.hunters.append(r)
        else:
            candidates = []
            for i in [[0,1],[0,-1],[1,0],[-1,0]]:
                x,y = [x+y for x,y in zip(self.bunny,i)]
                if x>=0 and x<self.sizes[0] and y>=0 and y<self.sizes[1]:
                    if [x,y] not in self.hunters:
                        candidates.append([x,y])
            if len(candidates):
                if self.intelligent:
                    best_dist = 99999
                    for c in candidates:
                        dist = min(c[0],c[1],self.sizes[0]-c[0]-1,self.sizes[1]-c[1]-1)
                        if dist < best_dist:
                            best_dist = dist
                            r = c
                else:
                    r = choice(candidates)
                self.hunters.append(r)
                if len(candidates) == 1:
                    print("Hunters wins")
                    self.winner = -1
                    self.gameover = True
        return r    
    
    def bunnySafe(self):
        if self.bunny[0] == 0 \
              or self.bunny[0] == self.sizes[0]-1 \
              or self.bunny[1] == 0 \
              or self.bunny[1] == self.sizes[1]-1:
                print("Bunny wins")
                self.winner = 1
                self.gameover = True
        return self.gameover

    def getWinner(self):
        return self.winner
    
    def reset(self):
        self.done=False
        self.gameover = False
        self.winner = 0
        if self.benchmark:
            self.loadGame(self.benchmark_game)
        else:
            self.bunny = [self.sizes[0]//2, self.sizes[1]//2]
            bunny_surrounded = 4
            while(bunny_surrounded == 4):
                self.hunters = []
                bunny_surrounded = 0
                for _ in range(self.start_hunter):
                    pos = self.spawnHunter()
                    dist = sum([abs(x-y) for x,y in zip(pos,self.bunny)])
                    if dist == 1:
                        bunny_surrounded+=1
            print("Reset tight is ", bunny_surrounded)

    def state(self):
        return {"hunters":deepcopy(self.hunters),"bunny":deepcopy(self.bunny)}
    
    def action(self,move, spawn=None):
        x,y = self.bunny
        if move == "UP":
            x-=1
        elif move == "DOWN":
            x+=1
        elif move == "RIGHT":
            y+=1
        elif move == "LEFT":
            y-=1
        else: return False
        if x>=0 and x<self.sizes[0] and y<self.sizes[1] and y>=0 and [x,y] not in self.hunters:
                self.bunny = [x,y]
                if not self.bunnySafe():
                    if spawn is None:
                        self.spawnHunter(rnd=False, spawn=None)
                    else:
                        self.spawnHunter(rnd=False, spawn=spawn)
        else: return False
        return True

    def draw(self) -> None:
        self.screen.fill((255,255,255))
        for row in range(self.sizes[0]):
            for column in range(self.sizes[1]):
                pygame.draw.rect(self.screen, (100,200,100), 
                [self.cell_properties["margin"] + (self.cell_properties["margin"] + self.cell_properties["width"]) * column, 
                self.cell_properties["margin"] + (self.cell_properties["margin"] + self.cell_properties["height"]) * row, 
                self.cell_properties["width"], self.cell_properties["height"]])

                if [row,column] == self.bunny:
                    self.screen.blit(self.BUNNY_IMG, 
                                     (self.cell_properties["margin"] + (self.cell_properties["margin"] + self.cell_properties["width"]) * column + 5, 
                                      self.cell_properties["margin"] + (self.cell_properties["margin"] + self.cell_properties["height"]) * row + 5))
                elif [row,column] in self.hunters:
                    self.screen.blit(self.HUNTER_IMG, 
                                     (self.cell_properties["margin"] + (self.cell_properties["margin"] + self.cell_properties["width"]) * column + 5, 
                                      self.cell_properties["margin"] + (self.cell_properties["margin"] + self.cell_properties["height"]) * row + 5))
        pygame.display.flip()
        self.clock.tick(60)

    def drawingLoop(self) -> None:
        while not self.done:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                            print("Exit")
                            pygame.quit()
                            self.done = True
                            break
                    elif event.key == pygame.K_RETURN:
                        self.reset()
                    elif event.key == pygame.K_r:
                        self.reset()
                    elif not self.gameover:
                        if event.key == pygame.K_UP:
                            self.action("UP")
                        elif event.key == pygame.K_DOWN:
                            self.action("DOWN")
                        elif event.key == pygame.K_RIGHT:
                            self.action("RIGHT")
                        elif event.key == pygame.K_LEFT:
                            self.action("LEFT")

if __name__ == "__main__":
    Forest(size = [7,6], verbose = True, intelligent=True)