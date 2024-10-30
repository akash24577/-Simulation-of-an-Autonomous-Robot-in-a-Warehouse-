import matplotlib.pyplot as plt
import time
import numpy as np
import matplotlib.image as mpimg

# Warehouse and Robot Parameters
warehouse_width = 10  # meters
warehouse_height = 10  # meters
start = (0, 0)
destination = (7, 9)
robot_speed = 1  # meters per second
movement_duration = 1  # seconds of movement
stop_duration = 2.0  # seconds of stop time

# Load the robot image
robot_image_path = 'robo.png'  # Make sure to provide the correct path to your robot image
robot_image = mpimg.imread(robot_image_path)

# Initialize robot position
robot_position = list(start)

# Define obstacles as circles with (x, y, radius)
obstacles = [
    (3, 3, 1),  # (x, y, radius)
    (5, 5, 1.5),
    (7, 7, 1),
    (4, 8, 1),
]

# Function to check if a position is inside an obstacle
def is_in_obstacle(x, y):
    for (ox, oy, radius) in obstacles:
        if (x - ox)**2 + (y - oy)**2 < radius**2:
            return True
    return False

# Check if the destination is inside any obstacle
if is_in_obstacle(destination[0], destination[1]):
    print("WE CAN NOT REACH THAT DESTINATION POINT :( ")
else:
    # Plot settings
    fig, ax = plt.subplots()
    plt.xlim(0, warehouse_width)
    plt.ylim(0, warehouse_height)
    ax.set_aspect('equal', 'box')
    plt.plot(destination[0], destination[1], 'rx', label="")  # Destination point in red

    # Draw the obstacles once outside the loop
    for (ox, oy, radius) in obstacles:
        circle = plt.Circle((ox, oy), radius, color='red', fill=False, linewidth=1.5)
        ax.add_patch(circle)

    # Simulation loop
    def move_robot():
        plt.ion()  # Enable interactive mode
        current_time = 0
        positions_x = [start[0]]
        positions_y = [start[1]]

        while tuple(robot_position) != destination:
            # Calculate the direction vector
            dx = destination[0] - robot_position[0]
            dy = destination[1] - robot_position[1]
            distance = (dx**2 + dy**2)**0.5
            
            # Stop if the robot is at the destination
            if distance < robot_speed * movement_duration:
                robot_position[0], robot_position[1] = destination
                positions_x.append(robot_position[0])
                positions_y.append(robot_position[1])
                break
            
            # Move towards destination
            direction_x = dx / distance
            direction_y = dy / distance

            # Calculate new position
            new_x = robot_position[0] + direction_x * robot_speed * movement_duration
            new_y = robot_position[1] + direction_y * robot_speed * movement_duration

            # Check for obstacle collision; if collision, adjust direction slightly
            if is_in_obstacle(new_x, new_y):
                angle_offset = np.pi / 4  # 45-degree offset to avoid obstacle
                direction_x = np.cos(np.arctan2(dy, dx) + angle_offset)
                direction_y = np.sin(np.arctan2(dy, dx) + angle_offset)
                new_x = robot_position[0] + direction_x * robot_speed * movement_duration
                new_y = robot_position[1] + direction_y * robot_speed * movement_duration

            # Update the robot position
            robot_position[0] = max(0, min(warehouse_width, new_x))
            robot_position[1] = max(0, min(warehouse_height, new_y))

            # Append the new position to the path
            positions_x.append(robot_position[0])
            positions_y.append(robot_position[1])

            # Clear and redraw the plot
            ax.clear()
            plt.xlim(0, warehouse_width)
            plt.ylim(0, warehouse_height)
            plt.plot(destination[0], destination[1], 'rx', label="Destination")  # Destination
            
            # Redraw obstacles
            for (ox, oy, radius) in obstacles:
                circle = plt.Circle((ox, oy), radius, color='red', fill=False, linewidth=1.5)
                ax.add_patch(circle)
            
            # Plot path as a continuous line
            plt.plot(positions_x, positions_y, 'b-', label="Path")  # Robot's path as a line
            
            # Display the robot image at the current position
            ax.imshow(robot_image, extent=(robot_position[0]-0.5, robot_position[0]+0.5,
                                            robot_position[1]-0.5, robot_position[1]+0.5))
            
            plt.xlabel('X (m)')
            plt.ylabel('Y (m)')
            plt.title(f"Robot Simulation with Obstacles - Time: {current_time:.1f} s")
            plt.legend(loc="upper right")
            plt.grid(True)
            plt.draw()
            plt.pause(movement_duration)  # Pause to simulate real-time plotting

            # Increase time and simulate stopping
            current_time += movement_duration
            time.sleep(stop_duration)  # Simulate the robot's 2-second stop

        plt.ioff()  # Disable interactive mode
        plt.show()

    # Run the simulation
    move_robot()
