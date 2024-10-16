'''
BioMechanica_practicum_w4.py

Make a simulation of an arm without the rotation of the elbow.
For simplification, imagine it as a simple single pendulum.

PART 1
1) make a numerical simulation using Euler integration
2) graph
3) assess the output; what defines your simulation

PART 2
1) give additional momentum to the pendulum
2) graph
3) assess the output


Jerome Kemper
'''

# import libraries
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import math


def define_body():
    # set constant of body

    # length of body parts
    lengths = {
        "hand": 20,
        "upperarm": 32,
        "underarm": 30
    }

    # total mass of person
    bodyweight = 74

    # percentage weight of body part
    mass_percentages = {
        "hand": 0.6,
        "upperarm": 1.6,
        "underarm": 2.7
    }

    # Calculate mass
    masses = {part: bodyweight * (percentage / 100) for part, percentage in mass_percentages.items()}

    return lengths, masses


def calculate_center_of_gravity_of_arm(body_info):
    lengths, masses = body_info

    x1, x2, x3 = lengths["hand"], lengths["upperarm"], lengths["underarm"]
    m1, m2, m3 = masses["hand"], masses["upperarm"], masses["underarm"]

    distance_center_of_gravity = (m1 * x1 + m2 * x2 + m3 * x3) / (m1 + m2 + m3)  # calculate center of gravity with three body parts

    return distance_center_of_gravity, (m1 + m2 + m3)


def euler_integration(length_pendulum, initial_flick_angle=45, initial_flick_velocity=0.0, external_acceleration=0.0):
    # set simulation properties
    time_step = 1E-3  # s
    running_time = 0  # s

    # set external properties and starting conditions
    gravity = -9.81  # m/s^2
    phi = math.radians(initial_flick_angle)  # initial angle based on flick
    omega = initial_flick_velocity  # initial angular velocity based on flick
    acceleration = external_acceleration  # initial acceleration - not correctly implemented

    # formula used for simulation
    time_period = 2 * math.pi * math.sqrt(length_pendulum / abs(gravity))

    # save as
    data_points_phi = []
    data_points_omega = []
    data_points_acceleration = []
    data_timestamps = []

    # Euler integration loop
    while running_time <= time_period * 2:
        # Update angular acceleration considering gravity and external acceleration
        angular_acceleration = (gravity / length_pendulum) * math.sin(phi) + acceleration

        # Update omega and phi using Euler's method
        omega += angular_acceleration * time_step  # Update angular velocity
        phi += omega * time_step  # Update angle

        # Store the updated values
        data_points_phi.append(phi)
        data_points_omega.append(omega)
        data_points_acceleration.append(angular_acceleration)  # Save the angular acceleration
        data_timestamps.append(running_time)

        # Update running time
        running_time += time_step

    # Return the results
    return data_points_phi, data_points_omega, data_points_acceleration, data_timestamps, time_period


def graph(data1, data2):
    phi1, omega1, acceleration1, time1, time_period1 = data1
    phi2, omega2, acceleration2, time2, time_period2 = data2

    # Create subplots
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    # Calculate global y-axis limits for the angle, angular velocity, and angular acceleration
    all_phi = phi1 + phi2
    all_omega = omega1 + omega2
    all_acceleration = acceleration1 + acceleration2

    y_limits_phi = (min(all_phi) * 1.1, max(all_phi) * 1.1)
    y_limits_omega = (min(all_omega) * 1.1, max(all_omega) * 1.1)
    y_limits_acceleration = (min(all_acceleration) * 1.1, max(all_acceleration) * 1.1)

    # Plot for initial data
    axs[0].plot(time1, phi1, label='Angle (rad)')
    axs[0].plot(time1, omega1, label='Angular Velocity (rad/s)')
    axs[0].plot(time1, acceleration1, label='Angular Accel (rad/s²)')
    axs[0].set_title('Pendulum Simulation: Initial Conditions')
    axs[0].set_xlabel('Time [s]')
    axs[0].set_ylabel('Values (rad, rad/s, rad/s²)')
    axs[0].set_ylim(y_limits_phi)  # Set y-axis limit for angle
    axs[0].grid()
    axs[0].legend()

    # Plot for momentum data
    axs[1].plot(time2, phi2, label='Angle (rad)')
    axs[1].plot(time2, omega2, label='Angular Velocity (rad/s)')
    axs[1].plot(time2, acceleration2, label='Angular Accel (rad/s²)')
    axs[1].set_title('Pendulum Simulation: With Added Momentum')
    axs[1].set_xlabel('Time [s]')
    axs[1].set_ylabel('Values (rad, rad/s, rad/s²)')
    axs[1].set_ylim(y_limits_phi)  # Set y-axis limit for angle
    axs[1].grid()
    axs[1].legend()

    # Show the plot
    plt.tight_layout()
    plt.show()


def animate_pendelum(initial_data, momentum_data):
    phi1, _, _, time1, _ = initial_data
    phi2, _, _, time2, _ = momentum_data
    
    # Calculate pendulum positions for animation
    length_pendulum = define_body()[0]["upperarm"]  # use upperarm length for the pendulum length

    x1 = length_pendulum * np.sin(phi1)
    y1 = -length_pendulum * np.cos(phi1)

    x2 = length_pendulum * np.sin(phi2)
    y2 = -length_pendulum * np.cos(phi2)

    fig = plt.figure(figsize=(5, 4))
    ax = fig.add_subplot(autoscale_on=True, xlim=(-length_pendulum - 5, length_pendulum + 5), ylim=(-length_pendulum - 5, length_pendulum + 5.0))
    ax.set_aspect('equal')
    ax.grid()

    line_initial, = ax.plot([], [], 'o-', lw=2, label='Initial Conditions')
    line_momentum, = ax.plot([], [], 'o-', lw=2, color='r', label='With Momentum')
    time_template = 'time = %.1fs'
    time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

    def animate(i):
        phi1, _, _, time1, _ = initial_data
        phi2, _, _, time2, _ = momentum_data
        
        thisx_initial = [0, x1[i]]
        thisy_initial = [0, y1[i]]
        
        thisx_momentum = [0, x2[i]]
        thisy_momentum = [0, y2[i]]

        line_initial.set_data(thisx_initial, thisy_initial)
        line_momentum.set_data(thisx_momentum, thisy_momentum)
        time_text.set_text(time_template % (time1[i]))
        return line_initial, line_momentum, time_text

    ani = animation.FuncAnimation(fig, animate, frames=len(time1), interval=1000 * time1[1], blit=True)
    plt.legend()
    plt.show()



def main():
    center_point_distance, _ = calculate_center_of_gravity_of_arm(define_body())

    # Run Part 1
    initial_data = euler_integration(center_point_distance)

    # Run Part 2 with additional momentum (initial velocity of -0.5 rad/s - give additional speed)
    momentum_data = euler_integration(center_point_distance, initial_flick_velocity=-1)

    graph(initial_data, momentum_data)
    animate_pendelum(initial_data, momentum_data)

if __name__ == "__main__":
    main()
