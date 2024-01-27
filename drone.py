import pygame
import random
import math
import numpy as np

# Window setup
WIDTH = 800
HEIGHT = 600
GRAVITY = 5
START_HEIGHT = 0.9 # topside is standard
REACTION = 0.0 # reaction rate; the more bigger, the less reaction

BOOST = 20

# Colour
Colour = {
    "BlACK": (0, 0, 0),
    "GRAY": (50, 50, 50),
    "WHITE": (255, 255, 255),
    "RED": (255, 0, 0)
}


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
        self.collision = False

    def update(self, delta_t):
        if self.fixed == False:
            # Collision Process
            if self.x < 0 or self.x > WIDTH:
                self.x, self.oldx = self.oldx * (1 - REACTION), self.x
                self.collision = True
            if self.y < 0 or self.y > HEIGHT:
                self.y, self.oldy = self.oldy * (1 - REACTION), self.y
                self.collision = True
            # Verlet Integration
            self.newx = 2.0 * self.x - self.oldx + self.ax * delta_t * delta_t 
            self.newy = 2.0 * self.y - self.oldy + self.ay * delta_t * delta_t 
            self.oldx = self.x
            self.oldy = self.y
            self.x = self.newx
            self.y = self.newy

    def draw(self, surf, size):
        if self.selected == True:
            color = self.colour[1]
        else:
            color = self.colour[0]
        pygame.draw.circle(surf, color, (int(self.x), int(self.y)), size)

    def get_info(self):
        return (self.x, self.y)

    def get_collision(self):
        return self.collision

    def change_boost(self, ax, ay):
        self.ax = ax
        self.ay = ay


"""
Constraint

connect nodes by graph.
"""
class Constraint:
    def __init__(self, index0, index1, Nodes):
        self.index0 = index0
        self.index1 = index1
        self.Nodes = Nodes
        delta_x = self.Nodes[index0].x - self.Nodes[index1].x
        delta_y = self.Nodes[index0].y - self.Nodes[index1].y
        self.restLength = math.sqrt(delta_x * delta_x + delta_y * delta_y)

    def update(self):
        delta_x = self.Nodes[self.index1].x - self.Nodes[self.index0].x
        delta_y = self.Nodes[self.index1].y - self.Nodes[self.index0].y
        deltaLength = math.sqrt(delta_x * delta_x + delta_y * delta_y)
        diff = (deltaLength - self.restLength) / (deltaLength + 0.001)

        if self.Nodes[self.index0].fixed == False:
            self.Nodes[self.index0].x += 0.5 * diff * delta_x
            self.Nodes[self.index0].y += 0.5 * diff * delta_y
        if self.Nodes[self.index1].fixed == False:
            self.Nodes[self.index1].x -= 0.5 * diff * delta_x
            self.Nodes[self.index1].y -= 0.5 * diff * delta_y

    # Draw a line between two points.
    def draw(self, surf, size):
        x0 = self.Nodes[self.index0].x
        y0 = self.Nodes[self.index0].y
        x1 = self.Nodes[self.index1].x
        y1 = self.Nodes[self.index1].y

        pygame.draw.line(surf, Colour["WHITE"], (int(x0), int(y0)), (int(x1), int(y1)), size)


"""
Target

drone's final destination and reward when it approach.
"""
class Target:
    def __init__(self, radius):
        self._LIMIT = 200

        self.x = random.randint(self._LIMIT, WIDTH - self._LIMIT)
        self.y = random.randint(self._LIMIT, HEIGHT - self._LIMIT / 2)
        self.radius = radius

    # Change location randomly
    def change_location(self):
        self.x = random.randint(self._LIMIT, WIDTH - self._LIMIT)
        self.y = random.randint(self._LIMIT, HEIGHT - self._LIMIT)

    # Check collision with drone
    def collision(self, x, y) -> bool:
        dist = math.sqrt(math.pow((self.x - x), 2) + math.pow((self.y - y), 2)) # distance; (x^2 + y^2)^(1/2)
        return (True if dist < self.radius else False)

    def draw(self, surf):
        pygame.draw.circle(surf, Colour["RED"], (int(self.x), int(self.y)), self.radius, 2)




