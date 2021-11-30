                                    ##Flappy Bird Game##

import pygame
import sys, random


pygame.init()

score = 0


width = 300
height = 512
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Flappy Bird')

playerImg = pygame.image.load('images/bird.png')
backgroundImg = pygame.image.load('images/background.png')
baseImg = pygame.image.load('images/base.png')
pipeImg = pygame.image.load('images/pipe.png')


pipeDict = {'pipe': (pipeImg, pygame.transform.rotate(pipeImg, 180))}

playerX = 60
playerY = 220
baseX = 0
baseY = 400


def player():
    screen.blit(playerImg, (playerX, playerY))

def background():
    screen.blit(backgroundImg, (0, 0))

def base():
    screen.blit(baseImg, (baseX, baseY))

def welcome_message():
    font = pygame.font.SysFont('Courier', 24)
    text = font.render('Flappy Bird Game', True, (255,255,255))
    text1 = font.render('by Prakash Sakari', True, (255,255,255))
    text2 = font.render('Press Space to Play', True, (255,255,255))
    screen.blit(text, (30, 100))
    screen.blit(text1, (30, 134))
    screen.blit(text2, (15, 168))

def show_score():
    global score
    font = pygame.font.SysFont('calibri', 32)
    text = font.render(f'Score: {score}', True, (0, 0, 0))
    screen.blit(text, (100, 450))
    


def welcomeScreen():
    global playerX, playerY
    playerX = 60
    playerY = 220
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return None

            else:
                background()
                player()
                base()
                welcome_message()
                pygame.display.update()



def mainGame():
    global playerX, playerY, score
    playerX = 60
    playerY = 150
    playerYchange = 0

    pipe1 = getRandompipe()
    pipe2 = getRandompipe()

    upperPipes = [{'x': width + 200, 'y':pipe1[0]['y']},
                  {'x': width + 200 + (width/2), 'y':pipe2[0]['y']}]

    lowerPipes = [{'x': width + 200, 'y':pipe1[1]['y']},
                  {'x': width + 200 + (width/2), 'y':pipe2[1]['y']}]

    pipeXchange = -4

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if playerY > 0:
                        playerYchange = -7
                        wingSound = pygame.mixer.Sound('audio/wing.wav')
                        wingSound.play()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    playerYchange = 4
                    wingSound = pygame.mixer.Sound('audio/wing.wav')
                    wingSound.play()

        #Player Movement
        playerY = playerY + playerYchange

        #Checking if the bird touches the top or base of the screen
        if playerY <= 0 or playerY >= baseY - playerImg.get_height():
            score = 0
            hit_sound = pygame.mixer.Sound('audio/hit.wav')
            hit_sound.play()
            return None

        #Checking if the bird touches the upper pipe
        for upperPipe in upperPipes:
            pipe_height = pipeImg.get_height()
            if playerY < pipe_height + upperPipe['y'] and abs(playerX - upperPipe['x']) < pipeImg.get_width():
                score = 0
                hit_sound = pygame.mixer.Sound('audio/hit.wav')
                hit_sound.play()
                return None

        #Checking if bird touches the lower pipe
        for lowerPipe in lowerPipes:
            if playerY > lowerPipe['y'] and abs(playerX - lowerPipe['x']) < pipeImg.get_width(): 
                score = 0
                hit_sound = pygame.mixer.Sound('audio/hit.wav')
                hit_sound.play()
                return None

        #Check for score
        for upperPipe in upperPipes:
            if playerX > upperPipe['x'] and (playerX < upperPipe['x'] + 5):
                score += 1#score = score + 1
                point_sound = pygame.mixer.Sound('audio/point.wav')
                point_sound.play()
        

        #Moving the pipes to the left
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] = upperPipe['x'] + pipeXchange
            lowerPipe['x'] = lowerPipe['x'] + pipeXchange

        #if pipe moves out the screen remove the pipe
        if upperPipes[0]['x'] <= -pipeImg.get_width():
            #deleting items at index 0 from the list
            upperPipes.pop(0)
            lowerPipes.pop(0)

        #Adding a new pipe
        if upperPipes[0]['x'] > 0 and upperPipes[0]['x'] < 5:
            newPipe = getRandompipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])
            

        background()
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            screen.blit(pipeDict['pipe'][1], (upperPipe['x'], upperPipe['y']))
            screen.blit(pipeDict['pipe'][0], (lowerPipe['x'], lowerPipe['y']))
            
        base()
        player()
        show_score()
        pygame.display.update()
        pygame.time.delay(25)
        

def getRandompipe():
    global height, width
    offset = int(height/3)
    y2 = offset + random.randrange(0, (height - baseImg.get_height() - 1.2*offset))
    pipeHeight = pipeImg.get_height()
    y1 = pipeHeight - y2 + offset
    pipex = width + 10
    pipe = [{'x':pipex, 'y':-y1}, {'x':pipex, 'y':y2}]
    return pipe
    

#Main Loop
while True:
    welcomeScreen()
    mainGame()
