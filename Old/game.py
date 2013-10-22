import pygame
from pygame.locals import *

from Animal import Animal
from State import State
from GameState import GameState
from MiniGame1 import MiniGame1
from MiniGame2 import MiniGame2
from MiniGame3 import MiniGame3
from Menu import Menu
#parameters
SCREEN_HEIGHT, SCREEN_WIDTH = 400,400
BG_COLOR = 150, 150, 80
#media

#globals
currentState = Menu();

#init
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
clock = pygame.time.Clock()


#Main Loop
while True:
	time_passed = clock.tick(50)
	
	for event in pygame.event.get():
		#check events
		if event.type == pygame.QUIT:
			exit_game()
		
	#redraw background
	screen.fill(BG_COLOR)
		
	#update logic
	currentState.Update();

	currentState.Draw();
		
	pygame.display.flip()