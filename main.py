# https://www.geeksforgeeks.org/python/pygame-input-handling/

import pygame
from pygame.locals import *
from sys import exit

import Robot

pygame.init()

Dexter = Robot()

size = width, height = 740, 480
screen = pygame.display.set_mode(size)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
            
        if event.type == KEYDOWN:  
            if event.key == K_LEFT:  
                Dexter.left = True
                print("pressed LEFT")
            elif event.key == K_RIGHT:  
                Dexter.right = True
                print("pressed RIGHT")
            elif event.key == K_UP: 
                Dexter.forward = True
                print("pressed UP")
            elif event.key == K_DOWN: 
                Dexter.backward = True
                print("pressed DOWN")
  
    # updating coordinate values of x,y
    screen.fill((255, 255, 255))
    
    # the function will fill the background with white color
    screen.blit(img, (x, y)) # ? ? ? ?  ??
    
    # blit() function will copy image file to x,y coordinates.
    pygame.display.update()
    # draw the objects on screen