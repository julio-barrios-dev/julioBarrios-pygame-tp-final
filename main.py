import pygame
from constantes import *
from player import Player

pygame.init()
screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("El mejor juego")
clock_fps = pygame.time.Clock()

background_image = pygame.image.load('./images/locations/set_bg_01/forest/all.png').convert_alpha()
background_image = pygame.transform.scale(background_image, (ANCHO_VENTANA, ALTO_VENTANA))
run = True;    

bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

player_1= Player(x=0,y=300, speed_walk=4, speed_run=8, jump_power=15, frame_rate_ms=60, move_rate_ms= 10, jump_height=100, p_scale=1, interval_time_jump=300, bullet_group=bullet_group, list_enemies=enemy_group) 

while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    delta_ms = clock_fps.tick(FPS)
    keys = pygame.key.get_pressed()
    screen.blit(background_image, background_image.get_rect())

    player_1.events(keys, delta_ms)
    player_1.update(delta_ms)
    player_1.draw(screen)

    #update and draw groups
    bullet_group.update()
    bullet_group.draw(screen)
    



    pygame.display.update()