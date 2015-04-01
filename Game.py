# Sound and music from: http://www.freesfx.co.uk/

import pygame
import random
from pygame.locals import *

### Classes ###

class Player(pygame.sprite.Sprite):    
    'Controllable player capable of firing bullets'
    player = 0
    bullet_cooldown = 0
    default_image = None
    fire_image = None    
    fire_sound = pygame.mixer.Sound
    
    def __init__(self, player, (pos_x, pos_y)):
        pygame.sprite.Sprite.__init__(self)

        self.player = player
        self.default_image = pygame.image.load('images/player.jpg')
        self.fire_image = pygame.image.load('images/player_fire.jpg')
        if self.player == 2:
            self.default_image = pygame.transform.flip(self.default_image, False, True)
            self.fire_image = pygame.transform.flip(self.fire_image, False, True)
        self.fire_sound = pygame.mixer.Sound('sounds/player_fire.ogg')
        self.image = self.default_image
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

    def handle_input(self, event):   
        for e in event:
            if e.type == KEYDOWN:
                if e.key == K_w:
                    if self.bullet_cooldown == 0:
                        # Search for a free bullet and fire
                        bullets = None
                        bullet_origin_y = 0
                        if self.player == 1:
                            bullets = bullets_bottom
                            bullet_origin_y = self.rect.top + 5
                        else:
                            bullets = bullets_top
                            bullet_origin_y = self.rect.bottom - 5
                        
                        for bullet in bullets:
                            if not bullet.active:
                                bullet.rect.x = self.rect.centerx - 2.5
                                bullet.rect.y = bullet_origin_y
                                bullet.active = True
                                self.fire_bullet()
                                break
                                    
        # Movement
        keys = pygame.key.get_pressed()

        if keys[K_a]:
            self.rect = self.rect.move(-PLAYER_SPEED, 0)
        if keys[K_d]:
            self.rect = self.rect.move(PLAYER_SPEED, 0)

        # Prevent player from moving outside the screen    
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= RESOLUTION[0]:
            self.rect.right = RESOLUTION[0]

    def update(self):
        if self.bullet_cooldown > 0:
           self.bullet_cooldown -= 1
        if self.bullet_cooldown == BULLET_COOLDOWN / 2:
           self.image = self.default_image

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def fire_bullet(self):
        self.bullet_cooldown = BULLET_COOLDOWN
        self.image = self.fire_image
        if self.player == 1:
            self.fire_sound.play()

class Wall(pygame.sprite.Sprite):
    'A wall blocking bullets'
    def __init__(self, (pos_x, pos_y)):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('images/wall.jpg')
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

    def draw(self, screen):
        screen.blit(self.image, self.rect)        
        
class Bullet(pygame.sprite.Sprite):
    'Bullet fired by Player'
    active = False
    velocity = 0

    def __init__(self, velocity):
        pygame.sprite.Sprite.__init__(self)

        self.velocity = velocity
        self.image = pygame.image.load('images/bullet.jpg')
        self.rect = self.image.get_rect()

    def update(self):
        if self.active:
            self.rect.y += self.velocity

    def draw(self, screen):
        if self.active:
            screen.blit(self.image, self.rect)

class Number(pygame.sprite.Sprite):
    'A number floating horizontally, worth a certain score'
    number = 0
    velocity = 0

    def __init__(self, number, velocity, (pos_x, pos_y)):
        pygame.sprite.Sprite.__init__(self)

        self.number = number
        self.velocity = velocity
        self.image = numbers_all[number]
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

    def update(self):
        self.rect.x += self.velocity

    def set_velocity(self, velocity):
        self.velocity = velocity

### End of classes ###

### Initialization ###
        
## Setup Constants
RESOLUTION = (800, 600)
FRAMES_PER_SECOND = 60
FULLSCREEN = False
GAMEEVENT = USEREVENT + 1

BACKGROUND_COLOR = (255, 255, 255)
PLAYER_SPEED = 7
BULLET_SPEED = 10
NUMBER_SPEED = 1
BULLET_COOLDOWN = 15
ROUND_DISPLAY_TIME = 2000

