# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import pandas as pd
import pylab as plt
import math
import numpy as np

__package__ = "PDFs of velocity direction changes in time and difference between orientation and velocity direction"
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

#   The following section plot the probability of certain changes in velocity
#   direction. The graph will be relative to velocities above 2.0mm/s
#   if you put the > sign in the line:
#                 if running_avg_vel < v_limit :
#   Otherwise the graph will be relative to velocities under 2.0mm/s


theta = pd.DataFrame(pd.DataFrame(index=range(0,220000)))


diff = 0
exp_counter = -1
steps_for_running_avg = 7
v_limit = 2.0

for exp in data.exp.unique() :

  exp_counter += 1

  data_exp = data.loc[min(data.index[data['exp'] == exp]):max(data.index[data['exp'] == exp])]

#   The first time I create the dfs which will contain the orientation info
  if exp_counter == 0 :
    drug = " caf"
    theta_low = pd.DataFrame(pd.DataFrame(index=range(0,220000+2-steps_for_running_avg)))
    theta_low_shifted = pd.DataFrame(pd.DataFrame(index=range(0,220000+2-steps_for_running_avg)))
    theta_diff = pd.DataFrame(pd.DataFrame(index=range(0,220000+2-steps_for_running_avg)))
  if exp_counter == 1 :
    drug = " eth"
  if exp_counter == 2 :
    drug = " sug"
  
  data_exp.index = theta.index

  theta["theta -" + drug] = data_exp.theta
  
  
  inst_velocity = pd.DataFrame(data_exp.velmag_ctr)
  
  theta["theta running avg -" + drug] = np.nan
  theta["theta difference running avg -" + drug] = np.nan
  
  for i in range (int(steps_for_running_avg/2), len(inst_velocity)-int(steps_for_running_avg/2)-1):
  
#   I use the running average of the velocity and not the instant velocity
    running_avg_vel = 0.0
    
    for j in range (0, steps_for_running_avg) :
  
      running_avg_vel += inst_velocity.velmag_ctr[i-int(steps_for_running_avg/2)+j+diff]
  
    running_avg_vel = running_avg_vel/steps_for_running_avg

#   I also compute the running average of the orientation
    if running_avg_vel < v_limit :

      x_of_running_avg = 0.0
      y_of_running_avg = 0.0
      
      for j in range (0, steps_for_running_avg) :
    
        x_of_running_avg += np.cos(theta["theta -" + drug][i-int(steps_for_running_avg/2)+j])
        y_of_running_avg += np.sin(theta["theta -" + drug][i-int(steps_for_running_avg/2)+j])
        
      theta["theta running avg -" + drug][i-int(steps_for_running_avg/2)] = np.arctan2(y_of_running_avg, x_of_running_avg)

#   I can compute the difference only if there is a previous value
      if (i-int(steps_for_running_avg/2)-1) >= 0 :
        
        if theta["theta running avg -" + drug][i-int(steps_for_running_avg/2)-1] > -5 :
          
          theta["theta difference running avg -" + drug][i-int(steps_for_running_avg/2)] = theta["theta running avg -" + drug][i-int(steps_for_running_avg/2)]-theta["theta running avg -" + drug][i-int(steps_for_running_avg/2)-1]


#   This istogram is not easy to read so i take the bin information like
#   (n_sug, bins_sug, patches_sug) and graph it better later
numbins = 121

range_ext = 0.2

(n_sug, bins_sug, patches_sug) = plt.hist(theta["theta difference running avg - sug"], numbins, range=(-range_ext, range_ext), label="Sugar", color = 'r', alpha = 0.7)
(n_caf, bins_caf, patches_caf) = plt.hist(theta["theta difference running avg - caf"], numbins, range=(-range_ext, range_ext), label="Caffeine", color = 'b', alpha = 0.7)
(n_eth, bins_eth, patches_eth) = plt.hist(theta["theta difference running avg - eth"], numbins, range=(-range_ext, range_ext), label="Ethanol", color = 'g', alpha = 0.7)
plt.legend()
plt.xlabel("Variation of Orientation")
plt.ylabel("Frequency")
plt.tight_layout()
#plt.savefig('./Graphs/Variation of Orientation.pdf')
plt.show()
plt.close()

tot_caf = np.sum(n_caf)
tot_eth = np.sum(n_eth)
tot_sug = np.sum(n_sug)

#   I fill the df which will have all of the  information of the above hist
changes_of_theta = pd.DataFrame(pd.DataFrame(index=range(0, numbins)))

#   First I make a column with the central value for each bin
changes_of_theta["dtheta central"] = np.nan

for i in range (0, numbins) :
  changes_of_theta["dtheta central"][i] = -range_ext + range_ext/(numbins) + range_ext*2*(i/numbins)

#   Then for each bin and each drug I compute the probability
#   and the cumulative probability

