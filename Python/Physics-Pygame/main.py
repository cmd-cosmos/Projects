import pygame
import numpy as np

# Window Setup
pygame.init()
width = 1000
height = 800
screen = pygame.display.set_mode([width,height])
fps = 60
timer = pygame.time.Clock()

# Game Vars
wall_thickness = 10
gravity = 0.5
bounce_bounds = 0.2

mouse_trajectory = []

# Game Functions
def draw_wall():
    left = pygame.draw.line(screen, 'brown1', (0,0), (0,height), wall_thickness)
    right = pygame.draw.line(screen, 'brown1', (width,0), (width,height), wall_thickness)
    top = pygame.draw.line(screen, 'brown1', (0,0), (width,0), wall_thickness)
    bottom = pygame.draw.line(screen, 'brown1', (0,height), (width,height), wall_thickness)
    walls = [left,right,top,bottom]
    return walls

def calc_motion_vector():
    x_speed = 0
    y_speed = 0

    if len(mouse_trajectory) > 10:
        x_speed = (mouse_trajectory[-1][0] - mouse_trajectory[0][0]) / len(mouse_trajectory)
        y_speed = (mouse_trajectory[-1][1] - mouse_trajectory[0][1]) / len(mouse_trajectory)
    return x_speed, y_speed


# Custom Classes
class Ball:
    def __init__(self, id, color, radius, mass, x_position,y_position,x_speed, y_speed, retention, friction):
        self.id = id
        self.color = color
        self.radius = radius
        self.mass = mass
        self.x_position = x_position
        self.y_position = y_position
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.retention = retention # energy retention post bounce or impact ---> expressed in percentage ---> 0.9 == 90% retention of energy
        self.circle = None
        self.selected = False
        self.friction = friction
    
    def draw(self):
        self.circle = pygame.draw.circle(screen, self.color, (self.x_position,self.y_position), self.radius)

    def gravity(self):
        if not self.selected:
            if self.y_position < height - self.radius - (wall_thickness/2):
                self.y_speed += gravity
            else:
                if self.y_speed > bounce_bounds:
                    self.y_speed = self.y_speed * (-1)* self.retention # ensures flip in direction to up
                else:
                    if abs(self.y_speed) <= bounce_bounds:
                        self.y_speed = 0
                
            if (self.x_position < self.radius + (wall_thickness/2) and self.x_speed < 0) or (self.x_position > width - self.radius - (wall_thickness/2) and self.x_speed > 0):
                self.x_speed *= -1 *self.retention
                if abs(self.x_speed) < bounce_bounds:
                    self.x_speed = 0
            if self.y_speed == 0 and self.x_speed != 0:
                if self.x_speed > 0:
                    self.x_speed -= self.friction
                elif self.x_speed < 0:
                    self.x_speed += self.friction
        
        else: # reset speed when released
            self.x_speed = x_push
            self.y_speed = y_push
        
        return self.y_speed
    
    def update_position(self, mouse):
        if not self.selected:
            self.y_position += self.y_speed
            self.x_position += self.x_speed

        else:
            self.x_position = mouse[0]
            self.y_position = mouse[1]
        

    def check_select(self, position):
        self.selected = False
        if self.circle.collidepoint(position):
            self.selected = True # ensures mouse in contact with the ball shape
        return self.selected


# Custom Objects
ball1 = Ball(1, 'blue', 25, 50, 100, 100, 0, 5, 0.85, 0.02)
ball2 = Ball(2, 'green', 35, 80, 300, 100, 0, 2, 0.78, 0.025)
ball3 = Ball(3, 'yellow', 45, 120, 600, 100, 0, 3, 0.9, 0.018)
ball4 = Ball(4, 'white', 55, 150, 850, 150, 0, 0, 0.75, 0.03)

balls = [ball1,ball2, ball3, ball4]

# Game Loop
flag = True

while flag:
    timer.tick(fps)
    screen.fill('black')
    mouse_coordinates = pygame.mouse.get_pos()
    mouse_trajectory.append(mouse_coordinates)
    if len(mouse_trajectory) > 20:
        mouse_trajectory.pop(0)
    x_push, y_push = calc_motion_vector()
    walls = draw_wall()
    ball1.draw()
    ball2.draw()
    ball3.draw()
    ball4.draw()
    ball1.update_position(mouse_coordinates)
    ball2.update_position(mouse_coordinates)
    ball3.update_position(mouse_coordinates)
    ball4.update_position(mouse_coordinates)
    ball1.y_speed = ball1.gravity()
    ball2.y_speed = ball2.gravity()
    ball3.y_speed = ball2.gravity()
    ball4.y_speed = ball2.gravity()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if ball1.check_select(event.pos) or ball2.check_select(event.pos) or ball3.check_select(event.pos) or ball4.check_select(event.pos):
                    active_select = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                active_select = False
                for i in range(len(balls)):
                    balls[i].check_select((10000,10000))                        
    pygame.display.flip()

pygame.quit()





