"""
Plot data generated using main.py

python3 plot_homogeneous_3D.py

"""

import h5py
import numpy as np
import matplotlib.pyplot as plt
from   scipy.interpolate import interp1d

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "sans-serif",
    "font.sans-serif": "Helvetica",
    'text.latex.preamble': r'\usepackage{amsfonts}'
})


def main(data_dir):
    """Save plot of specified tasks for given range of analysis writes."""

    # Plot writes
    with h5py.File(data_dir + "/snapshots/snapshots_s1.h5", mode='r') as file:
        b = file['tasks/buoyancy'][:, :, :]
        t = file['tasks/buoyancy'].dims[0][0][:]; print(len(t))
        x = file['tasks/buoyancy'].dims[1][0][:]; print(x[-1],x[0])
        z = file['tasks/buoyancy'].dims[2][0][:]; print(z[-1],z[0])

        fig, ax = plt.subplots(figsize=(12,3),layout='constrained')
        ax.set_xlabel(r'$X_1$',fontsize=20)
        ax.set_ylabel(r'$X_2$',fontsize=20)
        ax.tick_params(axis='both', labelsize=20)
        quad = ax.pcolormesh(x, z, b[-1, :, :].T, cmap='RdBu_r', vmin=-0.005, vmax=0.005)
        #fig.colorbar(quad, ax=ax)
        fig.savefig('homogeneous_RBC', dpi=100)
        fig.clear()

    plt.close(fig)

    return None


def video(data_dir):
    """Save plot of specified tasks for given range of analysis writes."""

    import matplotlib.animation as animation

    # Plot writes
    with h5py.File(data_dir + "/snapshots/snapshots_s1.h5", mode='r') as file:
        
        b = file['tasks/buoyancy'][:, :, :]
        t = file['tasks/buoyancy'].dims[0][0][:]
        x = file['tasks/buoyancy'].dims[1][0][:]
        z = file['tasks/buoyancy'].dims[2][0][:]

        fig, ax = plt.subplots(figsize=(12,3),layout='constrained')
        ax.set_xlabel(r'$X_1$',fontsize=20)
        ax.set_ylabel(r'$X_2$',fontsize=20)
        ax.tick_params(axis='both', labelsize=20)
        quad = ax.pcolormesh(x, z, b[-1, :, :].T, cmap='RdBu_r', vmin=-0.005, vmax=0.005)
        #fig.colorbar(quad, ax=ax)
       
        # Animation function
        def update(frame):
            print('frame = %d/%d \n'%(frame,int(b.shape[0])))
            Z = b[frame, :, :].T
            quad.set_array(Z.ravel())  # Update the pcolormesh data
            return quad,

        # Create animation
        ani = animation.FuncAnimation(fig, update, frames=int(b.shape[0]), interval=5, blit=False)
        ani.save("Plumes_animation.mp4", writer="ffmpeg", fps=25)

        plt.close(fig)

    return None


