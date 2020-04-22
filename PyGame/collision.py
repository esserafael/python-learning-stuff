import pygame
import time
import random

class CreatedFormData:
    def __init__(self, name: str, x: int, y: int, width: int, height: int, color: str):
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
    return pygame.draw.rect(gameDisplay, color, [block_x, block_y, block_width, block_height])

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',50)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (round(display_width/2),round(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

def game_loop():
    gameExit = False
    
    form_x = round((display_width * 0.45))
    form_y = round((display_height * 0.8))
    form_x_change = 0
    form_y_change = 0
    form_move_speed = 10

    other_forms = []
    total_other_forms = 4

    total_forms_generated = 0

    while total_forms_generated < total_other_forms:
        other_forms.append(CreatedFormData("block_{}".format(total_forms_generated), random.randrange(0, display_width - 100), random.randrange(0, display_height - 100), 100, 100, black))
        total_forms_generated += 1

    print(other_forms)

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    form_x_change = -form_move_speed
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    form_x_change = form_move_speed
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    form_y_change = -form_move_speed
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    form_y_change = form_move_speed
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                    form_x_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                    form_y_change = 0 

        gameDisplay.fill(white)

        form_x += form_x_change
        form_y += form_y_change

        main_block = draw_block(form_x, form_y, 100, 100, red)

        if other_forms:
            for form in other_forms:
                draw_block(form.x, form.y, form.width, form.height, form.color)
        
        #print(blocks_generated)

        pygame.display.update()
        clock.tick(clock_ticks)
        

game_loop()
pygame.quit()
quit()