import pygame
import os
import random
pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
STICK_C = (168, 111, 50)
BACKGROUND_C = (112, 101, 214)
BACKGROUND_CC = (217, 192, 124)

class Game:
    def __init__(self):
        self.WIDTH, self.HEIGHT = 1000, 600
        self.BALL_W, self.BALL_H = 30, 30
        self.stick_w, self.stick_h = 20, 150
        self.player_score, self.AI_score = 0, 0
        self.final_score = 10

        self.win = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("PONG GAME...")
        self.image = pygame.transform.scale(pygame.image.load(
            os.path.join('Assets', 'ball.png')), (self.BALL_W, self.BALL_H))

        self.start = pygame.mixer.Sound(os.path.join('Assets', 'game_start.wav'))
        self.hit = pygame.mixer.Sound(os.path.join('Assets', 'hit.wav'))
        self.end = pygame.mixer.Sound(os.path.join('Assets', 'game_over.wav'))

        self.ball = pygame.Rect(600, 350, self.BALL_W, self.BALL_H)
        self.stick_1 = pygame.Rect(0, 350, self.stick_w, self.stick_h)
        self.stick_2 = pygame.Rect(980, 350, self.stick_w, self.stick_h)
        self.ball_vx = 0
        self.ball_vy = random.choice((-2, 2))

        self.box = []
        button = pygame.Rect(250, self.HEIGHT//2 - 30, 150, 60)
        self.box.append(button)
        button = pygame.Rect(450, self.HEIGHT//2 - 30, 150, 60)
        self.box.append(button)
        button = pygame.Rect(650, self.HEIGHT//2 - 30, 150, 60)
        self.box.append(button)


    def draw(self):
        self.win.fill(BACKGROUND_CC)
        self.win.blit(self.image, (self.ball.x, self.ball.y))
        pygame.draw.rect(self.win, STICK_C, self.stick_1)
        pygame.draw.rect(self.win, STICK_C, self.stick_2)

        font = pygame.font.SysFont('comicsans', 30)
        display_text = "Player Score: " + str(self.player_score)
        text = font.render(display_text, 1, WHITE)
        self.win.blit(text, (20, 0))
        display_text = "Computer Score: " + str(self.AI_score)
        text = font.render(display_text, 1, WHITE)
        self.win.blit(text, (self.WIDTH - text.get_width()-50, 0))
        pygame.display.update()


    def draw_winner(self, text):
        self.win.fill(WHITE)
        font = pygame.font.SysFont('comicsans', 100)
        dis_text = font.render(text, 1, BLACK)
        self.win.blit(dis_text, (self.WIDTH/2 - dis_text.get_width()/2, self.HEIGHT/2 - dis_text.get_height()/2))
        font = pygame.font.SysFont('comicsans', 50)
        text = "Press ENTER to Play Again."
        dis_text = font.render(text, 1, BLACK)
        self.win.blit(dis_text, (self.WIDTH/2 - dis_text.get_width()/2, self.HEIGHT - 200 - dis_text.get_height()/2))
        pygame.display.update()

    def winner(self):
        if self.player_score == self.final_score or self.AI_score == self.final_score:
            pygame.time.delay(1000)
            self.end.play()
            text = "YOU WON!"
            if self.AI_score ==  self.final_score:
                text = "COMPUTER WON!"
            
            FPS = 60
            clock = pygame.time.Clock()
            run = True
            while run:
                clock.tick(FPS)
                self.draw_winner(text)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN: 
                            obj = Game()
                            obj.play()
            
            pygame.quit()

    def ball_movement(self):
        collision_1 = pygame.Rect.colliderect(self.stick_1, self.ball)
        collision_2 = pygame.Rect.colliderect(self.stick_2, self.ball)

        if self.ball.x + self.BALL_W >= self.WIDTH:
            self.ball_vx *= -1
            self.player_score += 1
        if collision_1 or collision_2:
            self.ball_vx *= -1
            self.hit.play()
        if self.ball.x <= 0:
            self.ball_vx *= -1
            self.AI_score += 1
        if self.ball.y + self.BALL_H >= self.HEIGHT or self.ball.y <= 0:
            self.ball_vy *= -1

        self.ball.x += self.ball_vx
        self.ball.y += self.ball_vy


    def AI_player(self):
        if self.ball.x >= 500 and self.ball.x <= 550 and self.ball_vx > 0:
            self.stick_2.y = random.randint(self.ball.y - 5, self.ball.y + 5)
        if self.stick_2.y + self.stick_h > self.HEIGHT:
            self.stick_2.y = self.HEIGHT - self.stick_h
        if self.stick_2.y <= 0:
            self.stick_2.y = 0


    def draw_diff(self):
        self.win.fill(BACKGROUND_C)
        font = pygame.font.SysFont('comicsans', 50)
        text = font.render("Choose Difficulty!", 1, WHITE)
        self.win.blit(text, (300, 100))

        for i in range (3):
            pygame.draw.rect(self.win, WHITE, self.box[i])
        font = pygame.font.SysFont('comicsans', 20)
        text = font.render("EASY", 1, BLACK)
        self.win.blit(text, (self.box[0].x + 45, self.box[0].y + 15))
        text = font.render("MEDIUM", 1, BLACK)
        self.win.blit(text, (self.box[1].x + 30, self.box[1].y + 15))
        text = font.render("HARD", 1, BLACK)
        self.win.blit(text, (self.box[2].x + 45, self.box[2].y + 15))
        pygame.display.update()


    def difficulty(self):
        self.start.play()
        FPS = 60
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(FPS)
            self.draw_diff()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                if self.box[0].collidepoint(m_x, m_y):
                    return 5
                if self.box[1].collidepoint(m_x, m_y):
                    return 10
                if self.box[2].collidepoint(m_x, m_y):
                    return 15

        pygame.quit()

    def play(self):
        FPS = 60
        clock = pygame.time.Clock()
        speed = self.difficulty()
        self.ball_vx = random.choice((-speed, speed))
        run = True
        while run:
            clock.tick(FPS)
            self.draw()

            self.winner()
            self.AI_player()
            self.ball_movement()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                
            key_pressed = pygame.key.get_pressed()
            if key_pressed[pygame.K_UP] and self.stick_1.y >= 5:
                self.stick_1.y -= 5
            if key_pressed[pygame.K_DOWN] and self.stick_1.y + self.stick_h + 5 <= self.HEIGHT:
                self.stick_1.y +=5

        pygame.quit()


if __name__ == "__main__":
    obj = Game()
    obj.play()