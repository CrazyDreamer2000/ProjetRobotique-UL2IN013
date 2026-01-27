import math
import pygame
import random
from classrobot import Robot

keys2 = pygame.key.get_just_pressed()

if keys2[pygame.K_2]:
    
    x_mur = 800 * random.randint(0, 800)
    y_mur = 600 * random.randint(0, 600)

    pygame.draw.line(screen, (0, 255, 255), (x_mur, 0), (y_mur, 0), 1)
