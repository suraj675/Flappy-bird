import random  # for generating random numbers
import sys   # we will exit the program using sys.exit
import pygame
from pygame.locals import *   # basic pygame imports



#global variables for the game
FPS=45
SCREENWIDTH = 800
SCREENHEIGHT = 480
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.6
GAME_SPRITES={}
GAME_SOUNDS={}
PLAYER = 'gallery/sprites/player.png'
BACKGROUND = 'gallery/sprites/background.jpg'
PIPE = 'gallery/sprites/pipe.png'

def welcomeScreen():
    """
    Shows welcome image on the screen
    """
    playerx = int(SCREENWIDTH/4)
    playery = int(SCREENHEIGHT-GAME_SPRITES['player'].get_height())/2
    messagex = int(SCREENWIDTH-GAME_SPRITES['message'].get_width())/2
    messagey = int(SCREENHEIGHT*0.15)
    
    while True:
        for event in pygame.event.get():
            #if user clicks the cross button close the game
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()

            #if user presses space or up key start the game for them
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx,playery ))
                SCREEN.blit(GAME_SPRITES['message'], (messagex,messagey ))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    score=0
    playerx = int(SCREENWIDTH/6)
    playery = int(SCREENHEIGHT/2)

    #create 2 pipes for blitting on the screen
    newPipe1=getRandomPipe()
    newPipe2=getRandomPipe()

    #my list of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH +200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH +200 +(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
    ]

    #my list of lower pipes
    lowerPipes = [
         {'x': SCREENWIDTH +200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH +200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY= 10
    playerMinVelY= -8
    playerAccY= 1

    playerFlapAccv= -8 #velocity while flapping
    playerFlapped = False  # true only when the bird is flapping


    while True:
        for event in pygame.event.get():
            #if user clicks the cross button close the game
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()

    
            if event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                if playery> 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
        
        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)  #this function will return true if player is crashed
        if crashTest:
            return
        
        #check score
        playerMidPosition = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPosition=pipe['x']+GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPosition<= playerMidPosition <pipeMidPosition +4:
                score+=1
                print(f"Your score is {score}")

        if playerVelY< playerMaxVelY and not playerFlapped:
            playerVelY +=playerAccY

        if playerFlapped:
            playerFlapped= False
        playerHeight= GAME_SPRITES['player'].get_height()
        playery=playery + min(playerVelY, GROUNDY -playery -playerHeight)

        #move pipes to the left
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe+=pipeVelX
            lowerPipe+=pipeVelX
        #add a new pipe when first pipe is about to cross leftmost part of the screen
        if 0<upperPipes[o]['x']<5:
            newpipe= getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        #if pipe is out of the screen remove it
        if upperPipes[0]['x']< -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # let's blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigit=[int(x) for x in list(str(score))]
        width=0
        for digit in myDigit:
            width+= GAME_SPRITES['numbers'][digit].get_width()
        Xoffset= (SCREENWIDTH -width)/2

        for digit in myDigit:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12)) 
            Xoffset +=GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        


                




def getRandomPipe():
    """
    Generate positions of two pipes(one bottom straight and one top rotated) for blitting on the screen
    """
    pipeHeight=GAME_SPRITES['pipe'][0].get_height()
    offset=SCREENHEIGHT/3
    y2=offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2*offset))
    pipeX=SCREENWIDTH + 10
    y1=pipeHeight - y2 + offset
    pipe=[
        {'x': pipeX, 'y': -y1},  #upper pipe
        {'x': pipeX, 'y': y2}   #lower pipe
    ]
    return pipe 





if __name__ == "__main__":
    #this will be the main point where game will start
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy bird by Suraj')
    GAME_SPRITES['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    )
    GAME_SPRITES['message'] =pygame.image.load('gallery/sprites/message.png').convert_alpha(),
    GAME_SPRITES['pipe'] =(
        pygame.transform.rotate(pygame.image.load('gallery/sprites/pipe.png').convert_alpha(), 180),
        pygame.image.load('gallery/sprites/pipe.png').convert_alpha()
    )


    #game sounds
    GAME_SOUNDS['die'] =pygame.mixer.Sound('gallery/audio/die.mp3'),
    GAME_SOUNDS['hit'] =pygame.mixer.Sound('gallery/audio/hit.mp3')
    GAME_SOUNDS['acoustic'] =pygame.mixer.Sound('gallery/audio/acoustic.mp3')

    GAME_SPRITES['background'] =pygame.image.load('gallery/sprites/background.jpg').convert()
    GAME_SPRITES['player'] = pygame.image.load('gallery/sprites/player.png').convert_alpha()

    while True:
        welcomeScreen()    #shows welcome screen to the user till he presses the button
        mainGame()     # This is the main game function
    
    
    
