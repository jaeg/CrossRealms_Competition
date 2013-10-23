import pygame
from pygame.locals import *
import random
import math
import pygame.mixer

class invader:
	def __init__(self, x, y, number, problem, row):
		self.x = x
		self.y = y
		self.number = number
		self.problem = problem;
		self.rectangle = invaderRectangle.move(x,y)
		self.dead = False
		self.row = row

#parameters
SCREEN_HEIGHT, SCREEN_WIDTH = 450,400
BG_COLOR = 0, 0, 0
NUMBER_OF_INVADERS = 20

#globals
currentState = "MENU"
invaders = []
bullets = []
spaceDown = False
targetNumber = 0
problem = "0 + 0"
score = 0
lost = False
win = True
level = 1
ticks = 0

#init
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
clock = pygame.time.Clock()

pygame.mixer.init()
#MEDIA
myfont = pygame.font.SysFont("monospace", 15, True)
headerFont = pygame.font.SysFont("monospace", 20, True)
backUp = pygame.image.load('Media/backbuttonup.png')
backOver = pygame.image.load('Media/backbuttonover.png')
backRectangle = backUp.get_rect().move(139,333);
clickSound = pygame.mixer.Sound("Media/tone8.wav")
#menu
playUp = pygame.image.load('Media/playbuttonup.png')
playOver = pygame.image.load('Media/playbuttonover.png')
playRectangle = playUp.get_rect().move(139,200);
nextRectangle = playUp.get_rect().move(139,300);

creditsUp = pygame.image.load('Media/creditsbuttonup.png')
creditsOver = pygame.image.load('Media/creditsbuttonover.png')
creditsRectangle = creditsUp.get_rect().move(139,225);

helpUp = pygame.image.load('Media/helpbuttonup.png')
helpOver = pygame.image.load('Media/helpbuttonover.png')
helpRectangle = helpUp.get_rect().move(139,250);

#credits and help
creditsImage = pygame.image.load('Media/credits.png')
helpImage = pygame.image.load('Media/help.png')

#play
player = pygame.image.load("Media/ship.png")
background = pygame.image.load("Media/background.png")
playerRectangle = player.get_rect().move(184,368)
invaderImage = pygame.image.load("Media/invader.png")
invaderRectangle = invaderImage.get_rect()
bulletImage = pygame.image.load("Media/bullet.png")
shootSound = pygame.mixer.Sound("Media/shoot.wav")
explosion = pygame.mixer.Sound("Media/explosion.wav")
invaderKilled = pygame.mixer.Sound("Media/invaderkilled.wav")
rightSound = pygame.mixer.Sound("Media/right.wav")


def reset():
	global invaders
	global level
	global lost
	global win
	global ticks
	ticks = 0
	lost = False
	win = False

	invaders = []
	nextInvaderX = 0
	nextInvaderY = 0
	for i in range(NUMBER_OF_INVADERS):
		if nextInvaderX/32 > 9:
			nextInvaderX = 33
			nextInvaderY += 33
		else:
			nextInvaderX += 33
		#generate a problem
		a = random.randint(0, 10)
		b = random.randint(1, 10)
		c = 0
		d = ""
		if (level == 1):
			c = a + b
			d = str(a) + " + " + str(b)
		elif (level == 2):
			c = a - b
			d = str(a) + " - " + str(b)
		elif (level == 3):
			c = a * b
			d = str(a) + " * " + str(b)

		invaders.append(invader(nextInvaderX,nextInvaderY, c, d, nextInvaderY/33))
	playerRectangle = player.get_rect().move(184,368)
	getNewProblem()

def checkWin():
	global win
	global level
	
	if (win == False):
		win = True
		for i in range(len(invaders)):
			if (invaders[i].dead == False):
				win = False
			
		if (win == True):
			level += 1
	
def getNewProblem():
	global targetNumber
	global problem
	if (win == False and lost == False):
		frontMostRow = getFrontMostRow()
	
		i = random.randint(0, len(invaders)-1)
		
		while (i < len(invaders)):
			if (invaders[i].dead or invaders[i].row != frontMostRow):
				i = random.randint(0,len(invaders)-1)
			else:
				break
		
		targetNumber = invaders[i].number
		problem = invaders[i].problem
	
def getFrontMostRow():
	row = 0
	for i in range(len(invaders)):
		if invaders[i].row > row and invaders[i].dead == False:
			row = invaders[i].row
	return row
	
