import pygame
import math

pygame.init()

FPS = 60 # Frames per second setting
fpsClock = pygame.time.Clock()
GRAVITY = 9.8

# Font
font = pygame.font.Font(None, 24)

Colour = {
    "BlACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "RED": (255, 0, 0)
}

Graph = [
    [0, 1, 1, 1, 1, 0],
    [1, 0, 1, 1, 1, 1],
    [1, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 0, 1],
    [1, 1, 1, 0, 0, 1],
    [0, 1, 1, 1, 1, 0]
]

angle = 90
left_boost = 9.8 * 6
right_boost = 9.8 * 6

Title = "Drone Project"
# Set up the window 
WIDTH = 500
HEIGHT = 500

screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption(Title)
"""
Node
"""
class Node:
    def __init__(self, x, y, colour):
        self.x = x
        self.y = y
        self.oldx = x
        self.oldy = y
        self.newx = x
        self.newy = y
        self.ax = 0
        self.ay = GRAVITY

        self.colour = colour

        self.selected = False
        self.fixed = False

    def update(self, delta_t):
        if self.fixed == False:
            # Collision Process
            if self.x < 0 or self.x > WIDTH:
                self.x, self.oldx = self.oldx, self.x
            if self.y < 0 or self.y > HEIGHT:
                self.y, self.oldy = self.oldy, self.y

            # Verlet Integration
            self.newx = 2.0 * self.x - self.oldx + self.ax * delta_t * delta_t 
            self.newy = 2.0 * self.y - self.oldy + self.ay * delta_t * delta_t 
            self.oldx = self.x
            self.oldy = self.y
            self.x = self.newx
            self.y = self.newy

        if self.selected:
            pos = pygame.mouse.get_pos()
            self.x = pos[0]
            self.y = pos[1]

        if mouse == False:
            self.selected = False

    def draw(self, surf, size):
        if self.selected == True:
            color = self.colour[1]
        else:
            color = self.colour[0]
        pygame.draw.circle(surf, color, (int(self.x), int(self.y)), size)

    def show_info(self):
        return (self.x, self.y)
    
    def change_boost(self, ax, ay):
        self.ax = ax
        self.ay = ay # GRAVITY - ay
"""
Constraint -> trunk
"""
class Constraint:
    def __init__(self, index0, index1):
        self.index0 = index0
        self.index1 = index1
        delta_x = Nodes[index0].x - Nodes[index1].x
        delta_y = Nodes[index0].y - Nodes[index1].y
        self.restLength = math.sqrt(delta_x * delta_x + delta_y * delta_y)

    def update(self):
        delta_x = Nodes[self.index1].x - Nodes[self.index0].x
        delta_y = Nodes[self.index1].y - Nodes[self.index0].y
        deltaLength = math.sqrt(delta_x * delta_x + delta_y * delta_y)
        diff = (deltaLength - self.restLength)/(deltaLength + 0.001)

        if Nodes[self.index0].fixed == False:
            Nodes[self.index0].x += 0.5 * diff * delta_x
            Nodes[self.index0].y += 0.5 * diff * delta_y
        if Nodes[self.index1].fixed == False:
            Nodes[self.index1].x -= 0.5 * diff * delta_x
            Nodes[self.index1].y -= 0.5 * diff * delta_y

    def draw(self, surf, size):
        x0 = Nodes[self.index0].x
        y0 = Nodes[self.index0].y
        x1 = Nodes[self.index1].x
        y1 = Nodes[self.index1].y
        pygame.draw.line(surf, Colour["WHITE"], (int(x0), int(y0)), (int(x1), int(y1)), size)



def find_Node(pos):
    for i in range(len(Nodes)):
        dx = Nodes[i].x - pos[0]
        dy = Nodes[i].y - pos[1]
        if (dx * dx + dy * dy) < 400:
            Nodes[i].selected = True
            break

def show_info(title: str, data: float, x: int, y: int):
    text = font.render(f"{title}: {data}", True, Colour["WHITE"])
    textRect = text.get_rect()
    textRect.topleft = (x, y)
    screen.blit(text, textRect)

delta_t = 0.1
NUM_ITER = 10
mouse = False

# Create Nodes
Nodes = []

for i in range(4):
    x = 40.0 * math.cos(math.radians(90) * i + math.radians(45))
    y = 40.0 * math.sin(math.radians(90) * i + math.radians(45))
    if i in [0]: # 1, 2 angle x and y
        p = Node(WIDTH * 0.5 + x, HEIGHT * 0.9 + y, (Colour["RED"], Colour["RED"]))
        p.fixed = False
    else:
        p = Node(WIDTH * 0.5 + x, HEIGHT * 0.9 + y, (Colour["WHITE"], Colour["RED"]))
    Nodes.append(p)

x = 28.28427 * 3
y = 28.28427
p = Node(WIDTH * 0.5 - x, HEIGHT * 0.9 - y, (Colour["WHITE"], Colour["RED"]))
Nodes.append(p)

x = 28.28427 * 3
y = -28.28427
p = Node(WIDTH * 0.5 - x, HEIGHT * 0.9 - y, (Colour["RED"], Colour["RED"]))
Nodes.append(p)

constraints = []

for row in range(6):
    for column in range(row):
        if (Graph[row][column] == 1):
            constraints.append(Constraint(row, column))
"""
Rendering
"""
running = True
while running:
    screen.fill(Colour["BlACK"])

    # Constraints update
    for n in range(NUM_ITER):
        for i in range(len(constraints)):
            constraints[i].update()

    # Nodes draw
    for i in range(len(Nodes)):
        Nodes[i].draw(screen, 3)
    # Constraints draw
    for i in range(len(constraints)):
        constraints[i].draw(screen, 1)

    new_x, new_y = (0, 0)
    x, y = (0, 0)

    # Nodes update
    for i in range(len(Nodes)):
        if i == 1:
            new_x, new_y = Nodes[i].show_info()
            vec_x = left_boost * math.cos(angle)
            vec_y = GRAVITY - left_boost * math.sin(angle)
            # Nodes[i].change_boost(vec_x, vec_y)
        elif i == 2:
            x, y = Nodes[i].show_info()
            angle = math.atan2(new_y - y, new_x - x)
        vec_x = right_boost * math.cos(angle)
        vec_y = GRAVITY - right_boost * math.sin(angle)
        Nodes[i].change_boost(vec_x, vec_y)

        Nodes[i].update(delta_t)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = True
        if event.type == pygame.MOUSEBUTTONUP:
            mouse = False

    if mouse:
        pos = pygame.mouse.get_pos()
        find_Node(pos)

    show_info("Angle", round(math.degrees(angle), 3), 20, 20)
    show_info("LB", round(left_boost, 3), 20, 40)
    show_info("RB", round(right_boost, 3), 20, 60)

    pygame.display.update()
    fpsClock.tick(FPS)

pygame.quit()