# Image dictionary for the Number class
numbers_all = {1: pygame.image.load('images/number_1.jpg'),
               2: pygame.image.load('images/number_2.jpg'),
               3: pygame.image.load('images/number_3.jpg'),
               4: pygame.image.load('images/number_4.jpg'),
               5: pygame.image.load('images/number_5.jpg'),
               6: pygame.image.load('images/number_6.jpg'),
               7: pygame.image.load('images/number_7.jpg'),
               8: pygame.image.load('images/number_8.jpg'),
               9: pygame.image.load('images/number_9.jpg')}

# Initialize pygame
pygame.init()

# Setup screen
screen = pygame.display.set_mode(RESOLUTION, pygame.FULLSCREEN if FULLSCREEN else 0)

# Load music
pygame.mixer.music.load('sounds/music.ogg')

# Load sounds
sound_number_hit = pygame.mixer.Sound('sounds/number_hit.ogg')
sound_victory = pygame.mixer.Sound('sounds/victory.ogg')
sound_game_over = pygame.mixer.Sound('sounds/game_over.ogg')
sound_new_round = pygame.mixer.Sound('sounds/new_round.ogg')

# Setup timer
pygame.time.set_timer(GAMEEVENT, 1000)
    
# Setup clock
clock = pygame.time.Clock()

## Setup variables

# Objects
player_bottom = Player(1, (RESOLUTION[0] / 2 - 40, RESOLUTION[1] - 54))
player_top = Player(2, (RESOLUTION[0] / 2 - 40, 0))
wall = Wall((0, RESOLUTION[1] / 2 - 27))
bullets_bottom = pygame.sprite.Group()
bullets_bottom.add(Bullet(-BULLET_SPEED),
                   Bullet(-BULLET_SPEED),
                   Bullet(-BULLET_SPEED))
bullets_top = pygame.sprite.Group()
bullets_top.add   (Bullet(BULLET_SPEED),
                   Bullet(BULLET_SPEED),
                   Bullet(BULLET_SPEED))
numbers_bottom = [Number(1, NUMBER_SPEED, (0, wall.rect.bottom + 20)),
                  Number(2, NUMBER_SPEED, (0, wall.rect.bottom + 20)),
                  Number(3, NUMBER_SPEED, (0, wall.rect.bottom + 20)),
                  Number(4, NUMBER_SPEED, (0, wall.rect.bottom + 20)),
                  Number(5, NUMBER_SPEED, (0, wall.rect.bottom + 20)),
                  Number(6, NUMBER_SPEED, (0, wall.rect.bottom + 20)),
                  Number(7, NUMBER_SPEED, (0, wall.rect.bottom + 20)),
                  Number(8, NUMBER_SPEED, (0, wall.rect.bottom + 20)),
                  Number(9, NUMBER_SPEED, (0, wall.rect.bottom + 20))]
numbers_top =    [Number(1, -NUMBER_SPEED, (RESOLUTION[0], wall.rect.top - 80)),
                  Number(2, -NUMBER_SPEED, (RESOLUTION[0], wall.rect.top - 80)),
                  Number(3, -NUMBER_SPEED, (RESOLUTION[0], wall.rect.top - 80)),
                  Number(4, -NUMBER_SPEED, (RESOLUTION[0], wall.rect.top - 80)),
                  Number(5, -NUMBER_SPEED, (RESOLUTION[0], wall.rect.top - 80)),
                  Number(6, -NUMBER_SPEED, (RESOLUTION[0], wall.rect.top - 80)),
                  Number(7, -NUMBER_SPEED, (RESOLUTION[0], wall.rect.top - 80)),
                  Number(8, -NUMBER_SPEED, (RESOLUTION[0], wall.rect.top - 80)),
                  Number(9, -NUMBER_SPEED, (RESOLUTION[0], wall.rect.top - 80))]
numbers_bottom_active = pygame.sprite.Group()
numbers_top_active = pygame.sprite.Group()

# Data
players = 1

score = 0
target_score = 0

level = 3
total_rounds = 3
current_round = 0

round_timer = 0
inactive_numbers = 0

victory = True
game_over = False
round_starting = False
round_active = True

# Fonts
font = pygame.font.SysFont("Arial Black", 70)
font2 = pygame.font.SysFont("Arial Black", 25)

level_font = font.render("Level " + str(level), True, (135, 135, 230))
current_round_font = font.render("Round " + str(current_round), True, (135, 135, 230))
game_over_font = font.render("Game Over", True, (230, 135, 135))
victory_font = font.render("You win!", True, (135, 230, 135))
new_game_font = font.render("New Game?", True, (135, 230, 135))

