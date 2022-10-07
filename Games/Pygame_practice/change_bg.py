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

pygame.init()
screen = pygame.display.set_mode((640,240))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in key_dict:
                bg = key_dict[event.key]
                caption = f'{bg=}'
                pygame.display.set_caption(caption)
    screen.fill(bg)
    pygame.display.update()

pygame.quit()
