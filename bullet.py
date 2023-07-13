from player import *
from constantes import *
from auxiliar import Auxiliar
import math

class Bullet(pygame.sprite.Sprite):
    
    def __init__(self,x_init,y_init,speed,path,direction,bullet_group,frame_rate_ms,move_rate_ms,width=5,height=5, list_enemies=[]) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.tiempo_transcurrido_move = 0
        self.tiempo_transcurrido_animation = 0
        # self.owner = owner
        self.list_enemies = list_enemies
        self.bullet_group = bullet_group;
        self.speed = speed
        self.direction = direction
        self.image = pygame.image.load(path).convert()
        self.image = pygame.transform.scale(self.image,(width,height))
        self.rect = self.image.get_rect()
        self.rect.center = (x_init, y_init)
        self.frame_rate_ms = frame_rate_ms
        self.move_rate_ms = move_rate_ms

    def update(self):
        #move bullet
        if self.direction == 0:
            self.direction = -1
        self.rect.x += (self.direction * self.speed)

        #check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left >  ANCHO_VENTANA:
            self.kill()
            print("Delte")
            
        for enemy in self.list_enemies:
            if self.rect.colliderect(enemy.collition_rect):
                if self.enemy.alive:
                    self.enemy.lives -= 1
                    self.kill()

