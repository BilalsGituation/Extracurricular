import pygame
from pygame.locals import *

size = 640, 320
width, height = size
GREEN = (150, 255, 150)
RED = (255, 0, 0)


pygame.init()
screen = pygame.display.set_mode((size))
running = True

frog=pygame.image.load("frog.gif")
rect = frog.get_rect()
speed = [1,1]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    rect = rect.move(speed)
    if rect.left < 0 or rect.right > width:
        speed[0] = -speed[0]
    if rect.top < 0 or rect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(GREEN)
    pygame.draw.rect(screen, RED, rect, 1)
    screen.blit(frog, rect)

    pygame.display.update()

pygame.quit()
