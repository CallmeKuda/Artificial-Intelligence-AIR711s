import turtle

# Constants
CELL_SIZE = 40
OBSTACLE = 'X'
CLEANED = '.'

class Environment:
    def __init__(self, width, height, obstacles):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        self.populate_obstacles(obstacles)

    def populate_obstacles(self, obstacles):
        for obstacle in obstacles:
            x, y = obstacle
            self.grid[y][x] = OBSTACLE

    def is_obstacle(self, x, y):
        return self.grid[y][x] == OBSTACLE

    def is_cleaned(self, x, y):
        return self.grid[y][x] == CLEANED

    def clean_cell(self, x, y):
        self.grid[y][x] = CLEANED

    def draw(self, turtle):
        turtle.pensize(1)
        turtle.color('black')
        # Draw the grid
        for y in range(self.height):
            for x in range(self.width):
                turtle.penup()
                turtle.goto(x * CELL_SIZE, y * CELL_SIZE)
                turtle.pendown()
                for _ in range(4):
                    turtle.forward(CELL_SIZE)
                    turtle.left(90)
                # Fill in obstacles
                if self.is_obstacle(x, y):
                    turtle.fillcolor('grey')
                    turtle.begin_fill()
                    for _ in range(4):
                        turtle.forward(CELL_SIZE)
                        turtle.left(90)
                    turtle.end_fill()
        turtle.penup()

class CleaningRobotTurtle(turtle.Turtle):
    def __init__(self, environment):
        super().__init__()
        self.environment = environment
        self.orientation = 0 # 0: East, 90: North, 180: West, 270: South
        self.x = 0
        self.y = 0
        self.shape('square')
        self.color('blue')
        self.penup()
        self.goto(self.x * CELL_SIZE + CELL_SIZE / 2, self.y * CELL_SIZE + CELL_SIZE / 2)

    def move_forward(self):
        new_x, new_y = self.x, self.y
        if self.orientation == 0: # East
            new_x += 1
        elif self.orientation == 90: # North
            new_y += 1
        elif self.orientation == 180: # West
            new_x -= 1
        elif self.orientation == 270: # South
            new_y -= 1

        if 0 <= new_x < self.environment.width and 0 <= new_y < self.environment.height:
            if not self.environment.is_obstacle(new_x, new_y):
                self.x, self.y = new_x, new_y
                self.goto(self.x * CELL_SIZE + CELL_SIZE / 2, self.y * CELL_SIZE + CELL_SIZE / 2)
                self.environment.clean_cell(self.x, self.y)
                self.stamp()  # Stamp a cleaned mark

    def turn_left(self):
        self.orientation = (self.orientation + 90) % 360
        self.setheading(self.orientation)

    def turn_right(self):
        self.orientation = (self.orientation - 90) % 360
        self.setheading(self.orientation)

# Set up the screen
wn = turtle.Screen()
wn.bgcolor("white")
wn.title("Cleaning Robot Simulation")

# Create environment with obstacles
obstacles = [(1, 1), (1, 2), (2, 2), (3, 1)]
environment = Environment(5, 5, obstacles)
environment.draw(turtle)

# Create a cleaning robot
robot = CleaningRobotTurtle(environment)

# Control the robot using keyboard
wn.onkey(robot.move_forward, "Up")
wn.onkey(robot.turn_left, "Left")
wn.onkey(robot.turn_right, "Right")

# Listen to the keyboard events
wn.listen()

# Start the GUI loop
wn.mainloop()
