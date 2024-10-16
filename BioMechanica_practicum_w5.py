import numpy as np
import matplotlib.pyplot as plt

def Rotatie(q):
    R = np.array([[np.cos(q), -np.sin(q)],
                [np.sin(q), np.cos(q) ]])
    return R

angles = [[0,0],[0,(1.0/6.0)*np.pi],
          [(1.0/6.0)*np.pi,(1.0/6.0)*np.pi],
          [(1.0/4.0)*np.pi,(1.0/2.0)*np.pi]]

d1 = 0.6 # m
d2 = 0.5 # m
S, E, P = [0,0], [], []

for [q1,q2] in angles:
    e = np.dot(Rotatie(q1),[d1,0])
    p = e + np.dot(np.dot(Rotatie(q1),Rotatie(q2)),[d2,0])
    
    E.append(e)
    P.append(p)
    
if 1:
    fig, ax = plt.subplots()
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.grid()
        
    kleuren = ['red', 'magenta', 'green', 'blue']
    for i in range(len(E)):
        kleur = kleuren[i % len(kleuren)]
        line1, = ax.plot([], [], 'o-', lw=2, color=kleur)
        line1.set_data([S[0], E[i][0]], [S[1], E[i][1]])
        line1, = ax.plot([], [], 'o-', lw=2, color=kleur)
        line1.set_data([E[i][0], P[i][0]], [E[i][1], P[i][1]])
        
    plt.xlabel('x [m]')
    plt.ylabel('y [m]')
    plt.title("Slingeranimatie")
    plt.show()