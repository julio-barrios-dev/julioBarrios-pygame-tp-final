import pygame
from constantes import *
from auxiliar import Auxiliar
from bullet import Bullet
class Player:
    def __init__(self,x,y,speed_walk,speed_run ,jump_power,frame_rate_ms,move_rate_ms,jump_height,list_enemies,bullet_group,p_scale=1,interval_time_jump=100, gravity = GRAVITY) -> None:
        '''
        self.walk_r = Auxiliar.getSurfaceFromSpriteSheet("images/caracters/stink/walk.png",15,1,scale=p_scale)[:12]
        '''

        self.stay_r = Auxiliar.getSurfaceFromSpriteSheet("images/caracters/players/virtual-guy/Idle (32x32).png",11,1,flip=False,scale=p_scale)
        self.stay_l = Auxiliar.getSurfaceFromSpriteSheet("images/caracters/players/virtual-guy/Idle (32x32).png",11,1,flip=True,scale=p_scale)
        self.jump_r = Auxiliar.getSurfaceFromSpriteSheet("images/caracters/players/virtual-guy/Jump (32x32).png",1,1,flip=False,scale=p_scale)
        self.jump_l = Auxiliar.getSurfaceFromSpriteSheet("images/caracters/players/virtual-guy/Jump (32x32).png",1,1,flip=True,scale=p_scale)
        self.fall_r = Auxiliar.getSurfaceFromSpriteSheet("images/caracters/players/virtual-guy/Fall (32x32).png",1,1,flip=False,scale=p_scale)
        self.fall_l= Auxiliar.getSurfaceFromSpriteSheet("images/caracters/players/virtual-guy/Fall (32x32).png",1,1,flip=True,scale=p_scale)
        self.walk_r = Auxiliar.getSurfaceFromSpriteSheet("images/caracters/players/virtual-guy/Run (32x32).png",12,1,flip=False,scale=p_scale)
        self.walk_l = Auxiliar.getSurfaceFromSpriteSheet("images/caracters/players/virtual-guy/Run (32x32).png",12,1,flip=True,scale=p_scale)
        self.animation_list = [self.stay_r, self.walk_r, self.jump_r, self.fall_r]
        self.shoot_r = []
        self.shoot_l = []
        self.knife_r = []
        self.knife_l = []

        self.moving_left = False
        self.moving_right = False
        self.action = 0
        self.flip = False

        self.shoot_cooldown = 0
        self.bullet_group = bullet_group

        self.frame = 0
        self.lives = 5
        self.alive = True
        self.score = 0
        # self.move_x = 0
        # self.move_y = 0
        self.vel_y = 0
        self.speed_walk =  speed_walk
        self.speed_run =  speed_run
        self.gravity = gravity
        self.jump_power = jump_power
        self.animation = self.stay_r
        self.direction = DIRECTION_R
        self.image = self.animation_list[self.action][self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.collition_rect = pygame.Rect(x+self.rect.width/3,y,self.rect.width/3,self.rect.height)
        self.ground_collition_rect = pygame.Rect(self.collition_rect)
        self.ground_collition_rect.height = GROUND_COLLIDE_H
        self.ground_collition_rect.y = y + self.rect.height - GROUND_COLLIDE_H

        self.in_air = False
        self.is_jump = False
        self.jump = False
        self.is_fall = False
        self.is_shoot = False
        self.is_knife = False
        self.control_jump = True

        self.tiempo_transcurrido_animation = 0
        self.frame_rate_ms = frame_rate_ms 
        self.tiempo_transcurrido_move = 0
        self.move_rate_ms = move_rate_ms
        self.y_start_jump = 0
        self.jump_height = jump_height
        self.num_jump = 0

        self.tiempo_transcurrido = 0
        self.tiempo_last_jump = 0 # en base al tiempo transcurrido general
        self.interval_time_jump = interval_time_jump

        self.list_enemies = list_enemies.sprites()

    def move(self, delta_ms):
        move_x = 0
        move_y = 0

        self.tiempo_transcurrido_move += delta_ms
        if(self.tiempo_transcurrido_move >= self.move_rate_ms):
            self.tiempo_transcurrido_move = 0

            if self.moving_left:
                move_x = -self.speed_walk
                self.flip = True
                self.direction = DIRECTION_L
            
            if self.moving_right:
                move_x = self.speed_walk
                self.flip = False
                self.direction = DIRECTION_R
            
            if self.jump == True and self.in_air == False:
                self.vel_y = -self.jump_power
                self.jump = False
                self.in_air = True

            if self.jump == True and self.in_air == True and self.num_jump > 2:
                self.vel_y = -self.jump_power
                if (move_y >= 0):
                    self.num_jump = 0

            #check is fall
            if self.vel_y > 0 and self.in_air == True:
                self.is_fall = True 
            else: 
                self.is_fall = False 

            #Apply gravity
            self.vel_y += self.gravity
            if self.vel_y > 10:
                self.vel_y = 10
            move_y += self.vel_y

            #check collision with floor
            if self.rect.bottom + move_y > 300:
                move_y = 300 - self.rect.bottom
                self.in_air = False
            
            #update rectangle position
            self.change_x(move_x)
            self.change_y(move_y)

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 20
            bullet = Bullet(x_init=self.rect.centerx + (0.6 * self.rect.size[0] * self.direction),speed=25,path="./images/caracters/bullets/bullet.png",y_init=self.rect.centery,direction=self.direction,frame_rate_ms=80,move_rate_ms=100, bullet_group=self.bullet_group, list_enemies=self.list_enemies)
            self.bullet_group.add(bullet)

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            #update the animation settings
            self.frame = 0
            self.tiempo_transcurrido_animation = 0

    def do_animation(self,delta_ms):
        self.tiempo_transcurrido_animation += delta_ms
        self.image = self.animation_list[self.action][self.frame]

        if(self.tiempo_transcurrido_animation >= self.frame_rate_ms):
            self.tiempo_transcurrido_animation = 0
            if(self.frame < len(self.animation_list[self.action]) - 1):
                self.frame += 1 
            else: 
                self.frame = 0
                        
    def walk(self,direction):
        if(self.is_jump == False and self.is_fall == False):
            if(self.direction != direction or (self.animation != self.walk_r and self.animation != self.walk_l)):
                self.frame = 0
                self.direction = direction
                if(direction == DIRECTION_R):
                    self.move_x = self.speed_walk
                    self.animation = self.walk_r
                else:
                    self.move_x = -self.speed_walk
                    self.animation = self.walk_l

    def receive_shoot(self):
        self.lives -= 1

    def knife(self,on_off = True):
        self.is_knife = on_off
        if(on_off == True and self.is_jump == False and self.is_fall == False):
            if(self.animation != self.knife_r and self.animation != self.knife_l):
                self.frame = 0
                if(self.direction == DIRECTION_R):
                    self.animation = self.knife_r
                else:
                    self.animation = self.knife_l      

    # def jump(self,on_off = True):
    #     if(on_off and self.is_jump == False and self.is_fall == False):
    #         self.y_start_jump = self.rect.y
    #         if(self.direction == DIRECTION_R):
    #             self.move_x = int(self.move_x / 2)
    #             self.move_y = -self.jump_power
    #             self.animation = self.jump_r
    #         else:
    #             self.move_x = int(self.move_x / 2)
    #             self.move_y = -self.jump_power
    #             self.animation = self.jump_l
    #         self.frame = 0
    #         self.is_jump = True
    #     if(on_off == False):
    #         self.is_jump = False
    #         self.stay()

    def stay(self):
        if(self.animation != self.stay_r and self.animation != self.stay_l):
            if(self.direction == DIRECTION_R):
                self.animation = self.stay_r
            else:
                self.animation = self.stay_l
            self.move_x = 0
            self.move_y = 0
            self.frame = 0
        

    def fall(self):
        if(self.animation != self.fall_r and self.animation != self.fall_l):
            if(self.direction == DIRECTION_R):
                    self.animation = self.fall_r
            else:
                self.animation = self.fall_l
            self.frame = 0
            
    def change_x(self,delta_x):
        self.rect.x += delta_x
        self.collition_rect.x += delta_x
        self.ground_collition_rect.x += delta_x

    def change_y(self,delta_y):
        
        self.rect.y += delta_y
        self.collition_rect.y += delta_y
        self.ground_collition_rect.y += delta_y

    def do_movement(self,delta_ms,plataform_list):
        self.tiempo_transcurrido_move += delta_ms
        if(self.tiempo_transcurrido_move >= self.move_rate_ms):
            self.tiempo_transcurrido_move = 0

            if(abs(self.y_start_jump - self.rect.y) > self.jump_height and self.is_jump):
                self.move_y = 0
          
            self.change_x(self.move_x)
            self.change_y(self.move_y)

            if(not self.is_on_plataform(plataform_list)):
                if(self.move_y == 0):
                    self.is_fall = True
                    self.change_y(self.gravity)
            else:
                if (self.is_jump): 
                    self.jump(False)
                self.is_fall = False            

    def is_on_plataform(self,plataform_list):
        retorno = False
        
        if(self.ground_collition_rect.bottom >= GROUND_LEVEL):
            retorno = True     
        else:
            for plataforma in  plataform_list:
                if(self.ground_collition_rect.colliderect(plataforma.ground_collition_rect)):
                    retorno = True
                    break       
        return retorno                 
 
    def update(self,delta_ms):
        self.move(delta_ms)
        self.do_animation(delta_ms)
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        
    def draw(self,screen):
        
        if(DEBUG):
            pygame.draw.rect(screen,color=(255,0 ,0),rect=self.collition_rect)
            pygame.draw.rect(screen,color=(255,255,0),rect=self.ground_collition_rect)
        
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        

    def events(self,keys, delta_ms):
        self.tiempo_transcurrido += delta_ms

        if self.alive:
            if self.is_shoot:
                self.shoot()
            elif self.in_air and self.is_fall:
                self.update_action(3)#3: fall
            elif self.in_air:
                self.update_action(2)#2: jump
            elif self.moving_left or self.moving_right:
                self.update_action(1)#1: walk
            else:
                self.update_action(0)#0: idle

        #keyboard presses
        if keys[pygame.K_LEFT]:
            self.moving_left = True

        if keys[pygame.K_RIGHT]:
            self.moving_right = True 

        if keys[pygame.K_a]:
            self.is_shoot = True 

        if(keys[pygame.K_SPACE] and self.control_jump == True):
            self.jump = True
            self.control_jump = False
            self.num_jump += 1
            # self.tiempo_last_jump = self.tiempo_transcurrido 

        

        #keyboard button released
        if not keys[pygame.K_LEFT]:
            self.moving_left = False

        if not keys[pygame.K_RIGHT]:
            self.moving_right = False 

        if not keys[pygame.K_a]:
            self.is_shoot = False 

        if not keys[pygame.K_SPACE]:
            self.control_jump = True
