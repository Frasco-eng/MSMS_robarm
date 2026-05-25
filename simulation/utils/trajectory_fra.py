import numpy as np
from scipy.interpolate import PchipInterpolator

import os
import matplotlib.pyplot as plt



def generate_curve(t_sp, x_sp, t_eval):

    csx = PchipInterpolator(t_sp, x_sp)
    
    x_traj = csx(t_eval) # Result is shape (len(t_eval), ns)
    
    return x_traj


def main():
    T_end = 100.0
    dt = 1.0
    # [-0.81725, -0.19145, -0.005491]
    n_points = 10
    t_sp = np.array([0.0, T_end/10, 2*T_end/10, 3*T_end/10, 4*T_end/10, 5*T_end/10, 6*T_end/10, 7*T_end/10, 8*T_end/10, 9*T_end/10, T_end])
    x_sp = np.array([[-0.72, -0.11, 0.007], [0.0, 0.5, 0.2], [0.3, 0.0, 0.2],[0.3, 0.0, 0.05], [0.3, 0.0, 0.2], [0.0, -0.5, 0.2], [-0.3, 0.0, 0.2], [-0.3, 0.0, 0.05], [-0.3, 0.0, 0.2], [0.0, 0.3, 0.5], [0.0, 0.3, 0.5]])
    cond_sp = np.array([False, False, False, True, True, True, True, False, False, False, False])
    t_eval = np.arange(0, T_end, dt)
    
    x_traj =generate_curve(t_sp, x_sp, t_eval)

    
    indices = np.digitize(t_eval, t_sp, right=False) - 1
    indices = np.clip(indices, 0, len(cond_sp) - 1)
    cond_traj = cond_sp[indices]
    
    
    plt.figure(figsize=(10, 6))
    plt.plot(t_eval, cond_traj)
    plt.plot(t_eval, x_traj[:, 0])
    plt.plot(t_eval, x_traj[:, 1])
    plt.plot(t_eval, x_traj[:, 2])
    
    plt.legend(['cond', 'X', 'Y', 'Z'])
    plt.grid()
    plt.show()
    
    t_eval_reshaped = t_eval.reshape(-1, 1)
    cond_traj_reshaped = cond_traj.reshape(-1, 1)
    
    output = np.hstack((t_eval_reshaped, cond_traj_reshaped, x_traj))
    
    np.savetxt("trajectory.csv", output, delimiter=',', header="Time,Cond,X,Y,Z", comments="")


if __name__ == "__main__":
    main()