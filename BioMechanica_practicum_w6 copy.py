'''
BioMechanica_practicum_w6.py

Make a simulation of an arm with the rotation of the elbow.
For simplification, imagine it as a double pendulum.

Jerome Kemper
'''

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

from matplotlib.widgets import Button


def define_body():
    lengths = {
        "hand": 20,
        "upperarm": 32,
        "underarm": 30
    }

    bodyweight = 74
    mass_percentages = {
        "hand": 0.6,
        "upperarm": 1.6,
        "underarm": 2.7
    }

    masses = {part: bodyweight * (percentage / 100) for part, percentage in mass_percentages.items()}

    return lengths, masses


def rotation_matrix(angle):
    # 2D rotation matrix
    return np.array([[np.cos(angle), -np.sin(angle)],
                     [np.sin(angle), np.cos(angle)]])


def double_pendulum_simulation(length_upperarm, length_underarm_hand, angles, external_velocity=0):
    # Simulation setup
    time_step = 1E-2
    gravity = -9.81
    running_time = 0

    # Assume starting angles and velocities for both pendulums
    phi1 = np.radians(angles[0])  # angle of upper arm
    phi2 = np.radians(angles[1])  # angle of underarm/hand
    omega1 = external_velocity  # angular velocity of upper arm
    omega2 = 0.0  # initial angular velocity of underarm/hand

    time_period = 2 * np.pi * np.sqrt((length_upperarm + length_underarm_hand) / abs(gravity))

    # Lists for data collection
    data_points_phi1 = []
    data_points_phi2 = []
    data_points_omega1 = []
    data_points_omega2 = []
    data_points_acceleration1 = []
    data_points_acceleration2 = []
    data_timestamps = []

    while running_time <= time_period * 10:
        # Angular accelerations of upper arm and underarm
        angular_acceleration1 = (gravity / length_upperarm) * np.sin(phi1)
        angular_acceleration2 = (gravity / length_underarm_hand) * np.sin(phi2)

        # Update angular velocities
        omega1 += angular_acceleration1 * time_step
        omega2 += angular_acceleration2 * time_step

        # Update angles
        phi1 += omega1 * time_step
        phi2 += omega2 * time_step

        # Store the computed values
        data_points_phi1.append(phi1)
        data_points_phi2.append(phi2)
        data_points_omega1.append(omega1)
        data_points_omega2.append(omega2)
        data_points_acceleration1.append(angular_acceleration1)
        data_points_acceleration2.append(angular_acceleration2)
        data_timestamps.append(running_time)

        running_time += time_step

    return data_points_phi1, data_points_phi2, data_points_omega1, data_points_omega2, data_points_acceleration1, data_points_acceleration2, data_timestamps, time_period



def save_animation(ani, filename='double_pendulum_simulation.gif', fps=30, writer='pillow'):
    print("SAVING ANIMATION")
    ani.save(filename, writer=writer, fps=fps)
    print("DONE")



def animate_double_pendulum(data1, data2):
    phi1_1, phi2_1, _, _, _, _, time1, _ = data1
    phi1_2, phi2_2, _, _, _, _, time2, _ = data2

    body_info = define_body()
    length_upperarm = body_info[0]["upperarm"]
    length_underarm_hand = body_info[0]["underarm"] + body_info[0]["hand"]

    # Calculate positions of the two pendulums for animation
    x1_1 = length_upperarm * np.sin(phi1_1)
    y1_1 = -length_upperarm * np.cos(phi1_1)
    x2_1 = x1_1 + length_underarm_hand * np.sin(phi2_1)
    y2_1 = y1_1 - length_underarm_hand * np.cos(phi2_1)

    x1_2 = length_upperarm * np.sin(phi1_2)
    y1_2 = -length_upperarm * np.cos(phi1_2)
    x2_2 = x1_2 + length_underarm_hand * np.sin(phi2_2)
    y2_2 = y1_2 - length_underarm_hand * np.cos(phi2_2)

    fig, ax = plt.subplots(figsize=(5, 4))
    ax.set_xlim(-length_upperarm - length_underarm_hand - 5, length_upperarm + length_underarm_hand + 5)
    ax.set_ylim(-length_upperarm - length_underarm_hand - 5, length_upperarm + length_underarm_hand + 5)
    ax.set_aspect('equal')
    ax.grid()

    line_initial, = ax.plot([], [], 'o-', lw=2, label='Initial Conditions')
    trace_initial, = ax.plot([], [], 'b.-', lw=1, ms=1, label='Initial Trace')
    line_momentum, = ax.plot([], [], 'o-', lw=2, color='r', label='With Momentum')
    trace_momentum, = ax.plot([], [], 'r.-', lw=1, ms=1, label='Momentum Trace')
    time_template = 'time = %.1fs'
    time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

    # Button visibility flags
    trace_initial_visible = True
    trace_momentum_visible = True

    def animate(i):
        # Initial conditions pendulum
        thisx_initial = [0, x1_1[i], x2_1[i]]
        thisy_initial = [0, y1_1[i], y2_1[i]]
        
        history_x = x2_1[:i]
        history_y = y2_1[:i]

        # With added momentum pendulum
        thisx_momentum = [0, x1_2[i], x2_2[i]]
        thisy_momentum = [0, y1_2[i], y2_2[i]]
        
        history_x2 = x2_2[:i]
        history_y2 = y2_2[:i]

        line_initial.set_data(thisx_initial, thisy_initial)
        line_momentum.set_data(thisx_momentum, thisy_momentum)
        time_text.set_text(time_template % time1[i])

        # Update trace visibility
        if trace_initial_visible:
            trace_initial.set_data(history_x, history_y)
        else:
            trace_initial.set_data([], [])

        if trace_momentum_visible:
            trace_momentum.set_data(history_x2, history_y2)
        else:
            trace_momentum.set_data([], [])

        return line_initial, line_momentum, trace_initial, trace_momentum, time_text

    ani = animation.FuncAnimation(fig, animate, frames=len(time1), interval=10 * time1[1], blit=True)
    plt.legend()

    # Create buttons for toggling visibility
    ax_trace_initial = plt.axes([0.1, 0.01, 0.15, 0.05])  # Button position
    btn_trace_initial = Button(ax_trace_initial, 'Toggle Initial Trace')

    ax_trace_momentum = plt.axes([0.3, 0.01, 0.15, 0.05])  # Button position
    btn_trace_momentum = Button(ax_trace_momentum, 'Toggle Momentum Trace')

    def toggle_trace_initial(event):
        nonlocal trace_initial_visible
        trace_initial_visible = not trace_initial_visible

    def toggle_trace_momentum(event):
        nonlocal trace_momentum_visible
        trace_momentum_visible = not trace_momentum_visible

    btn_trace_initial.on_clicked(toggle_trace_initial)
    btn_trace_momentum.on_clicked(toggle_trace_momentum)

    plt.show()
    
    # uncomment statement to save pendulum as a gif - set at 30 fps.
    #save_animation(ani, filename='double_pendulum_simulation.gif')



def main():
    body_info = define_body()
    upperarm_length = body_info[0]["upperarm"]
    underarm_hand_length = body_info[0]["underarm"] + body_info[0]["hand"]

    # Initial conditions: angles for upper arm and underarm (no momentum)
    initial_data = double_pendulum_simulation(upperarm_length, underarm_hand_length, angles=[45, 30])

    # With added momentum: initial velocity on upper arm
    momentum_data = double_pendulum_simulation(upperarm_length, underarm_hand_length, angles=[45, 30], external_velocity=-1)

    animate_double_pendulum(initial_data, momentum_data)


if __name__ == "__main__":
    main()