score_font = font2.render("Score: " + str(score), True, (230, 180, 135))
target_score_font = font2.render("Target: " + str(target_score), True, (230, 180, 135))

score_font_pos = (0, RESOLUTION[1] - score_font.get_height())
target_score_font_pos = (625, RESOLUTION[1] - target_score_font.get_height())
game_over_font_pos = (RESOLUTION[0] / 2 - game_over_font.get_rect().width / 2, 125)
victory_font_pos = (RESOLUTION[0] / 2 - victory_font.get_rect().width / 2, 125)
new_game_font_pos = (RESOLUTION[0] / 2 - new_game_font.get_rect().width / 2, 325)
level_font_pos = (RESOLUTION[0] / 2 - level_font.get_rect().width / 2, 125)
current_round_font_pos = (RESOLUTION[0] / 2 - current_round_font.get_rect().width / 2, 325)

### End of initialization ###

def main():    
    # Game loop
    running = True
    while running:
        # Event handling
        ev = pygame.event.get()
        for e in ev:
            if e.type == QUIT:
                running = False
            elif e.type == KEYUP:
                if e.key == K_ESCAPE:
                    running = False

        if game_over or victory:
            game_inactive(ev)
        else:
            if round_starting:
                new_round()
            if round_active:
                update(ev)
            else:
                check_if_activate_round()

        draw(screen)

    pygame.quit()

# Game is not in a round
def game_inactive(event):
    for e in event:
        if e.type == KEYUP:
            if e.key == K_1:
                new_game(1)
            elif e.key == K_2:
                new_game(2)
            elif e.key == K_3:
                new_game(3)

# Start a new round
def new_round():
    global round_timer, round_starting
    global round_active, inactive_numbers
    
    round_timer = pygame.time.get_ticks()
    round_starting = False
    round_active = False

    update_round(current_round + 1)
    
    if level == 1:
        update_target_score(target_score + random.randint(10, 30))
    else:
        update_target_score(target_score + random.randint(30, 80))

    random.shuffle(numbers_bottom)
    numbers_bottom_active.empty()
    
    if players == 2:
        random.shuffle(numbers_top)
        numbers_top_active.empty()

    if current_round > 1:
        sound_new_round.play()
    
    inactive_numbers = len(numbers_bottom)    

    # Reset position of numbers
    for number in numbers_bottom:
        number.rect.x = 0
        
    if players == 2:        
        for number in numbers_top:
            number.rect.x = RESOLUTION[0]   

    # Start the adding numbers timer
    pygame.time.set_timer(GAMEEVENT, 1000)    

# Start a new game of level 1-3
def new_game(level):
    global game_over, round_starting 
    global victory, players, total_rounds

    game_over = False
    victory = False
    round_starting = True

    update_level(level)
    
    if level == 1:
        players = 1
        total_rounds = 3
    elif level == 2:
        players = 2
        total_rounds = 5
    elif level == 3:
        players = 2
        total_rounds = 10
        
    reset_data()
    reset_objects()
    
    sound_game_over.stop()
    sound_victory.stop()
    pygame.mixer.music.play(-1)            

def reset_data():
    global current_round
    
    current_round = 0
    update_score(0)
    update_target_score(0)
    
def reset_objects():
    player_bottom.rect.x = RESOLUTION[0] / 2 - player_bottom.rect.width / 2
    player_bottom.rect.y = 546

    for bullet in bullets_bottom:
        bullet.active = False

    if players == 2:
        player_top.rect.x = RESOLUTION[0] / 2 - player_top.rect.width / 2
        player_top.rect.y = 0

        for bullet in bullets_top:
            bullet.active = False

def update(event):
    global inactive_numbers
    
    for e in event:
        if e.type == GAMEEVENT:
            # Small delay before starting to move the numbers
            if pygame.time.get_ticks() - round_timer > ROUND_DISPLAY_TIME + 500:
                if inactive_numbers == 0:
                    pygame.time.set_timer(GAMEEVENT, 0)
                else:
                    # Send out a new number
                    inactive_numbers -= 1
                    numbers_bottom_active.add(numbers_bottom[inactive_numbers])

                    if players == 2:
                        numbers_top_active.add(numbers_top[inactive_numbers])
                    
    # Update objects
    player_bottom.handle_input(event)
    player_bottom.update()
    bullets_bottom.update()
    numbers_bottom_active.update()

    if players == 2:
        player_top.handle_input(event)
        player_top.update()
        bullets_top.update()
        numbers_top_active.update()

    check_collision()

