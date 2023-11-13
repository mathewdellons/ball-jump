import pygame
import os
import random
pygame.init()

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

Rolling = [pygame.image.load(os.path.join("images/football.png")),
           pygame.image.load(os.path.join("images/football2.png"))]
Jumping = pygame.image.load(os.path.join("images/football3.png"))

Disturb = [pygame.image.load(os.path.join("images/football-goal.png")),
                pygame.image.load(os.path.join("images/pine-tree.png"))]

Balloon = pygame.image.load(os.path.join("images/balloon.png"))

BG = pygame.image.load(os.path.join("images/grass.png"))


class Ball:
    X_POS = 80
    Y_POS = 310
    JUMP_VEL = 8.5

    def __init__(self):
    
        self.roll_img = Rolling
        self.jump_img = Jumping

        self.ball_roll = True
        self.ball_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.roll_img[0]
        self.ball_rect = self.image.get_rect()
        self.ball_rect.x = self.X_POS
        self.ball_rect.y = self.Y_POS

    def update(self, userInput):
        if self.ball_roll:
            self.roll()
        if self.ball_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.ball_jump:
            self.ball_roll = False
            self.ball_jump = True
        elif not self.ball_jump:
            self.ball_roll = True
            self.ball_jump = False


    def roll(self):
        self.image = self.roll_img[self.step_index // 5]
        self.ball_rect = self.image.get_rect()
        self.ball_rect.x = self.X_POS
        self.ball_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.ball_jump:
            self.ball_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.ball_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.ball_rect.x, self.ball_rect.y))


class BALLOON:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = Balloon
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class Disturbance(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 1)
        super().__init__(image, self.type)
        self.rect.y = 290

def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    roll = True
    clock = pygame.time.Clock()
    player = Ball()
    Balloon = BALLOON()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 390
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while roll:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                roll = False

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 1) == 0:
                obstacles.append(Disturbance(Disturb))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.ball_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)

        background()

        Balloon.draw(SCREEN)
        Balloon.update()

        score()

        clock.tick(30)
        pygame.display.update()


def menu(death_count):
    global points
    roll = True
    while roll:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0, 0, 0))
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(Rolling[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                roll = False
            if event.type == pygame.KEYDOWN:
                main()


menu(death_count=0)