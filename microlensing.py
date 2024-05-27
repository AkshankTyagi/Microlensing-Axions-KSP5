import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parameters
D_l = 1.0  # distance to lens
R_E = 0.5  # Einstein radius
x_closest = 0.1  # distance of closest approach

# Time array
time = np.linspace(-2, 2, 500)

# Lens and source positions as functions of time
def lens_position(t):
    return np.array([0, 0])  # Lens stays at origin

def source_position(t):
    return np.array([t, x_closest])  # Source moves in a straight line

# Magnification function
def magnification(u):
    return (u**2 + 2) / (u * np.sqrt(u**2 + 4))

# Compute magnification for each time step
def compute_magnification(t):
    source_pos = source_position(t)
    lens_pos = lens_position(t)
    u = np.linalg.norm(source_pos - lens_pos) / R_E
    return magnification(u)

# Initialize the plot
fig, ax = plt.subplots()
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
lens_dot, = ax.plot([], [], 'bo', label='Lens', markersize=10)
source_dot, = ax.plot([], [], 'ro', label='Source', markersize=5)
magnification_text = ax.text(-1.8, 1.8, '', fontsize=12)
ax.legend()

# Update function for animation
def update(frame):
    t = time[frame]
    lens_dot.set_data(*lens_position(t))
    source_dot.set_data(*source_position(t))
    mag = compute_magnification(t)
    magnification_text.set_text(f'Magnification: {mag:.2f}')
    return lens_dot, source_dot, magnification_text

# Create animation
ani = FuncAnimation(fig, update, frames=len(time), blit=True, interval=20)

# Show the animation
plt.show()
