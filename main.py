import sys

import pygame
import os
import random
from code.Const import *


pygame.init()

clock = pygame.time.Clock()

# Define font
font_game = pygame.font.SysFont('Lucida Sans Typewriter', 25)
font_menu = pygame.font.SysFont('Lucida Sans Typewriter', 35)
font_title = pygame.font.SysFont('Lucida Sans Typewriter', 75)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Joy Hunter")

# Define Player action variables
moving_left = False
moving_right = False

# Load Images
# Background
bg_images = []
for i in range(0,6):
    bg_image = pygame.image.load(f"./asset/Level1/Level1Bg{i}.png").convert_alpha()
    bg_images.append(bg_image)
bg_width = bg_images[0].get_width()

# Health
heart_img = pygame.image.load("./asset/heart.png").convert_alpha()
heart_img = pygame.transform.scale(heart_img, (int(heart_img.get_width() / 1.5), int(heart_img.get_height() / 1.5)))

# Box
box_img = pygame.image.load("./asset/Item/box.png").convert_alpha()
box_img = pygame.transform.scale(box_img, (int(box_img.get_width() / 4), int(box_img.get_height() / 4)))

# Menu
menu_bg = pygame.image.load("./asset/Menu/bg.png").convert_alpha()

# Crystals
yellow_img = pygame.image.load("./asset/Item/0.png").convert_alpha()
yellow_img = pygame.transform.scale(yellow_img, (int(yellow_img.get_width() / 10), int(yellow_img.get_height() / 10)))
blue_img = pygame.image.load("./asset/Item/1.png").convert_alpha()
blue_img = pygame.transform.scale(blue_img, (int(blue_img.get_width() / 10), int(blue_img.get_height() / 10)))
red_img = pygame.image.load("./asset/Item/2.png").convert_alpha()
red_img = pygame.transform.scale(red_img, (int(red_img.get_width() / 10), int(red_img.get_height() / 10)))
crystals = {
    'Yellow'  : yellow_img,
    'Blue'   : blue_img,
    'Red'  : red_img,
}


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_bg():
    for i in range(10):
        speed = 1
        for j in bg_images:
            screen.blit(j, ((i * bg_width) - bg_scroll * speed, 0))
            speed += 0.2


