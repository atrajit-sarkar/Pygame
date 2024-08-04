import pygame
import random

pygame.init()

#colors
white=(255,255,255)
red=(255,0,0)
black=(0,0,0)

# Creating window
screen_width=900
half_screen_width=int(screen_width/2)
screen_height=600
half_screen_height=int(screen_height/2)
gameWindow=pygame.display.set_mode((screen_width,screen_height))

pygame.display.set_caption("SnakeWithFounder")
pygame.display.update()

#Game specific variables
exit_game=False
game_over=False
snake_x=45
snake_y=55
velocity_x=0
velocity_y=0
score=0
food_x=random.randint(20,half_screen_width)
food_y=random.randint(20,half_screen_height)
snake_size=20
fps=60
init_velocity=5

clock=pygame.time.Clock()
font=pygame.font.SysFont(None,30)

def text_screen(text,color,x,y):
    screen_text=font.render(text,True,color)
    gameWindow.blit(screen_text,[x,y])

def plot_snake(gameWindow,color,snk_list,snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow,color,[x,y,snake_size,snake_size])
snk_list=[]
snk_length=1   
#Game loop
while not exit_game:
    for event in pygame.event.get():
    # print(event)
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
    
    snake_x+=velocity_x
    snake_y+=velocity_y
    
    if abs(snake_x-food_x)<10 and abs(snake_y-food_y)<10:
        score+=1
        food_x=random.randint(20,half_screen_width)
        food_y=random.randint(20,half_screen_height)
        snk_length+=5
        # print("Score: ",score*10)
        
        
    gameWindow.fill(white)  
    text_screen(f"Score: {score*10}",red,5,5)
    pygame.draw.rect(gameWindow,red,[food_x,food_y,snake_size,snake_size])
    
    head=[]
    head.append(snake_x)
    head.append(snake_y)
    snk_list.append(head)
    
    if len(snk_list)>snk_length:
        del snk_list[0]
    
    plot_snake(gameWindow,black,snk_list,snake_size)
    pygame.display.update()
    clock.tick(fps)


pygame.quit()
quit()