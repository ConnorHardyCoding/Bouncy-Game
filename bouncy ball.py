
import pygame
import random

class BouncyGame:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        self.window_height = 700
        self.window_width = 800
        self.window = pygame.display.set_mode((self.window_width, self.window_height))

        self.player_variables()
        self.enemy_variables()

        pygame.display.set_caption("Bouncy Game")

        self.main_loop()

    def main_loop(self):
        while True:
            self.check_events()
            self.draw_window()
            self.spawn_enemy()
            self.clock.tick(60)
    
    def player_variables(self):
        self.bouncy_ball_image = pygame.image.load("/Users/connorhardy/Documents/Coding_projects_CH/Bouncy Game/bouncy_ball.png")
        self.ball_x = self.window_width /2 - self.bouncy_ball_image.get_width()/2
        self.ball_y =  self.window_height - self.bouncy_ball_image.get_height()
        self.bouncy = self.Player(self.window, self.ball_x, self.ball_y, self.bouncy_ball_image, self.window_width, self.window_height)
    
    def enemy_variables(self):
        self.enemy_image = pygame.image.load("/Users/connorhardy/Documents/Coding_projects_CH/Bouncy Game/frog_enemy-export.png")
        self.enemy_x = 0
        self.enemy_y = self.window_height - self.enemy_image.get_height()
        self.spawn_timer = 0
        self.enemy_direction = ""
        self.enemy_orientation = ""
        self.enemies = []

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  # Ball left
                    self.bouncy.to_left = True
                if event.key == pygame.K_RIGHT:  # Ball right
                    self.bouncy.to_right = True
                if event.key == pygame.K_SPACE: # Jump
                    self.bouncy.is_jump = True
                if event.key == pygame.K_ESCAPE:
                    exit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.bouncy.to_left = False
                if event.key == pygame.K_RIGHT:
                    self.bouncy.to_right = False

            

    def draw_window(self):
        self.window.fill((255, 255, 255))

        # Draw and move player
        self.bouncy.move()
        self.bouncy.draw_player()

        for enemy in self.enemies:
            enemy.draw_enemy()
            enemy.move()

        pygame.display.flip()
    
    def spawn_enemy(self):
        if self.spawn_timer % 100 == 0:  # Spawn timer for enemy
            if random.randint(0,1) == 0:
                self.enemy_x = 0 - self.enemy_image.get_width()
                self.enemy_direction = "right"
            else:
                self.enemy_x = self.window_width + self.enemy_image.get_width()
                self.enemy_direction = "left"

            new_enemy = self.Enemy(self.window, self.enemy_x, self.enemy_y, self.enemy_image, self.window_width, self.window_height, self.enemy_direction)
            self.enemies.append(new_enemy)

        self.spawn_timer += 1
    
    class Player:
        def __init__(self, window, x, y, image, window_width, window_height):
            self.window = window
            self.window_width = window_width
            self.window_height = window_height
            self.image = image
            self.to_right = False
            self.to_left = False
            self.x = x
            self.y = y
            self.rect = self.image.get_rect(topleft=(self.x, self.y))
            self.is_jump = False
            self.jump_count = 10

        def draw_player(self):
            self.window.blit((self.image), (self.x, self.y))
        
        def move(self):
            if self.to_left:
                self.x -= 10
            if self.to_right:
                self.x += 10
            if self.x <= 0:  # Player can go past left screen
                self.x = 0
            if self.x >= self.window_width - self.image.get_width():  # Player cant go past right screen
                self.x = self.window_width - self.image.get_width()

            if self.is_jump:
                if self.jump_count >= -10:
                        self.y -= (self.jump_count * abs(self.jump_count)) * 0.5
                        self.jump_count -= 0.5
                else:
                    self.is_jump = False
                    self.jump_count = 10
    
    class Enemy(Player):
        def __init__(self, window, x, y, image, window_width, window_height, direction):
            super().__init__(window, x, y, image, window_width, window_height)
            self.spawn_count = 0
            self.direction = direction
            if self.direction == "right":
                self.image = pygame.transform.flip(self.image, True, False)
    
            self.is_jump = False    # Is frog jumping
            self.enemy_jump_count = 8   # Jump height/time variable

        def draw_enemy(self):
            self.window.blit(self.image, (self.x, self.y))
        
        def move(self):
            if self.direction == "right":
                self.x += 3
            if self.direction == "left":
                self.x -= 3

            if random.randint(1, 200) == 1:
                self.is_jump = True
            
            if self.is_jump:
                if self.enemy_jump_count >= -8:
                        self.y -= (self.enemy_jump_count * abs(self.enemy_jump_count)) * 0.5
                        self.enemy_jump_count -= 0.5
                else:
                    self.is_jump = False
                    self.enemy_jump_count = 8
    



BouncyGame()


