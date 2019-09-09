# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import pandas as pd
import pylab as plt
import numpy as np

__package__ = "PDF of distance to the closest Drosophila"
__author__  = "Davide Ravaglia (davide.ravaglia3@studio.unibo.it)"

#%%

data_name = 'data_original.csv'

plt.rcParams.update({'font.size': 15,
                    'xtick.major.size': 4,
                    'xtick.major.width': 2,
                    'ytick.major.size': 4,
                    'ytick.major.width': 2,
                    'axes.linewidth': 1.5})

if(os.path.isdir('./Graphs')):
  print('Folder already existing. The program will substitute existing files with the same name')
else:
  os.mkdir('Graphs')
  print('Creating folder "Graphs"')

data = pd.read_csv(data_name, sep=',', header=0, usecols=['exp', 'id',
       'theta', 'timestamps', 'x_mm', 'y_mm', 'phi', 'velmag_ctr','du_ctr',
       'dv_ctr', 'phisideways', 'dist2wall', 'theta2wall', 'dcenter',
       'anglesub', 'absthetadiff_center', 'closestfly_center', 'frame', 'dcenter'])

#I substitute 1 with 01 and so on so the id 10 will be after the id 9
#I only need to do it for exp_1 because the others are called: fly#_205_1

data['id'] = data['id'].replace('fly#_1_1', 'fly#_001_1')
data['id'] = data['id'].replace('fly#_2_1', 'fly#_002_1')
data['id'] = data['id'].replace('fly#_3_1', 'fly#_003_1')
data['id'] = data['id'].replace('fly#_4_1', 'fly#_004_1')
data['id'] = data['id'].replace('fly#_5_1', 'fly#_005_1')
data['id'] = data['id'].replace('fly#_6_1', 'fly#_006_1')
data['id'] = data['id'].replace('fly#_7_1', 'fly#_007_1')
data['id'] = data['id'].replace('fly#_8_1', 'fly#_008_1')
data['id'] = data['id'].replace('fly#_9_1', 'fly#_009_1')
data['id'] = data['id'].replace('fly#_10_1', 'fly#_010_1')

#So now I can sort the file

data = data.sort_values(['exp', 'id', 'timestamps'])

#%%

numbins_zoom = 50
maxrange_zoom = 10
maxrange_no_zoom = 50

numbins_no_zoom = int(numbins_zoom*maxrange_no_zoom/maxrange_zoom)
(n_real, bins_real, patches_real) =  plt.hist(data.dcenter, numbins_no_zoom, range=(0, maxrange_no_zoom))
plt.xlabel("Distance to Closest Fly (mm)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig('./Graphs/Distance to Closest Fly (freq).pdf')
plt.show()
plt.close()

#   Here I graph the cumulative probability of the probability distribution
cumprobs = pd.DataFrame(pd.DataFrame(index=range(0, numbins_no_zoom)))

#   First I make two columns with the central value for each bin
cumprobs["central"] = np.nan

for i in range (0, numbins_no_zoom) :
  cumprobs["central"][i] = maxrange_no_zoom/numbins_no_zoom*i + maxrange_no_zoom/(2*numbins_no_zoom)
  
#   Then for each bin, each drug and high and low I compute the probability
#   and the cumulative probability

#   Real part
cumprobs["prob (real)"] = n_real/n_real.sum()
cumprobs["cumprob (real)"] = np.nan
cumulative_prob = 0.0

for i in range (0, numbins_no_zoom) :
  cumulative_prob += cumprobs["prob (real)"][i]
  cumprobs["cumprob (real)"][i] = cumulative_prob

  
plt.plot(cumprobs["central"], cumprobs["prob (real)"], color='gold', label="Real Trails", marker='o', markersize=4, linewidth = 3)
plt.xlabel("Distance to closest Drosophila (mm)")
#plt.xlim(0, 10)
plt.ylabel("Probability")
plt.tight_layout()
plt.legend()
plt.savefig('./Graphs/Distance to closest Drosophila (prob).pdf')
#plt.savefig('./Graphs/Distance to closest Drosophila (zoom) (prob).pdf')
plt.show()
plt.close()
