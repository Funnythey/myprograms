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

# create cooldown for sword
# when swung, starts a cooldown timer (sword_cooldown)
# every frame after the first, it cools down (-=1) regardless of whether the button is held or not
# when cooldown timer reaches 0, can swing again

# how to keep sword swung for longer than 1 frame
# make the amount of time it's set to greater so there's longer until the cooldown reaches 5?
# swing; set cooldown to 10; cooldown ticks down until it's at 5; cooldown prevents sword from being drawn

#make a second timer
# if sword is being drawn, second timer ticks down
# when second timer is at 0, first timer ticks down
# when swung, second timer resets

# make it like the shoot_button variable
# press q, swing = True, then cooldown
# when cooldown == 0, swing = False and it stops swinging
# cooldown is 10, when reaches 5 or below swing = False & swing can only be turned back to True if cooldown = 0
if keys[pygame.K_q] and sword_have and sword_cooldown <= 0: # checks if able to swing
        sword_swing = True # swingability
        
        if playerA.direction == 'left':
            sword_hitbox = pygame.Rect(playerA.x-30,playerA.y+playerA.height//2, 40,20)
            sword_cooldown = 30
            
        if playerA.direction == 'right':
            sword_hitbox = pygame.Rect(playerA.x + playerA.width-10,playerA.y + playerA.height//2, 40,20)
            sword_cooldown = 30
            
        if playerA.direction == 'up':
            sword_hitbox = pygame.Rect(playerA.x,playerA.y-30, 20,40)
            sword_cooldown = 30
            
        if playerA.direction == 'down':
            sword_hitbox = pygame.Rect(playerA.x,playerA.y+playerA.height-10, 20,40)
            sword_cooldown = 30

    
            
    if sword_cooldown <= (sword_cooldown//2):
        sword_swing = False
            
    if sword_cooldown > 0:
        sword_cooldown -= 0.2

    if sword_swing == True:    
        playerA.swing(sword,sword_hitbox,BLUE)

        
        
    if keys[pygame.K_q] and sword_have and sword_cooldown <= 0: # checks if able to swing
        sword_swing = True # swingability
        sword_cooldown = 30
        
    if sword_swing == True:
        
        if playerA.direction == 'left': # determines the position & proportions of the hitbox
            sword_hitbox = pygame.Rect(playerA.x-30,playerA.y+playerA.height//2, 40,20)
                        
        if playerA.direction == 'right':
            sword_hitbox = pygame.Rect(playerA.x + playerA.width-10,playerA.y + playerA.height//2, 40,20)           
            
        if playerA.direction == 'up':
            sword_hitbox = pygame.Rect(playerA.x,playerA.y-30, 20,40)
            
        if playerA.direction == 'down':
            sword_hitbox = pygame.Rect(playerA.x,playerA.y+playerA.height-10, 20,40)
            
        playerA.swing(sword,sword_hitbox,BLUE)
        
            
    if sword_cooldown <= (sword_cooldown//2):
        sword_swing = False
        
    sword_cooldown -= 1

# CURRENT TASKS
# enemy changing player colour
# fixing coin collision
#


why do others change player colour
replicate results

border collision changes colour using timer
try that

use sword timer, less finicky


# give sword it's own class
    # can refer to it's own hitbox
    # can refer to it's own cooldown
    # can refer to it's own 'have'
    # can use symbol 

# bullet hitboxes are only being drawn on the player character
# do away with bullet hitboxes, just use projectile.rect

the rect needs to follow the bullet. When the bullet is drawn, the rect follows
when the bullet isnt drawn, the rect needs to stay out of bounds

enemy.collision(playerA,BLUE,staff_shot_big.rect,staff_damage)
enemy.collision(playerA,BLUE,staff_shot.rect,staff_damage*2)

enemies need to have random spawns within the background rect, regular width/height,
regular speed, random directional movement (up,down,left,right), reg colour, health, damage
needs random spawn and movement, thats it
(random.randint(border_thick,win_width - border_thick)), (random.randint(menu_thick,win_width - border_thick)),20,60,3,random.randint(1,4),PINK,10,0.5)


if len(enemy_list_spawns) <= 0:
        enemy_list_spawns.append(enemy((random.randint(border_thick,win_width - border_thick)), (random.randint(menu_thick,win_width - border_thick)),20,60,3,random.randint(1,4),PINK,10,0.5))

variables are fine, enemy object cant be called?

if len(enemy_list_spawns) <= 0:
        enemy_1234 = enemy((random.randint(border_thick,win_width - border_thick)),
                                       (random.randint(menu_thick,win_width - border_thick)),20,60,3,
                                        random.randint(1,4),PINK,10,0.5)
        enemy_list_spawns.append(enemy_1234)


if keys[pygame.K_f] == False and staff_timer >= 50: # allowing bullets to be shot
            shoot_button = True
            if len(staff_bullets) <= 20: #max bullet count
                
                staff_bullets.append(staff_shot_big) # adds a BIG bullet to the charge

# when an enemy dies, it is removed from the list.
# when the list is empty, it needs to be refilled.
# this should be the same as it is for the projectiles.
# figure out why it isnt

# works when using previously created objects (enemyA)
# randomize spawns & movements of enemies

# SO.
# enemy values randomized outside game loop aren't randomized every generation.
# Let's try to fix.
# enemy object can't be created inside game loop, says isnt callable.
# why

# using enemies init outside loop works but breaks it.
# invincible for last one killed, rest are flashy? flashing.
# even after adding them back, list still says empty
# why why why

change .x .y .direciton after they're initialized when readding hem

# enemy collision
        for enemy in enemy_list_spawns:
            enemy.collision(playerA,BLUE,sword_hitbox,sword_damage)
            
            if enemy.health <= 0:
                del enemy_list_spawns[enemy_list_spawns.index(enemy)] # if len(enemy_list_spawns) <= 0:

                spawn_range_x = list(range(50, 750))
                spawn_range_x.remove(range(playerA.x,playerA.width))

i = 0
while i < len(spawn_range_x):
    if spawn_range_x[i] >= playerA.x and spawn_range_x[i] <= (playerA.x + playerA.width):
        spawn_range_x.pop(i)
    i+=1

for i in spawn_range_x:
    if i >= playerA.x and i <= (playerA.x + playerA.width):
        spawn_range_x.pop(i)


# kill all enemies, respawns coins.

# when all enemies are dead, flag allows coins to respawn
# flag goes back down once list is full WRONG

# when all enemies die, triggers a flag
# flag sets coins_list_spawns to contain all of coins_list
# randomizes coin x/y values



# every 3 levels, adds another enemy & makes all enemies faster
# could draw additional enemies OOB until certain levels?
# only draw enemy_list_spawns[:enemy_spawn_limit]

# enemy_flag works, enemies keep being added since player level doesn't change
# when level == mult3, 

# make enemies outside spawnlimit have different x/y
# enemy difficulty scaling works, just need to make it work better
# every 3 levels, flag triggers. When all enemies die, checks flag.
# if flag is true, adds enemies, lowers flag

if timer > 0:
    counter is up
    timer -=1
