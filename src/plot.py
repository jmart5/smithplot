import matplotlib.pyplot as plt
import numpy as np
import skrf as rf

s_dummy = np.linspace(-1, 1, 100) + 1j * np.linspace(-1, 1, 100)

rf.plotting.plot_smith(s_dummy)

for line in plt.gca().get_lines():
    line.set_visible(False)

def on_click(event):
    if event.inaxes is not None:
        x, y = event.xdata, event.ydata
        z = complex(x, y)  # Convert x, y to complex (reflection coefficient)
        
        gamma = abs(z)
        
        if gamma < 1:
            vswr = (1 + gamma) / (1 - gamma)
        else:
            vswr = np.inf  # Infinite VSWR for |Gamma| = 1 (total reflection)

        print(f'Clicked at: x={x}, y={y}, Impedance={z}')
        print(f'Reflection Coefficient (|Γ|): {gamma:.4f}, VSWR: {vswr:.4f}')
    else:
        print('Clicked outside axes bounds')

fig = plt.gcf()
fig.canvas.mpl_connect('button_press_event', on_click)

plt.show()
