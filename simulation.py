import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

class RPSSimulation:
    def __init__(self, size=50, reproduction=True):
        self.size = size
        self.reproduction = reproduction
        # 0: Empty, 1: Rock (Red), 2: Paper (Green), 3: Scissors (Blue)
        self.grid = np.random.choice([0, 1, 2, 3], size=(size, size), p=[0.8, 0.066, 0.067, 0.067])
        
        # Win dictionary: Key beats Value
        self.rules = {1: 3, 2: 1, 3: 2} 

    def get_move(self, x, y):
        # Choose a random direction: Up, Down, Left, Right
        dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        return (x + dx) % self.size, (y + dy) % self.size

    def step(self):
        # Find all current agents
        coords = np.argwhere(self.grid > 0)
        np.random.shuffle(coords) # Randomize order to prevent directional bias

        for x, y in coords:
            val = self.grid[x, y]
            if val == 0: continue # Might have been deleted earlier this step

            nx, ny = self.get_move(x, y)
            target = self.grid[nx, ny]

            if target == 0:
                # Move to empty space
                self.grid[nx, ny] = val
                self.grid[x, y] = 0
            elif target == val:
                # Same type: Reproduction (if enabled)
                if self.reproduction:
                    # Try to find a different empty neighbor to spawn into
                    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        sx, sy = (x + dx) % self.size, (y + dy) % self.size
                        if self.grid[sx, sy] == 0:
                            self.grid[sx, sy] = val
                            break
            elif self.rules[val] == target:
                # I beat them: Delete loser and move into their spot
                self.grid[nx, ny] = val
                self.grid[x, y] = 0
            else:
                # I lost: Delete me
                self.grid[x, y] = 0

        return self.grid

# --- Animation Setup ---
size = 40
sim = RPSSimulation(size=size, reproduction=True)

fig, ax = plt.subplots()
# We use a custom colormap: 0=Black, 1=Red, 2=Green, 3=Blue
cmap = plt.get_cmap('gnuplot2', 4)
img = ax.imshow(sim.grid, cmap=cmap, vmin=0, vmax=3)

def update(frame):
    new_grid = sim.step()
    img.set_array(new_grid)
    
    # Check for game over
    remaining = np.unique(new_grid)
    if len(remaining) <= 2 and 0 in remaining: # Only one type + empty space left
        plt.title(f"Simulation Ended! Winner: {remaining[remaining > 0]}")
        ani.event_source.stop()
    return [img]

ani = animation.FuncAnimation(fig, update, interval=50, blit=True)
# plt.show()
