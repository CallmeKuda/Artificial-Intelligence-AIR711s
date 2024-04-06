import turtle
from collections import deque

CELL_SIZE = 40
OBSTACLE = 'X'
CLEANED = '.'
START = 'S'
END = 'E'

class Environment:
    def __init__(self, width, height, obstacles, start, end):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        self.populate_obstacles(obstacles)
        self.start_pos = start
        self.end_pos = end
        self.grid[start[1]][start[0]] = START
        self.grid[end[1]][end[0]] = END

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

        ########## Drawing the grid ###############
        for y in range(self.height):
            for x in range(self.width):
                turtle.penup()
                turtle.goto(x * CELL_SIZE, y * CELL_SIZE)
                turtle.pendown()
                for _ in range(4):
                    turtle.forward(CELL_SIZE)
                    turtle.left(90)

                ############# Adding in the obstacles #############
                if self.is_obstacle(x, y):
                    turtle.fillcolor('grey')
                    turtle.begin_fill()
                    for _ in range(4):
                        turtle.forward(CELL_SIZE)
                        turtle.left(90)
                    turtle.end_fill()
                elif self.grid[y][x] == START: #Where the robot starts cleaning
                    turtle.fillcolor('green')
                    turtle.begin_fill()
                    for _ in range(4):
                        turtle.forward(CELL_SIZE)
                        turtle.left(90)
                    turtle.end_fill()
                elif self.grid[y][x] == END: #Where the charging station is
                    turtle.fillcolor('red')
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
        self.orientation = 0  
        self.x, self.y = self.environment.start_pos
        self.shape('square')
        self.color('blue')
        self.penup()
        self.goto(self.x * CELL_SIZE + CELL_SIZE / 2, self.y * CELL_SIZE + CELL_SIZE / 2)

    def move_forward(self):
        new_x, new_y = self.x, self.y
        if self.orientation == 0:  # Which is East
            new_x += 1
        elif self.orientation == 90:  # Which is North
            new_y += 1
        elif self.orientation == 180:  # Which is West
            new_x -= 1
        elif self.orientation == 270:  # Which is South
            new_y -= 1

        if (0 <= new_x < self.environment.width and 0 <= new_y < self.environment.height):
            if not self.environment.is_obstacle(new_x, new_y):
                self.x, self.y = new_x, new_y
                self.goto(self.x * CELL_SIZE + CELL_SIZE / 2, self.y * CELL_SIZE + CELL_SIZE / 2)
                self.environment.clean_cell(self.x, self.y)
                self.stamp()  # Add a mark showing it's been cleaned

    def turn_left(self):
        self.orientation = (self.orientation + 90) % 360
        self.setheading(self.orientation)

    def turn_right(self):
        self.orientation = (self.orientation - 90) % 360
        self.setheading(self.orientation)




   #####################  Manhattan distance heuristic   ####################
def heuristic(pos, end):
    x1, y1 = pos
    x2, y2 = end
    return abs(x1 - x2) + abs(y1 - y2)

def a_star_search(environment):
    start = environment.start_pos
    end = environment.end_pos
    open_set = deque([(0, start)])
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    while open_set:
        current = open_set.popleft()[1]

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if (0 <= neighbor[0] < environment.width and 0 <= neighbor[1] < environment.height and
                    not environment.is_obstacle(neighbor[0], neighbor[1])):
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                    if neighbor not in [node[1] for node in open_set]:
                        open_set.append((f_score[neighbor], neighbor))
                    open_set = deque(sorted(open_set))

    return []


               ########### Depth First Search ################
def dfs(environment, start, end, path, visited, all_paths):
    if start == end:
        all_paths.append(path.copy())
        return

    visited.add(start)

    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        neighbor = (start[0] + dx, start[1] + dy)
        if (0 <= neighbor[0] < environment.width and 0 <= neighbor[1] < environment.height and
                not environment.is_obstacle(neighbor[0], neighbor[1]) and neighbor not in visited):
            path.append(neighbor)
            dfs(environment, neighbor, end, path, visited, all_paths)
            path.pop()

    visited.remove(start)