changes_of_theta["prob caf"] = n_caf/tot_caf
changes_of_theta["cumprob caf"] = np.nan
cumulative_prob = 0.0

for i in range (0, numbins) :
  cumulative_prob += changes_of_theta["prob caf"][i]
  changes_of_theta["cumprob caf"][i] = cumulative_prob

changes_of_theta["prob eth"] = n_eth/tot_eth
changes_of_theta["cumprob eth"] = np.nan
cumulative_prob = 0.0

for i in range (0, numbins) :
  cumulative_prob += changes_of_theta["prob eth"][i]
  changes_of_theta["cumprob eth"][i] = cumulative_prob

changes_of_theta["prob sug"] = n_sug/tot_sug
changes_of_theta["cumprob sug"] = np.nan
cumulative_prob = 0.0

for i in range (0, numbins) :
  cumulative_prob += changes_of_theta["prob sug"][i]
  changes_of_theta["cumprob sug"][i] = cumulative_prob


plt.plot(changes_of_theta["dtheta central"], changes_of_theta["prob caf"], color='b', markersize=3, marker='o', label="Caffeine")
plt.plot(changes_of_theta["dtheta central"], changes_of_theta["prob eth"], color='g', markersize=3, marker='o', label="Ethanol")
plt.plot(changes_of_theta["dtheta central"], changes_of_theta["prob sug"], color='r', markersize=3, marker='o', label="Sugar")
plt.legend()
plt.xlabel("Variation of Orientation (rad)")
plt.ylabel("Probability")
plt.xlim(-0.2, 0.2)
plt.ylim(0, 0.5)
plt.tight_layout()
plt.savefig('./Graphs/Variation of Orientation (probability) (low).pdf')
plt.show()
plt.close()

#   The following section plot the probability of certain differences
#   between orientation and velocity direction.
#   The graph will be relative to velocities above 2.0mm/s
#   if you put the > sign in the line:
#                 if running_avg_vel > v_limit :
#   Otherwise the graph will be relative to velocities under 2.0mm/s


theta = pd.DataFrame(pd.DataFrame(index=range(0,220000)))
phi = pd.DataFrame(pd.DataFrame(index=range(0,220000)))


diff = 0
exp_counter = -1
steps_for_running_avg = 7
v_limit = 2.0

for exp in data.exp.unique() :

  exp_counter += 1

  data_exp = data.loc[min(data.index[data['exp'] == exp]):max(data.index[data['exp'] == exp])]

#   The first time I create the dfs which will contain the orientation info
  if exp_counter == 0 :
    drug = " caf"
    theta_low = pd.DataFrame(pd.DataFrame(index=range(0,220000+2-steps_for_running_avg)))
    theta_low_shifted = pd.DataFrame(pd.DataFrame(index=range(0,220000+2-steps_for_running_avg)))
    theta_diff = pd.DataFrame(pd.DataFrame(index=range(0,220000+2-steps_for_running_avg)))
    phi_low = pd.DataFrame(pd.DataFrame(index=range(0,220000+2-steps_for_running_avg)))
    phi_low_shifted = pd.DataFrame(pd.DataFrame(index=range(0,220000+2-steps_for_running_avg)))
    phi_diff = pd.DataFrame(pd.DataFrame(index=range(0,220000+2-steps_for_running_avg)))
  if exp_counter == 1 :
    drug = " eth"
  if exp_counter == 2 :
    drug = " sug"
  
  data_exp.index = theta.index

  theta["theta -" + drug] = data_exp.theta
  phi["phi -" + drug] = data_exp.phi
    
  inst_velocity = pd.DataFrame(data_exp.velmag_ctr)
  
  theta["theta running avg -" + drug] = np.nan
  theta["theta difference running avg -" + drug] = np.nan
  phi["phi running avg -" + drug] = np.nan
  phi["phi difference running avg -" + drug] = np.nan
  
  for i in range (int(steps_for_running_avg/2), len(inst_velocity)-int(steps_for_running_avg/2)-1):
  
#   As in the whole work above I use the running average of the velocity
#   and not the instant velocity
    running_avg_vel = 0.0
    
    for j in range (0, steps_for_running_avg) :
  
      running_avg_vel += inst_velocity.velmag_ctr[i-int(steps_for_running_avg/2)+j+diff]
  
    running_avg_vel = running_avg_vel/steps_for_running_avg

#   I also compute the running average of the orientation
    if running_avg_vel > v_limit :

      x_of_running_avg = 0.0
      y_of_running_avg = 0.0
      
      for j in range (0, steps_for_running_avg) :
    
        x_of_running_avg += np.cos(theta["theta -" + drug][i-int(steps_for_running_avg/2)+j])
        y_of_running_avg += np.sin(theta["theta -" + drug][i-int(steps_for_running_avg/2)+j])
        
      theta["theta running avg -" + drug][i-int(steps_for_running_avg/2)] = np.arctan2(y_of_running_avg, x_of_running_avg)

