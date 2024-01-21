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

|     | 0   | 1   | 2   | 3   | 4   | 5   |
| --- | --- | --- | --- | --- | --- | --- |
| 0   | 0   | 1   | 1   | 1   | 1   | 0   |
| 1   | 1   | 0   | 1   | 1   | 1   | 1   |
| 2   | 1   | 1   | 0   | 1   | 1   | 1   |
| 3   | 1   | 1   | 1   | 0   | 0   | 1   |
| 4   | 1   | 1   | 1   | 0   | 0   | 1   |
| 5   | 0   | 1   | 1   | 1   | 1   | 0   |

## III. Input Layer

- left boost
- right boost
- angle
