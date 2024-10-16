import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from functools import partial

# Create figure and axis
fig, ax = plt.subplots()
line_sin, = ax.plot([], [], 'ro', label='Sine')  # Line for sine
line_cos, = ax.plot([], [], 'bo', label='Cosine')  # Line for cosine

# Custom data (example lists)
custom_x_data = np.linspace(0, 2 * np.pi, 128)
custom_y_data_1 = np.sin(custom_x_data)  # Sine wave
custom_y_data_2 = np.cos(custom_x_data)  # Cosine wave

def init():
    ax.set_xlim(0, 2 * np.pi)
    ax.set_ylim(-2, 2)
    ax.legend()  # Show legend
    return line_sin, line_cos  # Return both line objects

def update(frame, ln_sin, ln_cos):
    # Use the frame index to get current x-value and corresponding y-values
    x = custom_x_data[:frame + 1]  # Up to the current frame
    y_sin = custom_y_data_1[:frame + 1]  # Sine data
    y_cos = custom_y_data_2[:frame + 1]  # Cosine data
    
    # Update the lines with the new data
    ln_sin.set_data(x, y_sin)
    ln_cos.set_data(x, y_cos)
    return ln_sin, ln_cos  # Return both line objects

# Creating the animation
ani = FuncAnimation(
    fig, partial(update, ln_sin=line_sin, ln_cos=line_cos),
    frames=len(custom_x_data),  # Use the length of your custom x data
    init_func=init, blit=True, interval=10)  # Control speed with interval (milliseconds)

plt.show()
