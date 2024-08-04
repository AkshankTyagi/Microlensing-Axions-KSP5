import numpy as np
import matplotlib.pyplot as plt

# Define the function to calculate g_star
def g_star_R(T):
    # print ('calculating g_star_R')
    a0 = 1.21
    a_j1 = np.array([0.572, 0.330, 0.579, 0.138, 0.108])
    a_j2 = np.array([-8.77, -2.95, -1.80, -0.162, 3.76])
    a_j3 = np.array([0.682, 1.01, 0.165, 0.934, 0.869])

    # for T in Temp:
    t = np.log(T / 1.0)
    sum_terms = [a_j1[i] * (1.0 + np.tanh((t - a_j2[i]) / a_j3[i])) for i in range(5)]
    # print(f"dum terms: {sum_terms}")
    g_star_r_value = np.exp(a0 + np.sum(sum_terms))

    return g_star_r_value # np.array(result)

def g_star_S(T):
    # print ('calculating g_star_S')
    a0 = 1.36
    a_j1 = np.array([0.498, 0.327, 0.579, 0.140, 0.109])
    a_j2 = np.array([-8.74, -2.89, -1.79, -0.102, 3.82])
    a_j3 = np.array([0.693, 1.01, 0.155, 0.963, 0.907])

    # for T in Temp:
    t = np.log(T / 1.0)
    sum_terms = [a_j1[i] * (1.0 + np.tanh((t - a_j2[i]) / a_j3[i])) for i in range(5)]
    # print(f"dum terms: {sum_terms}")
    g_star_s_value = np.exp(a0 + np.sum(sum_terms))

    return g_star_s_value # np.array(result)

# Temperature range
Temp = np.logspace(-6, 3, 500)  # T in GeV

# Calculate g_star_R and g_star_S
g_star_r = [g_star_R(T) for T in Temp]
g_star_s = [g_star_S(T) for T in Temp]

# Plotting
plt.figure(figsize=(7, 4))
plt.plot(Temp, g_star_r, label=r'$g_{\star R}$ fit', color='b')
plt.plot(Temp, g_star_s, label=r'$g_{\star S}$ fit', color='r')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Temperature (GeV)')
plt.ylabel(r'$g_{\star}$')
plt.title(r'$g_{\star R}$ and $g_{\star S}$ vs Temperature')
plt.legend()
plt.grid(True)
plt.show()