import pygame
from pygame.locals import *
import random

class invader:
	def __init__(self, x, y, number, problem):
		self.x = x
		self.y = y
		self.number = number
		self.problem = problem;
		self.rectangle = invaderRectangle.move(x,y)
		self.dead = False

#parameters
SCREEN_HEIGHT, SCREEN_WIDTH = 500,400
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
lost = True
level = 1

#init
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
clock = pygame.time.Clock()


#MEDIA
myfont = pygame.font.SysFont("monospace", 15, True)
headerFont = pygame.font.SysFont("monospace", 50, True)
backUp = pygame.image.load('Media/backbuttonup.png')
backOver = pygame.image.load('Media/backbuttonover.png')
backRectangle = backUp.get_rect().move(0,300);
#menu
playUp = pygame.image.load('Media/playbuttonup.png')
playOver = pygame.image.load('Media/playbuttonover.png')
playRectangle = playUp.get_rect().move(100,100);

creditsUp = pygame.image.load('Media/creditsbuttonup.png')
creditsOver = pygame.image.load('Media/creditsbuttonover.png')
creditsRectangle = creditsUp.get_rect().move(100,125);

helpUp = pygame.image.load('Media/helpbuttonup.png')
helpOver = pygame.image.load('Media/helpbuttonover.png')
helpRectangle = helpUp.get_rect().move(100,150);

#credits and help
creditsImage = pygame.image.load('Media/credits.png')
helpImage = pygame.image.load('Media/help.png')

#play
player = pygame.image.load("Media/ship.png")
playerRectangle = player.get_rect().move(184,368)
invaderImage = pygame.image.load("Media/invader.png")
invaderRectangle = invaderImage.get_rect()
bulletImage = pygame.image.load("Media/bullet.png")


def reset():
	global invaders
	global level
	global lost
	lost = False

	invaders = []
	nextInvaderX = 0
	nextInvaderY = 0
	for i in range(NUMBER_OF_INVADERS):
		if nextInvaderX/32 > 9:
			nextInvaderX = 33
			nextInvaderY += 33
		else:
			nextInvaderX += 33
		invaders.append(invader(nextInvaderX,nextInvaderY, i, str(i) + " + 0"))
	playerRectangle = player.get_rect().move(184,368)
	
def getNewProblem():
	global targetNumber
	global problem
	i = random.randint(0, len(invaders))
	while (invaders[i].dead):
		i = random.randint(0,len(invaders))
	
	targetNumber = invaders[i].number
	problem = invaders[i].problem
def update():
	if (currentState == "PLAY"):
		global playerRectangle
		global spaceDown
		global invaders
		global bullets
		global targetNumber
		global score
		global problem
		global lost
		global level
		
		if (lost == False):
			keys = pygame.key.get_pressed()
			if (keys[K_LEFT]):
				playerRectangle = playerRectangle.move(-2, 0)
			if (keys[K_RIGHT]):
				playerRectangle = playerRectangle.move(2, 0)
			if (keys[K_SPACE]):
				if (spaceDown == False):
					bullets.append(bulletImage.get_rect().move(playerRectangle.topleft[0]+8,playerRectangle.topleft[1]))
					spaceDown = True
			else:
				spaceDown = False
			for i in range(len(bullets)):
				bullets[i] = bullets[i].move(0,-4)
				
			#update the invaders
			for i in range(len(invaders)):
				if (invaders[i].dead == False):
					#check for bullet first
					for j in range(len(bullets)):
						if (invaders[i].rectangle.colliderect(bullets[j])):
							invaders[i].dead = True
							if (invaders[i].number == targetNumber):
								score += 10
								getNewProblem()
							bullets.remove(bullets[j])
							break;
					if (invaders[i].rectangle.bottomleft[1] > 368):
						lost = True;
					invaders[i].rectangle = invaders[i].rectangle.move(0,1)

def draw():
	mousePos = pygame.mouse.get_pos()
	if currentState == "MENU":
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
		screen.blit(player,playerRectangle)
		for i in range(len(invaders)):
			if (invaders[i].dead == False):
				screen.blit(invaderImage, invaders[i].rectangle)
				screen.blit(myfont.render(str(invaders[i].number), 1, (255,0,0)), (invaders[i].rectangle.topleft[0]+10,invaders[i].rectangle.topleft[1]+8))
		for i in range(len(bullets)):
			screen.blit(bulletImage, bullets[i])
		
		screen.blit(myfont.render("Score: " + str(score), 1, (255,255,255)), (10,450))
		screen.blit(myfont.render("Problem: " + problem + " = ?", 1, (255,255,255)), (10,475))
		
		if (lost):
			screen.blit(headerFont.render("You Lost!", 1, (255,255,255)), (80,200))
			if backRectangle.collidepoint(mousePos[0],mousePos[1]):
				screen.blit(backOver, backRectangle)
			else:
				screen.blit(backUp, backRectangle)
		
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
	time_passed = clock.tick(50)
	
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
					level = 1
					reset()
				if creditsRectangle.collidepoint(mousePos[0],mousePos[1]):
					currentState = "CREDITS"
				if helpRectangle.collidepoint(mousePos[0],mousePos[1]):
					currentState = "HELP"
			elif (currentState == "CREDITS" or currentState == "HELP" or lost == True):
				if backRectangle.collidepoint(mousePos[0],mousePos[1]):
					currentState = "MENU"
	
	#redraw background
	screen.fill(BG_COLOR)
	
	update()
	draw()
		
	pygame.display.flip()
	
	
