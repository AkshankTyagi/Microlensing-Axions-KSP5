import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Constants
G = 6.67430e-11  # Gravitational constant, m^3 kg^-1 s^-2
c = 3.0e8  # Speed of light, m/s
M_sun = 1.989e30  # Solar mass, kg
AU = 1.496e11  # Astronomical unit, meters
kpc = 3.086e19  # Kiloparsec, meters

# Parameters
# log10_masses = [ -9]

# Masses = [ (10**m )*M_sun for m in log10_masses] # Mass of minicluster, kg

M = 1e-8 * M_sun
v_t = 100 * 1000  # Tangential velocity, m/s
b = 1.6 * AU * 1e-3  # Impact parameter, meters
D_S = 778 * kpc  # Distance to source (Andromeda), meters
D_L = D_S / 2  # Distance to lens, meters
D_LS = D_S - D_L  # Distance between lens and source, meters

# Calculate Einstein radius
def einstein_radius(M, D_L, D_S, D_LS):
    return np.sqrt((4 * G * M * D_L*D_LS) / (c**2  * D_S))
    # return 4e11*np.sqrt(M*D_S/M_sun/kpc)

# for M in Masses:

R_E = einstein_radius(M, D_L, D_S, D_LS)


# Magnification calculation
def magnification(u):
    return (u**2 + 2) / (u * np.sqrt(u**2 + 4))

# Animation setup
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 10))

time = np.linspace(-10000, 10000, 500)
x_lens = v_t * time   # Convert time from days to seconds
y_lens = np.ones_like(x_lens) * b
magnification_arr =[]

print(R_E)

# Initial plot setup
source_plot, = ax1.plot([0], [0], 'ro', label='Source Star')

lens_plot, = ax1.plot([], [], 'bo', label='Lens')
einstein_radius_circle = plt.Circle((0, 0), R_E, color='blue', fill=False, linestyle='--', label='Einstein Radius')

# Scale plot in R_E units
limit = 7*b
ax1.set_xlim(-limit, limit)
ax1.set_ylim(-limit, limit)
param_text = ax1.text(0.9*-limit, 0.9*-limit, '', fontsize=10)
ax1.set_xlabel('X axis (m) ~ 20b')
ax1.set_ylabel('Y axis (m) ~ 20b')
ax1.set_aspect('equal')
ax1.add_artist(einstein_radius_circle)
ax1.legend(loc='lower right', prop={'size': 8})

# ax1.legend(loc='lower right', bbox_to_anchor=(1.25, ))
ax1.set_title('Lens and Source Star Positions')

light_curve_plot, = ax2.plot([], [], 'k-')
ax2.set_xlim(time[0], time[-1])
ax2.set_ylim(0, 8)
mag_text = ax2.text(0.9*time[0], 0.3, '', fontsize=9 )
ax2.set_xlabel('Time (S)')
ax2.set_ylabel('Magnification')
ax2.set_title('Microlensing Light Curve')

def init():
    lens_plot.set_data([], [])
    light_curve_plot.set_data([], [])
    return lens_plot, light_curve_plot, einstein_radius_circle , param_text, mag_text

def toggle_pause(event):
    global ani, paused
    if event.key == ' ':
        if paused:
            ani.event_source.start()
        else:
            ani.event_source.stop()
        paused = not paused

def update(frame):
    # Update lens position
    x_pos = x_lens[frame] #/ R_E
    y_pos = y_lens[frame] #/ R_E
    lens_plot.set_data([x_pos], [y_pos])
    # print(R_E, [x_pos], [y_pos])
    
    # Update Einstein radius circle position
    einstein_radius_circle.set_center((x_pos, y_pos))

    # Calculate distance u and magnification
    u = np.sqrt((x_lens[frame]**2 + y_lens[frame]**2) / R_E**2)
    mu = magnification(u)
    magnification_arr.append(mu)
    
    param_text.set_text(f'$M_{{\\text{{Lens}}}}$ = {M/M_sun} $ M_{{\\text{{sun}}}}$,   $R_{{\\text{{Einstein}}}}$ = {R_E/AU:.5f} AU\n$D_{{\\text{{S}}}}$ = {D_S/kpc} kpc,   $D_{{\\text{{Lens}}}}$ = $D_{{\\text{{S}}}}$ / 2\nImpact_Param = {b/AU:.5f} AU\nVelocity = {int(v_t/1000)} km/sec\nMagnification: {mu:.3f}')
    mag_text.set_text(f'Impact_Param={b/R_E:.3f} X R_e\nMagnification: {mu:.2f}')
    # Update light curve
    light_curve_plot.set_data(time[:frame+1], magnification_arr[:frame+1] )
    # light_curve_plot.set_data(time[:frame+1], magnification(np.sqrt((x_lens[:frame+1]**2 + y_lens[:frame+1]**2) / R_E**2)))
    
    return lens_plot, light_curve_plot, einstein_radius_circle, param_text, mag_text

global paused
paused = False
fig.canvas.mpl_connect('key_press_event', toggle_pause)

ani = animation.FuncAnimation(fig, update, frames=len(time), init_func=init, blit=True, interval=10, repeat='False')
fig.suptitle(f'Microlensing Event ')
plt.tight_layout()
# plt.show()
ani.save(rf"C:\Users\Akshank Tyagi\Documents\GitHub\Microlensing-Axions-KSP5\output\lensing2_{M/M_sun}_{b/AU}_{int(v_t/1000)}.gif", writer='pillow', fps=40)
# plt.savefig(r")
