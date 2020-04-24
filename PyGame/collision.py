import pygame
import time
import random

class FormData:
    def __init__(self, name: str, x: int, y: int, width: int, height: int, color: tuple):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

pygame.init()

clock = pygame.time.Clock()

#fps
clock_ticks = 60

# display
display_width = 1024
display_height = 768
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Collision')

# colors
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

def draw_block(block_x, block_y, block_width, block_height, color):

    def message_display(text, size, x, y):
        largeText = pygame.font.Font('freesansbold.ttf',size)
        TextSurf, TextRect = text_objects(text, largeText)
        TextRect.center = x,y
        gameDisplay.blit(TextSurf, TextRect)

    block = pygame.draw.rect(gameDisplay, color, [block_x, block_y, block_width, block_height])

    block_center_x = round(block_x + block_width / 2)
    block_center_y = round(block_y + block_height / 2)

    message_display("x:{} y:{}".format(block_center_x, block_center_y), 12, block_center_x, block_center_y)

    return block

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

    pygame.display.update()

def game_loop():
    gameExit = False
    
    main_form_x = round((display_width * 0.45))
    main_form_y = round((display_height * 0.8))
    main_form_width = 100 
    main_form_height = 100
    main_form_x_change = 0
    main_form_y_change = 0
    main_form_move_speed = 10

    #other_forms = []
    total_other_forms = 4

    #total_forms_generated = 0
    #while total_forms_generated < total_other_forms:
    #    other_forms.append(CreatedFormData("block_{}".format(total_forms_generated), random.randrange(0, display_width - 100), random.randrange(0, display_height - 100), 100, 100, black))
    #    total_forms_generated += 1

    other_forms = [
        (FormData(
            "block_{}".format(form), 
            random.randrange(0, display_width - 100), 
            random.randrange(0, display_height - 100), 
            100, 
            100, 
            (
                random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)
            ))) 
            for form in range(total_other_forms)]

    #print(other_forms)

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    main_form_x_change = -main_form_move_speed
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    main_form_x_change = main_form_move_speed
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    main_form_y_change = -main_form_move_speed
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    main_form_y_change = main_form_move_speed
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                    main_form_x_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                    main_form_y_change = 0 

        gameDisplay.fill(white)

        main_form_x += main_form_x_change
        main_form_y += main_form_y_change

        #"""
        display_x_boundary = display_width - main_form_width
        display_y_boundary = display_height - main_form_height

        if main_form_x > display_x_boundary:
            main_form_x = display_x_boundary
        elif main_form_x < 0:
            main_form_x = 0

        if main_form_y > display_y_boundary:
            main_form_y = display_y_boundary
        elif main_form_y < 0:
            main_form_y = 0
        #"""

        main_block = draw_block(main_form_x, main_form_y, main_form_width, main_form_height, red)

        if other_forms:
            for form in other_forms:
                draw_block(form.x, form.y, form.width, form.height, form.color)
                
        
        #print(blocks_generated)

        pygame.display.update()
        clock.tick(clock_ticks)
        

game_loop()
pygame.quit()
quit()