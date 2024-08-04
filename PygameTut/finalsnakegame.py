import pygame
import random
import os


pygame.mixer.init()

pygame.init()

#colors
white=(255,255,255)
red=(255,0,0)
black=(0,0,0)
head_color=(221,179,246)

# Creating window
screen_width=900
half_screen_width=int(screen_width/2)
screen_height=600
half_screen_height=int(screen_height/2)
gameWindow=pygame.display.set_mode((screen_width,screen_height))

# Background Image
bgimg=pygame.image.load("assets/background.jpg")
bgimg=pygame.transform.scale(bgimg,(screen_width,screen_height)).convert_alpha()
# Welcome Image
welcomeimg=pygame.image.load("assets/snake.webp")
welcomeimg=pygame.transform.scale(welcomeimg,(screen_width,screen_height)).convert_alpha()
# Gameove
gameoverimg=pygame.image.load('assets/gameover.jpg')
gameoverimg=pygame.transform.scale(gameoverimg,(screen_width,screen_height)).convert_alpha()

#Sounds
bgsound = pygame.mixer.Sound('assets/background.mp3')
foodeatsound = pygame.mixer.Sound('assets/foodeat.mp3')
# Get two channels
channel1 = pygame.mixer.Channel(0)
channel2 = pygame.mixer.Channel(1)

# Game Title
pygame.display.set_caption("SnakeWithFounder")
pygame.display.update()
clock=pygame.time.Clock()
score_font=pygame.font.SysFont(None,30)
gameover_font=pygame.font.SysFont(None,55)
welcome_font=pygame.font.SysFont(None,55)
GameOverAlert="Game Over!  Press Enter to Continue"

    
    
def text_screen(font,text,color,x,y):
    screen_text=font.render(text,True,color)
    gameWindow.blit(screen_text,[x,y])

def plot_snake(gameWindow,color1,color2,snk_list,snake_size):
    for x,y in snk_list[:-1]:
        pygame.draw.rect(gameWindow,color1,[x,y,snake_size,snake_size])
    
    pygame.draw.rect(gameWindow,color2,[snk_list[-1][0],snk_list[-1][1],snake_size,snake_size])
    
  
def welcome():
    global hiscore
    if not os.path.exists("hiscore.txt"):
        with open("hiscore.txt","w") as f:
            f.write("0")
    with open ("hiscore.txt","r") as f:
        hiscore=f.read()
    global exit_game
    exit_game=False
    pygame.mixer.music.load("assets/welcome.mp3")
    pygame.mixer.music.play()
    while not exit_game:
        gameWindow.fill(white)
        gameWindow.blit(welcomeimg,(0,0))
        text_screen(welcome_font,"Welcome to Snakes",white,300,50)
        text_screen(welcome_font,"Press SpaceBar To Play",white,260,100)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit_game=True
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    pygame.mixer.music.pause()
                    channel1.play(bgsound)
                    gameloop(int(hiscore))
        pygame.display.update()
        clock.tick(60)
#Game loop
def gameloop(hiscore):
    #Game specific variables
    exit_game=False
    game_over=False
    snake_x=45
    snake_y=55
    velocity_x=0
    velocity_y=0
    score=0
    snk_list=[]
    snk_length=1
    
    food_x=random.randint(20,half_screen_width)
    food_y=random.randint(20,half_screen_height)
    snake_size=20
    fps=60
    init_velocity=2
    increament=0

    
    while not exit_game:
        if game_over:
            gameWindow.fill(white)
            gameWindow.blit(gameoverimg,(0,0))
            text_screen(gameover_font,GameOverAlert,red,100,250)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    exit_game=True
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                        welcome()
        else:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    exit_game=True
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RIGHT:
                        velocity_x=init_velocity
                        velocity_y=0
                    if event.key==pygame.K_LEFT:
                        velocity_x=-init_velocity
                        velocity_y=0
                    if event.key==pygame.K_UP:
                        velocity_y=-init_velocity
                        velocity_x=0
                    if event.key==pygame.K_DOWN:
                        velocity_y=init_velocity
                        velocity_x=0
                    if event.key==pygame.K_q:
                        score+=10
            
            snake_x+=velocity_x
            snake_y+=velocity_y
            
            if abs(snake_x-food_x)<10 and abs(snake_y-food_y)<10:
                score+=10
                food_x=random.randint(20,half_screen_width)
                food_y=random.randint(20,half_screen_height)
                snk_length+=5
                init_velocity+=(0.1)*increament
                increament+=1
                channel2.play(foodeatsound)
                if score>hiscore:
                    hiscore=score
                    with open("hiscore.txt","w") as f:
                        f.write(str(hiscore))
                
                
            gameWindow.fill(white)
            gameWindow.blit(bgimg,(0,0))  
            text_screen(score_font,f"Score: {score}  HiScore: {hiscore}",white,5,5)
            pygame.draw.rect(gameWindow,red,[food_x,food_y,snake_size,snake_size])
            
            head=[]
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)
            
            if len(snk_list)>snk_length:
                del snk_list[0]
            
            if head in snk_list[:-1]:
                channel1.pause()
                channel2.pause()
                pygame.mixer.music.load('assets/gameover.wav')
                pygame.mixer.music.play()
                game_over=True
            if snake_x<3 or snake_x>screen_width-3 or snake_y<3 or snake_y>screen_height-3:
                channel1.pause()
                channel2.pause()
                pygame.mixer.music.load('assets/bigexplode.mp3')
                pygame.mixer.music.play()
                game_over=True
                
            plot_snake(gameWindow,white,head_color,snk_list,snake_size)
        pygame.display.update()
        clock.tick(fps)


    pygame.quit()
    quit()
    
welcome()    
