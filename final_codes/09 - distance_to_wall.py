# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import pandas as pd
import pylab as plt
import numpy as np
import math

__package__ = "PDF and CDF of the distance to the wall both for the real data and one of the sets of random walks"
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
       'anglesub', 'absthetadiff_center', 'closestfly_center', 'frame'])

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

dist_to_center_rndm = pd.DataFrame(pd.DataFrame(index=range(0,660000)))
dist_to_center_rndm["distance"] = np.nan

#   path were you saved the random walks
extraction_path = './random_walk/many_walks/rndm_walks (seed=1).csv'
rndm_walks = pd.read_csv(extraction_path, sep=',', header=0, index_col='Unnamed: 0')

for exp in range(0, 3) :

  if exp == 0 :
    drug = "- caf"
  if exp == 1 :
    drug = "- eth"
  if exp == 2 :
    drug = "- sug"

  for id in range(0, 10) :

    print(exp, id)
    header_x = str(exp) + " - " + str(id) + " x"
    header_y = str(exp) + " - " + str(id) + " y"

    for i in range (0, 22000):
      
      dist_to_center_rndm["distance"][i+22000*id+220000*exp] =  50.0 - math.sqrt(math.pow(rndm_walks[header_x][i], 2) + math.pow(rndm_walks[header_y][i], 2))


numbins = 50
min_range = 0
max_range = 50

(n_real, bins_real, patches_real) = plt.hist(data.dist2wall, numbins, range=(min_range, max_range), color='gold', alpha=0.6, label="Real Trails")
(n_fake, bins_fake, patches_fake) = plt.hist(dist_to_center_rndm["distance"], numbins, range=(min_range, max_range), color='darkviolet', alpha=0.6, label="Random Walks")
plt.xlabel("Distance to closest wall (mm)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.legend()
plt.show()
plt.close()

#   Here I graph the cumulative probability of the probability distribution
cumprobs = pd.DataFrame(pd.DataFrame(index=range(0, numbins)))

#   First I make two columns with the central value for each bin
cumprobs["central"] = np.nan

for i in range (0, numbins) :
  cumprobs["central"][i] = max_range/numbins*i + max_range/(2*numbins)
  
#   Then for each bin, each drug and high and low I compute the probability
#   and the cumulative probability

#   Real part
cumprobs["prob (real)"] = n_real/n_real.sum()
cumprobs["cumprob (real)"] = np.nan
cumulative_prob = 0.0

for i in range (0, numbins) :
  cumulative_prob += cumprobs["prob (real)"][i]
  cumprobs["cumprob (real)"][i] = cumulative_prob

#   Rndm walks part
cumprobs["prob (fake)"] = n_fake/n_fake.sum()
cumprobs["cumprob (fake)"] = np.nan
cumulative_prob = 0.0

for i in range (0, numbins) :
  cumulative_prob += cumprobs["prob (fake)"][i]
  cumprobs["cumprob (fake)"][i] = cumulative_prob

plt.plot(cumprobs["central"], cumprobs["prob (real)"], color='gold', label="Real Trails", marker='o', markersize=4, linewidth = 3)
plt.plot(cumprobs["central"], cumprobs["prob (fake)"], color='darkviolet', label="Random Walks", marker='o', markersize=4, linewidth = 3)
plt.xlabel("Distance to closest wall (mm)")
plt.xlim(0, 10)
plt.ylabel("Probability")
plt.tight_layout()
plt.legend()
plt.savefig('./Graphs/Distance to closest wall (prob).pdf')
plt.show()
plt.close()

plt.plot(cumprobs["central"], cumprobs["cumprob (real)"], color='gold', label="Real Trails", marker='o', markersize=4, linewidth = 3)
plt.plot(cumprobs["central"], cumprobs["cumprob (fake)"], color='darkviolet', label="Random Walks", marker='o', markersize=4, linewidth = 3)
plt.xlabel("Distance to closest wall (mm)")
plt.xlim(0, 50)
plt.ylabel("Cumulative Probability")
plt.tight_layout()
plt.legend()
plt.savefig('./Graphs/Distance to closest wall (cum prob).pdf')
plt.show()
plt.close()
