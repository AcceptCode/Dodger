import os
from random import randint
import pygame
import sys

pygame.init()
pygame.mixer.init()

os.chdir(os.path.dirname(os.path.abspath(__file__)))

screen = pygame.display.set_mode((800, 500))
logo = pygame.image.load("Assets\\Pics\\logo.ico")
pygame.display.set_caption("Dodger!")
pygame.display.set_icon(logo)

# GameState Handler
class GameState:
    def __init__(self):
        self.game_active = False
        self.hit = False
        self.reg_health = False
        self.refill_spawn = False
        self.counter = 0

    def play_bg_music(self, sound):
        pygame.mixer.music.load(sound)
        pygame.mixer.music.set_volume(0.03)
        pygame.mixer.music.play(-1)
    
    def play_beep_sound(self, sound):
        beep = pygame.mixer.Sound(sound)
        beep.set_volume(0.1)
        beep.play(loops=0)

    def play_end_sound(self, sound):
        beep = pygame.mixer.Sound(sound)
        beep.set_volume(0.1)
        beep.play(loops=0)

    def score(self, color, font, size, x, y, surf):
        current = int(pygame.time.get_ticks()/1000) - self.counter
        score = pygame.font.Font(font, size)
        score_surf = score.render(f"Time Passed: {current}", True, color)
        sc_rect = score_surf.get_rect(center=(x, y))

        surf.blit(score_surf, sc_rect)


    def update_cars(self, window):
        enemy.screen_update(window)
        enemy1.screen_update(window)
        enemy2.screen_update(window)
        enemy3.screen_update(window)

    def collide(self, rect):
        enemy.check_collide(rect)
        enemy1.check_collide(rect)
        enemy2.check_collide(rect)
        enemy3.check_collide(rect)

    def start_game(self):
        if game_state.reg_health:
            player.health = 100
            game_state.reg_health = False
        keys_pressed = pygame.key.get_pressed()
        screen.fill("#694414")
        road.update_screen()
        player.draw(screen)
        player.movement(keys_pressed)
        game_state.score((255, 0, 0), None, 50, 135, 85, screen)
        game_state.update_cars(screen)
        player.check_health()
        game_state.collide(player.player_rect)
        healthbar.update_blit(screen)

class Road(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        super().__init__()
        self.road = pygame.image.load(img).convert_alpha()
        self.road_rect = self.road.get_rect()
        self.road_rect.center = (x, y)
    
    def update_screen(self):
        screen.blit(self.road, self.road_rect)

class HealthBar(pygame.sprite.Sprite):
    def __init__(self, img, x, y, font_type, text_size, txt_color, txt_x, txt_y):
        self.healthbarimg = pygame.transform.scale(pygame.image.load(img), (150,20)).convert_alpha()
        self.health_rect = self.healthbarimg.get_rect(center=(x, y))
        self.font_type = font_type
        self.text_size = text_size
        self.txt_x = txt_x
        self.txt_y = txt_y
        self.txt_color = txt_color

    def update_blit(self, surface):
        surface.blit(self.healthbarimg, self.health_rect)
        font_health = pygame.font.Font(self.font_type, self.text_size)
        font_render1 = font_health.render(f"{player.health}", False, self.txt_color)
        rect_font = font_render1.get_rect(center=(self.txt_x, self.txt_y))
        surface.blit(font_render1, rect_font)


class Intro(pygame.sprite.Sprite):
    def __init__(self, image, image_x, image_y, width, height):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image), (width, height)).convert_alpha()
        self.image_rect = self.image.get_rect(topleft=(image_x, image_y))
    
    def update(self, listen_keys):
        """
        Listens for key press, then destroys the intro sprite
        """
        screen.blit(self.image, self.image_rect)
        if listen_keys[pygame.K_x]:
            game_state.game_active = True
            game_state.reg_health = True
            enemy.enemy_rect.y = -100
            enemy1.enemy_rect.y = -100
            enemy2.enemy_rect.y = -100
            enemy3.enemy_rect.y = -100
            enemy4.enemy_rect.y = -100


