import pygame
import os

pygame.init()

height = 600
width = 1100
screen = pygame.display.set_mode((width,height))

rolling = [pygame.image.load(os.path.join("bola.png"))]

player = [pygame.image.load(os.path.join("player.png"))]

BG = [pygame.image.load(os.path.join("rumput.jpg"))]

class Ball:
    x_pos = 80
    y_pos = 310

    def __init__(self):
        self.roll_img = rolling

        self.ball_roll = True

        self.step_index = 0
        self.image = self.roll_img[0]
        self.ball_rect = self.image.get_rect()
        self.ball_rect.x = self.x_pos
        self.ball_rect.y = self.y_pos

    def update(self,userInput):
        if self.ball_roll:
            self.roll()

        # if self.step_index >= 10:
        #     self.step_index = 0

        if userInput[pygame.K_SPACE]:
            self.ball_roll = True
        
    def roll(self):
        self.ball_rect = self.image.get_rect()
        self.ball_rect.x = self.x_pos
        self.ball_rect.y = self.y_pos

    def draw(self,screen):
        screen.blit(self.image,(self.ball_rect.x,self.ball_rect.y))    


    def jump(self):
        pass

def main():
    roll = True
    clock = pygame.time.Clock()
    ball = Ball()
    while roll:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                roll = False

        screen.fill((255,255,255))
        userInput = pygame.key.get_pressed()

        ball.draw(screen)
        ball.update(userInput)

        clock.tick(30)
        pygame.display.update()


main()