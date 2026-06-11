import pygame

win_width = 800
win_height = 500
win = pygame.display.set_mode((win_width,win_height))

background = pygame.image.load("./images/dice.png") # CHECK WHEN YOU GET ERROR MESSAGES   
win.blit(background,(win_width,win_height)) #blits it onto the window
background_rect = background.get_rect()


class player:
    def __init__(self,x,y,width,height,colour,level,health,health_max,damage): #for initializing the player
        self.x = x # player spawning x coord
        self.y = y # player spawning y coord
        self.width = width # width of player
        self.height = height # height of player
        self.colour = colour # colour of player
        self.vel = 3 # how fast the player moves
        self.direction = 'up'
        self.rect = pygame.Rect(x,y,width,height) #player rect or 'hitbox'

        self.level = level
        self.health = health
        self.health_max = health_max
        self.damage = damage + self.level
    def draw(self): # for drawing the player
        self.rect.topleft = (self.x,self.y)
        pygame.draw.rect(win,self.colour,self.rect)
    def swing(self,weapon,hitbox,colour):
        pygame.draw.rect(win,colour,hitbox)
    
    # every swing, create a hitbox in the direction player is facing 

class pickup(pygame.sprite.Group):
    def __init__(self,x,y,colour):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.colour = colour
        self.rect = pygame.Rect(x,y,self.width,self.height)
    def draw(self):
        self.rect.topleft = (self.x,self.y)
        pygame.draw.rect(win, self.colour, self.rect)


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
    def __init__(self,x,y,width,height,velocity,direction,colour,damage):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.velocity = velocity
        self.direction = direction
        self.rect = pygame.Rect(x,y,width,height)

        self.damage = damage
    def draw(self): 
        self.rect.topleft = (self.x,self.y)
        pygame.draw.rect(win,self.colour,self.rect)
        
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
    def __init__(self,x,y,width,height,velocity,direction,colour,health,health_max,damage):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = velocity
        self.hurt_velocity = velocity//1.3
        self.regular_velocity = velocity
        self.direction = direction
        self.colour = colour
        self.rect = pygame.Rect(x,y,width,height)

        self.health = health
        self.health_max = health_max
        self.damage = damage
    def draw(self,border_left,border_right,border_top,border_bottom):
        pygame.draw.rect(win,self.colour,self.rect)
        self.rect.topleft = (self.x,self.y)
        if self.rect.colliderect(border_right):
            self.direction = 1
        if self.rect.colliderect(border_left):
            self.direction = 2
        if self.rect.colliderect(border_top):
            self.direction = 4
        if self.rect.colliderect(border_bottom):
            self.direction = 3

        if self.rect.colliderect(background_rect):
            if self.direction == 1:
                self.x -= self.velocity 
            if self.direction == 2:
                self.x += self.velocity
            if self.direction == 3:
                self.y -= self.velocity
            if self.direction == 4:
                self.y += self.velocity
            if self.direction == 0:
                pass
                
    def collision(self,player,hurt_colour,weapon_hitbox,weapon_damage):
        if self.rect.colliderect(player.rect):
            player.colour = hurt_colour
            player.health -= self.damage
        if self.rect.colliderect(weapon_hitbox):
            self.health -= weapon_damage
            
            self.velocity = self.hurt_velocity
        else:
            self.velocity = self.regular_velocity