class Drone:
    def __init__(self, screen, genome):
        self.screen = screen

        self.genome = genome

        # font
        self.font = pygame.font.Font(None, 22)

        self.l_margin = 20 # left-margin
        self.t_margin = 20 # top-margin

        # clock
        self.FPS = 60
        self.fpsClock = pygame.time.Clock()
        self.ticks = 0

        # constraint number
        self.NUM_ITER = 10

        self.Graph = [
            [0, 1, 1, 1, 1, 0],
            [1, 0, 1, 1, 1, 1],
            [1, 1, 0, 1, 1, 1],
            [1, 1, 1, 0, 0, 1],
            [1, 1, 1, 0, 0, 1],
            [0, 1, 1, 1, 1, 0]
        ]
        self.delta_t = 0.1

        self.reset()

    def reset(self):
        self.score = 0
        self.fitness = 0

        self.last_ticks = pygame.time.get_ticks()

        self.direction = 0 # Start direction is UP.

        self.Nodes = []
        self.constraints = []
        self.target = Target(30)

        self.angle = 0
        self.left_boost = BOOST
        self.right_boost = BOOST

        # Set nodes' position
        for i in range(4):
            x = 40.0 * math.cos(math.radians(90) * i + math.radians(45))
            y = 40.0 * math.sin(math.radians(90) * i + math.radians(45))

            if i == 0: # 1, 2 angle x and y
                p = Node(WIDTH * 0.5 + x, HEIGHT * START_HEIGHT + y, (Colour["RED"], Colour["RED"]))
                p.fixed = False
            else:
                p = Node(WIDTH * 0.5 + x, HEIGHT * START_HEIGHT + y, (Colour["WHITE"], Colour["RED"]))

            self.Nodes.append(p)

        x = 28.28427 * 3
        y = 28.28427
        p = Node(WIDTH * 0.5 - x, HEIGHT * START_HEIGHT - y, (Colour["WHITE"], Colour["RED"]))
        self.Nodes.append(p)

        x = 28.28427 * 3
        y = -28.28427
        p = Node(WIDTH * 0.5 - x, HEIGHT * START_HEIGHT - y, (Colour["RED"], Colour["RED"]))
        self.Nodes.append(p)

        # Connect constraints by 'graph'.
        for row in range(6):
            for column in range(row):
                if (self.Graph[row][column] == 1):
                    self.constraints.append(Constraint(row, column, self.Nodes))

    # Show infomation on window.
    def show_info(self, txt: str, x: int, y: int):
        text = self.font.render(txt, True, Colour["WHITE"])
        textRect = text.get_rect()
        textRect.topleft = (x, y)
        self.screen.blit(text, textRect)

    """
    Next step

    [ direction ]
    0 : UP    [0, 0, 0, 1] # start dircetion
    1 : STOP  [0, 0, 1, 0]
    2 : LEFT  [0, 1, 0, 0]
    3 : RIGHT [1, 0, 0, 0]
    """
    def go_up(self):
        self.right_boost = BOOST
        self.left_boost = BOOST

    def go_stop(self):
        self.right_boost = 0
        self.left_boost = 0

    def go_left(self):
        self.right_boost = BOOST
        self.left_boost = BOOST / 2

    def go_right(self):
        self.right_boost = BOOST / 2
        self.left_boost = BOOST

    # get input layer
    def get_input(self) -> np.array:
        result = [1., 1., 1., 1., 0., 0., 0., 0.]

        return np.array(result)

    def run(self):
        running = True
        while running:
            self.fpsClock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # key events
                if __name__=="__main__" and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.direction = 0
                    elif event.key == pygame.K_DOWN:
                        self.direction = 1
                    elif event.key == pygame.K_LEFT:
                        self.direction = 2
                    elif event.key == pygame.K_RIGHT:
                        self.direction = 3

            if self.direction == 0:   # UP
                self.go_up()
            elif self.direction == 1: # STOP
                self.go_stop()
            elif self.direction == 2: # LEFT
                self.go_left()
            elif self.direction == 3: # RIGHT
                self.go_right()


            new_x, new_y = (0, 0)
            x, y = (0, 0)
            centre_x, centre_y = (0, 0)

            """
            Update
            """
            # Update constraints
            for _ in range(self.NUM_ITER):
                for i in range(len(self.constraints)):
                    self.constraints[i].update()

            # Update nodes
            for i, node in enumerate(self.Nodes):
                # Reset condition
                # -40 < angle < 40
                if node.get_collision() or math.degrees(self.angle) >= 40 or math.degrees(self.angle) <= -40:
                    self.fitness -= 20
                    self.reset()

                # Get angle between two nodes; index number 1 and 2.
                if i == 1:
                    new_x, new_y = node.get_info()
                    centre_x = new_x
                    centre_y = new_y - 28
                elif i == 2:
                    x, y = node.get_info()
                    self.angle = math.atan2(new_y - y, new_x - x) - math.pi / 2 # get angle


                # Set right boost vector.
                if i == 0:
                    vec_x = self.right_boost * math.sin(self.angle)
                    # Since the force opposing the Earth's gravity is input, it was calculated by subtracting the value from the gravity. 
                    vec_y = GRAVITY - self.right_boost * math.cos(self.angle)
                    node.change_boost(vec_x, vec_y)

                # Set left boost vector.
                elif i == 5:
                    vec_x = self.left_boost * math.sin(self.angle)
                    # Since the force opposing the Earth's gravity is input, it was calculated by subtracting the value from the gravity. 
                    vec_y = GRAVITY - self.left_boost * math.cos(self.angle)
                    node.change_boost(vec_x, vec_y)

                node.update(self.delta_t)

            # Check collision with drone
            if self.target.collision(centre_x, centre_y):
                self.score += 1
                self.fitness += 10
                self.target.change_location()
            """
            Draw
            """
            # Draw background
            self.screen.fill(Colour["GRAY"])

            # Draw constraints
            for i in range(len(self.constraints)):
                self.constraints[i].draw(self.screen, 1)

            # Draw nodes
            for i in range(len(self.Nodes)):
                self.Nodes[i].draw(self.screen, 4)

            # Draw target
            self.target.draw(self.screen)

            # real-time clock
            self.ticks = pygame.time.get_ticks() - self.last_ticks
            millis = self.ticks % 1000
            seconds = int(self.ticks / 1000 % 60)
            minutes = int(self.ticks / 60000 % 24)

            self.show_info(f"Timer {minutes:02d}:{seconds:02d}:{millis}", 20, 20)
            """
            List format
            - text, parameter
            """
            display_list = [
                ["Score", self.score],
                ["Fitness", self.fitness],
                ["Angle", round(math.degrees(self.angle), 3)],
                ["LB", round(self.left_boost, 3)],
                ["RB", round(self.right_boost, 3)]
            ]
            for i, data in enumerate(display_list):
                self.show_info(f"{data[0]}: {data[1]}", self.l_margin, self.t_margin * (i + 2))

            pygame.display.update()

            if __name__!="__main__":

                return self.fitness, self.score

        pygame.quit()


if __name__=="__main__":
    pygame.init()
    pygame.font.init()

    Title = "Drone Project (User)"
    pygame.display.set_caption(Title)

    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

    drone = Drone(screen, genome=None)
    drone.run()