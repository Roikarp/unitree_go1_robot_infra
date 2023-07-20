#!/usr/bin/env python3
import pygame
from pygame.locals import *
import math
import webcolors
import copy

def get_color(name):
    try:
        rgb_tuple = webcolors.name_to_rgb(name)
        return rgb_tuple
    except ValueError:
        return None

class position:
    def __init__(self,x,y,v = 2,ang_v = 5,theta = 0):
        self.x = x
        self.y = y
        self.v = v
        self.theta = theta
        self.ang_v = ang_v;
    def __sub__(self, other):
        return position(self.x-other.x,self.y-other.y,self.v-other.v,self.theta-other.theta)
    def __add__(self, other):
        return position(self.x+other.x,self.y+other.y,self.v+other.v,self.theta+other.theta)
    def dist(self):
        return distance(self.x,self.y,0,0)
    def right(self):
        self.theta += self.ang_v;
    def left(self):
        self.theta -= self.ang_v;
    def forward(self):
        self.x += math.cos(math.radians(self.theta)) * self.v
        self.y += math.sin(math.radians(self.theta)) * self.v
    def backwards(self):
        self.x -= math.cos(math.radians(self.theta)) * self.v
        self.y -= math.sin(math.radians(self.theta)) * self.v



class visualizer:
    def __init__(self,vis_name,color,width,trail_color,trail_width,window,trail_len=400):
        self.vis_name = vis_name
        self.color = color
        self.width = width
        self.trail_color = trail_color
        self.trail_width = trail_width
        self.window   = window
        self.parent   = None
        self.trail    = [] # List to store previous positions of the dot
        self.trail_len = trail_len
    def update_trail(self,pos):
        self.trail.insert(0,pos)
        if len(self.trail)>self.trail_len:
            self.trail = self.trail[:self.trail_len]

    def draw(self):
        self.draw_trail()
        self.draw_shape()
    def draw_trail(self):
        for pos in self.trail:
            pygame.draw.circle(self.window, self.trail_color, (int(pos.x),int(pos.y)), self.trail_width)
    def draw_shape(self):
        if self.vis_name=='arrow':
            pygame.draw.polygon(self.window, self.color,
                [(
                    self.parent.pos.x + self.width * math.cos(math.radians(self.parent.pos.theta)),
                    self.parent.pos.y + self.width * math.sin(math.radians(self.parent.pos.theta))
                ),
                (
                    self.parent.pos.x + self.width * math.cos(math.radians(self.parent.pos.theta - 135)),
                    self.parent.pos.y + self.width * math.sin(math.radians(self.parent.pos.theta - 135))
                ),
                (
                    self.parent.pos.x + self.width * math.cos(math.radians(self.parent.pos.theta + 135)),
                    self.parent.pos.y + self.width * math.sin(math.radians(self.parent.pos.theta + 135))
                )])


class turtle:
    def __init__(self,pos,vis):
        self.pos        = pos
        self.vis        = vis
        self.vis.parent = self
    def right(self):
        self.pos.right()
    def left(self):
        self.pos.left()
    def forward(self):
        self.pos.forward()
    def backwards(self):
        self.pos.backwards()
    def update_trail(self):
        self.vis.update_trail(copy.copy(self.pos))
    def draw(self):
        self.vis.draw()

class follower(turtle):
    def __init__(self, pos, vis, master,offset = position(2,2)):
        turtle.__init__(self, pos, vis)
        self.master = master
        self.offset = offset
    def follow(self):
        target         = self.master.pos + self.offset - self.pos
        self.pos.theta = math.degrees(math.atan2(target.y,target.x))
        if target.dist() > 2:
            self.forward()


# Initialize Pygame
pygame.init()

# Define window dimensions
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

# Create the game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


# Define dot dimensions
DOT_RADIUS = 10
DOT_COLOR = get_color('red')  # Red color

# Define dot dimensions
TRAIL_RADIUS = 2
TRAIL_COLOR = get_color('red')

# Define movement speed and rotation angle
MOVEMENT_SPEED = 0.3
ROTATION_ANGLE = 0.6

# Define dot initial position, velocity, and orientation
human_pos = position(WINDOW_WIDTH // 2,WINDOW_HEIGHT // 2,MOVEMENT_SPEED,ROTATION_ANGLE)
human_vis = visualizer('arrow',DOT_COLOR,DOT_RADIUS,TRAIL_COLOR,TRAIL_RADIUS,window)
human = turtle(human_pos,human_vis)

# Define folower initial position, velocity, and orientation
robot_pos = position(WINDOW_WIDTH // 2,WINDOW_HEIGHT // 2,MOVEMENT_SPEED/2,ROTATION_ANGLE/2)
robot_vis = visualizer('arrow',get_color('blue'),10,get_color('blue'),2,window)
robot = follower(robot_pos,robot_vis,human)

pygame.display.set_caption("Robot Control")



# Function to calculate the distance between two points
def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Get the state of arrow keys
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        running = False

    if keys[K_UP]:
        human.forward()
    if keys[K_DOWN]:
        human.backwards()
    if keys[K_LEFT]:
        human.left()
    if keys[K_RIGHT]:
        human.right()
    # Add current position to the trail list
    human.update_trail()
    robot.update_trail()

    robot.follow()

    # Fill the window with a white background
    window.fill(get_color('white'))

    # Draw the dot trail on the window
    human.draw()
    robot.draw()


    # Update the window display
    pygame.display.update()

# Quit the game
pygame.quit()
