'''
BioMechanica_practicum_w5.py

Make a simulation of an arm without the rotation of the elbow.

Jerome Kemper
'''

import numpy as np
import matplotlib.pyplot as plt

def define_body():
    # Set constant body parameters [metre]
    lengths = {
        "hand": 0.20,
        "upperarm": 0.32,
        "underarm": 0.30
    }
    bodyweight = 74  # kg
    mass_percentages = {
        "hand": 0.6,
        "upperarm": 1.6,
        "underarm": 2.7
    }
    masses = {part: bodyweight * (percentage / 100) for part, percentage in mass_percentages.items()}
    return lengths, masses


def Rotatie(q):
    R = np.array([[np.cos(q), -np.sin(q)],
                [np.sin(q), np.cos(q)]])
    return R


def main():
    # Get body properties
    body_info = define_body()
    length_upperarm = body_info[0]["upperarm"]
    length_underarm_hand = body_info[0]["underarm"] + body_info[0]["hand"]

    angles = [[0,0],
              [0,(1.0/6.0)*np.pi],
              [(1.0/6.0)*np.pi, (1.0/6.0)*np.pi],
              [(1.0/4.0)*np.pi, (1.0/2.0)*np.pi]]

    S, E, P = [0,0], [], []

    for [q1,q2] in angles:
        e = np.dot(Rotatie(q1),[length_upperarm,0])
        p = e + np.dot(np.dot(Rotatie(q1),Rotatie(q2)),[length_underarm_hand,0])
        
        E.append(e)
        P.append(p)

    # Scaling factor to make the arm appear larger visually
    scale_factor = 1

    if 1:
        fig, ax = plt.subplots()
        ax.set_xlim(-scale_factor * 1.0, scale_factor * 1.0)  # Apply scaling to axes limits
        ax.set_ylim(-scale_factor * 0.5, scale_factor * 1.0)
        ax.set_aspect('equal')
        ax.grid()
            
        kleuren = ['red', 'magenta', 'green', 'blue']
        for i in range(len(E)):
            kleur = kleuren[i % len(kleuren)]
            # Scale the arm's position for visualization
            line1, = ax.plot([], [], 'o-', lw=2, color=kleur)
            line1.set_data([S[0], scale_factor * E[i][0]], [S[1], scale_factor * E[i][1]])
            line1, = ax.plot([], [], 'o-', lw=2, color=kleur)
            line1.set_data([scale_factor * E[i][0], scale_factor * P[i][0]], [scale_factor * E[i][1], scale_factor * P[i][1]])
            
        plt.xlabel('x [m]')
        plt.ylabel('y [m]')
        plt.title(f"Simulation of Arm")
        plt.show()
    

if __name__ == "__main__":
    main()
