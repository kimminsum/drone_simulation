import pygame
import random
import math

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
Constraint -> trunk
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
    # draw line between two points.
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
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self._LIMIT = 70

    # change location randomly
    def change_location(self):
        self.x = random.randint(self._LIMIT, WIDTH - self._LIMIT)
        self.y = random.randint(self._LIMIT, WIDTH - self._LIMIT)

    def draw(self, surf):
        pygame.draw.circle(surf, Colour["RED"], (int(self.x), int(self.y)), self.radius, 2)


class Drone:
    def __init__(self, screen):
        self.screen = screen
        # Font
        self.font = pygame.font.Font(None, 22)

        # Clock
        self.FPS = 60
        self.fpsClock = pygame.time.Clock()

        """
        Drone Structure
        """
        # Constraints number
        self.NUM_ITER = 10

        self.Graph = [
            [0, 1, 1, 1, 1, 0],
            [1, 0, 1, 1, 1, 1],
            [1, 1, 0, 1, 1, 1],
            [1, 1, 1, 0, 0, 1],
            [1, 1, 1, 0, 0, 1],
            [0, 1, 1, 1, 1, 0]
        ]
        """
        Movement
        """
        self.angle = 0 # initial angle
        self.left_boost = BOOST
        self.right_boost = BOOST

        self.delta_t = 0.1
        self.Nodes = []
        self.constraints = []

        self.reset()

    def reset(self):
        """
        [ direction ]
        0 : UP    [0, 0, 0, 1] # start dircetion
        1 : STOP  [0, 0, 1, 0]
        2 : LEFT  [0, 1, 0, 0]
        3 : RIGHT [1, 0, 0, 0]
        """
        self.direction = 0

        self.Nodes = []
        self.constraints = []

        self.angle = 0
        self.left_boost = BOOST
        self.right_boost = BOOST
        # Set nodes' position
        for i in range(4):
            x = 40.0 * math.cos(math.radians(90) * i + math.radians(45))
            y = 40.0 * math.sin(math.radians(90) * i + math.radians(45))
            if i in [0]: # 1, 2 angle x and y
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
    """
    Show info on window.
    """
    def show_info(self, title: str, data: float, x: int, y: int):
        text = self.font.render(f"{title}: {data}", True, Colour["WHITE"])
        textRect = text.get_rect()
        textRect.topleft = (x, y)
        self.screen.blit(text, textRect)
    """
    Next step
    """
    def go_up(self):
        self.right_boost = BOOST
        self.left_boost = BOOST

    def go_right(self):
        self.right_boost = BOOST / 2
        self.left_boost = BOOST

    def go_left(self):
        self.right_boost = BOOST
        self.left_boost = BOOST / 2

    def go_stop(self):
        self.right_boost = 0
        self.left_boost = 0
    """
    Rendering
    """
    def run(self):
        running = True
        while running:
            self.screen.fill(Colour["GRAY"]) # make background colour black.

            # Constraints update
            for n in range(self.NUM_ITER):
                for i in range(len(self.constraints)):
                    self.constraints[i].update()
            """
            Draw objects
            """
            # Nodes draw
            for i in range(len(self.Nodes)):
                self.Nodes[i].draw(self.screen, 4)
            # Constraints draw
            for i in range(len(self.constraints)):
                self.constraints[i].draw(self.screen, 1)

            new_x, new_y = (0, 0)
            x, y = (0, 0)

            # Nodes update
            for i, node in enumerate(self.Nodes):
                # get angle between two nodes; index number 1 and 2.
                if i == 1:
                    new_x, new_y = node.get_info()
                elif i == 2:
                    x, y = node.get_info()
                    # print(f"Center: {new_x} {new_y - 28}")
                    self.angle = math.atan2(new_y - y, new_x - x) - math.pi / 2 # get angle

                # set right boost vector
                if i == 0:
                    vec_x = self.right_boost * math.sin(self.angle)
                    # Since the force opposing the Earth's gravity is input, it was calculated by subtracting the value from the gravity. 
                    vec_y = GRAVITY - self.right_boost * math.cos(self.angle)
                    node.change_boost(vec_x, vec_y)
                # set left boost vector
                elif i == 5:
                    vec_x = self.left_boost * math.sin(self.angle)
                    # Since the force opposing the Earth's gravity is input, it was calculated by subtracting the value from the gravity. 
                    vec_y = GRAVITY - self.left_boost * math.cos(self.angle)
                    node.change_boost(vec_x, vec_y)

                node.update(self.delta_t) # update every change

                # reset condition
                if node.get_collision() or math.degrees(self.angle) >= 40 or math.degrees(self.angle) <= -40:
                    self.reset()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if __name__=="__main__":
                    # key events
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.direction = 0
                        elif event.key == pygame.K_DOWN:
                            self.direction = 1
                        elif event.key == pygame.K_LEFT:
                            self.direction = 2
                        elif event.key == pygame.K_RIGHT:
                            self.direction = 3

            if self.direction == 0:
                self.go_up()
            elif self.direction == 1:
                self.go_stop()
            elif self.direction == 2:
                self.go_left()
            elif self.direction == 3:
                self.go_right()

            txt_margin = 20
            self.show_info("Score", 0, 20, txt_margin)
            self.show_info("Fitness", 0, 20, txt_margin * 2)
            self.show_info("Angle", round(math.degrees(self.angle), 3), 20, txt_margin * 3) # show angle infomation; degrees
            self.show_info("LB", round(self.left_boost, 3), 20, txt_margin * 4) # show left boost information
            self.show_info("RB", round(self.right_boost, 3), 20, txt_margin * 5) # show right boost information

            pygame.display.update()
            self.fpsClock.tick(self.FPS)

        pygame.quit() # end up program.


if __name__=="__main__":
    pygame.init()
    pygame.font.init()

    Title = "Drone Project (User)"
    pygame.display.set_caption(Title)

    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

    drone = Drone(screen)
    drone.run()