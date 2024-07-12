import pygame
import time
import random

pygame.init()

screen = pygame.display.set_mode((720, 1280))
clock = pygame.time.Clock()

bg_img = pygame.image.load('mbg.png')
dt = 0

# Explosion sprite class
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = explosion_anim[0]
        self.rect = self.image.get_rect(center=center)
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50  # 50ms between frames

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.frame]
                self.rect = self.image.get_rect(center=center)

# Load explosion animation
explosion_anim = []
for i in range(1, 9):  # Assuming 8 frames in explosion sprite sheet
    filename = f'l0_sprite_{i}.png'
    img = pygame.image.load(filename).convert_alpha()
    img = pygame.transform.scale(img, (96, 96))
    explosion_anim.append(img)

# Create monsters with more hit points and an additional row
def create_monsters():
    return [
        pygame.Vector2(50, 40),
        pygame.Vector2(175, 40),
        pygame.Vector2(300, 40),
        pygame.Vector2(425, 40),
        pygame.Vector2(550, 40),
        pygame.Vector2(50, 140),
        pygame.Vector2(175, 140),
        pygame.Vector2(300, 140),
        pygame.Vector2(425, 140),
        pygame.Vector2(550, 140),
        pygame.Vector2(50, 240),
        pygame.Vector2(175, 240),
        pygame.Vector2(300, 240),
        pygame.Vector2(425, 240),
        pygame.Vector2(550, 240),
        pygame.Vector2(50, 340),  # New row
        pygame.Vector2(175, 340),
        pygame.Vector2(300, 340),
        pygame.Vector2(425, 340),
        pygame.Vector2(550, 340),
        
    ]

# Movement variables
move_directions = [1] * len(create_monsters())  # 1 represents moving right, -1 represents moving left
move_intervals = [60] * len(create_monsters())  # Move every 60 frames (1 second at 60 FPS)
move_counters = [0] * len(create_monsters())

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 1.5)
monsters = create_monsters()
coelhoassado = pygame.Vector2(690, 1)

tartaruga = pygame.Vector2(player_pos.x, 700)
tartaruga1 = pygame.Vector2(player_pos.x, 825)

shooting = False
player_lives = 30
monster_bullets = []
tiro_img = pygame.image.load("tartaruga.png")
monstro_img = pygame.image.load("New Piskel.gif")
nave_img = pygame.image.load('Nave1.png')
amongus_img = pygame.image.load("coelhoassado.gif")

font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

explosions = pygame.sprite.Group()

def draw_retry_button():
    text = font.render('Retry', True, (255, 0, 0))
    rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(text, rect)
    return rect

def draw_entry_menu():
    screen.blit(bg_img, (0, 0))
    round_text = small_font.render(f'Game Developed by Zé, Dinis and Miguel', True, (255, 255, 255))
    screen.blit(round_text, (10, 10))
    play_button = font.render('Play', True, (0, 255, 0))
    button_rect = play_button.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(play_button, button_rect)
    pygame.display.flip()
    return button_rect


    

def draw_round_level(round_num):
    round_text = small_font.render(f'Round: {round_num}', True, (255, 255, 255))
    screen.blit(round_text, (10, 10))

def reset_game():
    global player_pos, monsters, tartaruga, tartaruga1, shooting, player_lives, monster_bullets
    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 1.5)
    monsters = create_monsters()
    tartaruga = pygame.Vector2(player_pos.x + 34, 825)
    tartaruga1 = pygame.Vector2(player_pos.x - 38, 825)
    shooting = False
    player_lives = 30
    monster_bullets = []

running = True
in_menu = True
game_over = False
current_round = 1
max_rounds = 8  # Number of rounds you want to play

# Track hits for each monster
monster_lives = [5] * len(create_monsters())

