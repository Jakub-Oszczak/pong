from email.header import Header
import pygame as pg

pg.init()

WIDTH, HEIGHT = 700, 500
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 10
WINNING_SCORE = 10
FPS = 60
win = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Pong game")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (222, 148, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREYISH = (138, 132, 150)
GOLD = (138, 132, 150)
FONT = pg.font.SysFont("comicsans", 50)
WIN_FONT = pg.font.SysFont("comicsans", 28)

class Ball:
    MAX_VELOCITY = 5

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.x_vel = self.MAX_VELOCITY
        self.y_vel = 0

    def draw(self, win):
        pg.draw.circle(win, WHITE, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

class Paddle:
    STEP = 4

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pg.draw.rect(win, WHITE, (self.x, self.y, self.width, self.height))

    def move(self, up):
        if up:
            self.y -= self.STEP
        else:
            self.y += self.STEP

def handle_collision(ball, left_paddle, right_paddle):
    scaling_factor = ball.MAX_VELOCITY/(PADDLE_HEIGHT/2)
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.height/2
                ball.y_vel = -(middle_y - ball.y) * scaling_factor
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1 

                middle_y = right_paddle.y + right_paddle.height/2
                ball.y_vel = -(middle_y - ball.y) * scaling_factor

def move_paddles(keys, left_paddle, right_paddle):
    if keys[pg.K_w] and left_paddle.y - left_paddle.STEP >= 0:
        left_paddle.move(up=True)
    if keys[pg.K_s] and left_paddle.y + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)

    if keys[pg.K_UP] and right_paddle.y - right_paddle.STEP >= 0:
        right_paddle.move(up=True)
    if keys[pg.K_DOWN] and right_paddle.y + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)

def reset(ball, left_paddle, right_paddle):
    ball.y_vel = 0
    ball.x_vel *= -1
    ball.x = WIDTH/2
    ball.y = HEIGHT/2
    left_paddle.y = HEIGHT//2 - PADDLE_HEIGHT//2
    right_paddle.y = HEIGHT//2 - PADDLE_HEIGHT//2
    scored = True
    return scored

def update_score(ball, left_paddle, right_paddle, left_score, right_score):
    scored = False
    if ball.x <= 0:
        right_score += 1
        scored = reset(ball, left_paddle, right_paddle)
    elif ball.x >= WIDTH:
        left_score += 1
        scored = reset(ball, left_paddle, right_paddle)
    return right_score, left_score, scored
    
def draw(win, paddles, ball, right_score, left_score):
    win.fill(BLACK)

    for paddle in paddles:
        paddle.draw(win)
    
    for i in range(HEIGHT//50, HEIGHT, HEIGHT//10):
        pg.draw.rect(win, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))

    score_text = FONT.render(f'{left_score}     {right_score}', 1, BLUE)
    win.blit(score_text, (WIDTH/2 - score_text.get_width()/2, 15))

    ball.draw(win)
    pg.display.update()

def main():
    run = True
    clock = pg.time.Clock()

    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS)
    right_score = 0
    left_score = 0
    scored = False

    while run:
        clock.tick(FPS)
        draw(win, [left_paddle, right_paddle], ball, right_score, left_score)
        if scored:
            pg.time.delay(1000)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break
        
        keys = pg.key.get_pressed()
        move_paddles(keys, left_paddle, right_paddle)
        ball.move()
        handle_collision(ball, left_paddle, right_paddle)
        right_score, left_score, scored = update_score(ball, left_paddle, right_paddle, left_score, right_score)
        if right_score == WINNING_SCORE:
            right_score = 0
            left_score = 0
            reset(ball, left_paddle, right_paddle)
            right_win_text = WIN_FONT.render('RIGHT PLAYER WON', 1, RED)
            win.blit(right_win_text, (WIDTH/2 + 20, HEIGHT/2 - right_win_text.get_height()))
            pg.display.update()
            pg.time.delay(3500)
        elif left_score == WINNING_SCORE:
            right_score = 0
            left_score = 0
            reset(ball, left_paddle, right_paddle)
            left_win_text = WIN_FONT.render('LEFT PLAYER WON', 1, RED)
            win.blit(left_win_text, (WIDTH/2 - left_win_text.get_width() - 20, HEIGHT/2 - left_win_text.get_height()))
            pg.display.update()
            pg.time.delay(3500)


    pg.quit()

if __name__ == '__main__':
    main()