def update():
	global currentState
	if (currentState == "PLAY"):
		global ticks
		global playerRectangle
		global spaceDown
		global invaders
		global bullets
		global targetNumber
		global score
		global problem
		global lost
		global win
		global level

		ticks += 1
		if (lost == False and win == False):
			keys = pygame.key.get_pressed()
			if (keys[K_LEFT]):
				if (playerRectangle.topleft[0] > 0):
					playerRectangle = playerRectangle.move(-6, 0)
			if (keys[K_RIGHT]):
				if (playerRectangle.topleft[0] < SCREEN_WIDTH - 32):
					playerRectangle = playerRectangle.move(6, 0)
			if (keys[K_SPACE]):
				if (spaceDown == False):
					shootSound.play()
					bullets.append(bulletImage.get_rect().move(playerRectangle.topleft[0]+8,playerRectangle.topleft[1]))
					spaceDown = True	
			else:
				spaceDown = False
			if (keys[K_ESCAPE]):
				currentState = "MENU"
			for i in range(len(bullets)):
				bullets[i] = bullets[i].move(0,-10)
				
			#update the invaders
			for i in range(len(invaders)):
				if (invaders[i].dead == False):
					#check for bullet first
					for j in range(len(bullets)):
						if (invaders[i].rectangle.colliderect(bullets[j])):
							invaders[i].dead = True
							checkWin()
							if (invaders[i].number == targetNumber):
								score += 10
								rightSound.play()
								getNewProblem()
							else:
								invaderKilled.play()
							bullets.remove(bullets[j])
							break;
					if (invaders[i].rectangle.bottomleft[1] > 368):
						lost = True;
						explosion.play();
					if (ticks % 2 == 0):
						invaders[i].rectangle = invaders[i].rectangle.move(math.sin(invaders[i].rectangle.topleft[1])*10,1)

def draw():
	mousePos = pygame.mouse.get_pos()
	if currentState == "MENU":
		screen.blit(headerFont.render("Math Invaders", 1, (255,255,255)), (133,150))
		if playRectangle.collidepoint(mousePos[0],mousePos[1]):
			screen.blit(playOver, playRectangle)
		else:
			screen.blit(playUp, playRectangle)
			
		if creditsRectangle.collidepoint(mousePos[0],mousePos[1]):
			screen.blit(creditsOver, creditsRectangle)
		else:
			screen.blit(creditsUp, creditsRectangle)
			
		if helpRectangle.collidepoint(mousePos[0],mousePos[1]):
			screen.blit(helpOver, helpRectangle)
		else:
			screen.blit(helpUp, helpRectangle)
	elif currentState == "PLAY":
		screen.blit(background,(0,0))
		screen.blit(player,playerRectangle)
		for i in range(len(invaders)):
			if (invaders[i].dead == False):
				screen.blit(invaderImage, invaders[i].rectangle)
				screen.blit(myfont.render(str(invaders[i].number), 1, (255,0,0)), (invaders[i].rectangle.topleft[0]+8,invaders[i].rectangle.topleft[1]+8))
		for i in range(len(bullets)):
			screen.blit(bulletImage, bullets[i])
		
		screen.blit(myfont.render("Score: " + str(score), 1, (255,255,255)), (10,405))
		screen.blit(myfont.render("Problem: " + problem + " = ?", 1, (255,255,255)), (10,420))
		
		if (lost):
			screen.blit(headerFont.render("You Lost!", 1, (255,255,255)), (80,200))
			if backRectangle.collidepoint(mousePos[0],mousePos[1]):
				screen.blit(backOver, backRectangle)
			else:
				screen.blit(backUp, backRectangle)
				
		if (win):
			screen.blit(headerFont.render("You've killed all the invaders!", 1, (255,255,255)), (0,200))
			if backRectangle.collidepoint(mousePos[0],mousePos[1]):
				screen.blit(backOver, backRectangle)
			else:
				screen.blit(backUp, backRectangle)
			if level < 4:
				if nextRectangle.collidepoint(mousePos[0],mousePos[1]):
					screen.blit(playOver, nextRectangle)
				else:
					screen.blit(playUp, nextRectangle)
	elif currentState == "CREDITS":
		screen.blit(creditsImage, (0,0))
		if backRectangle.collidepoint(mousePos[0],mousePos[1]):
			screen.blit(backOver, backRectangle)
		else:
			screen.blit(backUp, backRectangle)
			
	elif currentState == "HELP":
		screen.blit(helpImage, (0,0))
		if backRectangle.collidepoint(mousePos[0],mousePos[1]):
			screen.blit(backOver, backRectangle)
		else:
			screen.blit(backUp, backRectangle)
	
running = 1
#Main Loop
while running == 1:
	for event in pygame.event.get():
		#check events
		if event.type == pygame.QUIT:
			running = 0
		elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #left mouse click
			mousePos = pygame.mouse.get_pos()
			if (currentState == "MENU"):
				#check for buttons clicked
				if playRectangle.collidepoint(mousePos[0],mousePos[1]):
					currentState = "PLAY"
					clickSound.play()
					pygame.mixer.music.rewind()
					level = 1
					reset()
				if creditsRectangle.collidepoint(mousePos[0],mousePos[1]):
					currentState = "CREDITS"
					clickSound.play()
				if helpRectangle.collidepoint(mousePos[0],mousePos[1]):
					currentState = "HELP"
					clickSound.play()
			elif (currentState == "CREDITS" or currentState == "HELP" or lost):
				if backRectangle.collidepoint(mousePos[0],mousePos[1]):
					currentState = "MENU"
					clickSound.play()
			elif (currentState == "PLAY" and win):
				if (level < 4):
					if nextRectangle.collidepoint(mousePos[0],mousePos[1]):
						reset()
						clickSound.play()
				if backRectangle.collidepoint(mousePos[0],mousePos[1]):
					currentState = "MENU"
					clickSound.play()
	
	#redraw background
	screen.fill(BG_COLOR)
	
	update()
	draw()
		
	pygame.display.flip()
	
	
