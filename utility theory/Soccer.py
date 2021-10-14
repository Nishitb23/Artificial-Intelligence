import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox
import numpy as np

class player(object):

    def __init__(self,x,y,color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self, surface):
        pygame.draw.circle(surface, self.color,(self.x,self.y),10)
    	
    def getpos(self):
    	return (self.x,self.y)
    
    def getx(self):
    	return self.x
    	
    def gety(self):
    	return self.y
        
        
class ball(object):
	
	def __init__(self,x,y,color):
		self.x = x
		self.y = y
		self.color = color
	
	def draw(self,surface):
		pygame.draw.circle(surface, self.color,(self.x,self.y),3)
		
	def update(self,x,y):
		self.x = x
		self.y = y
		
	def getx(self):
		return self.x
		
	def gety(self):
		return self.y

class goalpost(object):

    def __init__(self,leftpost,rightpost):
        self.leftpost = leftpost
        self.rightpost = rightpost

    def getLeft(self):
    	return self.leftpost
    	
    def getRight(self):
    	return self.rightpost
    	
#function to get distance of point from line(enter first line coordinate then point coordinates)
def getDistLine(x0,y0,x1,y1,x2,y2):
	p1 = np.array([x0,y0])
	p2 = np.array([x1,y1])
	p3 = np.array([x2,y2])
	d= abs(np.cross(p2-p1,p3-p1)/np.linalg.norm(p2-p1) )
	#print("p1:",p1)
	#print("p2:",p2)
	#print("p3:",p3)
	#print("d: ",d)
	return d
	
def getDistance(blueA,blueB):
	p1 = np.array([blueA.getx(),blueA.gety()])
	p2 = np.array([blueB.getx(),blueB.gety()])
	return np.linalg.norm(p2-p1)
	
def checkObstacle(redpos,blue_first,blue_second):
	flag = False
	for i in range(3):
		if(getDistLine(blue_first.getx(),blue_first.gety(),blue_second.getx(),blue_second.gety(),redpos[i][0],redpos[i][1])<20):
			maxy = max(blue_first.gety(),blue_second.gety())
			miny = min(blue_first.gety(),blue_second.gety())
			if(redpos[i][1]<maxy and redpos[i][1]>miny):
				flag = True
				break
	#print(flag)
	return flag
			      
def getUtilityListCenter(redpos,bluec,blue1,blue2,blue3):
	l = []
	if(checkObstacle(redpos,bluec,blue1)):
		l.append(100000)
	else:
		l.append(getDistance(bluec,blue1))
	
	if(checkObstacle(redpos,bluec,blue2)):
		l.append(100000)
	else:
		l.append(getDistance(bluec,blue2))
		
	if(checkObstacle(redpos,bluec,blue3)):
		l.append(100000)
	else:
		l.append(getDistance(bluec,blue3))
		
	return np.array(l)
	
def getUtilityListGoal(redpos,goalObj,blue1,blue2,blue3):
	l = []
	leftpost = goalObj.getLeft()
	rightpost = goalObj.getRight()
	
	mindist = 10000
	for i in range(leftpost[0],rightpost[0]+1):
		dummyBlue = player(i,leftpost[1],(0,0,255))
		if(checkObstacle(redpos,dummyBlue,blue1)!=True):
			dist = getDistance(dummyBlue,blue1)
			if(dist<mindist):
				mindist = dist
	l.append(mindist)
	
	mindist = 10000
	for i in range(leftpost[0],rightpost[0]+1):
		dummyBlue = player(i,leftpost[1],(0,0,255))
		if(checkObstacle(redpos,dummyBlue,blue2)!=True):
			dist = getDistance(dummyBlue,blue2)
			if(dist<mindist):
				mindist = dist
	l.append(mindist)
	
	mindist = 10000
	for i in range(leftpost[0],rightpost[0]+1):
		dummyBlue = player(i,leftpost[1],(0,0,255))
		if(checkObstacle(redpos,dummyBlue,blue3)!=True):
			dist = getDistance(dummyBlue,blue3)
			if(dist<mindist):
				mindist = dist
	l.append(mindist)
	
	return np.array(l)
	
