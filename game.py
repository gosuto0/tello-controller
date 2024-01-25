import sys, random
import pygame
from pygame.locals import *
import time

pygame.init()
screen = pygame.display.set_mode((600, 400))
white = (255,255,255)
black = (0,0,0)
x=200
y=0

while True:
    screen.fill(black)
    pygame.draw.circle(screen, white, (x,y), 30)
    if y <= 350:
        y=y+0.01
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()