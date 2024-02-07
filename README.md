# Drone Simulation with AI

## Environment

### Python version 3.8.0

- To use tensorflow, python version must be under 3.11 | standard 2023.11.23.
  I tried to make the tensorflow model, but it made error I didn't solve.
  So, I decide to make the model by numpy.
  As a result...we just use python version over 3.

- I use the virtual environment
  - .gitignore -> /venv

### Library

| Purpose     | Library Name |
| ----------- | ------------ |
| Game Engine | pygame       |
| Math        | math         |
| ETC         | sys          |

## I. Physics

- Reference: Verlet Algorithm
  <br> This algorithm works as tree structure that node is vertex and trunk is side.

## II. Drone Structure

  The table shows how the nodes are connected.

|     | 0   | 1   | 2   | 3   | 4   | 5   |
| --- | --- | --- | --- | --- | --- | --- |
| 0   | 0   | 1   | 1   | 1   | 1   | 0   |
| 1   | 1   | 0   | 1   | 1   | 1   | 1   |
| 2   | 1   | 1   | 0   | 1   | 1   | 1   |
| 3   | 1   | 1   | 1   | 0   | 0   | 1   |
| 4   | 1   | 1   | 1   | 0   | 0   | 1   |
| 5   | 0   | 1   | 1   | 1   | 1   | 0   |

## III. CNN Structure

- Input Layer (8 inputs)
- Hidden Layer (20 nodes)
- Hidden Layer (20 nodes)
- Output Layer (4 outputs)

### Input Layer Structure

[UP, STOP, LEFT, RIGHT, UP-weight, STOP-weight, LEFT-weight, RIGHT-weight]

## IV. Learning Attempt

### 1. Version 1.0 - 2024.02.07.
Since the weight ratio of UP, STOP, LEFT, and RIGHT increases in multiples of 0.2, 
the drone should move left and right, but it tends to move only up and down.

I tried to solve this problem by calculating a multiple of 100px, 
which is the standard length on the top, bottom, left and right * as the default weight value, 
but due to acceleration up and down, the weight value was focused on UP and STOP.

This seems to be possible to solve by adjusting the weight values ​​on the left and right.