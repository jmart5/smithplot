import matplotlib.pyplot as plt
import numpy as np
import skrf as rf
import csv

# Create dummy data for the Smith chart
s_dummy = np.linspace(-1, 1, 100) + 1j * np.linspace(-1, 1, 100)

# Plot the Smith chart
fig, ax = plt.subplots()  # Create a figure and axes
rf.plotting.plot_smith(s_dummy, ax=ax)  # Specify the axes for the plot

# Hide all lines in the Smith chart
for line in ax.get_lines():
    line.set_visible(False)

# Create a list to store the clicked points
clicked_points = []

def on_click(event):
    # Check if the click was within the axes
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

        # Store the clicked point
        clicked_points.append((x, y))  # Append the (x, y) tuple to the list
        
        # Plot the clicked point on the chart
        ax.plot(x, y, 'ro')  # 'ro' means red color, circle marker
        
        # Optionally, update the figure
        plt.draw()

        # Print the collected points
        print('x, real part of the reflection coefficient (Γ)')
        print('y, imaginary part of the reflection coefficient (Γ)')
        print(f'Collected Points: {clicked_points}')  # Print all collected points
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

# Create a button to save the points
from matplotlib.widgets import Button

save_ax = plt.axes([0.81, 0.05, 0.1, 0.075])  # Button position
save_button = Button(save_ax, 'Save Points')

# Connect the button to the save_to_csv function
save_button.on_clicked(lambda event: save_to_csv())

# Connect the click event to the on_click function
fig.canvas.mpl_connect('button_press_event', on_click)

# Show the plot
plt.show()
