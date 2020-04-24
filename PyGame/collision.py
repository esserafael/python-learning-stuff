import pygame
import time
import random

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

#def draw_block(block_x, block_y, block_width, block_height, color):
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
    
    main_form_x = round((display_width * 0.45))
    main_form_y = round((display_height * 0.8))
    main_form_width = 100 
    main_form_height = 100
    main_form_x_change = 0
    main_form_y_change = 0
    main_form_move_speed = 5

    #other_forms = []
    total_other_forms = 4
    other_forms_centersum = []

    #total_forms_generated = 0
    #while total_forms_generated < total_other_forms:
    #    other_forms.append(CreatedFormData("block_{}".format(total_forms_generated), random.randrange(0, display_width - 100), random.randrange(0, display_height - 100), 100, 100, black))
    #    total_forms_generated += 1

    main_block = FormData(
        "main_block", 
        FormDataPosition(main_form_x, main_form_y), 
        FormDataSize(main_form_width, main_form_height), 
        FormDataPosition(round(main_form_x + main_form_width / 2), round(main_form_y + main_form_height / 2)),
        red)

    other_forms = [
        (FormData(
            "block_{}".format(form),
            FormDataPosition(random.randrange(0, display_width - 100), random.randrange(0, display_height - 100)),
            FormDataSize(100, 100),
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

        #print(event)

        gameDisplay.fill(white)

        main_block.posbef = main_block.pos
        main_block.pos = FormDataPosition(main_block.pos.x + main_form_x_change, main_block.pos.y + main_form_y_change)

        #"""
        display_x_boundary = display_width - main_block.size.width
        display_y_boundary = display_height - main_block.size.height

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
                #other_forms_centersum.append(form.centersum)
                #print(form.centersum)
                draw_block(form)
                if (main_block.pos.x >= form.pos.x and 
                        main_block.pos.x <= form.pos.x + form.size.width -1 and 
                        main_block.pos.y >= form.pos.y and 
                        main_block.pos.y <= form.pos.y + form.size.height -1):
                        
                    if main_block.posbef.x >= form.pos.x + form.size.width:
                        print("Opax")
                        main_block.pos.x = form.pos.x + form.size.width
                    elif main_block.posbef.y >= form.pos.y + form.size.height:
                        print("Opay")
                        main_block.pos.y = form.pos.y + form.size.height
                
                if (main_block.pos.x <= form.pos.x and 
                        main_block.pos.x + main_block.size.width >= form.pos.x and 
                        main_block.pos.y <= form.pos.y and 
                        main_block.pos.y + main_block.size.height >= form.pos.y):
                    if main_block.posbef.x + main_block.size.width <= form.pos.x:
                        
                        main_block.pos.x = form.pos.x - main_block.size.width
                    if main_block.posbef.y + main_block.size.height >= form.pos.y:
                        
                        main_block.pos.y = form.pos.y - main_block.size.height
                    

        
        print("--")
        draw_block(main_block)

        pygame.display.update()
        clock.tick(clock_ticks)
        

game_loop()
pygame.quit()
quit()