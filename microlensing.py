import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parameters
R_E = 1  # Einstein radius
impact_parameters = [0.5]#[ 0.5, 0.3, 0.2, 0.1, 0.05]  # Multiple distances of closest approach

impact_params = np.array(impact_parameters)*R_E

# Time array or X array
num_frames = 200
x_start = -2*R_E
x_end = 2*R_E
time_per_param = np.linspace(x_start, x_end, num_frames)
time = np.concatenate([time_per_param + i * 4 for i in range(len(impact_params))])

# Lens position (fixed at origin)
lens_pos = np.array([0,0])
x_lens, y_lens = lens_pos

# Source position as a function of time
def source_position(t, impact_param):
    return np.array([t, impact_param + y_lens])  

# Calculate image positions based on the lens equation
def image_positions(source_pos):
    x_s, y_s = source_pos
    u = np.sqrt((x_s - x_lens) ** 2 + (y_s - y_lens) ** 2) / R_E
    if u == 0:
        theta = np.linspace(0, 2 * np.pi, 100)
        return np.vstack((R_E * np.cos(theta), R_E * np.sin(theta)))
    theta_1 = (u + np.sqrt(u ** 2 + 4)) / 2 * R_E
    theta_2 = (u - np.sqrt(u ** 2 + 4)) / 2 * R_E
    image1 = np.array([theta_1 * (x_s - x_lens) / np.sqrt((x_s - x_lens) ** 2 + (y_s - y_lens) ** 2) + x_lens,
                       theta_1 * (y_s - y_lens) / np.sqrt((x_s - x_lens) ** 2 + (y_s - y_lens) ** 2) + y_lens])
    image2 = np.array([theta_2 * (x_s - x_lens) / np.sqrt((x_s - x_lens) ** 2 + (y_s - y_lens) ** 2) + x_lens,
                       theta_2 * (y_s - y_lens) / np.sqrt((x_s - x_lens) ** 2 + (y_s - y_lens) ** 2) + y_lens])
    return np.vstack((image1, image2)).T

# Magnification function
def magnification(u):
    return (u ** 2 + 2) / (u * np.sqrt(u ** 2 + 4))

# Compute magnification for each time step
def compute_magnification(t, impact_param):
    source_pos = source_position(t, impact_param)
    x_s, y_s = source_pos
    u = np.sqrt((x_s-x_lens)**2 + (y_s-y_lens)**2) / R_E
    return magnification(u)

# Initialize the plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6.5))

# Plot settings for the microlensing event
ax1.set_xlim(x_start-abs(x_lens), x_end+abs(x_lens))
ax1.set_ylim(x_start-abs(y_lens), x_end+abs(y_lens))
lens_dot, = ax1.plot([], [], 'bo', label='Lens', markersize=10)
source_dot, = ax1.plot([], [], 'ro', label='Source', markersize=5)
image_dots, = ax1.plot([], [], 'go', label='Images', markersize=5)
magnification_text = ax1.text(0.9*x_start-abs(x_lens), 0.9*x_start-abs(y_lens), '', fontsize=12)
circle = plt.Circle(lens_pos, R_E, color='b', fill=False, linestyle='--', label='Einstein Radius')
ax1.add_patch(circle)
ax1.legend()
# ax1.grid()

# Plot settings for the magnification vs time plot
ax2.set_xlim(x_start, x_end)
ax2.set_ylim(0, 10)
magnification_line, = ax2.plot([], [], 'r-')
impact_text = ax2.text(0.9*x_start, 0.3, '', fontsize=12)
ax2.set_xlabel('Time')
ax2.set_ylabel('Magnification')

# Data for the magnification plot
magnifications = []
for impact_param in impact_params:
    magnifications.append([compute_magnification(t, impact_param) for t in time_per_param])

def toggle_pause(event):
    global ani, paused
    if event.key == ' ':
        if paused:
            ani.event_source.start()
        else:
            ani.event_source.stop()
        paused = not paused

# Update function for animation
def update(frame):
    t = time[frame]
    impact_param_idx = frame // num_frames
    impact_param = impact_params[impact_param_idx]
    # print(impact_params, impact_param_idx, impact_param)
    local_frame = frame % num_frames
    if local_frame == 1:
        print(impact_param_idx,')   R_E:', R_E , '  impact_parameter:' , impact_parameters[impact_param_idx] )
    
    lens_dot.set_data([lens_pos[0]], [lens_pos[1]])
    source_pos = source_position(time_per_param[local_frame], impact_param)
    source_dot.set_data([source_pos[0]], [source_pos[1]])
    images = image_positions(source_pos)
    image_dots.set_data(images[0], images[1])
    mag = compute_magnification(time_per_param[local_frame], impact_param)
    magnification_text.set_text(f'$R_{{\\text{{Einstein}}}}$ = {R_E}\nImpact_Param={impact_parameters[impact_param_idx]} X R_e\nMagnification: {mag:.2f}')
    ax1.set_title(f'Microlensing Event')

    # Update magnification vs time plot
    magnification_line.set_data(time_per_param[:local_frame + 1], magnifications[impact_param_idx][:local_frame + 1])
    impact_text.set_text(f'Impact_Param={impact_parameters[impact_param_idx]} X R_e\nMagnification: {mag:.2f}')
    ax2.set_title(f'Magnification vs Time')

    # if  local_frame % (num_frames) == 160:
        # plt.savefig(fr'C:\Users\Akshank Tyagi\Documents\GitHub\Microlensing-Axions-KSP5\output\stationery_frame.png')        

    return lens_dot, source_dot, image_dots, magnification_text, circle, magnification_line, impact_text

