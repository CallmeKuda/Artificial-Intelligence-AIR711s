# Home Cleaning Robot & Traveling Salesman Problem Solver
## Description

### This repository contains the implementation of two algorithms:

1. A* search algorithm for a home cleaning robot navigating in a rectangular environment with obstacles.
   
![image](https://github.com/CallmeKuda/Artificial-Intelligence-AIR711s/assets/84506806/8224fc6e-4963-439e-a2a3-75ccab847c65)

Constants defined for the **grid cell size**, **obstacle representation**, and **cleaned cell representation**, respectively.

![image](https://github.com/CallmeKuda/Artificial-Intelligence-AIR711s/assets/84506806/56dedb5d-31ed-4d5c-8c69-6514a389758d)

The Environment class represents the grid environment where the cleaning robot operates. 
It has methods to initialize the environment with obstacles, check if a cell is an obstacle or cleaned, 
mark a cell as cleaned, and draw the environment on the screen using turtle graphics.

![image](https://github.com/CallmeKuda/Artificial-Intelligence-AIR711s/assets/84506806/7aca30ed-0037-4e39-951d-abd6336b1995)

The _CleaningRobotTurtle_ class, which represents the cleaning robot as a turtle. It has methods to initialize the robot, move it forward, turn left, and turn right. The robot keeps track of its position, orientation, and interacts with the environment to clean cells

![image](https://github.com/CallmeKuda/Artificial-Intelligence-AIR711s/assets/84506806/498c1d76-daf0-467e-9b5d-2d8d007fa62d)

This part sets up the GUI window using Turtle. It creates an environment with obstacles,
creates a cleaning robot, and sets up keyboard controls for the robot's movements.
Then, it starts the event loop to listen for user input and update the simulation accordingly.


![image](https://github.com/CallmeKuda/Artificial-Intelligence-AIR711s/assets/84506806/3b519065-6276-46bd-9c6c-01ceb07a6956)

This is the result of the envirnoment creation

2.This repository explores the application of the Hill climbing algorithm for solving the Traveling Salesman Problem (TSP) in the context of visiting various places in Windhoek. The objective is to visit a set of places exactly once, returning to the starting point, while minimizing total travel distance.
