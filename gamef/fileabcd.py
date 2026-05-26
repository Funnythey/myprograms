import pygame

win_width = 800
win_height = 500
win = pygame.display.set_mode((win_width,win_height))

background = pygame.image.load("./images/dice.png") # CHECK WHEN YOU GET ERROR MESSAGES   
win.blit(background,(win_width,win_height)) #blits it onto the window
background_rect = background.get_rect()


class player:
    def __init__(self,x,y,width,height,colour): #for initializing the player
        self.x = x # player spawning x coord
        self.y = y # player spawning y coord
        self.width = width # width of player
        self.height = height # height of player
        self.colour = colour # colour of player
        self.vel = 3 # how fast the player moves
        self.direction = 'up'
        self.rect = pygame.Rect(x,y,width,height) #player rect or 'hitbox'
    def draw(self): # for drawing the player
        self.rect.topleft = (self.x,self.y)
        pygame.draw.rect(win,self.colour,self.rect)
    def swing(self,weapon,hitbox,colour):
        pygame.draw.rect(win,colour,hitbox)
    
    # every swing, create a hitbox in the direction player is facing 

class pickup(pygame.sprite.Sprite):
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


class border(pygame.sprite.Sprite):
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

class projectile(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height,direction,colour):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.vel = 6
        self.direction = direction
        self.rect = pygame.Rect(x,y,width,height)
    def draw(self): 
        self.rect.topleft = (self.x,self.y)
        pygame.draw.rect(win,self.colour,self.rect)
        
        if self.rect.colliderect(background_rect):
            if self.direction == 'left':
                self.x -= self.vel
                
            if self.direction == 'right':
                self.x += self.vel

            if self.direction == 'up':
                self.y -= self.vel

            if self.direction == 'down':
                self.y += self.vel
    
# set direction to player direction on init YES
# the bullet needs to spawn at the players CURRENT location, meaning
# the bullet's initial x/y values need to be updated every frame
 
# last direction moved determines shoot direction
# while projectile is colliding with background, WHILE self is on background
# depending on direction shot (if statement),
# continue moving in that direction
# if a thingy is shot,
# add a sprite to that group names projectile_+{i}
# i+=1
# shoot it