def energy_spectrum(data_dir, N=100):
    """
    Compute the energy spectrum and the horizontally averaged spectra of the velocity field
    
    The energy spectrum see chapter 6 pope is defined as
    
    E(k,t) = < u_hat*(k,t) u_hat(k,t)>

    where 
    
    u(x) = sum u_hat e^ikx = sum (A_k + i*B_k)*(cos(k x) + i*sin(k x))

    thus

    E(k,t) = < u_hat*(k,t) u_hat(k,t)> = A_k**2 + B_k**2

    In Dedalus the amplitudes are stored as sine and cosine 

    u(x) = sum_k A_k cos(k x) - B_k sin(k x)
    
    therefore we just access A_k and B_k and square them.
    """

    f = h5py.File(data_dir + "/snapshots/snapshots_s1.h5", mode='r')
    
    # Ordering of coefficients is 
    # cos(0*x),sin(0*x), cos(1*x),sin(1*x), .... 
    # in each dimension
    b_k = f['tasks/b_k'][-1, :, :, :]

    u_k = f['tasks/u_k'][-1, :, :, :]
    v_k = f['tasks/v_k'][-1, :, :, :]
    w_k = f['tasks/w_k'][-1, :, :, :]
    
    t  = f['tasks/u_k'].dims[0][0][:]
    kx = f['tasks/u_k'].dims[1][0][::2, ::2, ::2]
    ky = f['tasks/u_k'].dims[2][0][::2, ::2, ::2]
    kz = f['tasks/u_k'].dims[3][0][::2, ::2, ::2]

    f.close()

    # 1) First square all the amplitudes
    R_ii = u_k**2 + v_k**2 + w_k**2
    B_k = b_k**2

    # 2) Convert to k=0,1,2,.. ordering
    R_ii = R_ii[::2, ::2, ::2] + R_ii[1::2, 1::2, 1::2]
    B_k  = B_k[::2, ::2, ::2]  +  B_k[1::2, 1::2, 1::2]
    
    # 3) Define the vector k = (kx,ky,kz)
    kx = np.unique(kx)
    ky = np.unique(ky)
    kz = np.unique(kz)

    # 4) Convert to the energy spectrum i.e. E(|k|) vs. |k|     
    Eu_1d, k = average_over_shells_3D_v2(R_ii,kx, ky, kz)
    Eb_1d, k = average_over_shells_3D_v2(B_k, kx, ky, kz)

    # 5) Convert to the 2D energy spectrum i.e. E(k_h,k_z) vs. k_h = |(k_x,k_y)|, k_z     
    Eu_2d, kh = average_over_discs_2D_v2(R_ii,kx, ky, kz)
    Eb_2d, kh = average_over_discs_2D_v2(B_k, kx, ky, kz)


    fig = plt.figure(figsize=(8,4), layout='constrained')

    ax1 = fig.add_subplot(121)
    ax1.semilogy(k, Eu_1d)
    ax1.set_xlabel(r'$|\mathbf{k}|$')
    ax1.set_ylabel(r'$E_U(|\mathbf{k}|,t)$')
    #ax1.set_ylim([1e-08, 1e-02])
    ax1.set_xlim([0, np.max(k)])
    
    ax2 = fig.add_subplot(122)
    for i, kz_i in enumerate(kz):
        if (i%5 == 0) and (i !=0):
            ax2.semilogy(kh, Eu_2d[:, i], label=r'$k_z = %d$' % kz_i)
    ax2.set_xlabel(r'$k_H$')
    ax2.set_ylabel(r'$E_U(k_H,k_z,t)$')
    #ax2.set_ylim([1e-16, 1e-02])
    ax2.set_xlim([0, np.max(k)])
    ax2.legend()

    fig.savefig('Kinetic Energy Spectra', dpi=100)
    plt.close(fig)

    # Create a 3D plot
    fig = plt.figure(figsize=(8,4), layout='constrained')

    ax1 = fig.add_subplot(121)
    ax1.semilogy(k, Eb_1d)
    ax1.set_xlabel(r'$|\mathbf{k}|$')
    ax1.set_ylabel(r'$E_B(|\mathbf{k}|,t)$')
    #ax1.set_ylim([1e-08, 1e-02])
    ax1.set_xlim([0, np.max(k)])
    
    ax2 = fig.add_subplot(122)
    for i, kz_i in enumerate(kz):
        if (i%5 == 0) and (i !=0):
            ax2.semilogy(kh, Eb_2d[:, i], label=r'$k_z = %d$' % kz_i)
    ax2.set_xlabel(r'$k_H$')
    ax2.set_ylabel(r'$E_B(k_H,k_z,t)$')
    #ax2.set_ylim([1e-16, 1e-02])
    ax2.set_xlim([0, np.max(kh)])
    ax2.legend()

    fig.savefig('Buoyancy Energy Spectra', dpi=100)
    plt.close(fig)

    return None


def time_series(data_dir):
    """Plot the time-series of the Kinetic energy and buoyancy variance."""

    f  = h5py.File(data_dir + 'scalar_data/scalar_data_s1.h5', mode='r')
    
    # Shape time,x,y,z
    Eu     = f['tasks/Eu(t)'][:,0,0]
    Eb     = f['tasks/Eb(t)'][:,0,0]
    wB_avg = f['tasks/<wB>'][:,0,0]
    B_avg  = f['tasks/<B>' ][:,0,0]

    dU2_avg = f['tasks/dU^2(t)_div_Re'][:,0,0]
    dB2_avg  = f['tasks/dB^2(t)' ][:,0,0]

    t      = f['scales/sim_time'][()]
    
    f.close()

    fig, axs = plt.subplots(nrows=2,ncols=2,figsize=(8,4),constrained_layout=True)
    
    axs[0, 0].semilogy(t,Eu,'b-',label=r'$E_u$')
    axs[0, 0].set_title(r'$E_u$')
    axs[0, 1].semilogy(t,Eb,'r-',label=r'$E_b$')
    axs[0, 1].set_title(r'$E_b$')
    
    axs[1, 0].plot(t,wB_avg,'b:',label=r'$\langle wB \rangle$')
    axs[1, 0].set_title(r'$\langle wB \rangle$')
    axs[1, 1].plot(t, B_avg,'r:',label=r'$\langle B  \rangle$')
    axs[1, 1].set_title(r'$\langle B  \rangle$')
    
    fig.savefig('EnergyTimeSeries.png',dpi=100)
    plt.close(fig)

    return None



def interp(y, x, x_new):
    """Interpolate the Chebyshev points onto a uniform grid."""

    y_new = interp1d(x, y, axis=1, fill_value="extrapolate")

    return y_new(x_new)

