import os, pickle
from PdfGenerator import PdfGenerator
from PdfPlotter import PdfPlotter

Dir = '/home/pmannix/Stratification-DNS/'


intervals = {'IC':{'w':(-0.05,0.05),'b':(0.004,0.008)}, 'ICR':{'w':(-0.05,0.05),'b':(0.004,0.008)}, 'RBC':{'w':(-1,1),'b':(0.4,0.6)}, 
                'PLUME':{'w':(-0.075,0.075),'b':(-0.01,0.01)}, 'SINE':{'w':(-.5,.5),'b':(0.05,.25)}, 'STEP':{'w':(-1,1),'b':(0.2,.8)},'WALLPLUME':{'w':(-0.005,0.005),'b':(-0.005,0.005)}}


# # Paper figures section f_BZ
# # ~~~~~~~~~~~~~~ # ~~~~~~~~~~~~~~
# name = 'figures_fBZ_heterogeneous'
# print(name)
# os.mkdir(Dir+name) 
# os.chdir(Dir+name)

# with open(Dir+'data/STEP_pickled.pickle', 'rb') as f:
#     plotter = PdfPlotter(pdf=pickle.load(f), interval=intervals['STEP'])
#     plotter.plot_EBZ(term=r'\|\nabla B\|^2', figname='STEP_EdB2_BZ_and_f_BZ.png', Nlevels=40, sigma_smooth=.1)

# with open(Dir+'data/SINE_pickled.pickle', 'rb') as f:
#     plotter = PdfPlotter(pdf=pickle.load(f), interval=intervals['SINE'])
#     plotter.plot_EBZ(term=r'\|\nabla B\|^2', figname='SINE_EdB2_BZ_and_f_BZ.png', Nlevels=40, sigma_smooth=.1)


# with open(Dir+'data/PLUME_Intervalpickled.pickle', 'rb') as f:
#     plotter = PdfPlotter(pdf=pickle.load(f), interval=intervals['PLUME'])
#     plotter.plot_EBZ(term=r'\|\nabla B\|^2', figname='PLUME_EdB2_BZ_and_f_BZ_interval.png', Nlevels=20, sigma_smooth=.1)

# with open(Dir+'data/PLUME_pickled.pickle', 'rb') as f:
#     plotter = PdfPlotter(pdf=pickle.load(f), interval=intervals['PLUME'])
#     plotter.plot_EBZ(term=r'\|\nabla B\|^2', figname='PLUME_EdB2_BZ_and_f_BZ_normal.png', Nlevels=20, sigma_smooth=.1)


# with open(Dir+'data/WALLPLUME_Intervalpickled.pickle', 'rb') as f:
#     plotter = PdfPlotter(pdf=pickle.load(f), interval=intervals['WALLPLUME'])
#     plotter.plot_EBZ(term=r'\|\nabla B\|^2', figname='WALLPLUME_EdB2_BZ_and_f_BZ_interval.png', Nlevels=20, sigma_smooth=.1)

# with open(Dir+'data/WALLPLUME_pickled.pickle', 'rb') as f:
#     plotter = PdfPlotter(pdf=pickle.load(f), interval=intervals['WALLPLUME'])
#     plotter.plot_EBZ(term=r'\|\nabla B\|^2', figname='WALLPLUME_EdB2_BZ_and_f_BZ_normal.png', Nlevels=20, sigma_smooth=.1)


# os.chdir(Dir)



# Paper figures section f_WZ
# ~~~~~~~~~~~~~~ # ~~~~~~~~~~~~~~
name = 'figures_fWZ_heterogeneous'
print(name)
os.mkdir(Dir+name) 
os.chdir(Dir+name)

with open(Dir+'data/STEP_pickled.pickle', 'rb') as f:
    plotter = PdfPlotter(pdf=pickle.load(f), interval=intervals['STEP'])
    plotter.plot_EWZ(term=r'\|\nabla W \|^2', figname='STEP_E_dW2_WZ_and_f_WZ.png', Nlevels=100, sigma_smooth=1, Ra=1e09, norm='log')

with open(Dir+'data/SINE_pickled.pickle', 'rb') as f:
    plotter = PdfPlotter(pdf=pickle.load(f), interval=intervals['SINE'])
    plotter.plot_EWZ(term=r'\|\nabla W \|^2', figname='SINE_E_dW2_WZ_and_f_WZ.png', Nlevels=100, sigma_smooth=1, Ra=1e10, norm='log')

with open(Dir+'data/PLUME_Intervalpickled.pickle', 'rb') as f:
    plotter = PdfPlotter(pdf=pickle.load(f), interval=intervals['PLUME'])
    plotter.plot_EWZ(term=r'\|\nabla W \|^2', figname='PLUME_E_dW2_WZ_and_f_WZ.png', Nlevels=100, sigma_smooth=1, Ra=1e09, norm='log')

with open(Dir+'data/WALLPLUME_Intervalpickled.pickle', 'rb') as f:
    plotter = PdfPlotter(pdf=pickle.load(f), interval=intervals['WALLPLUME'])
    plotter.plot_EWZ(term=r'\|\nabla W \|^2', figname='WALLPLUME_E_dW2_WZ_and_f_WZ.png', Nlevels=100, sigma_smooth=1, Ra=1e09, norm='log')

os.chdir(Dir)


# Paper figures section f_WB
# ~~~~~~~~~~~~~~ # ~~~~~~~~~~~~~~
# name = 'figures_fWB_heterogeneous'
# print(name)
# os.mkdir(Dir+name) 
# os.chdir(Dir+name)

# with open(Dir+'data/STEP_pickled.pickle', 'rb') as f:
#     plotter = PdfPlotter(pdf=pickle.load(f), interval=intervals['STEP'])
#     plotter.plot_EWB(term=r'\nabla W^T \nabla B', figname='STEP_E_dWdB_WB_and_f_WB.png',  Nlevels=30, sigma_smooth=2, Ra=1e09)

# with open(Dir+'data/SINE_pickled.pickle', 'rb') as f:
#     plotter = PdfPlotter(pdf=pickle.load(f), interval=intervals['SINE'])
#     plotter.plot_EWB(term=r'\nabla W^T \nabla B', figname='SINE_E_dWdB_WB_and_f_WB.png',  Nlevels=30, sigma_smooth=1, Ra=1e10)

# with open(Dir+'data/PLUME_Intervalpickled.pickle', 'rb') as f:
#     plotter = PdfPlotter(pdf=pickle.load(f), interval=intervals['PLUME'])
#     plotter.plot_EWB(term=r'\nabla W^T \nabla B', figname='PLUME_E_dWdB_WB_and_f_WB.png', Nlevels=30, sigma_smooth=2, Ra=1e09)

# with open(Dir+'data/WALLPLUME_Intervalpickled.pickle', 'rb') as f:
#     plotter = PdfPlotter(pdf=pickle.load(f), interval=intervals['WALLPLUME'])
#     plotter.plot_EWB(term=r'\nabla W^T \nabla B', figname='WALLPLUME_E_dWdB_WB_and_f_WB.png',   Nlevels=30, sigma_smooth=2, Ra=1e09)

# os.chdir(Dir)