global paused
paused = False
fig.canvas.mpl_connect('key_press_event', toggle_pause)

# Create animation
ani = FuncAnimation(fig, update, frames=len(time), blit=True, interval=30, repeat=False)

# Set the figure title
fig.suptitle('Gravitational Microlensing Simulation', fontsize=16)

# Show the animation
plt.tight_layout()
plt.show()

# Save the animation
# print("saving")
# ani.save(r'C:\Users\Akshank Tyagi\Documents\GitHub\Microlensing-Axions-KSP5\output\microlensing_animation_trial.gif', writer='pillow', fps=40)
# print("output saved")




#--------------------------------------------------------------------------------------#

# printing the Microlensing animation through snapshots

impact_parameters = [ 0.2 ]

frame_nos =[30, 50, 70, 90, 100, 110, 130, 150, 170 ]
time_stamps =np.array([time_per_param[f] for f in frame_nos])
impact_param = impact_parameters[0]*R_E

fig, axes = plt.subplots(3, 3, figsize=(7, 8.5))
axes = axes.flatten()
fig.subplots_adjust(hspace=0.4, wspace=0.3)

for i, ax in enumerate(axes):
    ax.set_xlim(x_start-abs(x_lens), x_end+abs(x_lens))
    ax.set_ylim(x_start-abs(y_lens), x_end+abs(y_lens))

    lens_dot, = ax.plot(0, 0, 'bo', label='Lens', markersize=10)

    source_pos = source_position(time_stamps[i], impact_param)
    source_dot, = ax.plot([source_pos[0]], [source_pos[1]], 'ro', label='Source', markersize=5)

    images = image_positions(source_pos)
    image_dots, = ax.plot(images[0], images[1], 'go', label='Images', markersize=5)

    mag = compute_magnification(time_stamps[i], impact_param)
    magnification_text = ax.text(0.9*x_start-abs(x_lens), 0.9*x_start-abs(y_lens), '', fontsize=8)
    magnification_text.set_text(f'Magnification: {mag:.2f}')

    circle = plt.Circle(lens_pos, R_E, color='b', fill=False, linestyle='--', label='Einstein Radius')
    ax.add_patch(circle)
    ax.set_title(f"Frame number ={frame_nos[i]}", fontsize=10)

    # ax.legend()
# $R_{{\\text{{Einstein}}}}$ = {R_E}\nImpact_Param= 0.1 X R_e\n
fig.suptitle(f'Microlensing Event at $R_E$ = {R_E}, Impact_Param = {impact_parameters[0]} X R_e')
# plt.tight_layout()
# plt.savefig(r'C:\Users\Akshank Tyagi\Documents\GitHub\Microlensing-Axions-KSP5\output\Microlensing_snapshot.png') 
plt.show()




#======================================================================================================#

# Plotting the various lightcurves for multiple impact params

Impact_parameters = [ 0.8, 0.5, 0.3, 0.2, 0.1, 0.05]
Impact_param = np.array(Impact_parameters) * R_E
# print(Impact_parameters)

plt.figure(figsize=(8, 6))
plt.xlim(x_start, x_end)
plt.ylim(0, 11)


for j, ip in enumerate(Impact_param):
    # print(impact_param)
    magnifications = []
    magnifications = [compute_magnification(t, ip) for t in time_per_param]
    plt.plot(time_per_param, magnifications, label=f'\u03C1 = {Impact_parameters[j]}')
    plt.annotate(f'\u03C1 = {Impact_parameters[j]}', xy=(time_per_param[96], magnifications[104]+(0.02/Impact_parameters[j])),  fontsize=10)# xytext=(10, 10), textcoords='offset points',


plt.xlabel('Time')
plt.ylabel('Magnification')
plt.title('Magnification Light curves for \u03C1 = Impact parameter/R_E')
# plt.legend()

# plt.savefig(r'C:\Users\Akshank Tyagi\Documents\GitHub\Microlensing-Axions-KSP5\output\Microlensing_Light_Curves.png')
plt.show()