def getClosestGoal(redpos,goalObj,agent):
	leftpost = goalObj.getLeft()
	rightpost = goalObj.getRight()
	mindist = 10000
	minx = 0
	miny = 0
	for i in range(leftpost[0],rightpost[0]+1):
		dummyBlue = player(i,leftpost[1],(0,0,255))
		if(checkObstacle(redpos,dummyBlue,agent)!=True):
			dist = getDistance(dummyBlue,agent)
			if(dist<mindist):
				mindist = dist
				minx = i
				miny = leftpost[1]
	#print("minx; ",minx,"miny; ",miny)
	return minx,miny
	
def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass
	
# initialize game engine
pygame.init()

window_width=570
window_height=726

animation_increment=10
clock_tick_rate=20

# Open a window
size = (window_width, window_height)
screen = pygame.display.set_mode(size)

# Set title to the window
pygame.display.set_caption("Goal Assist")

dead=False
clock = pygame.time.Clock()

#loading the game background image
background_image = pygame.image.load("AI2_Assignment1_T3_2021.png").convert()

#defining fixed random agents i.e team members
bluecenter = player(288,363,(0,0,255))
blue1 = player(90+random.randrange(210),50+random.randrange(100),(0,0,255))
blue2 = player(30+random.randrange(400),50+random.randrange(300),(0,0,255))
blue3 = player(30+random.randrange(400),50+random.randrange(300),(0,0,255))
red1 = player(90+random.randrange(210),50+random.randrange(100),(255,0,0))
red2 = player(30+random.randrange(400),50+random.randrange(300),(255,0,0))
red3 = player(30+random.randrange(400),50+random.randrange(300),(255,0,0))
#defining ball object
ballObj = ball(288,363,(255,255,255))
#defining goal object
goalObj = goalpost((250,30),(330,30))


#defining ball moving parameters
finalx = ballObj.getx()
finaly = ballObj.gety()
currentx = ballObj.getx()
currenty = ballObj.gety()
    
#creating list of red agent co-ordinate
redpos = [red1.getpos(),red2.getpos(),red3.getpos()]
print("position of all agents:")
print("redpos: ",redpos)
print("bluecenter: ",bluecenter.getpos())
print("blue1: ",blue1.getpos())
print("blue2: ",blue2.getpos())
print("blue3: ",blue3.getpos())
#get utility
u = getUtilityListCenter(redpos,bluecenter,blue1,blue2,blue3)
print("utility from center: ",u)
u = u + getUtilityListGoal(redpos,goalObj,blue1,blue2,blue3)
print("utility from goal: ",u)
index = np.argmin(u)
print("first pass to blue agent number: ",index+1)

pas = 0

while(dead==False):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
        	dead = True
        if event.type == pygame.MOUSEBUTTONUP:
        	if pas == 0:
        		if u[index]>10000:
        			message_box('play again', 'goal not possible..red player too close!')
        			break
        		if index == 0:
        			finalx = blue1.getx()
        			finaly = blue1.gety()
        		elif index == 1:
        			finalx = blue2.getx()
        			finaly = blue2.gety()
        		else:
        			finalx = blue3.getx()
        			finaly = blue3.gety()
        		pas = 1
        	else:
        		if index == 0:
        			finalx,finaly = getClosestGoal(redpos,goalObj,blue1)
        		elif index == 1:
        			finalx,finaly = getClosestGoal(redpos,goalObj,blue2)
        		else:
        			finalx,finaly = getClosestGoal(redpos,goalObj,blue3)
        		pas = 1						

    
    #static drawing of environment and players
    screen.blit(background_image, [0, 0])
    bluecenter.draw(screen)
    blue1.draw(screen)
    blue2.draw(screen)
    blue3.draw(screen)
    red1.draw(screen)
    red2.draw(screen)
    red3.draw(screen)
    
    #Moving the ball on press of enter
    currentx = ballObj.getx()
    currenty = ballObj.gety()
    #print(currentx,finalx)
    #print(currenty,finaly)
    if(finalx!= currentx or finaly!= currenty):
    	if(finalx == currentx):
    		#print("inside")
    		currenty = currenty-1
    		ballObj.update(currentx,currenty)
    	elif(finalx >= currentx):
    		currenty = currenty+math.ceil((finaly-currenty)/(finalx-currentx))
    		currentx = currentx+1
    		ballObj.update(currentx,currenty)
    	else:
    		currenty = currenty+math.ceil((finaly-currenty)/(currentx-finalx))
    		currentx = currentx-1
    		ballObj.update(currentx,currenty)
    		
    ballObj.draw(screen)
    		    
    #window refresh		    
    pygame.display.update()
    clock.tick(clock_tick_rate)
    
    