def explore_paths(environment):
    start = environment.start_pos
    end = environment.end_pos
    all_paths = []
    visited = set()
    dfs(environment, start, end, [start], visited, all_paths)
    return all_paths

def follow_path(robot, all_paths, optimal_path):
    # Follow all explored paths in black
    robot.color('black')
    for path in all_paths:
        for i in range(len(path) - 1):
            current_pos = path[i]
            next_pos = path[i + 1]

            # Determine the direction to turn
            if next_pos[0] > current_pos[0]:  # Right
                robot.orientation = 0
            elif next_pos[0] < current_pos[0]:  # Left
                robot.orientation = 180
            elif next_pos[1] > current_pos[1]:  # Up
                robot.orientation = 90
            elif next_pos[1] < current_pos[1]:  # Down
                robot.orientation = 270

            robot.setheading(robot.orientation)

            # Move forward
            robot.move_forward()

    # Follow the optimal path in green
    robot.color('green')
    robot.pensize(3)  # Increase the pen size to make the optimal path thicker
    for i in range(len(optimal_path) - 1):
        current_pos = optimal_path[i]
        next_pos = optimal_path[i + 1]

        # Determine the direction to turn
        if next_pos[0] > current_pos[0]:  # Right
            robot.orientation = 0
        elif next_pos[0] < current_pos[0]:  # Left
            robot.orientation = 180
        elif next_pos[1] > current_pos[1]:  # Up
            robot.orientation = 90
        elif next_pos[1] < current_pos[1]:  # Down
            robot.orientation = 270

        robot.setheading(robot.orientation)

        # Move forward, but skip the last step to the end position
        if current_pos != optimal_path[-2]:
            robot.move_forward()
        else:
            break  # Break out of the loop when reaching the end position

    robot.pensize(1)  # Reset the pen size to the default

    # Follow the optimal path in red
    robot.color('red')
    for i in range(len(optimal_path) - 1):
        current_pos = optimal_path[i]
        next_pos = optimal_path[i + 1]

        # Determine the direction to turn
        if next_pos[0] > current_pos[0]:  # Right
            robot.orientation = 0
        elif next_pos[0] < current_pos[0]:  # Left
            robot.orientation = 180
        elif next_pos[1] > current_pos[1]:  # Up
            robot.orientation = 90
        elif next_pos[1] < current_pos[1]:  # Down
            robot.orientation = 270

        robot.setheading(robot.orientation)

        # Move forward
        robot.move_forward()

        # Change color after optimal path is found
        if current_pos == optimal_path[0]:
            robot.color('blue')


        
        if current_pos != optimal_path[-2]:
            robot.move_forward()
        else:
            break  

    robot.pensize(1)  # Reset the pen size to the default

    # Follow the optimal path in red
    robot.color('red')
    for i in range(len(optimal_path) - 1):
        current_pos = optimal_path[i]
        next_pos = optimal_path[i + 1]

        # Determine the direction to turn
        if next_pos[0] > current_pos[0]:  # Right
            robot.orientation = 0
        elif next_pos[0] < current_pos[0]:  # Left
            robot.orientation = 180
        elif next_pos[1] > current_pos[1]:  # Up
            robot.orientation = 90
        elif next_pos[1] < current_pos[1]:  # Down
            robot.orientation = 270

        robot.setheading(robot.orientation)

        # Move forward
        robot.move_forward()

# Set up the screen
wn = turtle.Screen()
wn.bgpic("carpet.png")
wn.title("Cleaning Robot Simulation")

# Create environment with obstacles, start, and end positions
obstacles = [(1, 1), (1, 2), (2, 2), (3, 1)]
start = (0, 0)
end = (4, 4)
environment = Environment(5, 5, obstacles, start, end)
environment.draw(turtle)

# Create a cleaning robot
robot = CleaningRobotTurtle(environment)

# Explore all paths
all_paths = explore_paths(environment)

# Find the optimal path using A* search
optimal_path = a_star_search(environment)
print("Optimal path:", optimal_path)

# Follow all explored paths and the optimal path
follow_path(robot, all_paths, optimal_path)

# Start the GUI loop
turtle.done()