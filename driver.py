import pygame
import os
import time
from sys import platform
#josh and anacan did this, josh made the gorgeous graphics:)
#this file creates a pygame window and allows you to graphically select
#whether you want to play a user-inputted flappy bird or watch the NEAT model run
#there were some minor issues with pygame, but no significant ones that really affected functionality
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800
pygame.init()
win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
 
backgroundImage = pygame.transform.scale(pygame.image.load(os.path.join("images","bg.png")),(WINDOW_WIDTH,WINDOW_HEIGHT))
font = pygame.font.Font(None,100)
text = font.render("Flappy Learn", True, (0, 0, 0))

red = (200,0,0)
green = (0,200,0)
 
bright_red = (255,0,0)
bright_green = (0,255,0)

birdText = font.render("BIRD", True, green)
learnText = font.render("LEARN", True, red)

 
menu = True
 
 
while menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
       
    win.blit(backgroundImage, (0,0))
    win.blit(text, (100,100))
    win.blit(birdText,(100,360))
    win.blit(learnText,(300,360))
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if 150+100 > mouse[0] > 150 and 450+50 > mouse[1] > 450:
        pygame.draw.rect(win, bright_green,(150,450,100,50))
        if click[0] == 1:
            pygame.display.quit()
            pygame.quit()
            if platform == "darwin": #if its mac, use python3
                os.system('python3 flappybird2.py')
            elif platform == "win32": #if its windows, use python
                os.system('python flappyBird2.py')
            #we COULD have added a statement for linux
            #but nah nobody likes linux
            
    else:
        pygame.draw.rect(win, green,(150,450,100,50))
    if 350+100 > mouse[0] > 350 and 450+50 > mouse[1] > 450:
        pygame.draw.rect(win, bright_red,(350,450,100,50))
        if click[0] == 1:
            pygame.display.quit()
            pygame.quit()
            if platform == "darwin": #if its mac, use python3
                os.system('python3 flappyLearn.py')
            elif platform == "win32": #if its windows, use python
                os.system('python flappyLearn.py')
            #we COULD have added a statement for linux
            #but nah nobody likes linux
            
    else:
        pygame.draw.rect(win, red,(350,450,100,50))

    pygame.display.update()