"""
flappyLearn.py
Contributors: Josh, Anacan, Eric
Description: Uses the NEAT genetic algorithm to create a machine learning model of flappy bird
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
#here are all of the images that we use :)
images = [pygame.transform.scale2x(pygame.image.load(os.path.join("images","bird1.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("images","bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("images","bird3.png")))]
backgroundImage = pygame.transform.scale(pygame.image.load(os.path.join("images","bg.png")),(WINDOW_WIDTH,WINDOW_HEIGHT))
pipe_img = pygame.transform.scale2x(pygame.image.load(os.path.join("images","pipe.png")))
baseImage = pygame.transform.scale2x(pygame.image.load(os.path.join("images","base.png")).convert_alpha())
#######################
score = 0#this is a counter for how many time

font = pygame.font.Font(None, 32)
text = font.render(str(score), True, (255, 0, 0))

networks = [] #anacan, i use these heavily and want them to be global
gens = [] #although there probably was a better way to keep all the data
birds = [] #i wanted to use lists, mostly cause I'm comfortable with them 
#all of these are very closely related, every bird has an associated genome and theres network objects

 
class Bird:#anacan
    def __init__(self,y):
        self.x = 150  #initial x and y positions
        self.y = y
        self.animationCounter = 0
        self.animation = images[0]
        self.isAlive = True

 
    def flap(self):
        self.y -= 40
 
    def grav(self):
        self.y +=20
       
    
    def animate(self):
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
        self.vel = 20
 
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
    

#anacan
# def updateScore():
#     global score
#     word = "Score: " + str(score)
#     text = font.render(word, True, (255, 0, 0))
#     win.blit(text, (10,10))
#     pygame.display.update()

# def updateAlive():
#     global birds
#     word = "Birds Alive: " +str(len(birds))
#     text = font.render(word,True, (255,0,0))
#     win.blit(text, (10,40))
#     pygame.display.update()
#uncomment these two methods for a live, in-window display
#of both the score and how many birds are alive
#HOWEVER, it puts a lot of strain on the processor, cause 
#constantly blitting to the screen is heavy

 
def interaction(pipes, birds):
    #fundamentals made by josh, anacan cleaned the algorithm up to run
    #more ideally, as well as added functionality for the
    #NEAT algorithm
    global gens
    global networks
    global score

    pipes = pipes
    add_pipe = False
    for pipe in pipes:
        for count, bird in enumerate(birds):
            if (pipe.collide(bird, win) or bird.isOffScreen()):
                gens[count].fitness-=1
                birds.pop(count)
                networks.pop(count)
                gens.pop(count)
            
            #updateAlive()

            if ((not pipe.passed) and (pipe.x+pipe.pipeTop.get_width()) < bird.x):
                for g in gens:
                    g.fitness+=5 #if the bird gets through a pipe, increase its fitness
                pipe.passed = True
                pipes.append(Pipe(WINDOW_WIDTH))
                score+=1
                print(score, "score")
                
                
        pipe.drawPipe(win)
        pipe.move()
           
    if(pipes[0].passed and (pipes[0].x + pipe.pipeTop.get_width())<=0):
            pipes.remove(pipes[0])
            print(len(birds), "birds alive")
       
       

def draw(win,birds,pipes):
    #josh and anacan
    win.blit(backgroundImage, (0,0))
    for bird in birds:
        bird.animate()
        win.blit(bird.animation, (bird.x,bird.y))
    for pipe in pipes:
        pipe.drawPipe(win)
    #updateScore()
    pygame.display.update()


 

   
def main(genomes, config):
    #anacan
    global gens
    global networks
    global birds
    global score
    win.blit(backgroundImage, (0,0))
    pygame.display.flip()
    score = 0

    for genome_id, g in genomes:
        #anacan
        #the immediately below block is more specifics to setting up my NEAT model
        #initializes the a bunch of birds, each with 0 fitness
        #something confusing may be the fact that the birds themselves don't have a fitness property
        #however, the genomes themselves take care of this
        network = neat.nn.FeedForwardNetwork.create(g,config)
        networks.append(network)
        birds.append(Bird(150))
        g.fitness = 0
        gens.append(g)



    pipe = Pipe(WINDOW_WIDTH)
    pipes = [pipe]
    #this makes a list of pipes with 1 pipe in it to start,
    #don't worry, more are added and removed as needed

    runCondition = True 
    #if this is true, I run the main loop continuously
    #i have a fair amount of redundancy for quitting, just to make sure I can quit no matter what
    #don't want my machine learning algorithm running rogue!
    while(runCondition):
        #updateScore()
        #anacan
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #if you click the red 'X' in the pygame window, quit
                runCondition = False
                pygame.quit()
                break
        
        #this if statement below makes sure that the birds make calculations off of an upcoming pipe, not one that they've passed
        #this was an error that, before i added the below code, was a not fun error
        #anacan:)
        pipeCheck = 0
        if (len(birds)>0):
            if(len(pipes)>1 and ((pipes[0].x + pipes[0].pipeTop.get_width())<150)):
                pipeCheck = 1
        else:
            #if there are no more birds alive :(
            runCondition = False
            break
        
        
        
        for count, bird in enumerate(birds):
            #anacan
            gens[count].fitness += .1 #this gives the birds a smidge of fitness for just being alive still
            
            #absolute values are the bird's distance from top and bottom of the pipe
            out = networks[birds.index(bird)].activate((bird.y, abs(bird.y-pipes[pipeCheck].height), abs(bird.y-pipes[pipeCheck].bot)))
            #out is the output of the activation function tanh (range of -1, 1)
            if(out[0]>= 0.5): #if out is >=.5 then flap, otherwise fall
                bird.flap()
            else:
                bird.grav()
        #anacan    
        interaction(pipes,birds) #checks for collision between all the birds and pipes, does related stuff
        draw(win, birds, pipes) #draws the updated remaining birds and pipes
        


#anacan
#everything below is specific to setting up the NEAT model, pretty complicated and available in the docs
#the NEAT algorithm was very handy, and cool to work with
def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,neat.DefaultSpeciesSet, neat.DefaultStagnation,config_path)
    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats) 
    best = pop.run(main, 50)
    

if __name__ == "__main__": 
    #establishing path tp the configuration settings
    #which you can edit (Carefully, again, read docs!) in config.txt
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)