#   I can compute the difference only if there is a previous value
      if (i-int(steps_for_running_avg/2)-1) >= 0 :
        
        if theta["theta running avg -" + drug][i-int(steps_for_running_avg/2)-1] > -5 :
          
          theta["theta difference running avg -" + drug][i-int(steps_for_running_avg/2)] = theta["theta running avg -" + drug][i-int(steps_for_running_avg/2)]-theta["theta running avg -" + drug][i-int(steps_for_running_avg/2)-1]

      x_of_running_avg = 0.0
      y_of_running_avg = 0.0

      for j in range (0, steps_for_running_avg) :
    
        x_of_running_avg += np.cos(phi["phi -" + drug][i-int(steps_for_running_avg/2)+j])
        y_of_running_avg += np.sin(phi["phi -" + drug][i-int(steps_for_running_avg/2)+j])
        
      phi["phi running avg -" + drug][i-int(steps_for_running_avg/2)] = np.arctan2(y_of_running_avg, x_of_running_avg)

#   I can compute the difference only if there is a previous value
      if (i-int(steps_for_running_avg/2)-1) >= 0 :
        
        if phi["phi running avg -" + drug][i-int(steps_for_running_avg/2)-1] > -5 :
          
          phi["phi difference running avg -" + drug][i-int(steps_for_running_avg/2)] = phi["phi running avg -" + drug][i-int(steps_for_running_avg/2)]-phi["phi running avg -" + drug][i-int(steps_for_running_avg/2)-1]

#   Giving these values to na values these differences will be outside the range
#   and so will not be considered
theta = theta.fillna(-10)
phi = phi.fillna(10)


#   This istogram is not easy to read so i take the bin information like
#   (n_sug, bins_sug, patches_sug) and graph it better later

numbins = 121
range_ext = 2*math.pi

(n_sug, bins_sug, patches_sug) = plt.hist(theta["theta running avg - sug"] - phi["phi running avg - sug"], numbins, range=(-range_ext, range_ext), label="Sugar", color = 'r', alpha = 0.7)
(n_caf, bins_caf, patches_caf) = plt.hist(theta["theta running avg - caf"] - phi["phi running avg - caf"], numbins, range=(-range_ext, range_ext), label="Caffeine", color = 'b', alpha = 0.7)
(n_eth, bins_eth, patches_eth) = plt.hist(theta["theta running avg - eth"] - phi["phi running avg - eth"], numbins, range=(-range_ext, range_ext), label="Ethanol", color = 'g', alpha = 0.7)
plt.legend()
plt.xlabel("Theta - Phi (rad)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()
plt.close()

tot_caf = np.sum(n_caf)
tot_eth = np.sum(n_eth)
tot_sug = np.sum(n_sug)

#   I fill the df which will have all of the  information of the above hist
changes_of_theta = pd.DataFrame(pd.DataFrame(index=range(0, numbins)))

#   First I make a column with the central value for each bin
changes_of_theta["dtheta central"] = np.nan

for i in range (0, numbins) :
  changes_of_theta["dtheta central"][i] = -range_ext + range_ext/(numbins) + range_ext*2*(i/numbins)

#   Then for each bin and each drug I compute the probability
#   and the cumulative probability

changes_of_theta["prob caf"] = n_caf/tot_caf
changes_of_theta["cumprob caf"] = np.nan
cumulative_prob = 0.0

for i in range (0, numbins) :
  cumulative_prob += changes_of_theta["prob caf"][i]
  changes_of_theta["cumprob caf"][i] = cumulative_prob

changes_of_theta["prob eth"] = n_eth/tot_eth
changes_of_theta["cumprob eth"] = np.nan
cumulative_prob = 0.0

for i in range (0, numbins) :
  cumulative_prob += changes_of_theta["prob eth"][i]
  changes_of_theta["cumprob eth"][i] = cumulative_prob

changes_of_theta["prob sug"] = n_sug/tot_sug
changes_of_theta["cumprob sug"] = np.nan
cumulative_prob = 0.0

for i in range (0, numbins) :
  cumulative_prob += changes_of_theta["prob sug"][i]
  changes_of_theta["cumprob sug"][i] = cumulative_prob


#   I plot the probability of the histogram before
plt.plot(changes_of_theta["dtheta central"], changes_of_theta["prob caf"], color='b', markersize=3, marker='o', label="Caffeine")
plt.plot(changes_of_theta["dtheta central"], changes_of_theta["prob eth"], color='g', markersize=3, marker='o', label="Ethanol")
plt.plot(changes_of_theta["dtheta central"], changes_of_theta["prob sug"], color='r', markersize=3, marker='o', label="Sugar")
plt.legend()
plt.xlabel("Theta - Phi (rad)")
plt.ylabel("Probability")
plt.tight_layout()
plt.savefig('./Graphs/Theta - Phi (probability) (low).pdf')
plt.show()
plt.close()