while running:
    if in_menu:
        play_button_rect = draw_entry_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and play_button_rect.collidepoint(event.pos):
                in_menu = False
                game_over = False
                reset_game()
                current_round = 1  # Reset to first round

    elif not game_over:
        if not shooting:
            tartaruga.x = player_pos.x + 78
            tartaruga1.x = player_pos.x + 2
        if tartaruga.y < 0 or tartaruga1.y < 0:
            shooting = False

        screen.blit(bg_img, (0, 0))
        if shooting:
            screen.blit(tiro_img, tartaruga)
            screen.blit(tiro_img, tartaruga1)
            tartaruga.y -= 15
            tartaruga1.y -= 15

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and (len(monsters) == 0 or player_lives == 0):
                retry_button = draw_retry_button()
                if retry_button.collidepoint(event.pos):
                    reset_game()
                    in_menu = False
                    current_round = 1  # Reset to first round

        screen.blit(nave_img, player_pos)

        keys = pygame.key.get_pressed()
       
        if keys[pygame.K_LEFT]:
            player_pos.x -= 300 * dt
        if keys[pygame.K_RIGHT]:
            player_pos.x += 300 * dt
        if keys[pygame.K_UP]:
            if not shooting:
                tartaruga.y =  825
                tartaruga1.y = 825
            shooting = True

        if player_pos.x >= 580:
            player_pos.x = 580

        if player_pos.x <= 20:
            player_pos.x = 20

        # Move monsters left and right
        for i, monster in enumerate(monsters):
            move_counters[i] += 1
            if move_counters[i] >= move_intervals[i]:
                move_counters[i] = 0
                monsters[i].x += 30 * move_directions[i]  # Adjust the speed here as needed

            # Check if monsters reached screen edges and reverse direction
            if monsters[i].x <= 10:
                move_directions[i] = 1
            elif monsters[i].x >= screen.get_width() - 10:
                move_directions[i] = -1

        # Draw and update monsters
        for monster_index, monster in enumerate(monsters[:]):  # Create a copy of the list to modify while iterating
            screen.blit(monstro_img, monster)
            monster_rect = monstro_img.get_rect(topleft=monster)
            tiro_rect = tiro_img.get_rect(topleft=tartaruga).inflate(-20, -20)  # Reduce the size of the hitbox
            tiro1_rect = tiro_img.get_rect(topleft=tartaruga1).inflate(-20, -20)  # Reduce the size of the hitbox
            
            if monster_rect.colliderect(tiro_rect) or monster_rect.colliderect(tiro1_rect):
                # Decrease the monster's life points
                monster_lives[monster_index] -= 1
                # Add explosion effect
                explosion = Explosion(monster_rect.center)
                explosions.add(explosion)
                # Check if the monster has run out of lives
                if monster_lives[monster_index] <= 0:
                    monsters.remove(monster)  # Remove monster if it has no more lives

            # Randomly shoot bullets from monsters
            if current_round == 1:
                if random.random() < 0.005:
                    bullet = pygame.Vector2(monster.x + monstro_img.get_width() // 2, monster.y + monstro_img.get_height())
                    monster_bullets.append(bullet)

            if current_round == 2:
                if random.random() < 0.01:
                    bullet = pygame.Vector2(monster.x + monstro_img.get_width() // 2, monster.y + monstro_img.get_height())
                    monster_bullets.append(bullet)

            if current_round == 3:
                if random.random() < 0.015:
                    bullet = pygame.Vector2(monster.x + monstro_img.get_width() // 2, monster.y + monstro_img.get_height())
                    monster_bullets.append(bullet)

            if current_round == 4:
                if random.random() < 0.020:
                    bullet = pygame.Vector2(monster.x + monstro_img.get_width() // 2, monster.y + monstro_img.get_height())
                    monster_bullets.append(bullet)

            if current_round == 5:
                if random.random() < 0.025:
                    bullet = pygame.Vector2(monster.x + monstro_img.get_width() // 2, monster.y + monstro_img.get_height())
                    monster_bullets.append(bullet)

            if current_round == 6:
                if random.random() < 0.030:
                    bullet = pygame.Vector2(monster.x + monstro_img.get_width() // 2, monster.y + monstro_img.get_height())
                    monster_bullets.append(bullet)

            if current_round == 7:
                if random.random() < 0.035:
                    bullet = pygame.Vector2(monster.x + monstro_img.get_width() // 2, monster.y + monstro_img.get_height())
                    monster_bullets.append(bullet)

            if current_round == 8:
                if random.random() < 10:
                    bullet = pygame.Vector2(monster.x + monstro_img.get_width() // 2, monster.y + monstro_img.get_height())
                    monster_bullets.append(bullet)
                    
            



        
                

        # Update and draw monster bullets
        for bullet in monster_bullets[:]:
            bullet.y += 9
            screen.blit(tiro_img, bullet)
            if bullet.y > screen.get_height():
                monster_bullets.remove(bullet)
            
            # Check for collision with player
            nave_rect = nave_img.get_rect(topleft=player_pos).inflate(-20, -20)  # Reduce the size of the hitbox
            bullet_rect = tiro_img.get_rect(topleft=bullet).inflate(-20, -20)  # Reduce the size of the hitbox
            if nave_rect.colliderect(bullet_rect):
                player_lives -= 1
                monster_bullets.remove(bullet)
                if player_lives == 0:
                    game_over = True  # Set game_over flag when lives reach zero

        screen.blit(amongus_img, coelhoassado)

        # Draw lives
        lives_text = small_font.render(f'Lives: {player_lives}', True, (255, 255, 255))
        screen.blit(lives_text, (10, 50))

        # Draw round level
        draw_round_level(current_round)

        # Check if all monsters are gone
        if len(monsters) == 0:
            if current_round < max_rounds:
                current_round += 1
                monsters = create_monsters()  # Reset monsters for the next round
                monster_lives = [5] * len(monsters)  # Reset hit points for new monsters
            else:
                game_over = True  # If all rounds are completed, end the game

        if game_over:
            in_menu = True

        # Update explosions
        explosions.update()
        explosions.draw(screen)

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()