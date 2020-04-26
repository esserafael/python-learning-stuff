import pygame
import time
import random
from collision_config import DefaultConfig

CONFIG = DefaultConfig()

class FormDataPosition:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class FormDataSize:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height


class FormData:
    def __init__(self, name: str, pos: FormDataPosition, size: FormDataSize, center: FormDataPosition, color: tuple):
        self.name = name
        self.pos = pos
        self.posbef = FormDataPosition(pos.x, pos.y)
        self.size = size
        self.center = pos.x + size.width / 2, pos.y + size.height / 2
        self.color = color
        self.centersum = center.x + center.y
           

pygame.init()

clock = pygame.time.Clock()

# Display
gameDisplay = pygame.display.set_mode((CONFIG.DISPLAY_WIDTH, CONFIG.DISPLAY_HEIGHT))
pygame.display.set_caption('Collision')

# Colors
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

def draw_block(block: FormData):

    def message_display(text, size, x, y):
        largeText = pygame.font.Font('freesansbold.ttf',size)
        TextSurf, TextRect = text_objects(text, largeText)
        TextRect.center = x,y
        gameDisplay.blit(TextSurf, TextRect)

    pygame.draw.rect(gameDisplay, block.color, [block.pos.x, block.pos.y, block.size.width, block.size.height])

    message_display(block.name, 12, block.center.x, block.center.y - 15)
    message_display("x:{} y:{}".format(block.center.x, block.center.y), 12, block.center.x, block.center.y)

    return

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

    pygame.display.update()

def game_loop():
    gameExit = False
    
    main_form_x_change = 0
    main_form_y_change = 0

    total_other_forms = 4

    main_block = FormData(
        "main_block", 
        FormDataPosition(round((CONFIG.DISPLAY_WIDTH * 0.45)), round((CONFIG.DISPLAY_HEIGHT * 0.8))), 
        FormDataSize(CONFIG.SIZE_WIDTH, CONFIG.SIZE_HEIGHT), 
        FormDataPosition(0, 0),
        red)

    other_forms = [
        (FormData(
            "block_{}".format(form),
            FormDataPosition(random.randrange(0, CONFIG.DISPLAY_WIDTH - CONFIG.SIZE_WIDTH), random.randrange(0, CONFIG.DISPLAY_HEIGHT - CONFIG.SIZE_HEIGHT)),
            FormDataSize(CONFIG.SIZE_WIDTH, CONFIG.SIZE_HEIGHT),
            FormDataPosition(0, 0),
            (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
            )) 
            for form in range(total_other_forms)]

  

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    main_form_x_change = -CONFIG.MOVE_SPEED
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    main_form_x_change = CONFIG.MOVE_SPEED
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    main_form_y_change = -CONFIG.MOVE_SPEED
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    main_form_y_change = CONFIG.MOVE_SPEED
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                    main_form_x_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                    main_form_y_change = 0

        #print(event)

        gameDisplay.fill(white)

        main_block.posbef = main_block.pos
        main_block.pos = FormDataPosition(main_block.pos.x + main_form_x_change, main_block.pos.y + main_form_y_change)

        #"""
        display_x_boundary = CONFIG.DISPLAY_WIDTH - main_block.size.width
        display_y_boundary = CONFIG.DISPLAY_HEIGHT - main_block.size.height

        if main_block.pos.x > display_x_boundary:
            main_block.pos.x = display_x_boundary
        elif main_block.pos.x < 0:
            main_block.pos.x = 0

        if main_block.pos.y > display_y_boundary:
            main_block.pos.y = display_y_boundary
        elif main_block.pos.y < 0:
            main_block.pos.y = 0
        #"""

        main_block.center = FormDataPosition(round(main_block.pos.x + main_block.size.width / 2), round(main_block.pos.y + main_block.size.height / 2))
        main_block.centersum = main_block.center.x + main_block.center.y

        if other_forms:
            for form in other_forms:
                form.center = FormDataPosition(round(form.pos.x + form.size.width / 2), round(form.pos.y + form.size.height / 2))
                form.centersum = form.center.x + form.center.y
                draw_block(form)
                # southeast
                if (main_block.pos.x >= form.pos.x and 
                    main_block.pos.x <= form.pos.x + form.size.width -1 and 
                    main_block.pos.y >= form.pos.y and 
                    main_block.pos.y <= form.pos.y + form.size.height -1):

                    if main_block.posbef.x >= form.pos.x + form.size.width:
                        #print("Opax")
                        main_block.pos.x = form.pos.x + form.size.width
                    elif main_block.posbef.y >= form.pos.y + form.size.height:
                        #print("Opay")
                        main_block.pos.y = form.pos.y + form.size.height
                
                # southwest
                if (main_block.pos.x <= form.pos.x and 
                    main_block.pos.x + main_block.size.width >= form.pos.x +1 and 
                    main_block.pos.y >= form.pos.y and 
                    main_block.pos.y <= form.pos.y + form.size.height -1):

                    if main_block.posbef.x + main_block.size.width <= form.pos.x:
                        #print("Opax")
                        main_block.pos.x = form.pos.x - form.size.width
                    elif main_block.posbef.y >= form.pos.y + form.size.height:
                        #print("Opay")
                        main_block.pos.y = form.pos.y + form.size.height

                
                # northeast
                if (main_block.pos.x >= form.pos.x and 
                    main_block.pos.x <= form.pos.x + form.size.width -1 and 
                    main_block.pos.y + main_block.size.height >= form.pos.y +1 and 
                    main_block.pos.y <= form.pos.y):

                    print(main_block.pos.y)
                    print(form.pos.y +1)

                    if main_block.posbef.x >= form.pos.x + form.size.width:
                        #print("Opax")
                        main_block.pos.x = form.pos.x + form.size.width
                    elif main_block.posbef.y + main_block.size.height <= form.pos.y:
                        #print("Opay")
                        main_block.pos.y = form.pos.y - main_block.size.height
                    
                # northwest
                if (main_block.pos.x <= form.pos.x and 
                    main_block.pos.x + main_block.size.width >= form.pos.x +1 and 
                    main_block.pos.y + main_block.size.height >= form.pos.y +1 and 
                    main_block.pos.y <= form.pos.y):

                    if main_block.posbef.x + main_block.size.width <= form.pos.x:
                        #print("Opax")
                        main_block.pos.x = form.pos.x - form.size.width
                    elif main_block.posbef.y + main_block.size.height <= form.pos.y:
                        #print("Opay")
                        main_block.pos.y = form.pos.y - main_block.size.height

        
        print("--")
        draw_block(main_block)

        pygame.display.update()
        clock.tick(CONFIG.CLOCK_TICKS)
        

game_loop()
pygame.quit()
quit()