"""
flappybird2.py
Contributors: Josh, Anacan, Eric
Description: User controlled flappy bird, use the up arrow key or space bar to flap
"""
import pygame
import neat
import os
import random
import time
#######################
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800
pygame.init()
win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
#######################
images = [pygame.transform.scale2x(pygame.image.load(os.path.join("images","bird1.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("images","bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("images","bird3.png")))]
backgroundImage = pygame.transform.scale(pygame.image.load(os.path.join("images","bg.png")),(WINDOW_WIDTH,WINDOW_HEIGHT))
pipe_img = pygame.transform.scale2x(pygame.image.load(os.path.join("images","pipe.png")))
baseImage = pygame.transform.scale2x(pygame.image.load(os.path.join("images","base.png")).convert_alpha())
#######################
score = 0 #this is a counter for how many times you pass through
font = pygame.font.Font(None, 32)
text = font.render(str(score), True, (255, 0, 0))


class Bird:#anacan
    def __init__(self,y):
        self.x = 150  #initial x and y positions
        self.y = y
        self.animationCounter = 0
        self.animation = images[0]
        self.isAlive = True

    def flap(self):
        self.y -= 10
    def grav(self):
        self.y +=5

    def ani(self):#these have two different names between the 2 files, don't know why i did that :/
        #anacan
        #changes the image that the bird object will currently display
        #which makes it look like it is flapping
        if(self.animationCounter == 0):
            self.animationCounter +=1
        elif(self.animationCounter == 1):
            self.animationCounter +=1
        elif(self.animationCounter == 2):
            self.animationCounter = 0
        self.animation = images[self.animationCounter]

    def isOffScreen(self):
        #anacan
        #returns true if the bird goes off the screen, false otherwise
        if(self.y<= 0 or self.y >= 760):
            return True
        else:
            return False

    def get_mask(self):
        #i think that josh  added this bit
        #if so, thanks josh<3
        return pygame.mask.from_surface(self.animation)


 
#makes Pipe class
#pipes are what are going to move, eventually will have variability in height
class Pipe:
    #space that will always be there for bird to go through
    #josh
    gap = 200
    def __init__(self, x):
        self.x = x
        self.height = 0
        self.vel = 5
        self.top = 0
        self.bot = 0
        self.pipeTop = pygame.transform.flip(pipe_img, False, True)
        self.pipeBot = pipe_img
        self.passed = False
        self.set_height()
    def set_height(self):
        self.height = random.randrange(50,450)
        self.top = self.height - self.pipeTop.get_height()
        self.bot = self.height + self.gap
    def move(self):
        self.x -= self.vel
        # if (self.x <= 0):
        #     self.x =800
    def drawPipe(self, win):
       win.blit(self.pipeTop, (self.x,self.top))
       win.blit(self.pipeBot, (self.x,self.bot))
    def collide(self, bird, win):
        #masks look at the pixels within the image and see if the pixels are touching
        birdMask = bird.get_mask()
        topPipeMask = pygame.mask.from_surface(self.pipeTop)
        botPipeMask = pygame.mask.from_surface(self.pipeBot)
        topOffset = (self.x - bird.x, self.top - round(bird.y))
        botOffset = (self.x - bird.x, self.bot - round(bird.y))
        bPoint = birdMask.overlap(botPipeMask, botOffset)
        tPoint = birdMask.overlap(topPipeMask, topOffset)
        if bPoint or tPoint:
            return True
        return False

def pipe_bird_interaction(pipes, bird):
    #fundamentals made by josh, anacan cleaned the algorithm up to run
    #more ideally
    pipes = pipes
    add_pipe = False
    for pipe in pipes:
        pipe.move()
        if pipe.collide(bird, win) or bird.isOffScreen():
            bird.isAlive = False
        if not pipe.passed and (pipe.x+pipe.pipeTop.get_width()) < bird.x:
            global score
            score +=1
            pipe.passed = True
            pipes.append(Pipe(WINDOW_WIDTH))
    if(pipes[0].passed and (pipes[0].x + pipe.pipeTop.get_width())<=0):
            pipes.remove(pipes[0])
 
#anacan
def updateScore():
    global score
    word = "Score: " + str(score)
    text = font.render(word, True, (255, 0, 0))
    win.blit(text, (10,10))
    pygame.display.flip()

#anacan and josh
def draw(win,bird,pipes):
    bird.ani()
    win.blit(backgroundImage, (0,0))
    win.blit(bird.animation, (bird.x,bird.y))
    for pipe in pipes:
        pipe.drawPipe(win)   
   
    updateScore()
    pygame.display.update()


def main():
    #josh and anacan
    updateScore()
    bird = Bird(150)

    pipe = Pipe(WINDOW_WIDTH)
    pipes = [pipe]

    runCondition = True
    while(runCondition):
        if(bird.isAlive):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    runCondition = False
                    pygame.quit()
                    break
            keys = pygame.key.get_pressed()
            if(keys[pygame.K_UP] or keys[pygame.K_SPACE]):
                bird.flap()
            else:
                bird.grav()
            #print(len(pipes))
            #koop.move()
            draw(win, bird, pipes)
            pipe_bird_interaction(pipes,bird)
        else:
            os.system('python driver.py')
            #runs the driver file again
            #not the cleanest, but gets the job done
            break
    win.blit(backgroundImage, (0,0))
    pygame.display.flip() #flip is similar to blit, i forget the precise difference
    pygame.time.delay(5000)#this makes a delay so that the window doesn't instantly close
    pygame.quit()
main()