def check_collision():
    # If a number has moved outside the screen, deactivate it
    # and check round status
    for number in numbers_bottom_active:
        if number.rect.left > RESOLUTION[0]:
            numbers_bottom_active.remove(number)
            check_round_status()
            break
    
    # Bullet collision
    for bullet in bullets_bottom:
        if bullet.active:
            # If a bullet has collided with a number, deactivate both
            # of them and update the score
            for number in numbers_bottom_active:
                if pygame.sprite.collide_rect(bullet, number):
                    bullet.active = False
                    numbers_bottom_active.remove(number)
                    update_score(score + number.number)
                    sound_number_hit.play()
                    check_score_status()
                    break
        
            if pygame.sprite.collide_rect(bullet, wall):
                bullet.active = False

    if players == 2:
        for number in numbers_top_active:
            if number.rect.right < 0:
                numbers_top_active.remove(number)
                check_round_status()
                break    
        
        for bullet in bullets_top:
            if bullet.active:
                for number in numbers_top_active:
                    if pygame.sprite.collide_rect(bullet, number):
                        bullet.active = False
                        numbers_top_active.remove(number)
                        update_score(score + number.number)
                        sound_number_hit.play()
                        check_score_status()
                        break
        
                if pygame.sprite.collide_rect(bullet, wall):
                    bullet.active = False    

def check_score_status():
    global round_starting
    
    if score > target_score:
        set_game_over()
    elif score == target_score:
        if current_round < total_rounds:
            round_starting = True
        else:
            set_victory()

def set_game_over():
    global game_over

    game_over = True
    pygame.mixer.music.stop()
    sound_game_over.play()

def set_victory():
    global victory

    victory = True
    pygame.mixer.music.stop()
    sound_victory.play()    
    
def check_if_activate_round():
    global round_active
    
    if pygame.time.get_ticks() - round_timer > ROUND_DISPLAY_TIME:
        round_active = True    

def check_round_status():
    global game_over
    
    if round_over():
        set_game_over()      

def round_over():
    return True if len(numbers_bottom_active) == 0 else False

def update_level(chosen_level):
    global level, level_font
    
    level = chosen_level
    level_font = font.render("Level " + str(level), True, (135, 135, 230))
    
def update_score(new_score):
    global score, score_font
    
    score = new_score
    score_font = font2.render("Score: " + str(score), True, (230, 180, 135))

def update_target_score(new_target_score):
    global target_score, target_score_font
    
    target_score = new_target_score
    target_score_font = font2.render("Target: " + str(target_score), True, (230, 180, 135))    

def update_round(new_round):
    global current_round, current_round_font
    
    current_round = new_round
    current_round_font = font.render("Round " + str(current_round), True, (135, 135, 230))

def draw(screen):
        # Set background
        screen.fill(BACKGROUND_COLOR)

        # Draw sprites
        player_bottom.draw(screen)
        wall.draw(screen)
        numbers_bottom_active.draw(screen)
        
        for bullet in bullets_bottom:
            bullet.draw(screen)

        if players == 2:
            player_top.draw(screen)
            numbers_top_active.draw(screen)
        
            for bullet in bullets_top:
                bullet.draw(screen)            

        # Draw current level and round text
        if not round_active:
            screen.blit(level_font, level_font_pos)
            screen.blit(current_round_font, current_round_font_pos)

        # Draw victory/game over text
        if victory:
            screen.blit(victory_font, victory_font_pos)
            screen.blit(new_game_font, new_game_font_pos)             
        elif game_over:
            screen.blit(game_over_font, game_over_font_pos)
            screen.blit(new_game_font, new_game_font_pos)        

        # Draw score and target score
        screen.blit(score_font, score_font_pos)
        screen.blit(target_score_font, target_score_font_pos)

        # Flip display and wait for next frame
        pygame.display.flip()
        clock.tick(FRAMES_PER_SECOND)
      
main()
