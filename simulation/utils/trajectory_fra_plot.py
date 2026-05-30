import numpy as np
from scipy.interpolate import PchipInterpolator
import os
import matplotlib.pyplot as plt

def generate_curve(t_sp, x_sp, t_eval):
    csx = PchipInterpolator(t_sp, x_sp)
    x_traj = csx(t_eval) # Result is shape (len(t_eval), ns)
    return x_traj

def main():
    # Set global plot style
    plt.rc('font', family='serif')
    
    T_end = 10.0
    dt = 0.01
    n_points = 12
    t_sp = np.array([0.0, 1*T_end/20, 2*T_end/20, 3*T_end/20, 6*T_end/20, 9*T_end/20, 10*T_end/20, 11*T_end/20, 14*T_end/20, 17*T_end/20, 18*T_end/20, T_end])
    x_sp = np.array([[-0.78, -0.15145, -0.005491, np.pi/2, 0, 0], 
                     [-0.5, 0.0, 0.2, np.pi/2, 0, 0], 
                     [0.0, 0.5, 0.2, np.pi, 0, 0], 
                     [0.3, 0.0, 0.2, np.pi, 0, 0],
                     [0.3, 0.0, 0.05, np.pi, 0, 0], 
                     [0.3, 0.0, 0.2, np.pi, 0, 0], 
                     [0.0, -0.5, 0.2, np.pi, 0, 0], 
                     [-0.3, 0.0, 0.2, np.pi, 0, 0], 
                     [-0.3, 0.0, 0.05, np.pi, 0, 0],
                     [-0.3, 0.0, 0.2, np.pi, 0, 0], 
                     [0.0, 0.3, 0.5, np.pi, 0, 0], 
                     [0.0, 0.3, 0.5, np.pi, 0, 0]])
    cond_sp = np.array([False, False, False, False, True, True, True, True, False, False, False, False])
    t_eval = np.arange(0, T_end+1, dt)
    
    x_traj = generate_curve(t_sp, x_sp, t_eval)
    
    indices = np.digitize(t_eval, t_sp, right=False) - 1
    indices = np.clip(indices, 0, len(cond_sp) - 1)
    cond_traj = cond_sp[indices]
    
    # --- PLOTTING ---
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 10), sharex=True)
    # fig.suptitle('Trajectory Reference', fontsize=16)

    # 1. Position Plot
    # ax1.set_title('Position')
    labels_pos = ['X', 'Y', 'Z']
    for i in range(3):
        line, = ax1.plot(t_eval, x_traj[:, i], label=labels_pos[i])
        ax1.plot(t_sp, x_sp[:, i], 'o', color=line.get_color())
        
    ax1.set_ylabel('Position [m]')
    ax1.grid(True)
    ax1.set_xlim(0, T_end)
    ax1.legend(loc='upper right')

    # 2. Orientation Plot
    # ax2.set_title('Orientation')
    labels_ori = ['Roll', 'Pitch', 'Yaw']
    for i in range(3, 6):
        line, = ax2.plot(t_eval, x_traj[:, i], label=labels_ori[i-3])
        ax2.plot(t_sp, x_sp[:, i], 'o', color=line.get_color())
        
    ax2.set_ylabel('Orientation [rad]')
    ax2.grid(True)
    ax2.set_xlim(0, T_end)
    ax2.legend(loc='upper right')

    # 3. Condition Plot (Boolean)
    # ax3.set_title('Condition')
    line, = ax3.plot(t_eval, cond_traj, label='Cond', color='tab:red')
    ax3.plot(t_sp, cond_sp, 'o', color=line.get_color())
    
    ax3.set_ylabel('State')
    ax3.set_yticks([0, 1])
    ax3.set_yticklabels(['False', 'True'])
    ax3.set_xlabel('Time [s]')
    ax3.grid(True)
    ax3.set_xlim(0, T_end)
    ax3.legend(loc='upper right')

    plt.tight_layout()
    plt.show()
    
    # --- SAVING CSV ---
    t_eval_reshaped = t_eval.reshape(-1, 1)
    cond_traj_reshaped = cond_traj.reshape(-1, 1)
    
    output = np.hstack((t_eval_reshaped, cond_traj_reshaped, x_traj))
    
    np.savetxt("trajectory.csv", output, delimiter=',', header="Time,Cond,X,Y,Z,Roll,Pitch,Yaw", comments="")

if __name__ == "__main__":
    main()