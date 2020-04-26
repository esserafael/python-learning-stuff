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
        self.poschange = FormDataPosition(0, 0)
        self.size = size
        self.center = pos.x + size.width / 2, pos.y + size.height / 2
        self.color = color
        self.centersum = center.x + center.y
        self.is_free_falling = True
           

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
    
    def text_objects(text, font):
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()

    def message_display(text, size, x, y):
        fontText = pygame.font.Font('freesansbold.ttf',size)
        TextSurf, TextRect = text_objects(text, fontText)
        TextRect.center = x,y
        gameDisplay.blit(TextSurf, TextRect)

    pygame.draw.rect(gameDisplay, block.color, [block.pos.x, block.pos.y, block.size.width, block.size.height])

    if CONFIG.SHOW_INFO_TEXT:
        message_display(block.name, 12, block.center.x, block.center.y - 15)
        message_display("x:{} y:{}".format(block.center.x, block.center.y), 12, block.center.x, block.center.y)

def detect_border_collision(block: FormData):

    display_x_boundary = CONFIG.DISPLAY_WIDTH - block.size.width
    display_y_boundary = CONFIG.DISPLAY_HEIGHT - block.size.height

    if block.pos.x > display_x_boundary:
        block.pos.x = display_x_boundary
    elif block.pos.x < 0:
        block.pos.x = 0

    if block.pos.y > display_y_boundary:            
        block.pos.y = display_y_boundary
        block.is_free_falling = False
    elif block.pos.y < 0:
        block.pos.y = 0

    return block

def detect_collision(block: FormData, otherblock: FormData):
    # southeast
    if (block.pos.x >= otherblock.pos.x and 
        block.pos.x <= otherblock.pos.x + otherblock.size.width -1 and 
        block.pos.y >= otherblock.pos.y and 
        block.pos.y <= otherblock.pos.y + otherblock.size.height -1):

        if block.posbef.x >= otherblock.pos.x + otherblock.size.width:
            #print("Opax")
            block.pos.x = otherblock.pos.x + otherblock.size.width
        elif block.posbef.y >= otherblock.pos.y + otherblock.size.height:
            #print("Opay")
            block.pos.y = otherblock.pos.y + otherblock.size.height
    
    # southwest
    if (block.pos.x <= otherblock.pos.x and 
        block.pos.x + block.size.width >= otherblock.pos.x +1 and 
        block.pos.y >= otherblock.pos.y and 
        block.pos.y <= otherblock.pos.y + otherblock.size.height -1):

        if block.posbef.x + block.size.width <= otherblock.pos.x:
            #print("Opax")
            block.pos.x = otherblock.pos.x - otherblock.size.width
        elif block.posbef.y >= otherblock.pos.y + otherblock.size.height:
            #print("Opay")
            block.pos.y = otherblock.pos.y + otherblock.size.height

    
    # northeast
    if (block.pos.x >= otherblock.pos.x and 
        block.pos.x <= otherblock.pos.x + otherblock.size.width -1 and 
        block.pos.y + block.size.height >= otherblock.pos.y +1 and 
        block.pos.y <= otherblock.pos.y):

        if block.posbef.x >= otherblock.pos.x + otherblock.size.width:
            #print("Opax")
            block.pos.x = otherblock.pos.x + otherblock.size.width
        elif block.posbef.y + block.size.height <= otherblock.pos.y + block.poschange.y + 1:
            #print("Opay")
            block.pos.y = otherblock.pos.y - block.size.height
            block.is_free_falling = False
        
    # northwest
    if (block.pos.x <= otherblock.pos.x and 
        block.pos.x + block.size.width >= otherblock.pos.x +1 and 
        block.pos.y + block.size.height >= otherblock.pos.y +1 and 
        block.pos.y <= otherblock.pos.y):

        if block.posbef.x + block.size.width <= otherblock.pos.x:
            #print("Opax")
            block.pos.x = otherblock.pos.x - otherblock.size.width
        elif block.posbef.y + block.size.height <= otherblock.pos.y + block.poschange.y + 1:
            #print("Opay")
            block.pos.y = otherblock.pos.y - block.size.height
            block.is_free_falling = False

    return block
    

def game_loop():
    gameExit = False

    main_block = FormData(
        "main_block", 
        FormDataPosition(round((CONFIG.DISPLAY_WIDTH * 0.45)), round((CONFIG.DISPLAY_HEIGHT * 0.1))), 
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
            for form in range(CONFIG.TOTAL_OTHER_FORMS)]
  

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    main_block.poschange.x = -CONFIG.MOVE_SPEED
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    main_block.poschange.x = CONFIG.MOVE_SPEED
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    main_block.poschange.y = -CONFIG.MOVE_SPEED
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    main_block.poschange.y = CONFIG.MOVE_SPEED
            if event.type == pygame.KEYUP:
                main_block.is_free_falling = True
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                    main_block.poschange.x = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                    main_block.poschange.y = 0

        #print(event)
        
        gameDisplay.fill(white)        

        if CONFIG.GRAVITY_ON and main_block.is_free_falling:
            main_block.poschange.y += CONFIG.GRAVITY_ACCEL / CONFIG.CLOCK_TICKS
            
        main_block.posbef = main_block.pos
        main_block.pos = FormDataPosition(main_block.pos.x + main_block.poschange.x, main_block.pos.y + main_block.poschange.y)

        main_block = detect_border_collision(main_block)

        main_block.center = FormDataPosition(round(main_block.pos.x + main_block.size.width / 2), round(main_block.pos.y + main_block.size.height / 2))
        main_block.centersum = main_block.center.x + main_block.center.y

        if other_forms:
            for form in other_forms:
                form.center = FormDataPosition(round(form.pos.x + form.size.width / 2), round(form.pos.y + form.size.height / 2))
                form.centersum = form.center.x + form.center.y

                if CONFIG.GRAVITY_ON and form.is_free_falling:
                    form.poschange.y += CONFIG.GRAVITY_ACCEL / CONFIG.CLOCK_TICKS
                
                form.pos.y += form.poschange.y

                form = detect_border_collision(form)
                main_block = detect_collision(main_block, form)
                
                draw_block(form)

        draw_block(main_block)
        
        pygame.display.update()        
        clock.tick(CONFIG.CLOCK_TICKS)

        print(clock.get_rawtime()) 
        print("--")        

game_loop()
pygame.quit()
quit()