def load_data(frames):
    """Load the data from the dedalus format."""    
    
    print('------  Loading Data ------- \n ')

    file  = h5py.File('snapshots/snapshots_s1.h5', mode='r')
    
    # Y = [W,B,Z], y = [w,b,z] 
    w_split = []; 
    b_split = []; 
    x_cheb = file['tasks/buoyancy'].dims[1][0][:]
    z_cheb = file['tasks/buoyancy'].dims[2][0][:]
    z_data = np.linspace(z_cheb[0],z_cheb[-1],2**10)
    
    # dpGrad_split = [];
    # b2Grad_split = []; 
    # wbGrad_split = []; 
    # w2Grad_split = []; 

    for i in range(1, frames + 1,1):
    
        # PDF variables ---------------------
        w_cheb = file['tasks/w'       ][-i,:,:]
        b_cheb = file['tasks/buoyancy'][-i,:,:]

        # # Expectation variables -------------
        # try:
        #     dP_z = file['tasks/grad_p'][-i,1,:,:]# d/dz
        #     dB_x = file['tasks/grad_b'][-i,0,:,:]# d/dx
        #     dB_z = file['tasks/grad_b'][-i,1,:,:]# d/dz
        #     dW_x = file['tasks/grad_w'][-i,0,:,:]# d/dx
        #     dW_z = file['tasks/grad_w'][-i,1,:,:]# d/dz
        # except:
        #     dP_z = file['tasks/grad_pz'][-i,:,:]# d/dz
        #     dB_x = file['tasks/grad_bx'][-i,:,:]# d/dx
        #     dB_z = file['tasks/grad_bz'][-i,:,:]# d/dz
        #     dW_x = file['tasks/grad_wx'][-i,:,:]# d/dx
        #     dW_z = file['tasks/grad_wz'][-i,:,:]# d/dz
            
        # R_00 = (dB_x**2   + dB_z**2  )
        # R_01 = (dB_x*dW_x + dB_z*dW_z)
        # R_11 = (dW_x**2   + dW_z**2  )
        
        w_split.append( interp(w_cheb, z_cheb, z_data) )
        b_split.append( interp(b_cheb, z_cheb, z_data) )
        # dpGrad_split.append( interp(dP_z, z_cheb, z_data) )
        # b2Grad_split.append(interp(R_00, z_cheb, z_data) )
        # wbGrad_split.append(interp(R_01, z_cheb, z_data) )
        # w2Grad_split.append(interp(R_11, z_cheb, z_data) )

    w_data = np.concatenate(w_split)
    b_data = np.concatenate(b_split)

    # dpGrad_data = np.concatenate(dpGrad_split)
    # b2Grad_data = np.concatenate(b2Grad_split)
    # wbGrad_data = np.concatenate(wbGrad_split)
    # w2Grad_data = np.concatenate(w2Grad_split)
    
    return w_data,b_data,z_data#,    dpGrad_data,b2Grad_data,wbGrad_data,w2Grad_data


def pdfs(frames):
    """Save plot the joint pdf f_WB."""

    w_data,b_data,z_data  = load_data(frames)

    f_WB, w_edges, b_edges = np.histogram2d(w_data.flatten(),b_data.flatten(), range = [[-0.05,0.05], [-0.005,0.005]], bins=(92, 92), density=True)
    w = .5*(w_edges[1:] + w_edges[:-1])
    b = .5*(b_edges[1:] + b_edges[:-1])

    dw = w[1]-w[0]
    db = b[1]-b[0]

    f_W = np.nansum(f_WB, axis=1)*db
    f_B = np.nansum(f_WB, axis=0)*dw

    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(12,6), layout='constrained')

    # First column
    ax[0].set_ylabel('$f_B$', fontsize=25)
    ax[0].set_xlabel('$b$', fontsize=25)
    #ax[0,0].plot(x, f_X, 'r-')
    ax[0].stairs(f_B, b_edges)
    ax[0].fill_between(x=b,y1=f_B,color= "r",alpha= 0.2)
    ax[0].set_ylim([0,1.1*max(f_B)])
    ax[0].set_xlim([-0.005,0.005])

    ax[1].set_title(r'$f_{WB}$', fontsize=25)
    cf = ax[1].pcolormesh(b,w,f_WB, cmap='Reds', norm='log')
    #fig.colorbar(cf, ax=ax1)
    ax[1].set_xlabel('$b$', fontsize=25)
    ax[1].set_ylabel('$w$', fontsize=25)
    ax[1].set_xlim([-0.005,0.005])
    ax[1].set_ylim([-0.05,0.05])

    ax[2].set_xlabel('$w$', fontsize=25)
    ax[2].set_ylabel('$f_W$', fontsize=25)
    #ax[2].plot(f_W, w, 'r-')
    ax[2].stairs(f_W, w_edges)
    ax[2].fill_between(x=w,y1=f_W,color= "r",alpha= 0.2)
    ax[2].set_ylim([0,1.1*max(f_W)])
    ax[2].set_xlim([-0.05,0.05])

    fig.savefig('PDF_Lundgren_f_WB.png', dpi=100)
    plt.show()

    return None


if __name__ == "__main__":

    #data_dir = "/data/pmannix/PDF_DNS_Data/Sim_WALLPLUME_Ra1e09/"
    #video(data_dir)
    #main(data_dir)

    data_dir = "/data/pmannix/PDF_DNS_Data/Sim_PLUME_Ra1e09/"
    video(data_dir)
    main(data_dir)
    #time_series(data_dir)
    #energy_spectrum(data_dir)
    #pdfs(frames = 10**3)