class Animal(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.health = 3
        self.max_health = self.health
        self.recover_time = 0
        self.hurt = False
        self.score = 0
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.is_in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        # AI specific variables
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.idling = False
        self.idling_counter = 0

        # Load all the images for the players
        animation_types = ['Idle', 'Run', 'Jump', 'Attack', 'Hurt', 'Dead']
        for animation in animation_types:
            # Reset temporary list of images
            temp_list = []
            # Count number of files in the folder
            num_of_frames = len(os.listdir(f'./asset/{self.char_type}/{animation}'))
            for j in range(num_of_frames):
                img = pygame.image.load(f'./asset/{self.char_type}/{animation}/{j}.png')
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.update_animation()
        self.check_alive()

    def move(self, moving_left, moving_right):
        # Reset movement variables
        screen_scroll = 0
        dx = 0
        dy = 0

        # Assign movement variables if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        # Jump
        if self.jump == True and self.is_in_air == False:
            self.vel_y = -15
            self.jump = False
            self.is_in_air = True

        # Apply Gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = self.vel_y
        dy += self.vel_y

        # Check collision with floor
        if self.rect.bottom + dy > 265:
            dy = 265 - self.rect.bottom
            self.is_in_air = False

        if self.char_type == 'Cat':
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0

        # Update rectangle
        self.rect.x += dx
        self.rect.y += dy

        # # Update scroll based on player position
        if self.char_type == 'Cat':
            if (self.rect.right > SCREEN_WIDTH - SCROLL_LIMIT and bg_scroll < (bg_width * 5) - SCREEN_WIDTH) or (self.rect.left < SCROLL_LIMIT and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll

    def ai(self):
        if self.alive and player.alive:
            if not self.idling and random.randint(1, 200) == 1:
                self.update_action(0) # 0 = idle
                self.idling = True
                self.idling_counter = 150
            # Check if the AI is near the player
            if self.vision.colliderect(player.rect):
                # Stop running and face the player
                self.update_action(3)
            else:
                if not self.idling:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1) # 1 = run
                    self.move_counter += 1
                    # Update AI vision as the enemy moves
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False
            # Collision
            if self.rect.colliderect(player.rect) and player.recover_time <= 0:
                player.health -= 1
                player.recover_time = 1000
            player.recover_time -= 1

        # Scroll
        self.rect.x += screen_scroll

    def update_animation(self):
        # Update animation
        animation_cooldown = 100
        # Updating image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        # Check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # Reset the animation back to start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 5:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0


    def update_action(self, new_action):
        # Check if the new action is different from the previous one
        if new_action != self.action:
            self.action = new_action
            # Update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.alive = False
        if not self.alive:
            self.speed = 0
            self.update_action(5)
            game_over_text = font_title.render("GAME OVER", True, RED)
            press_esc_text = font_game.render("PRESS ESC", True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
            screen.blit(press_esc_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))


    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class Crystal(pygame.sprite.Sprite):
    def __init__(self, crystal_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.crystal_type = crystal_type
        self.image = crystals[self.crystal_type]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        # Check if the player had picked up the crystal
        if pygame.sprite.collide_rect(self, player):
            if self.crystal_type == 'Red':
                player.health += 1
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.crystal_type == 'Blue':
                player.score += 10
            elif self.crystal_type == 'Yellow':
                player.score += 20
            # Delete the crystals
            self.kill()
        self.rect.x += screen_scroll

class Box(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = box_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        # Check if the player had picked up the crystal
        if pygame.sprite.collide_rect(self, player):
            player.speed = 0
            win_text = font_title.render("YOUR WIN!", True, WHITE)
            screen.blit(win_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
        self.rect.x += screen_scroll
    
    def draw(self):
        screen.blit(self.image, self.rect)

# Create sprite groups
enemy_group = pygame.sprite.Group()
crystal_group = pygame.sprite.Group()

for crystal_type, x, y in crystal_data:
    crystal_group.add(Crystal(crystal_type, x, y))
    
for char_type, x, y, scale, speed in enemy_data:
    enemy_group.add(Animal(char_type, x, y, scale, speed))


player = Animal('Cat', 100, SCREEN_HEIGHT - ground_height, 1.5, 4)
box = Box(2800, SCREEN_HEIGHT - ground_height + 10)

# Load music

if not start_game:
    pygame.mixer_music.load('./asset/Menu.mp3')
    pygame.mixer_music.set_volume(0.1)
    pygame.mixer_music.play(-1)
# else:
#     pygame.mixer_music.load(f'./asset/Level1/Level1.mp3')
#     pygame.mixer_music.set_volume(0.1)
#     pygame.mixer_music.play(-1)

menu_option = 0
# Game Loop
run = True
while run:
    clock.tick(FPS)

    if not start_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    menu_option = (menu_option + 1) % len(MENU_OPTION)
                if event.key == pygame.K_UP:
                    menu_option = (menu_option - 1) % len(MENU_OPTION)
                if event.key == pygame.K_RETURN:
                    if MENU_OPTION[menu_option] == "START GAME":
                        start_game = True
                        pygame.mixer_music.stop()
                        pygame.mixer_music.load('./asset/Level1/Level1.mp3')
                        pygame.mixer_music.set_volume(0.1)
                        pygame.mixer_music.play(-1)
                    else:
                        pygame.quit()
                        sys.exit()
            
            if not start_game:
                screen.blit(menu_bg, (0, 0))
                draw_text("Joy", font_title, GREEN, 30, 30)
                draw_text("Hunter", font_title, GREEN, 50, 80)
                for i in range(len(MENU_OPTION)):
                    color = WHITE if i == menu_option else GREEN
                    draw_text(MENU_OPTION[i], font_menu, color, 50, 150 + i * 35)
                
                pygame.display.flip()
    else:
        # Draw World
        draw_bg()
        # Show Score
        draw_text(f'SCORE: {player.score}', font_game, YELLOW, 10, 35)
        # Show Health
        draw_text('HEALTH: ', font_game, WHITE, 10, 10)
        for x in range(player.health):
            screen.blit(heart_img, (90 + (x * 20), 10))
    
        # player.collision()
        player.update()
        player.draw()
        
        for enemy in enemy_group:
            enemy.ai()
            enemy.update_animation()
            enemy.draw()
        
        box.update()
        box.draw()
    
        # Update and draw groups
        crystal_group.update()
        crystal_group.draw(screen)

        # Update player actions
        if player.alive:
            if player.is_in_air:
                player.update_action(2) # 2 = Jump
            elif moving_left or moving_right:
                player.update_action(1) # 1 = Run
            else:
                player.update_action(0) # 0 = Idle
        
        screen_scroll = player.move(moving_left, moving_right)
        bg_scroll -= screen_scroll


    # Events
    for event in pygame.event.get():
        # Quit Game
        if event.type == pygame.QUIT:
            run = False
        # Keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        # Keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

    pygame.display.update()

pygame.quit()