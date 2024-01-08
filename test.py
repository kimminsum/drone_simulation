import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation, rc

from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, ReLU
from tensorflow.python.keras.optimizer_v2.rmsprop import RMSprop

optimizer = RMSprop()

class Brain:
    def __init__(self, n_state, n_mid, n_action, gamma=0.9, r=0.99):
        self.eps = 1.0
        self.gamma = gamma
        self.r = r

        model = Sequential()
        model.add(Dense(n_mid, input_shape=(n_state,)))
        model.add(ReLU())
        model.add(Dense(n_mid))
        model.add(ReLU())
        model.add(Dense(n_action))
        model.compile(loss="mse", optimizer=optimizer)
        self.model = model

    def train(self, states, next_states, action, reward, terminal, next_action):
        q = self.model.predict(states)
        next_q = self.model.predict(next_states)
        t = np.copy(q)
        if terminal:
            t[:, action] = reward
        else:
            t[:, action] = reward + self.gamma * np.max(next_q, axis=1)
        self.model.train_on_batch(states, t)

    def get_action(self, states):
        q = self.model.predict(states)
        if np.random.rand() < self.eps:
            action = np.random.randint(q.shape[1], size=q.shape[0])
        else:
            action = np.argmax(q, axis=1)
        if self.eps > 0.1:
            self.eps *= self.r
        return action

class Agent:
    def __init__(self, v_x, v_y_sigma, v_jump, brain):
        self.v_x = v_x
        self.v_y_sigma = v_y_sigma
        self.v_jump = v_jump
        self.brain = brain
        self.reset()

    def reset(self):
        self.x = -1
        self.y = 0
        self.v_y = self.v_y_sigma * np.random.randn()
        states = np.array([[self.y, self.v_y]])
        self.action = self.brain.get_action(states)

    def step(self, g):
        states = np.array([[self.y, self.v_y]])
        self.x += self.v_x
        self.y += self.v_y

        reward = 0
        terminal = False
        if self.x > 1.0:
            reward = 1
            terminal = True
        elif self.y < -1.0 or self.y > 1.0:
            reward = -1
            terminal = True
        reward = np.array([reward])

        if self.action[0] == 0:
            self.v_y -= g
        else:
            self.v_y = self.v_jump
        next_states = np.array([[self.y, self.v_y]])

        next_action = self.brain.get_action(next_states)
        self.brain.train(states, next_states, self.action, reward, terminal, next_action)
        self.action = next_action

        if terminal:
            self.reset()
        states = np.array([[self.y, self.v_y]])
        self.x += self.v_x
        self.y += self.v_y

        reward = 0
        terminal = False
        if self.x > 1.0:
            reward = 1
            terminal = True
        elif self.y < -1.0 or self.y > 1.0:
            reward = -1
            terminal = True
        reward = np.array([reward])

        action = self.brain.get_action(states)
        if action[0] == 0:
            self.v_y -= g
        else:
            self.v_y = self.v_jump
        next_states = np.array([[self.y, self.v_y]])
        self.brain.train(states, next_states, action, reward, terminal, None)

        if terminal:
            self.reset()

class Environment:
    def __init__(self, agent, g):
        self.agent = agent
        self.g = g

    def step(self):
        self.agent.step(self.g)
        return (self.agent.x, self.agent.y)

def animate(environment, interval, frames):
    fig, ax = plt.subplots()
    plt.close()
    ax.set_xlim((-1, 1))
    ax.set_ylim((-1, 1))
    sc = ax.scatter([], [])

    def plot(data):
        x, y = environment.step()
        sc.set_offsets(np.array([[x, y]]))
        return (sc, )

    return animation.FuncAnimation(fig, plot, interval=interval, frames=frames)


n_state = 2
n_mid = 32
n_action = 2
brain = Brain(n_state, n_mid, n_action, r=1.0)

v_x = 0.05
v_y_sigma = 0.1
v_jump = 0.2
agent = Agent(v_x, v_y_sigma, v_jump, brain)

g = 0.2
environment = Environment(agent, g)

interval = 50
frames = 5024
anim = animate(environment, interval, frames)
rc("animation", html="jshtml")

anim.save("test.gif")