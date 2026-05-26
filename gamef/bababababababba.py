# holds code temporarily
# basically a clipboard

class projectile(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height,colour):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.vel = 3
        self.rect = pygame.Rect(x,y,width,height)
    def draw(self): 
        self.rect.topleft = (self.x,self.y)
        pygame.draw.rect(win,self.colour,self.rect)
    def shoot(self):
        while self.rect.colliderect(background_rect):
            if player.direction == 'left':
                self.x -= self.vel
                
            if player.direction == 'right':
                self.x += self.vel

            if player.direction == 'up':
                self.y -= self.vel

            if player.direction == 'down':
                self.y += self.vel

staff_shot = projectile(playerA.x,playerA.y,5,5,GREEN)

        self.direction = 'up'



                del coins_list[coins_list.index(coin)]

if shoot_button == True: 
        for bullet in staff_bullets: # drawing the bullets
            bullet.draw()
            if bullet.rect.colliderect(background_rect) == False:
                staff_bullets.pop(staff_bullets.index(bullet))


if shoot_button == True:
    shot = staff_bullets.min()
    shot.draw()
    if shot.rect.colliderect(background_rect) == False:
                staff_bullets.pop(staff_bullets.index(shot))


# attack
if keys[pygame.K_f] and staff_have: # make this so it starts a timer, then when the timer finishes and the key is released shoot
        staff_timer.tick() # timer
        if len(staff_bullets) <= 20: #max bullet count
            staff_bullets.append(
            projectile(round(playerA.x + playerA.width//2), round(playerA.y + playerA.height//2), 15, 15,
            playerA.direction, GREEN)) # reloads bullets

        
    if keys[pygame.K_f] == False and staff_timer.tick_busy_loop() >= 300: # allowing bullets to be shot
        shoot_button = True
        staff_timer.tick(0)

            
    if shoot_button == True: 
        for bullet in staff_bullets: # drawing the bullets
            bullet.draw()
            if bullet.rect.colliderect(background_rect) == False:
                staff_bullets.pop(staff_bullets.index(bullet))                

for coin in coins_list: # FOR COIN COLLECTION DO NOT DELETE 
        if coin.rect.colliderect(playerA.rect):
            score+=1
            coin.kill()
            del coins_list[coins_list.index(coin)]

# sword swing is 3 step process:
    # draw hitbox
    # check if hitbox is in contact with coins (enemies later)
    # if yes, collect coin *

# swing draws the sword, hitbox provides location data

# * need to have coins reference the player hitbox, not sure how
