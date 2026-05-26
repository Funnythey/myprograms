import sys
import pygame
from fileabcd import *

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

# inventory 
score = 0
level = 0
levelup = 0.5

staff_have = False
sword_have = False

# Objects
playerA = player((win_width //2),((win_height + menu_thick) //2), 30,50, RED)

coin1 = pickup(100,160,GOLD)
coin2 = pickup(220,90,GOLD)
coins_list = [coin1,coin2]

staff = pickup(140,200,GREEN)
staff_symbol = pickup(win_width - (border_thick*12),border_thick*2,GREEN)
staff_bullet = projectile(playerA.x,playerA.y,15,15,playerA.direction,GREEN)
staff_bullets = []
shoot_button = False
staff_timer = 0

sword = pickup(390,450, BLUE)
sword_symbol = pickup(win_width - (border_thick*20),border_thick*2,BLUE)
sword_hitbox = pickup(playerA.x,playerA.y+playerA.height,BLUE) #WORK HERE AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

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
    
    FPS = 240
    clock = pygame.time.Clock()
    
    # window Colour
    win.fill((0,0,0))  # Fills the screen with black

    # inventory items 
    if score == (levelup * 10):
        levelup+= levelup
        level+=1

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

    pygame.font.init()
    menu_font = pygame.font.SysFont('Arial', 20)
    
    coins_counter = menu_font.render(f'Coins: '+ str(score), False, (100,100,100))
    win.blit(coins_counter, (border_thick*2,border_thick * 2))
    level_counter = menu_font.render(f'Level: '+ str(level), False, (100,100,100))
    win.blit(level_counter, (border_thick*2,border_thick * 4))
    
    playerA.draw()
         
    for coin in coins_list:
        coin.draw()

    if staff_have == False:
        staff.draw()
    else:
        staff_symbol.draw()
        staff_counter = menu_font.render(f'staff {staff_timer}', False, GREEN)
        win.blit(staff_counter, (win_width - (border_thick*10),border_thick*2))

        bullet_counter = menu_font.render(f'ammo: {len(staff_bullets)}', False, GREEN)
        win.blit(bullet_counter, (win_width - (border_thick*10),border_thick*4))

    if sword_have == False:
        sword.draw()
    else:
        sword_symbol.draw()
        sword_counter = menu_font.render(f'sword', False, BLUE)
        win.blit(sword_counter, (win_width - (border_thick*18),border_thick*2))

    # collision items 
    for coin in coins_list: # FOR COIN COLLECTION DO NOT DELETE 
        if coin.rect.colliderect(playerA.rect):
            score+=1
            coin.kill()
            del coins_list[coins_list.index(coin)]

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
    if keys[pygame.K_f] and staff_have: # make this so it starts a timer, then when the timer finishes and the key is released shoot
        staff_timer += 0.5 # charge-up shot

    if keys[pygame.K_f] == False and staff_timer < 20:
        staff_timer = 0 
        
    if keys[pygame.K_f] and staff_timer >= 20 and staff_timer % 2 == 0:
        playerA.colour = GREEN
    if keys[pygame.K_f] and staff_timer >= 20 and staff_timer % 10 != 0:
        playerA.colour = RED
        
    if keys[pygame.K_f] == False and staff_timer >= 20: # allowing bullets to be shot
        shoot_button = True
        if len(staff_bullets) <= 20: #max bullet count
            staff_bullets.append(
            projectile(round(playerA.x + playerA.width//2), round(playerA.y + playerA.height//2), 15, 15,
            playerA.direction, GREEN)) # reloads bullets
        staff_timer = 0
     
    if shoot_button == True: 
        for bullet in staff_bullets: # drawing the bullets
            bullet.draw()
            if bullet.rect.colliderect(background_rect) == False or len(staff_bullets) > 20:
                staff_bullets.pop(staff_bullets.index(bullet))
    # sword attack
    if keys[pygame.K_q] and sword_have:
        sword_symbol.draw()
    
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

    pygame.display.update()

pygame.quit()

# -------------------------------------------------------------------------- #


# current plan: figure out how to create different levels/screens/ROOMS & how to move between
# figure out how to make collectables (coins) that disappear when collected
# make borders their own group so that different room borders are easier to make
# make menu work right
# make player.colour change when touching borders, USE A TIMER
# put the different inits into a different file and import into this one to make things cleaner
# give player a weapon (sword, bow/staff or smth)
# figure out how to make projectiles
# figure out how to make charged projectile maybe?idk
# figure out how to flash green while staff is fully charged
# figure out how to make a sword


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