class PlayerCar(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image_path), (45, 100)).convert_alpha()
        self.player_rect = self.image.get_rect(center=(x, y))
        self.health = 100
        self.vel = 5.8
    
    def draw(self, surface):
        surface.blit(self.image, self.player_rect)

    def movement(self, keys):
        if keys[pygame.K_RIGHT] and self.player_rect.x < 573:
            self.player_rect.x += self.vel
        elif keys[pygame.K_LEFT] and self.player_rect.x > 150:
            self.player_rect.x -= self.vel

    def check_health(self):
        if self.health >= 100:
            healthbar.healthbarimg = pygame.image.load("Assets\\Pics\\100.png")
        if self.health <= 75:
            healthbar.healthbarimg = pygame.image.load("Assets\\Pics\\75.png")
        if self.health <= 50:
            healthbar.healthbarimg = pygame.image.load("Assets\\Pics\\50.png")
        if self.health <= 25:
            healthbar.healthbarimg = pygame.image.load("Assets\\Pics\\25.png")
        if self.health <= 0:
            healthbar.healthbarimg = pygame.image.load("Assets\\Pics\\empty.png")
# Enemy Class
class EnemyCar(pygame.sprite.Sprite):
    def __init__(self, img, x, y, max_x):
        super().__init__()
        self.x = randint(x, 200)
        self.last_hit = pygame.time.get_ticks()
        self.cool = 1000
        self.max_x = max_x
        self.enemy = pygame.image.load(img).convert_alpha()
        self.enemy_rect = self.enemy.get_rect(center=(x, y))
        self.dmg = randint(10, 25)
        self.speed = randint(8, 10)
    
    def screen_update(self, surface):
        surface.blit(self.enemy, self.enemy_rect)
        self.enemy_rect.y += self.speed
        if self.enemy_rect.y > 530:
            self.enemy_rect.y = -100
            self.x = randint(self.x, 200)
            self.enemy_rect.x = randint(self.x, self.max_x)
            self.speed = randint(8, 10)
    
    def check_collide(self, sprite_rect):
        if player.health < 0:
            player.health = 0
            game_state.game_active = False
        if pygame.time.get_ticks() - self.last_hit > self.cool:
            if self.enemy_rect.colliderect(sprite_rect):
                game_state.play_beep_sound("Assets\\Sounds\\beep.ogg")
                game_state.hit = True
                self.last_hit = pygame.time.get_ticks()
                if game_state.hit:
                    if player.health > 0:
                        player.health -= self.dmg
                        game_state.hit = False
                        self.dmg = randint(10, 25)
                    if player.health <= 0:
                        game_state.play_end_sound("Assets\\Sounds\\end_game.ogg")
                        game_state.game_active = False
# Define all instances
game_state = GameState()
road = Road(400, 380, "Assets\\Pics\\road.png")
intr = Intro("Assets\\Pics\\intro_screen.png", 0, 0, 810, 950)
player = PlayerCar("Assets\\Pics\\car_player.png", 400, 450)
enemy = EnemyCar("Assets\\Pics\\car_enemy_red.png", 173, 200, 572)
enemy1 = EnemyCar("Assets\\Pics\\car_enemy_red.png", 173, 200, 572)
enemy2 = EnemyCar("Assets\\Pics\\car_enemy_red.png", 173, 200, 572)
enemy3 = EnemyCar("Assets\\Pics\\car_enemy_red.png", 173, 200, 572)
enemy4 = EnemyCar("Assets\\Pics\\car_enemy_red.png", 173, 200, 572)
healthbar = HealthBar("Assets\\Pics\\100.png", 80, 20, None, 50, "#006963", 120, 38)
clck = pygame.time.Clock()


game_state.play_bg_music("Assets\\Sounds\\bg.ogg")
while True:
    clck.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if game_state.game_active:
        game_state.start_game()
    else:
        # intro
        keys = pygame.key.get_pressed()
        intr.update(keys)
        game_state.counter = int(pygame.time.get_ticks()/1000)
    pygame.display.update()
