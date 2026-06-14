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

collision_timer = pygame.time.Clock()
coinage_timer = pygame.time.Clock()
staff_animation_timer = pygame.time.Clock()

# inventory
dead = False
health = 100
health_max = 100

score = 0
coins = 0
level = 0
levelup = 0.1

staff_have = False
sword_have = False

# Images
background = pygame.image.load("./images/dice.png") # CHECK WHEN YOU GET ERROR MESSAGES   
background = pygame.transform.scale(background, (win_width - border_thick, win_height - border_thick)) # sets it to the size of the window - borders
background_rect = background.get_rect() # BACKGROUND MUST BE MADE INSIDE GAMEPLAY LOOP OR EVERYTHING BREAKS

ballthey_reg = pygame.image.load("./images/ballthey.png")
ballthey_sad = pygame.image.load("./images/ballthey_sad.png")
ballthey_coinage = pygame.image.load("./images/ballthey_coinage.png")
ballthey_charge1= pygame.image.load("./images/ballthey_charge1.png")
ballthey_charge2 = pygame.image.load("./images/ballthey_charge2.png")
ballthey_dead = pygame.image.load("./images/ballthey_dead.png")

enemy_pink = pygame.image.load("./images/dapink.png")
enemy_purple = pygame.image.load("./images/Rectangledude.png")
enemy_orange = pygame.image.load("./images/orang.png")

staff_idle = pygame.image.load("./images/ballgal_idle.png")
staff_bullet_image1 = pygame.image.load("./images/ballgal1.png")
staff_bullet_image2 = pygame.image.load("./images/ballgal2.png")

sword_image = pygame.image.load("./images/ballblade.png")

# Fonts
pygame.font.init()
menu_font = pygame.font.SysFont('Arial', 20)
difficulty_font = pygame.font.SysFont('Arial', 70)
dead_font = pygame.font.SysFont('Arial',150)


# Objects

