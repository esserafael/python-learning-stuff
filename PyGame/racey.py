import pygame
import time
import random

pygame.init()

# display
display_width = 1024
display_height = 768
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Relâmpago Marquinhos')

# colors
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

# car
carImg = pygame.image.load('racecar.png')
car_width = carImg.get_width()
car_height = carImg.get_height()

# boundaries
display_x_boundary = display_width - car_width
display_y_boundary = display_height - car_height

clock = pygame.time.Clock()

def car(x,y):
    gameDisplay.blit(carImg, (x,y))

def draw_block(block_x, block_y, block_width, block_height, color):
    pygame.draw.rect(gameDisplay, color, [block_x, block_y, block_width, block_height])
    
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',50)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (round(display_width/2),round(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

def explode():
    message_display('Explosion!')

def game_loop():

    car_x =  round((display_width * 0.45))
    car_y = round((display_height * 0.8))

    car_x_change = 0
    car_y_change = 0
    car_speed = 10

    block_width = 100
    block_height = 100
    block_x = random.randrange(0, display_width - block_width)
    block_y = -block_height
    block_speed = 7   

    gameExit = False
    crashed = False

    while not gameExit:

        gameDisplay.fill(white)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

            #print(event)
                
            ############################
            if not crashed:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        car_x_change = -car_speed
                    elif event.key == pygame.K_RIGHT:
                        car_x_change = car_speed
                    elif event.key == pygame.K_UP:
                        car_y_change = -car_speed
                    elif event.key == pygame.K_DOWN:
                        car_y_change = car_speed
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        car_x_change = 0
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        car_y_change = 0              
            #######################

        car_x += car_x_change
        car_y += car_y_change

        block_y += block_speed        

        if car_x > display_x_boundary:
            car_x = display_x_boundary
        elif car_x < 0:
            car_x = 0

        if car_y > display_y_boundary:
            car_y = display_y_boundary
        elif car_y < 0:
            car_y = 0

        if car_y < block_y + block_height and car_y > block_y:
            #print('y crossover')

            if car_x > block_x and car_x < block_x + block_width or car_x + car_width > block_x and car_x + car_width < block_x + block_width:
                #print('x crossover')

                car_y = block_y + block_height
                crashed = True
                
                if car_y >= display_y_boundary:
                  explode()
        
        if crashed:
            if car_x_change < 1 and car_x_change >= 0 or car_x_change <= 0 and car_x_change > -1:
                car_x_change = 0
                crashed = False

            car_x_change = car_x_change / 1.05
            car_y_change = round(car_speed / 1.1)
                

        print(car_x_change)
        print(car_speed)
           # print(car_y_change)

        car(car_x,car_y)
        draw_block(block_x, block_y, block_width, block_height, black)                

        #print("Blk X: {} - {}; Blk Y: {} - {}".format(block_x, (block_x + block_width), block_y, (block_y + block_height)))

        if block_y > display_height:
            block_y = 0 - block_height
            block_x = random.randrange(0, display_width - block_width)
                
        #print("Car X: {} - {}; Car Y: {} - {}".format(car_x, (car_x + car_width), car_y, (car_y + car_height)))
        #print(keys_disabled)

        pygame.display.update()
        clock.tick(60)

game_loop()
pygame.quit()
quit()