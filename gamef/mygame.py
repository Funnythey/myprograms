import sys
import pygame
from fileabcd import *
import random
pygame.init()

# window + universal variables
win_width = 800
win_height = 500
win = pygame.display.set_mode((win_width,win_height))
pygame.display.set_caption("mygame")

border_thick = 15 # how large the borders are
menu_thick = border_thick * 6 # how large the menu is



RED = (255, 44, 0)
ORANGE = (255, 140, 0)
YELLOW = (242, 255, 0)
GREEN = (48, 252, 48)
BLUE = (0, 42, 255)
PURPLE = (79, 43, 117)
PINK = (255, 173, 225)
          
GOLD = (250,200,0)
BLACK = (0,0,0)
GREY = (100, 100, 100)

current_colour = RED

collision_timer = pygame.time.Clock()

# inventory
dead = False
health = 100
health_max = 100

score = 0
coins = 0
level = 0
levelup = 0.8

staff_have = False
sword_have = False

# Objects
playerA = player((win_width //2),((win_height + menu_thick) //2), 30,50, current_colour,
                 level, health, health_max, 1)

enemy_x = random.randint(50, 750)
enemy_y = random.randint(150,450)
spawn_range_x = list(range(40, 760))
spawn_range_y = list(range(140, 460))

i = 0
while i < len(spawn_range_x):
    if spawn_range_x[i] >= (playerA.x + 50) and spawn_range_x[i] <= ((playerA.x + 50)+ playerA.width):
        spawn_range_x.pop(i)
    i+=1

i = 0
while i < len(spawn_range_y):
    if spawn_range_y[i] >= (playerA.y + 50) and spawn_range_y[i] <= ((playerA.y + 50) + playerA.height):
        spawn_range_y.pop(i)
    i+=1

enemyA = enemy(random.randint(spawn_range_x[0],spawn_range_x[-1]),random.randint(spawn_range_y[0],spawn_range_y[-1]),40,80,2,random.randint(1,4),PURPLE,20,20,1)
enemyB = enemy(random.randint(spawn_range_x[0], spawn_range_x[-1]),random.randint(spawn_range_y[0],spawn_range_y[-1]),20,60,3,random.randint(1,4),PINK,10,10,0.5)
enemyC = enemy(random.randint(spawn_range_x[0],spawn_range_x[-1]),random.randint(spawn_range_y[0],spawn_range_y[-1]),20,60,3,random.randint(1,4),PINK,10,10,0.5)
enemyD = enemy(random.randint(spawn_range_x[0],spawn_range_x[-1]),random.randint(spawn_range_y[0],spawn_range_y[-1]),20,60,3,random.randint(1,4),PINK,10,10,0.5)
enemyE = enemy(random.randint(spawn_range_x[0],spawn_range_x[-1]),random.randint(spawn_range_y[0],spawn_range_y[-1]),20,60,3,random.randint(1,4),PURPLE,10,10,0.5)
enemyF = enemy(random.randint(spawn_range_x[0],spawn_range_x[-1]),random.randint(spawn_range_y[0],spawn_range_y[-1]),20,60,3,random.randint(1,4),ORANGE,10,10,0.5)

enemy_spawn_limit = 3
enemy_list = [enemyA,enemyB,enemyC,enemyD,enemyE,enemyF]
enemy_list_spawns = enemy_list
enemy_damage = 1
enemy_alive = len(enemy_list_spawns)

coin1 = pickup(random.randint(50, 750),random.randint(150,450),GOLD)
coin2 = pickup(random.randint(50, 750),random.randint(150,450),GOLD)
coins_list = [coin1,coin2]
coins_list_spawns = coins_list
coin_respawn = True

staff = pickup(140,200,GREEN)
staff_symbol = pickup(win_width - (border_thick*12),border_thick*2,GREEN)
staff_bullets = []
shoot_button = True
staff_timer = 0
staff_damage = 0.5 + playerA.damage

sword = pickup(390,450, BLUE)
sword_symbol = pickup(win_width - (border_thick*20),border_thick*2,BLUE)
sword_cooldown = 0
sword_swing = False
sword_hitbox = pygame.Rect(0,0,0,0)
sword_damage = 1 + playerA.damage

border_left = border(0,0,border_thick,win_height)
border_right = border(win_width - border_thick,0,border_thick,win_height)
border_top = border(0,0,win_width,border_thick)
border_bottom = border(0,win_height - 15,win_width,border_thick)

menuA = menu(border_thick,border_thick,win_width - (border_thick*2),menu_thick, PURPLE)

# Images
background = pygame.image.load("./images/dice.png") # CHECK WHEN YOU GET ERROR MESSAGES   
background = pygame.transform.scale(background, (win_width - border_thick, win_height - border_thick)) # sets it to the size of the window - borders

# Fonts
pygame.font.init()
menu_font = pygame.font.SysFont('Arial', 20)
dead_font = pygame.font.SysFont('Arial',150)

# note: initialize classes OUTSIDE loop or it will repeatedly initialize at the set location, making it unable to move
# im an idiot I FORGOT TO DO THE SAME FOR LISTS DONT FORGET TO DO THAT FOR LSITS TO


# -------------------------------------------------------------------------- #

# game loop
run = True
while run:
    
    FPS = 240
    clock = pygame.time.Clock()
    
    # window Colour
    win.fill((0,0,0))  # Fills the screen with black

    # inventory items 
    if score >= (levelup * 10):
        levelup+= levelup
        level+=1

    if playerA.health >= playerA.health_max:
        playerA.health = playerA.health_max
    
    if playerA.health <= 0:
        dead = True

    # map & object drawing
    background = pygame.image.load("./images/dice.png") # CHECK WHEN YOU GET ERROR MESSAGES   
    background = pygame.transform.scale(background, (win_width - border_thick, win_height - border_thick)) # sets it to the size of the window - borders
    background_rect = background.get_rect() # BACKGROUND MUST BE MADE INSIDE GAMEPLAY LOOP OR EVERYTHING BREAKS
    win.blit(background,(border_thick,menu_thick)) #blits it onto the window

    border_left.draw()
    border_right.draw()
    border_top.draw()
    border_bottom.draw()

    menuA.draw()

    playerA.draw()

    # enemies
    if playerA.level % 3 == 0:
        enemy_spawn_limit +=1
    
    if enemy_alive == 0:
        coin_respawn = True
        for enemy in enemy_list_spawns[:enemy_spawn_limit]:
            
            i = 0
            while i < len(spawn_range_x):
                if spawn_range_x[i] >= (playerA.x + 50) and spawn_range_x[i] <= ((playerA.x + 50)+ playerA.width):
                    spawn_range_x.pop(i)
                i+=1
           
            i = 0
            while i < len(spawn_range_y):
                if spawn_range_y[i] >= (playerA.y + 50) and spawn_range_y[i] <= ((playerA.y + 50) + playerA.height):
                    spawn_range_y.pop(i)
                i+=1
            i = 0
            
            enemy.x = random.randint(spawn_range_x[0],spawn_range_x[-1])
            enemy.y = random.randint(spawn_range_y[0],spawn_range_y[-1])
            enemy.direction = random.randint(1,4)
            enemy_alive +=1
            
    for enemy in enemy_list_spawns[:enemy_spawn_limit]:
        enemy.draw(border_left, border_right, menuA.rect, border_bottom)

    # pickups
    for coin in coins_list_spawns:
        if coin_respawn == True:   
            coin.x = random.randint(50,750)
            coin.y = random.randint(150,450)
    coin_respawn = False
    for coin in coins_list_spawns:
        coin.draw()     
            

    if staff_have == False:
        staff.draw()
    else:
        staff_symbol.draw()
        staff_counter = menu_font.render(f'staff {staff_timer}', False, GREEN)
        win.blit(staff_counter, (win_width - (border_thick*10),border_thick*2))
        bullet_counter = menu_font.render(f'ammo: {len(staff_bullets)}', False, GREEN)
        win.blit(bullet_counter, (win_width - (border_thick*10),border_thick*3))

    if sword_have == False:
        sword.draw()
    else:
        sword_symbol.draw()
        sword_counter = menu_font.render(f'sword', False, BLUE)
        win.blit(sword_counter, (win_width - (border_thick*18),border_thick*2))
        sword_cooldown_counter = menu_font.render(f'cooldown: {round(sword_cooldown)}', False, BLUE)
        win.blit(sword_cooldown_counter, (win_width - (border_thick*18),border_thick*3))

    # counters 
    health_counter = menu_font.render(f'Health: '+ str(playerA.health), False, (100,100,100))
    score_counter = menu_font.render(f'Score: '+ str(score), False, (100,100,100))
    coin_counter = menu_font.render(f'Coins: '+ str(coins), False, (100,100,100))
    level_counter = menu_font.render(f'Level: '+ str(level), False, (100,100,100))
    dead_counter = dead_font.render(f"YOU DIED", False, (100,100,100))

    win.blit(health_counter,(border_thick*2,border_thick * 2))
    win.blit(score_counter, (border_thick*2,border_thick * 3))
    win.blit(coin_counter, (border_thick*2,border_thick * 4))
    win.blit(level_counter, (border_thick*2,border_thick * 5))
    
    # collision items 
    for coin in coins_list_spawns: # FOR COIN COLLECTION DO NOT DELETE 
        if coin.rect.colliderect(playerA.rect):
            coins+=1
            playerA.health += 5
            coin.x = -50
            coin.y = -50

    if staff.rect.colliderect(playerA.rect):
        staff_have = True

    if sword.rect.colliderect(playerA.rect): 
        sword_have = True
        
    # border collision
    if playerA.rect.colliderect(border_left.rect):
        playerA.x += playerA.vel
        playerA.colour = BLUE
        collision_timer.tick()
    if playerA.rect.colliderect(border_left.rect) == False and collision_timer.tick_busy_loop() > 10:
        playerA.colour = RED
        collision_timer.tick(0)
        
    if playerA.rect.colliderect(border_right.rect):
        playerA.x -= playerA.vel
        playerA.colour = BLUE
        collision_timer.tick()
    if playerA.rect.colliderect(border_right.rect) == False and collision_timer.tick_busy_loop() > 20:
        playerA.colour = RED
        collision_timer.tick(0)
        
    if playerA.rect.colliderect(border_top.rect):
        playerA.y += playerA.vel
        playerA.colour = BLUE
    if playerA.rect.colliderect(border_top.rect) == False and collision_timer.tick_busy_loop() > 20:
        playerA.colour = RED
        collision_timer.tick(0)
        
    if playerA.rect.colliderect(border_bottom.rect):
        playerA.y -= playerA.vel
        playerA.colour = BLUE
    if playerA.rect.colliderect(border_bottom.rect) == False and collision_timer.tick_busy_loop() > 20:
        playerA.colour = RED
        collision_timer.tick(0)
    
    if playerA.rect.colliderect(menuA.rect):
        playerA.y += playerA.vel
        playerA.colour = BLUE
    if playerA.rect.colliderect(menuA.rect) == False and collision_timer.tick_busy_loop() > 20:
        playerA.colour = RED
        collision_timer.tick(0)
    

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if dead == False:
        
        # movement
        if keys[pygame.K_LEFT]:
            playerA.x -= playerA.vel
            playerA.direction = 'left'
            

        if keys[pygame.K_RIGHT]:
            playerA.x += playerA.vel
            playerA.direction = 'right'
            
        if keys[pygame.K_UP]:
            playerA.y -= playerA.vel
            playerA.direction = 'up'

        if keys[pygame.K_DOWN]:
            playerA.y += playerA.vel
            playerA.direction = 'down'

        # staff attack
        staff_shot_big = projectile(round(playerA.x + playerA.width//2), round(playerA.y + playerA.height//4),
                                    30, 30, 3, playerA.direction, GREEN, staff_damage * 2)
        staff_shot = projectile(round(playerA.x + playerA.width//2), round(playerA.y + playerA.height//2),
                                15, 15, 6, playerA.direction, GREEN, staff_damage)
                    
        if keys[pygame.K_f] and staff_have and staff_timer < 50: # make this so it starts a timer, then when the timer finishes and the key is released shoot
              staff_timer += 0.5 # charge-up shot

        if keys[pygame.K_f] == False and staff_timer < 20 and staff_timer > 0:
            staff_timer -= 1 # reduces charge of shot
            
        if keys[pygame.K_f] and staff_timer >= 20 and staff_timer % 2 == 0:
            playerA.colour = GREEN
        if keys[pygame.K_f] and staff_timer >= 20 and staff_timer % 10 != 0:
            playerA.colour = RED

        if keys[pygame.K_f] == False and staff_timer >= 50: # allowing bullets to be shot
            shoot_button = True
            if len(staff_bullets) <= 20: #max bullet count
                
                staff_bullets.append(staff_shot_big) # adds a BIG bullet to the charge
                                     
            staff_timer = 0
       
        elif keys[pygame.K_f] == False and staff_timer >= 20: # allowing bullets to be shot
            shoot_button = True
            
            if len(staff_bullets) <= 20: #max bullet count
                
                
                staff_bullets.append(staff_shot) # adds a regular bullet to the charge

            staff_timer = 0

        if shoot_button == True: 
            for bullet in staff_bullets: 
                bullet.draw() # drawing the bullets
                if bullet.rect.colliderect(background_rect) == False or len(staff_bullets) > 20:
                    staff_bullets.pop(staff_bullets.index(bullet))
                for enemy in enemy_list_spawns:
                    if bullet.rect.colliderect(enemy.rect):
                        enemy.collision(playerA,BLUE,bullet.rect,bullet.damage)
                        
            if len(staff_bullets)<=0:
                shoot_button = False
            
                   
        # sword attack
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
            
                
        if sword_cooldown <= 15:
            sword_swing = False
            sword_hitbox = pygame.Rect(0,0,0,0)
            
        if sword_cooldown > 0:   
            sword_cooldown -= 0.5

        # enemy collision
        for enemy in enemy_list_spawns:
            enemy.collision(playerA,BLUE,sword_hitbox,sword_damage)
            
            if enemy.health <= 0:
                enemy.x = -50
                enemy.y = -50
                enemy.direction = 0
                enemy_alive -=1
                enemy.health += enemy.health_max
                if enemy.health_max <= enemyB.health_max:
                    score+=3
                elif enemy.health_max <= enemyA.health_max:
                    score+=10
                elif enemy.health.max <= enemyF.health_max:
                    pass
                
        # changing colour
        if keys[pygame.K_1]:
            playerA.colour = RED
        if keys[pygame.K_2]:
            playerA.colour = ORANGE
        if keys[pygame.K_3]:
            playerA.colour = GOLD
        if keys[pygame.K_4]:
            playerA.colour = GREEN
        if keys[pygame.K_5]:
            playerA.colour = BLUE
        if keys[pygame.K_6]:
            playerA.colour = PURPLE
        if keys[pygame.K_7]:
            playerA.colour = PINK

    else:
        playerA.colour = GREY
        win.blit(dead_counter,(0,win_height//2))
    
    pygame.display.update()

pygame.quit()

# -------------------------------------------------------------------------- #

# it was that easy: 4

# current plan: figure out how to create different levels/screens/ROOMS & how to move between
# figure out how to make collectables (coins) that disappear when collected X
# make borders their own group so that different room borders are easier to make X
# make menu work right X
# make player.colour change when touching borders, USE A TIMER X
# put the different inits into a different file and import into this one to make things cleaner X
# give player a weapon (sword, bow/staff or smth) X
# figure out how to make projectiles X
# figure out how to make charged projectile maybe?idk X
# figure out how to flash green while staff is fully charged X
# figure out how to make a sword X
# give the sword a cooldown X
# make enemies FIRST THING GO DO THAT X
# make projectiles able to deal damage to enemies X
# use lists or however they do it to make an actual map
# make game into a class? not sure if needed
# figure out how pygame.sprite.Group works. This shouldnt be too hard
# difficulty scaling add more enemies at certain levels

# figured out how to properly blit & load images, how to print text,
#  what 'self' means (it's referring to the class object), and am trying to get the coints to work
# USE THIS vvvvvvvvv itll explain how classes work & how to call individual entities
# https://stackoverflow.com/questions/61689341/q-how-do-i-make-a-collecting-coin-for-my-platform-game
# COIN S FNH M
# FINALLY GOT THE COINS DONE
# putting things in classes, made coin deletion finally work thank god, now need to focus on making different rooms
# redid borders as a class
# got my first genuine crash, no errors thrown the game just didnt wanna do a while loop HA
# fixed border collision colour change issue, used the wrong function (get_time instead of tick_busy_loop)
# set up object classes in a different file & made em import right thx mr park
# got the pickup for weapons made
# FIGURE OUT WHY ITS GOING SO FAST, last I was working on projectiles, will try to remove & see what happens
# ^^^^^ compare mygame & test to see what the differences are
# the background. it was the background. why was it the background. moved these 3 down here.
# projectiles mostly work, need to make it so they can exist without holding f
# PROJECTILES WORK YIPPEEE just need to refine
# ^ add a delay between shots so theres no spam, maybe make it a charged shot?
# pygame.key.set_repeat() <<<<<< TRY THIS TRY THIS PLEASE
# YEEEEEEEESSSSSSS didnt need the repeating thing instead just figured it out HA
# got colour change working thank god ithought that would be so much harder than it was
# sword made yesterday forgot to add note at bottom here working on cooldown today
# proper cooldown done; sword can now be used to attack, stay on screen, then go on cooldown after
# got the staff able to do cool charge attack too now: if fully charged, shoots a big shot
# i may be an idiot, do more work on sprite groups
# work on health stuff & more enemy stuff, looking ok so far
# added death
# WORK ON ATTACK DAMAGE
# this game is breaking me slowly
# the number of times I've said 'it was that easy' while making this I'm gonna make a counter for it
# enemy not callable for some reason, fix later my back hurts
# ENEMIES NOW "RESPAWN" FINALLY, need to make it so the randrange doesnt include the player rect 
# randomized enemy spawn locations, added player levelling proper & adjusted damage so it scales with level
