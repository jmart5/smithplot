import matplotlib.pyplot as plt
import numpy as np
import skrf as rf
import csv
from matplotlib.widgets import Button

# Plot the Smith chart
fig, ax = plt.subplots()  # Create a figure and axes
fig.suptitle("Smith Chart")
s_line = 0j * np.linspace(-1, 1, 1)  # Dummy line
rf.plotting.plot_smith(s_line, ax=ax)  # Specify the axes for the plot
ax.set_title("")

clicked_points = []

def on_click(event):
    if event.inaxes is not None:
        x, y = event.xdata, event.ydata
        z = complex(x, y)  # Convert x, y to complex (reflection coefficient)
        
        gamma = abs(z)
        
        # Calculate VSWR
        if gamma < 1:
            vswr = (1 + gamma) / (1 - gamma)
        else:
            vswr = np.inf  # Infinite VSWR for |Gamma| = 1 (total reflection)

        print(f'Clicked at: x={x}, y={y}, Impedance={z}')
        print(f'Reflection Coefficient (|Γ|): {gamma:.4f}, VSWR: {vswr:.4f}')

        # Calculate phase
        phase_rad = np.arctan2(y, x)  # Phase in radians
        phase_deg = np.degrees(phase_rad)  # Phase in degrees

        print(f'Reflection Coefficient (|Γ|): {gamma:.4f}')
        print(f'VSWR: {vswr:.4f}')
        print(f'Phase: {phase_rad:.4f} radians, {phase_deg:.2f} degrees')

        clicked_points.append((x, y))
        
        ax.plot(x, y, 'ro')
        
        plt.draw()

        print('x, real part of the reflection coefficient (Γ)')
        print('y, imaginary part of the reflection coefficient (Γ)')
        print(f'Collected Points: {clicked_points}')
    else:
        print('Clicked outside axes bounds')

def save_to_csv():
    """Save the collected points to a CSV file."""
    print('todo')
    # with open('clicked_points.csv', 'w', newline='') as csvfile:
    #     csv_writer = csv.writer(csvfile)
    #     # Write the header
    #     csv_writer.writerow(['Real Part (Γ)', 'Imaginary Part (Γ)'])
    #     # Write the points
    #     csv_writer.writerows(clicked_points)
    
    print(f'Saved {len(clicked_points)} points to clicked_points.csv')

def clear_points(event):
    """Clear the plotted points and reset the clicked_points list."""
    global clicked_points
    clicked_points.clear()
    ax.clear()
    rf.plotting.plot_smith(s_line, ax=ax)
    plt.draw()
    print("Cleared all points.")

save_ax = plt.axes([0.81, 0.05, 0.1, 0.075]) 
save_button = Button(save_ax, 'Save Points')
save_button.on_clicked(lambda event: save_to_csv())

refresh_ax = plt.axes([0.65, 0.05, 0.1, 0.075])
refresh_button = Button(refresh_ax, 'Refresh')
refresh_button.on_clicked(clear_points)

fig.canvas.mpl_connect('button_press_event', on_click)

plt.show()
