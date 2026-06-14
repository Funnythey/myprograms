import pygame
import random

win_width = 800
win_height = 500
win = pygame.display.set_mode((win_width,win_height))

background = pygame.image.load("./images/dice.png") # CHECK WHEN YOU GET ERROR MESSAGES   
win.blit(background,(win_width,win_height)) #blits it onto the window
background_rect = background.get_rect()



class player:
    def __init__(self,x,y,width,height,image,coins,level,health,health_max,damage): #for initializing the player
        self.x = x # player spawning x coord
        self.y = y # player spawning y coord
        self.width = width # width of player
        self.height = height # height of player
        self.vel = 3 # how fast the player moves
        self.direction = 'up'
        self.rect = pygame.Rect(x,y,width-4,height-4) #player rect or 'hitbox'
        self.image = image
        self.image = pygame.transform.scale(image, (self.width, self.height))

        self.coins = coins
        self.level = level
        self.health = health
        self.health_max = health_max
        self.damage = damage + self.level
    def draw(self): # for drawing the player
        self.rect.topleft = (self.x,self.y)
        win.blit(self.image,self.rect.topleft)
    def swing(self,weapon,hitbox,colour):
        pygame.draw.rect(win,colour,hitbox)
    
    # every swing, create a hitbox in the direction player is facing 

class pickup(pygame.sprite.Group):
    def __init__(self,x,y,image):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.image = image
        self.image = pygame.transform.scale(image, (self.width, self.height))
        self.rect = pygame.Rect(x,y,self.width,self.height)
    def draw(self):
        self.rect.topleft = (self.x,self.y)
        win.blit(self.image,self.rect.topleft)
    def coin_collision(self,player):
        if player.rect.colliderect(self.rect):
            player.coins+=1
            player.health += 5
            self.x = -50
            self.y = -50
            

class border(pygame.sprite.Group):
    def __init__(self,x,y,width,height):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = (20,20,20)
        self.rect = pygame.Rect(x,y,width,height)
    def draw(self):
        self.rect.topleft = (self.x,self.y)
        pygame.draw.rect(win,self.colour,self.rect)
    
class menu(): 
    def __init__(self,x,y,width,height,colour):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.rect = pygame.Rect(x,y,width,height)
        self.surface = pygame.Surface((self.width,self.height))
        self.surface.fill(colour)
    def draw(self):
        self.rect.topleft = (self.x,self.y)
        pygame.draw.rect(win,self.colour,self.rect)

class projectile(pygame.sprite.Group):
    def __init__(self,x,y,width,height,velocity,direction,image,damage):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = velocity
        self.direction = direction
        self.image = image
        self.image = pygame.transform.scale(image, (self.width + 5, self.height + 5))
        self.rect = pygame.Rect(x,y,width,height)

        self.damage = damage
    def draw(self,image1,image2,timer): 
        self.rect.topleft = (self.x,self.y)
        win.blit(self.image,self.rect.topleft)
        image1 = pygame.transform.scale(image1, (self.width + 5, self.height + 5))
        image2 = pygame.transform.scale(image2, (self.width + 5, self.height + 5))
        timer.tick()
        
        if timer.tick_busy_loop() == 0:
            self.image = image1
            timer.tick()
        else:
            self.image = image2
            timer.tick(0)
        
        
        if self.rect.colliderect(background_rect):
            if self.direction == 'left':
                self.x -= self.velocity
                
            if self.direction == 'right':
                self.x += self.velocity

            if self.direction == 'up':
                self.y -= self.velocity

            if self.direction == 'down':
                self.y += self.velocity

class enemy(pygame.sprite.Group):
    def __init__(self,x,y,width,height,velocity,direction,image,health,health_max,damage):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = velocity
        self.hurt_velocity = velocity//1.3
        self.regular_velocity = velocity
        self.direction = direction
        self.image = image
        self.image = pygame.transform.scale(image, (self.width, self.height))
        self.rect = self.image.get_rect()

        self.health = health
        self.health_max = health_max
        self.damage = damage
    def draw(self,border_left,border_right,border_top,border_bottom,orange):
        self.rect.topleft = (self.x,self.y)
        win.blit(self.image,self.rect.topleft)

        if self.rect.colliderect(border_bottom) and self.image == orange:
            self.direction = random.choice((3,5,7))
        elif self.rect.colliderect(border_left) and self.direction == 1: # left
            self.direction = 2
        elif self.rect.colliderect(border_left) and self.direction == 5: # upleft 
            self.direction = 7
        elif self.rect.colliderect(border_left) and self.direction == 6: # downleft
            self.direction = 8
        

        if self.rect.colliderect(border_bottom) and self.image == orange:
            self.direction = random.choice((3,5,7))  
        elif self.rect.colliderect(border_right) and self.direction == 2:
            self.direction = 1
        elif self.rect.colliderect(border_right) and self.direction == 7: # upright
            self.direction = 5
        elif self.rect.colliderect(border_right) and self.direction == 8: # downright
            self.direction = 6

        if self.rect.colliderect(border_bottom) and self.image == orange:
            self.direction = random.choice((3,5,7))    
        elif self.rect.colliderect(border_top) and self.direction == 3:
            self.direction = 4
        elif self.rect.colliderect(border_top) and self.direction == 5: # upleft 
            self.direction = 6
        elif self.rect.colliderect(border_top) and self.direction == 7: # upright
            self.direction = 8
        

        if self.rect.colliderect(border_bottom) and self.image == orange:
            self.direction = random.choice((3,5,7)) 
        elif self.rect.colliderect(border_bottom) and self.direction == 4:
            self.direction = 3
        elif self.rect.colliderect(border_bottom) and self.direction == 6: # downleft 
            self.direction = 5
        elif self.rect.colliderect(border_bottom) and self.direction == 8: # downright
            self.direction = 7
        
        
            
        if self.rect.colliderect(background_rect):
            if self.direction == 1: # left
                self.x -= self.velocity 
            if self.direction == 2: # right
                self.x += self.velocity
            if self.direction == 3: # up
                self.y -= self.velocity
            if self.direction == 4: # down
                self.y += self.velocity
                
            if self.direction == 5: # left up
                self.x -= self.velocity 
                self.y -= self.velocity 
            if self.direction == 6: # left down
                self.x -= self.velocity
                self.y += self.velocity
            if self.direction == 7: #right up
                self.x += self.velocity
                self.y -= self.velocity
            if self.direction == 8: #right down
                self.x += self.velocity
                self.y += self.velocity
            if self.direction == 0: # no movement
                pass
                
    def collision(self,player,hurt_image,weapon_hitbox,weapon_damage):
        if self.rect.colliderect(player.rect):
            player.image = hurt_image
            player.health -= self.damage
        if self.rect.colliderect(weapon_hitbox):
            self.health -= weapon_damage
            
            self.velocity = self.hurt_velocity
        else:
            self.velocity = self.regular_velocity
