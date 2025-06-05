# Stratification-DNS

This repository contains the scripts used to produce the figures and supporting data for the paper: "Analysing the global joint probability density behind thermal stratifications for a set of heterogeneous forcings, Paul M. Mannix and John Craske, (2025)."

The data presented has been generated using the scripts:

`rayleigh_benard_d2.py`

and

`rayleigh_benard_d3.py`

which run using the open source psuedo-spectral code [Dedalus](https://dedalus-project.org).


The results of these simulations have been processed using:

`PdfGenerator.py`

which generates the probability density functions (pdfs) and conditional averages or expectations presented in this paper. For convinience we not have supplied the large quantity of raw simulation data which these classes process but rather the processed data (which has been pickled so that it be easily reloaded for plotting) along with the diagnostics of each simulation are contained in the folder *data/*. Using the pickled objects the figures presented throughout the main body of the paper are generated using:

`Intro_figures.ipynb`

to plot the figures shown in the introduction

`plot_figures_homogeneous.py`

to plot the figures shown in section 4.1 and

`plot_figures_heterogeneous.py`

to plot the figures shown in section 4.2, while the figures presented in appendix B as well as the details of each simulation quoted in the tables can be reproduced by running:

`PdfPlotter.py`
