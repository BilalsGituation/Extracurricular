import pygame
from pygame.locals import *

BLACK = (0, 0, 0)
GREY = (127, 127, 127)
WHITE = (255, 255, 255)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

bg = GREY

key_dict = {K_k: BLACK,K_r:RED, K_g: GREEN, K_b: BLUE, K_y:YELLOW, K_c: CYAN, K_m:MAGENTA,K_e:GREY, K_w:WHITE}

colour_list = [BLACK,CYAN,GREEN,GREY,MAGENTA,RED,WHITE,YELLOW]

start = (0, 0)
size = (0, 0)
drawing = False

pygame.init()
screen = pygame.display.set_mode((640,240))
running = True
rect_list = []
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key in key_dict:
                bg = key_dict[event.key]
                caption = f'{bg=}'
                pygame.display.set_caption(caption)
        elif event.type == MOUSEBUTTONDOWN:
            start = event.pos
            size = 0, 0
            drawing = True
        elif event.type == MOUSEBUTTONUP:
            end = event.pos
            size = end[0] - start[0], end[1] - start[1]
            drawing = False
            rect = pygame.Rect(start, size)
            rect_list.append(rect)
        elif event.type == MOUSEMOTION and drawing:
            end = event.pos
            size = end[0] - start[0], end[1] - start[1]
    screen.fill(bg)
    col_ind = 0
    for rect in rect_list:
        if col_ind < len(colour_list)-1:
            col_ind+=1
        else:
            col_ind=0
        colour = colour_list[col_ind]
        pygame.draw.rect(screen, colour, rect, 3)

    pygame.draw.rect(screen, BLUE, (start, size), 1)
    pygame.display.update()

pygame.quit()
