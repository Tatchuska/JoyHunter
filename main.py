import pygame
import os
import random

pygame.init()

clock = pygame.time.Clock()
FPS = 60

# Define Game variables
GRAVITY = 0.6 # Constant in Python is indicated by upper case
SCREEN_WIDTH = 576
SCREEN_HEIGHT = 324
SCROLL_LIMIT = 200
TILE_SIZE = 30
screen_scroll = 0
bg_scroll = 0
ground_height = 92


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

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Define font
font = pygame.font.SysFont('Roboto Mono', 25)

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


# Create sprite groups
enemy_group = pygame.sprite.Group()
crystal_group = pygame.sprite.Group()

# Create crystals
crystal = Crystal('Blue', 350, 150)
crystal_group.add(crystal)
crystal = Crystal('Blue', 400, 125)
crystal_group.add(crystal)
crystal = Crystal('Yellow', 450, 100)
crystal_group.add(crystal)
crystal = Crystal('Blue', 500, 125)
crystal_group.add(crystal)
crystal = Crystal('Blue', 550, 150)
crystal_group.add(crystal)

crystal = Crystal('Blue', 800, 120)
crystal_group.add(crystal)
crystal = Crystal('Blue', 850, 100)
crystal_group.add(crystal)
crystal = Crystal('Yellow', 900, 80)
crystal_group.add(crystal)
crystal = Crystal('Blue', 950, 100)
crystal_group.add(crystal)
crystal = Crystal('Blue', 1000, 120)
crystal_group.add(crystal)

crystal = Crystal('Blue', 1200, 150)
crystal_group.add(crystal)
crystal = Crystal('Blue', 1225, 125)
crystal_group.add(crystal)
crystal = Crystal('Red', 1250, 100)
crystal_group.add(crystal)
crystal = Crystal('Blue', 1275, 125)
crystal_group.add(crystal)
crystal = Crystal('Blue', 1300, 150)
crystal_group.add(crystal)

crystal = Crystal('Blue', 1500, 150)
crystal_group.add(crystal)
crystal = Crystal('Blue', 1550, 125)
crystal_group.add(crystal)
crystal = Crystal('Yellow', 1600, 100)
crystal_group.add(crystal)
crystal = Crystal('Blue', 1650, 125)
crystal_group.add(crystal)
crystal = Crystal('Blue', 1700, 150)
crystal_group.add(crystal)

crystal = Crystal('Blue', 2000, 150)
crystal_group.add(crystal)
crystal = Crystal('Blue', 2025, 125)
crystal_group.add(crystal)
crystal = Crystal('Yellow', 2050, 100)
crystal_group.add(crystal)
crystal = Crystal('Blue', 2075, 125)
crystal_group.add(crystal)
crystal = Crystal('Blue', 2100, 150)
crystal_group.add(crystal)

crystal = Crystal('Blue', 2400, 150)
crystal_group.add(crystal)
crystal = Crystal('Blue', 2450, 125)
crystal_group.add(crystal)
crystal = Crystal('Yellow', 2500, 100)
crystal_group.add(crystal)
crystal = Crystal('Blue', 2550, 125)
crystal_group.add(crystal)
crystal = Crystal('Blue', 2600, 150)
crystal_group.add(crystal)




player = Animal('Cat', 100, SCREEN_HEIGHT - ground_height, 1.5, 4)
enemy = Animal('Dog', 400, SCREEN_HEIGHT - ground_height, 1.5, 2)
enemy_group.add(enemy)
enemy = Animal('Dog', 2450, SCREEN_HEIGHT - ground_height, 1.5, 2)
enemy_group.add(enemy)
enemy = Animal('Dog', 1050, SCREEN_HEIGHT - ground_height, 1.5, 2)
enemy_group.add(enemy)
enemy = Animal('Dog', 1800, SCREEN_HEIGHT - ground_height, 1.5, 2)
enemy_group.add(enemy)
enemy = Animal('Dog', 2300, SCREEN_HEIGHT - ground_height, 1.5, 2)
enemy_group.add(enemy)
enemy = Animal('Hound', 800, SCREEN_HEIGHT - ground_height, 1.75, 3)
enemy_group.add(enemy)
enemy = Animal('Hound', 1250, SCREEN_HEIGHT - ground_height, 1.75, 3)
enemy_group.add(enemy)
enemy = Animal('Hound', 2050, SCREEN_HEIGHT - ground_height, 1.75, 3)
enemy_group.add(enemy)

pygame.mixer_music.load(f'./asset/Level1/Level1.mp3')
pygame.mixer_music.set_volume(0.1)
pygame.mixer_music.play(-1)

# Game Loop
run = True
while run:
    clock.tick(FPS)

    # Draw World
    draw_bg()

    # Show Score
    draw_text(f'SCORE: {player.score}', font, YELLOW, 10, 35)
    # Show Health
    draw_text('HEALTH: ', font, WHITE, 10, 10)
    for x in range(player.health):
        screen.blit(heart_img, (90 + (x * 20), 10))

    # player.collision()
    player.update()
    player.draw()
    for enemy in enemy_group:
        enemy.ai()
        enemy.update_animation()
        enemy.draw()

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
                run = False

        # Keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

    pygame.display.update()

pygame.quit()