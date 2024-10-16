import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


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


def calculate_center_of_gravity_of_arm(body_info):
    lengths, masses = body_info
    x1, x2, x3 = lengths["hand"], lengths["upperarm"], lengths["underarm"]
    m1, m2, m3 = masses["hand"], masses["upperarm"], masses["underarm"]
    distance_center_of_gravity = (m1 * x1 + m2 * x2 + m3 * x3) / (m1 + m2 + m3)
    return distance_center_of_gravity, (m1 + m2 + m3)


def rotation_matrix(angle):
    # 2D rotation matrix
    return np.array([[np.cos(angle), -np.sin(angle)],
                     [np.sin(angle), np.cos(angle)]])


def matrix_based_simulation(length_pendulum, angles, external_velocity=0):
    # Simulation setup
    time_step = 1E-3
    gravity = -9.81
    running_time = 0

    # Assume pendulum starting angle and velocity (in radians)
    phi = np.radians(angles[0])  
    omega = external_velocity  

    time_period = 2 * np.pi * np.sqrt(length_pendulum / abs(gravity))

    # Lists for data collection
    data_points_phi = []
    data_points_omega = []
    data_points_acceleration = []
    data_timestamps = []

    while running_time <= time_period * 2:
        angular_acceleration = (gravity / length_pendulum) * np.sin(phi)

        # Matrix-based integration of velocity and angle
        omega += angular_acceleration * time_step
        phi += omega * time_step

        # Store the computed values
        data_points_phi.append(phi)
        data_points_omega.append(omega)
        data_points_acceleration.append(angular_acceleration)
        data_timestamps.append(running_time)

        running_time += time_step

    return data_points_phi, data_points_omega, data_points_acceleration, data_timestamps, time_period


def animate_pendulum(data1, data2):
    phi1, _, _, time1, _ = data1
    phi2, _, _, time2, _ = data2

    length_pendulum = define_body()[0]["upperarm"]  # Using upperarm length

    x1 = length_pendulum * np.sin(phi1)
    y1 = -length_pendulum * np.cos(phi1)

    x2 = length_pendulum * np.sin(phi2)
    y2 = -length_pendulum * np.cos(phi2)

    fig = plt.figure(figsize=(5, 4))
    ax = fig.add_subplot(autoscale_on=True, xlim=(-length_pendulum - 5, length_pendulum + 5), ylim=(-length_pendulum - 5, length_pendulum + 5))
    ax.set_aspect('equal')
    ax.grid()

    line_initial, = ax.plot([], [], 'o-', lw=2, label='Initial Conditions')
    line_momentum, = ax.plot([], [], 'o-', lw=2, color='r', label='With Momentum')
    time_template = 'time = %.1fs'
    time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

    def animate(i):
        thisx_initial = [0, x1[i]]
        thisy_initial = [0, y1[i]]

        thisx_momentum = [0, x2[i]]
        thisy_momentum = [0, y2[i]]

        line_initial.set_data(thisx_initial, thisy_initial)
        line_momentum.set_data(thisx_momentum, thisy_momentum)
        time_text.set_text(time_template % time1[i])
        return line_initial, line_momentum, time_text

    ani = animation.FuncAnimation(fig, animate, frames=len(time1), interval=1000 * time1[1], blit=True)
    plt.legend()
    plt.show()


def main():
    center_point_distance, _ = calculate_center_of_gravity_of_arm(define_body())

    # Initial conditions (no momentum)
    initial_data = matrix_based_simulation(center_point_distance, angles=[45, 0])

    # With added momentum (initial velocity -1 rad/s)
    momentum_data = matrix_based_simulation(center_point_distance, angles=[45, 0], external_velocity=-1)

    animate_pendulum(initial_data, momentum_data)


if __name__ == "__main__":
    main()
