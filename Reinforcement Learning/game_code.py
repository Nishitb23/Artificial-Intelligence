import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox
import numpy as np

class agent(object):

    def __init__(self,pos):
        self.x = pos[0]
        self.y = pos[1]

    def draw(self, surface):
        pygame.draw.rect(surface, (0,0,255),[(self.x-1)*80,(self.y-1)*80,80,80])
    	
    def getpos(self):
    	return (self.x,self.y)
    	
    def update(self,pos):
    	self.x = pos[0]
    	self.y = pos[1]
    	

def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255,255,255), (x,0),(x,w))
        pygame.draw.line(surface, (255,255,255), (0,y),(w,y))
        
def drawboxes(pos,surface,color,istext,text):
	for w in pos:
		pygame.draw.rect(surface, color, [(w[0]-1)*80,(w[1]-1)*80,80,80])
		if istext:
			screen.blit(pygame.font.Font('freesansbold.ttf', 20).render(text, True, (0,0,0)), ((w[0]-1)*80,(w[1]-1)*80))
			
def isStatePossible(pos, wall, restart, powergate, goal):
	if pos in wall:
		return False
		
	if pos in restart:
		return False
		
	if pos in powergate:
		return False
		
	if pos in goal:
		return False
		
	return True
			
def getReward(pos, action, wall, restart, powergate, goal, powerpos):
	x = pos[0]
	y = pos[1]
	#up = 1
	#down = 2
	#right = 3
	#left = 4
	if action == 0:
		y = y-1
	elif action == 1:
		y = y+1
	elif action == 2:
		x = x+1
	elif action == 3:
		x = x-1
	
	if x<1 or x>8:
		return -50
	if y<1 or y>8:
		return -50
	if (x,y) in wall:
		return -50
	if (x,y) in restart:
		return -50
	if (x,y) in goal:
		return 100
	if (x,y) in powergate:
		return (abs(goal[0][0]-powerpos[0][0])+abs(goal[0][1]-powerpos[0][1]))*(-1)
	return (abs(goal[0][0]-x)+abs(goal[0][1]-y))*(-1)
	
def getFutureQ(pos,action,qtable):
	x = pos[0]
	y = pos[1]
	#up = 1
	#down = 2
	#right = 3
	#left = 4
	if action == 0:
		y = y-1
	elif action == 1:
		y = y+1
	elif action == 2:
		x = x+1
	elif action == 3:
		x = x-1

	if x<1 or x>8:
		return -50
	if y<1 or y>8:
		return -50
	return qtable[x-1][y-1][np.argmax(qtable[x-1][y-1])]
	
def moveAgent(agtObj, qtable, wall, restart, powergate, powerpos):
	currPos = agtObj.getpos()
	x = currPos[0]
	y = currPos[1]
	print("current position:(",x,y,")")
	action = np.argmax(qtable[x-1][y-1])
	newx = x
	newy = y
	if action == 0:
		newy = y-1
	elif action == 1:
		newy = y+1
	elif action == 2:
		newx = x+1
	elif action == 3:
		newx = x-1
	if (newx,newy) in wall:
		print("obstacle detected")
	elif (newx,newy) in restart:
		print("restarting")
		agtObj.update((1,8))
	elif (newx,newy) in powergate:
		agtObj.update(powerpos[0])
	else:
		agtObj.update((newx,newy))
	return qtable[x-1][y-1][action]*(-1)
		
def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass
    	
#start
pygame.init()
window_width=640
window_height=640

animation_increment=10
clock_tick_rate=1.5

# Open a window
size = (window_width, window_height)
screen = pygame.display.set_mode(size)

# Set title to the window
pygame.display.set_caption("Path Finder")

dead=False
clock = pygame.time.Clock()

#objects initialization
wall = [(3,1),(3,2),(3,3),(3,4),(3,6),(2,6),(5,2),(6,2),(5,4),(6,4),(7,4),(7,7),(8,7),(5,5),(5,6),(5,7)]
restart = [(1,5),(7,5)]
powerpos = [(8,4)]
powergate = [(2,3),(4,2),(8,8)]
agentObj = agent((1,8))
goalOptions = [(6,1),(6,3),(7,1),(7,2),(7,3),(8,1),(8,2),(8,3)]
goal= [goalOptions[random.randint(0,7)]]

#defining hyper-parameters and variable for q-learning
qtable = np.zeros((8,8,4))
learning_rate = 0.9
discount = 0.8
episodes = 1

#starting learning the model
for i in range(episodes):
	for x in range(8):
		for y in range(8):
			for action in range(4):
				if isStatePossible((x+1,y+1),wall,restart,powergate,goal):
					#print('x =',x+1,'y=',y+1,'action=',action,'value=',qtable[x][y][action])
					reward = getReward((x+1,y+1),action,wall,restart,powergate,goal,powerpos)
					#print('x =',x+1,'y=',y+1,'action=',action,'reward=',reward)
					futureQ = getFutureQ((x+1,y+1),action,qtable)
					qtable[x][y][action] = qtable[x][y][action] + learning_rate*(reward + discount*(futureQ - qtable[x][y][action]))
				
print("the learned q-table is:")
for x in range(8):
	for y in range(8):
		for action in range(4):
			print('x =',x+1,'y=',y+1,'action=',action,'value=',qtable[x][y][action])

move = False	
cost = 0
#window content display loop
while(dead==False):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
        	dead = True
        if event.type == pygame.MOUSEBUTTONUP:
        	move = True
        		    
    #static objects and enviroment creation
    drawGrid(window_width,8,screen)
    drawboxes(wall,screen,(165,42,42),False,"")
    drawboxes(restart,screen,(255,69,0),True,"Restart")
    drawboxes(powerpos,screen,(255,255,0),True,"Power")
    drawboxes(powergate,screen,(50,205,50),True,"Gate")
    drawboxes(goal,screen,(255,0,50),True,"Goal")
    agentObj.draw(screen)
    pygame.display.update()
    if agentObj.getpos() in goal:
    		print("cost of the path is:",abs(cost))
    		message_box('play again', 'goal reached!!')
    		break
    if move:
    	pygame.draw.rect(screen, (0,0,0),[(agentObj.getpos()[0]-1)*80,(agentObj.getpos()[1]-1)*80,80,80])
    	cost = cost + moveAgent(agentObj,qtable,wall,restart,powergate,powerpos)
    	if agentObj.getpos() in goal:
    		move = False
    clock.tick(clock_tick_rate)
