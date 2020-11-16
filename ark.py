import pygame
from random import randrange

#screen
FPS = 60
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

#colours
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,170,150)
BLUE = (0,0,255)
WHITE = (255, 255, 255)

#tiles
T_WIDTH = SCREEN_WIDTH/10
T_HEIGHT = SCREEN_HEIGHT/20

#paddle
MOVE = 10

### CLASSES ###

class Tile():
    def __init__(self, x_coord, y_coord):
        self.width = T_WIDTH-24
        self.height = T_HEIGHT-12
        self.colour = GREEN
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.destroyed = False

    def get_tile_size(self):
        return self.width, self.height

    def get_tile_coords(self):
        return self.x_coord, self.y_coord

    def get_tile_colour(self):
        return self.colour

    def if_destroyed(self):
        return self.destroyed

    def destroy(self):
        self.destroyed = True

    def draw_tile(self):
        tile_rect = pygame.Rect(self.x_coord, self.y_coord, self.width, self.height)
        return tile_rect

class Paddle():
    def __init__(self):
        self.width = SCREEN_WIDTH/5
        self.height = SCREEN_HEIGHT/30
        self.colour = BLUE
        self.x_coord = (SCREEN_WIDTH - self.width)/2
        self.y_coord = SCREEN_HEIGHT - self.height
        self.move_right = False
        self.move_left = False

    def get_paddle_size(self):
        return self.width, self.height

    def get_paddle_coords(self):
        return self.x_coord, self.y_coord

    def set_paddle_x_coord(self, new_x_coord):
        self.x_coord = new_x_coord

    def get_paddle_colour(self):
        return self.colour

    def get_move_right(self):
        return self.move_right

    def set_move_right(self, value):
        self.move_right = value

    def get_move_left(self):
        return self.move_left

    def set_move_left(self, value):
        self.move_left = value

    def draw_paddle(self):
        paddle_rect = pygame.Rect(self.x_coord, self.y_coord, self.width, self.height)
        return paddle_rect


class Ball():
    def __init__(self):
        self.width = SCREEN_WIDTH/60
        self.height = SCREEN_HEIGHT/60
        self.colour = WHITE
        self.x_coord = (SCREEN_WIDTH - self.width)/2
        self.y_coord = SCREEN_HEIGHT*9/10
        self.direction = [randrange(2, 5), 5]

    def get_ball_size(self):
        return self.width, self.height

    def get_ball_coords(self):
        return self.x_coord, self.y_coord

    def get_ball_colour(self):
        return self.colour

    def get_direction(self):
        return self.direction

    def change_direction(self, axis):
        if axis == "x":
            old_direction = self.direction[0]
            self.direction[0] = old_direction*-1
        elif axis == "y":
            old_direction = self.direction[1]
            self.direction[1] = old_direction*-1
        else: print("direction is different than x or y")

    def set_ball_coords(self, new_x_coord, new_y_coord):
        self.x_coord = new_x_coord
        self.y_coord = new_y_coord

    def draw_ball(self):
        ball_rect = pygame.Rect(self.x_coord, self.y_coord, self.width, self.height)
        return ball_rect

### GLOBAL FUNCTIONS ###

#change ball direction
def new_direction(ball, ball_rect, object):
    if type(object) is Paddle:
        object_rect = object.draw_paddle()
    elif type(object) is Tile:
        object_rect = object.draw_tile()
    else: print("wrong type of object given")
    if abs(ball_rect.bottom - object_rect.top) < 6 and ball.direction[1] < 0:
        print("dziala")
        ball.change_direction("y")
    if abs(ball_rect.top - object_rect.bottom) < 6 and ball.direction[1] > 0:
        print("dziala")
        ball.change_direction("y")
    if abs(ball_rect.left - object_rect.right) < 6 and ball.direction[0] > 0:
        print("dziala")
        ball.change_direction("x")
    if abs(ball_rect.right - object_rect.left) < 6 and ball.direction[0] < 0:
        print("dziala")
        ball.change_direction("x")
    return True

def update_direction():
    old_coords = ball.get_ball_coords()
    old_direction = ball.get_direction()

    #check for collision with side walls
    if old_coords[0]-old_direction[0] < 0 or old_coords[0]-old_direction[0] > SCREEN_WIDTH - ball.get_ball_size()[0]:
        ball.change_direction("x")
        return True
    #check for collision with upper wall
    elif old_coords[1]-old_direction[1] < 0:
        ball.change_direction("y")
        return True
    #check for collision with paddle
    elif ball_rect.colliderect(paddle_rect):
        paddle_coords = paddle.get_paddle_coords()
        happened = new_direction(ball, ball_rect, paddle)
        return True
    #check for collision with tiles
    coll_list = ball_rect.collidelistall(tiles_rect)
    if len(coll_list) > 0:
        for index in coll_list:
            if tiles[index].if_destroyed():
                pass
            else:
                happened = new_direction(ball, ball_rect, tiles[index])
                tiles[index].destroy()
        return True
    else: return False

### CREATING OBJECTS ###

#create tiles
tiles = []
for i in range(int(SCREEN_WIDTH/T_WIDTH)):
    for j in range(int(SCREEN_HEIGHT/(3*T_HEIGHT))):
        tiles.append(Tile(i*T_WIDTH+1, j*T_HEIGHT+1))

#create paddle
paddle = Paddle()

#create ball
ball = Ball()

### GAME ###

#initialize display
pygame.init()
gameDisplay = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock =  pygame.time.Clock()

#main loop
while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()
            elif event.key == pygame.K_RIGHT:
                paddle.set_move_right(True)
                # paddle.set_move_left(False)
            elif event.key == pygame.K_LEFT:
                paddle.set_move_left(True)
                # paddle.set_move_right(False)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                paddle.set_move_right(False)
            elif event.key == pygame.K_LEFT:
                paddle.set_move_left(False)

    gameDisplay.fill(BLACK)

    #show tiles
    tiles_rect = []
    for i in range(len(tiles)):
        tile_rect = tiles[i].draw_tile()
        tiles_rect.append(tile_rect)
        if tiles[i].if_destroyed():
            pass
        else:
            pygame.draw.rect(gameDisplay, tiles[i].get_tile_colour(), tile_rect)

    #show paddle
    paddle_rect = paddle.draw_paddle()
    pygame.draw.rect(gameDisplay, paddle.get_paddle_colour(), paddle_rect)

    #show ball
    ball_rect = ball.draw_ball()
    pygame.draw.rect(gameDisplay, ball.get_ball_colour(), ball_rect)

    #move ball
    update_direction()
    ball.set_ball_coords(ball.get_ball_coords()[0]-ball.get_direction()[0], ball.get_ball_coords()[1]-ball.get_direction()[1])

    #move paddle
    if paddle.get_move_right():
        old_coords = paddle.get_paddle_coords()
        if old_coords[0]+MOVE <= SCREEN_WIDTH - paddle.get_paddle_size()[0]:
            paddle.set_paddle_x_coord(old_coords[0]+MOVE)
    elif paddle.get_move_left():
        old_coords = paddle.get_paddle_coords()
        if old_coords[0]-MOVE >= 0:
            paddle.set_paddle_x_coord(old_coords[0]-MOVE)

    #update display
    pygame.display.update()
    clock.tick(FPS)