# player
playerA = player((win_width //2),((win_height + menu_thick) //2), 50,50,
                 ballthey_reg, coins, level, health, health_max, 1)

# enemies
enemy_x = random.randint(50, 750)
enemy_y = random.randint(150,450)
spawn_range_x = list(range(40, 760))
spawn_range_y = list(range(140, 460))

i = 0
while i < len(spawn_range_x):
    if spawn_range_x[i] >= (playerA.x + 100) and spawn_range_x[i] <= ((playerA.x + 100)+ playerA.width):
        spawn_range_x.pop(i)
    i+=1

i = 0
while i < len(spawn_range_y):
    if spawn_range_y[i] >= (playerA.y + 100) and spawn_range_y[i] <= ((playerA.y + 100) + playerA.height):
        spawn_range_y.pop(i)
    i+=1

enemyA = enemy(random.randint(spawn_range_x[0],spawn_range_x[-1]),random.randint(spawn_range_y[0],spawn_range_y[-1]),40,80,2,random.randint(1,8),enemy_purple,20,20,1)
enemyB = enemy(random.randint(spawn_range_x[0], spawn_range_x[-1]),random.randint(spawn_range_y[0],spawn_range_y[-1]),20,60,3,random.randint(1,8),enemy_pink,15,15,0.5)
enemyC = enemy(random.randint(spawn_range_x[0],spawn_range_x[-1]),random.randint(spawn_range_y[0],spawn_range_y[-1]),20,60,3,random.randint(1,8),enemy_pink,15,15,0.5)
enemyD = enemy(-50,-50,20,60,3,random.randint(1,8),enemy_pink,15,15,0.5)
enemyE = enemy(-50,-50,40,80,1.5,random.randint(1,8),enemy_purple,20,20,1)
enemyF = enemy(-50,-50,30,80,6,random.randint(1,8),enemy_orange,30,30,0.5)

enemy_spawn_limit = 3
enemy_list = [enemyA,enemyB,enemyC,enemyD,enemyE,enemyF]
enemy_list_spawns = enemy_list
enemy_damage = 1
enemy_alive = len(enemy_list_spawns) - enemy_spawn_limit
enemy_flag = False
difficulty_timer = 0

# pickups
coin1 = pickup(random.randint(50, 750),random.randint(150,450),ballthey_coinage)
coin2 = pickup(random.randint(50, 750),random.randint(150,450),ballthey_coinage)
coins_list = [coin1,coin2]
coins_list_spawns = coins_list
coin_respawn = True

staff = pickup(140,200,staff_idle)
staff_symbol = pickup(win_width - (border_thick*12),border_thick*2,staff_idle)
staff_bullets = []
shoot_button = True
staff_timer = 0
staff_damage = 0.5 + playerA.damage

sword = pickup(390,450, sword_image)
sword_symbol = pickup(win_width - (border_thick*20),border_thick*2,sword_image)
sword_cooldown = 0
sword_swing = False
sword_hitbox = pygame.Rect(0,0,0,0)
sword_damage = 1 + playerA.damage

border_left = border(0,0,border_thick,win_height)
border_right = border(win_width - border_thick,0,border_thick,win_height)
border_top = border(0,0,win_width,border_thick)
border_bottom = border(0,win_height - 15,win_width,border_thick)

menuA = menu(border_thick,border_thick,win_width - (border_thick*2),menu_thick, PURPLE)



# note: initialize classes OUTSIDE loop or it will repeatedly initialize at the set location, making it unable to move
# im an idiot I FORGOT TO DO THE SAME FOR LISTS DONT FORGET TO DO THAT FOR LSITS TO


# -------------------------------------------------------------------------- #

# game loop
run = True
while run:
    
    FPS = 120
    clock = pygame.time.Clock()
    clock.tick(FPS)
    
    # window Colour
    win.fill((0,0,0))  # Fills the screen with black

    # inventory items 
    if score >= (levelup * 10): # level up
        levelup+= 5 # level up rate (nonlinear)
        playerA.level+=1
        if playerA.level % 3 == 0:
            enemy_flag = True # allows enemy_spawn_limit to increase
        print(enemy_flag)
    
    if playerA.health >= playerA.health_max:
        playerA.health = playerA.health_max
    
    if playerA.health <= 0:
        dead = True

    # map & object drawing
    win.blit(background,(border_thick,menu_thick)) #blits it onto the window

    border_left.draw()
    border_right.draw()
    border_top.draw()
    border_bottom.draw()

    menuA.draw()

    playerA.draw()

    # enemies
    if enemy_flag and enemy_alive == 0:
        print('difficulty up', enemy_flag)
        difficulty_timer += 100
        enemy_spawn_limit +=1
        enemy_flag = False
    if enemy_alive == 0:
        coin_respawn = True # allows coins to randomize position/respawn
        
        print('test', enemy_spawn_limit)
        for enemy in enemy_list_spawns[:enemy_spawn_limit]:
            
            i = 0
            while i < len(spawn_range_x):
                if spawn_range_x[i] >= (playerA.x - 20) and spawn_range_x[i] <= ((playerA.x + 20)+ playerA.width):
                    spawn_range_x.pop(i)
                i+=1
           
            i = 0
            while i < len(spawn_range_y):
                if spawn_range_y[i] >= (playerA.y - 20) and spawn_range_y[i] <= ((playerA.y + 20) + playerA.height):
                    spawn_range_y.pop(i)
                i+=1
            i = 0
            
            enemy.x = random.randint(spawn_range_x[0],spawn_range_x[-1])
            enemy.y = random.randint(spawn_range_y[0],spawn_range_y[-1])
            enemy.direction = random.randint(1,8)
            enemy_alive +=1
            
    for enemy in enemy_list_spawns[:enemy_spawn_limit]:
        enemy.draw(border_left, border_right, menuA.rect, border_bottom,enemy_orange)

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
    coin_counter = menu_font.render(f'Coins: '+ str(playerA.coins), False, (100,100,100))
    level_counter = menu_font.render(f'Level: '+ str(playerA.level), False, (100,100,100))
    difficulty_counter = difficulty_font.render(f'Difficulty Up', False, (100,100,100))
    dead_counter = dead_font.render(f"YOU DIED", False, (100,100,100))

    win.blit(health_counter,(border_thick*2,border_thick * 2))
    win.blit(score_counter, (border_thick*2,border_thick * 3))
    win.blit(coin_counter, (border_thick*2,border_thick * 4))
    win.blit(level_counter, (border_thick*2,border_thick * 5))
    if difficulty_timer > 0:
        win.blit(difficulty_counter, (win_width//2,win_height//2))
        difficulty_timer -=1
        
    # weapon collision
    if staff.rect.colliderect(playerA.rect):
        staff_have = True

    if sword.rect.colliderect(playerA.rect): 
        sword_have = True
        
    # border collision
    if playerA.rect.colliderect(border_left.rect):
        playerA.x += playerA.vel
        playerA.image = ballthey_sad
        collision_timer.tick()
    if playerA.rect.colliderect(border_left.rect) == False and collision_timer.tick_busy_loop() > 10:
        playerA.image = ballthey_reg
        collision_timer.tick(0)
        
    if playerA.rect.colliderect(border_right.rect):
        playerA.x -= playerA.vel
        playerA.image = ballthey_sad
        collision_timer.tick()
    if playerA.rect.colliderect(border_right.rect) == False and collision_timer.tick_busy_loop() > 20:
        playerA.image = ballthey_reg
        collision_timer.tick(0)
        
    if playerA.rect.colliderect(border_top.rect):
        playerA.y += playerA.vel
        playerA.image = ballthey_sad
    if playerA.rect.colliderect(border_top.rect) == False and collision_timer.tick_busy_loop() > 20:
        playerA.image = ballthey_reg
        collision_timer.tick(0)
        
    if playerA.rect.colliderect(border_bottom.rect):
        playerA.y -= playerA.vel
        playerA.image = ballthey_sad
    if playerA.rect.colliderect(border_bottom.rect) == False and collision_timer.tick_busy_loop() > 20:
        playerA.image = ballthey_reg
        collision_timer.tick(0)
    
    if playerA.rect.colliderect(menuA.rect):
        playerA.y += playerA.vel
        playerA.image = ballthey_sad
    if playerA.rect.colliderect(menuA.rect) == False and collision_timer.tick_busy_loop() > 20:
        playerA.image = ballthey_reg
        collision_timer.tick(0)
        
    # coin collision
    for coin in coins_list_spawns:
        if coin_respawn == True:   # coin respawning
            
            coin.x = random.randint(50,750)
            coin.y = random.randint(150,450)
    coin_respawn = False # stops coin respawning
  
    for coin in coins_list_spawns:
        coin.draw()
        coin.coin_collision(playerA)
       
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if dead == False:
        
        # movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            playerA.x -= playerA.vel
            playerA.direction = 'left'
            
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            playerA.y -= playerA.vel
            playerA.direction = 'up'

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            playerA.x += playerA.vel
            playerA.direction = 'right'

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            playerA.y += playerA.vel
            playerA.direction = 'down'

        # staff attack
        staff_shot_big = projectile(round(playerA.x + playerA.width//3), round(playerA.y + playerA.height//3),
                                    30, 30, 3, playerA.direction, staff_bullet_image1, staff_damage * 2)
        staff_shot = projectile(round(playerA.x + playerA.width//2), round(playerA.y + playerA.height//2),
                                15, 15, 6, playerA.direction, staff_bullet_image1, staff_damage)
                    
        if keys[pygame.K_f] and staff_have and staff_timer < 50: # make this so it starts a timer, then when the timer finishes and the key is released shoot
              staff_timer += 0.5 # charge-up shot

        if keys[pygame.K_f] == False and staff_timer < 20 and staff_timer > 0:
            staff_timer -= 1 # reduces charge of shot
            
        if keys[pygame.K_f] and staff_timer >= 20 and staff_timer % 2 == 0:
            playerA.image = ballthey_charge1
        if keys[pygame.K_f] and staff_timer >= 20 and staff_timer % 10 != 0:
            playerA.image = ballthey_charge2

        if keys[pygame.K_f] == False and staff_timer >= 50: # allowing bullets to be shot
            shoot_button = True
            if len(staff_bullets) <= 20: # max bullet count
                
                staff_bullets.append(staff_shot_big) # adds a BIG bullet to the charge
                                     
            staff_timer = 0
       
        elif keys[pygame.K_f] == False and staff_timer >= 20: # allowing bullets to be shot
            shoot_button = True
            
            if len(staff_bullets) <= 20: # max bullet count
                
                
                staff_bullets.append(staff_shot) # adds a regular bullet to the charge

            staff_timer = 0

        if shoot_button == True: 
            for bullet in staff_bullets: 
                bullet.draw(staff_bullet_image1,staff_bullet_image2,staff_animation_timer) # drawing the bullets
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
            enemy.collision(playerA,ballthey_sad,sword_hitbox,sword_damage)
            
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
                elif enemy.health_max <= enemyF.health_max:
                    score+=30
                
        # changing colour
        if keys[pygame.K_1]:
            playerA.image = ballthey_reg
        if keys[pygame.K_2]:
            playerA.image = ballthey_sad
        if keys[pygame.K_3]:
            playerA.image = ballthey_coinage
        if keys[pygame.K_4]:
            playerA.colour = GREEN
        if keys[pygame.K_5]:
            playerA.colour = BLUE
        if keys[pygame.K_6]:
            playerA.colour = PURPLE
        if keys[pygame.K_7]:
            playerA.colour = PINK

        # cheats
        if keys[pygame.K_DELETE]:
            enemy_spawn_limit = 6
            
    else:
        playerA.image = ballthey_dead
        win.blit(dead_counter,(0,win_height//2))
    
    pygame.display.update()

pygame.quit()

