# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import pandas as pd
import pylab as plt
import math
import numpy as np

__package__ = "df phi: Running average of velocity direction and its variation. df stats_of_bars : number and averages of velocities which are correlated to certain vel dir changes."
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

v_limit = 2.0

#   I have to use a running avg for the velocity otherwise it changes too fast
#   so I define how many steps of 1/15 s I consider in the running average
steps_for_running_avg = 7


#   I divide the x-axis (velocity direction difference) into n_division
#   bars for both the low and the high graph. For each bar I compute the
#   mean and the deviation
n_division = 301

stats_of_bars = pd.DataFrame(pd.DataFrame(index=range(0,n_division)))

#   Here I merge all of what I've done before and do more stuff.
#   Basically I fill the df stats_of_bars with the different stats
#   dividing for the 3 groups.

#   Phi central is only determined by n_division so it will be the same for
#   all the different drugs
stats_of_bars["phi central"] = np.nan

for i in range (0, n_division) :
  
  higher = -math.pi*2 + math.pi*4*(i+1)/n_division
  lower = -math.pi*2 + math.pi*4*i/n_division
  
  stats_of_bars["phi central"][i] = lower + (higher-lower)/2

phi = pd.DataFrame(pd.DataFrame(index=range(0,220000)))

exp_counter = 0

for exp in data.exp.unique() :

  exp_counter += 1

  if exp_counter == 1 :
    drug = "- caf"
  if exp_counter == 2 :
    drug = "- eth"
  if exp_counter == 3 :
    drug = "- sug"
    
  print(drug)
  
#   average and std are exactly what they look like, high and low are the
#   two different parts divided by v_limit
  avg_high_header = "average (high)"
  avg_low_header = "average (low)"
  std_high_header = "std (high)"
  std_low_header = "std (low)"
  counter_high_header = "counter (high)"
  counter_low_header = "counter (low)"

  avg_high_header += drug
  avg_low_header += drug
  std_high_header += drug
  std_low_header += drug
  counter_high_header += drug
  counter_low_header += drug

  stats_of_bars[avg_high_header] = np.nan
  stats_of_bars[avg_low_header] = np.nan
  stats_of_bars[std_high_header] = np.nan
  stats_of_bars[std_low_header] = np.nan
  stats_of_bars[counter_high_header] = np.nan
  stats_of_bars[counter_low_header] = np.nan

#   The data I will use  
  data_exp = data.loc[min(data.index[data['exp'] == exp]):max(data.index[data['exp'] == exp])]

  print("Estratto data")

#   I reset to 0 the start of the data_exp index  
  data_exp.index = phi.index

  phi["phi running avg " + drug] = 0.0
  phi["phi difference running avg " + drug] = 0.0
  
  phi["phi " + drug] = data_exp.phi

#   I extract the velocity from the data
  inst_velocity = pd.DataFrame(data_exp.velmag_ctr)

#   I divide the velocity based the v_limit into high and low
  inst_velocity_high = pd.DataFrame(pd.DataFrame(index=range(0,len(inst_velocity)+1-steps_for_running_avg)))
  inst_velocity_low = pd.DataFrame(pd.DataFrame(index=range(0,len(inst_velocity)+1-steps_for_running_avg)))
  
  inst_velocity_high["velocity"] = np.nan
  inst_velocity_low["velocity"] = np.nan

  for i in range (int(steps_for_running_avg/2), len(inst_velocity)-int(steps_for_running_avg/2)-1):

#   I also compute the running average of the velocity direction
    x_of_running_avg = 0.0
    y_of_running_avg = 0.0
    
    for j in range (0, steps_for_running_avg) :
  
      x_of_running_avg += np.cos(phi["phi " + drug][i-int(steps_for_running_avg/2)+j])
      y_of_running_avg += np.sin(phi["phi " + drug][i-int(steps_for_running_avg/2)+j])
      
    phi["phi running avg " + drug][i-int(steps_for_running_avg/2)] = np.arctan2(y_of_running_avg, x_of_running_avg)
    
    if (i-int(steps_for_running_avg/2)) > 0 :
      
      phi["phi difference running avg " + drug][i-int(steps_for_running_avg/2)] = phi["phi running avg " + drug][i-int(steps_for_running_avg/2)]-phi["phi running avg " + drug][i-int(steps_for_running_avg/2)-1]

    else : phi["phi difference running avg " + drug][i-int(steps_for_running_avg/2)] = 0.0
  
phi.to_csv('./random_walk/phi_diff_running_avg.csv')


phi = pd.read_csv('./random_walk/phi_diff_running_avg.csv', sep=',', header=0, index_col='Unnamed: 0')

exp_counter = 0

for exp in data.exp.unique() :

  exp_counter += 1

  if exp_counter == 1 :
    drug = "- caf"
  if exp_counter == 2 :
    drug = "- eth"
  if exp_counter == 3 :
    drug = "- sug"
    
  print(drug)
  
#   average and std are exactly what they look like, high and low are the
#   two different parts divided by v_limit
  avg_high_header = "average (high)"
  avg_low_header = "average (low)"
  std_high_header = "std (high)"
  std_low_header = "std (low)"
  counter_high_header = "counter (high)"
  counter_low_header = "counter (low)"

  avg_high_header += drug
  avg_low_header += drug
  std_high_header += drug
  std_low_header += drug
  counter_high_header += drug
  counter_low_header += drug

  stats_of_bars[avg_high_header] = np.nan
  stats_of_bars[avg_low_header] = np.nan
  stats_of_bars[std_high_header] = np.nan
  stats_of_bars[std_low_header] = np.nan
  stats_of_bars[counter_high_header] = np.nan
  stats_of_bars[counter_low_header] = np.nan

#   The data I will use  
  data_exp = data.loc[min(data.index[data['exp'] == exp]):max(data.index[data['exp'] == exp])]

  print("Estratto data")

#   I reset to 0 the start of the data_exp index  
  data_exp.index = phi.index
#   I extract the velocity from the data
  inst_velocity = pd.DataFrame(data_exp.velmag_ctr)

#   I divide the velocity based the v_limit into high and low
  inst_velocity_high = pd.DataFrame(pd.DataFrame(index=range(0,len(inst_velocity)+1-steps_for_running_avg)))
  inst_velocity_low = pd.DataFrame(pd.DataFrame(index=range(0,len(inst_velocity)+1-steps_for_running_avg)))
  
  inst_velocity_high["velocity"] = np.nan
  inst_velocity_low["velocity"] = np.nan

  for i in range (int(steps_for_running_avg/2), len(inst_velocity)-int(steps_for_running_avg/2)-1):

#   As in the whole work above I use the running average of the velocity
#   and not the instant velocity
    running_avg_vel = 0.0
    
    for j in range (0, steps_for_running_avg) :

      running_avg_vel += inst_velocity.velmag_ctr[i-int(steps_for_running_avg/2)+j]

    running_avg_vel = running_avg_vel/steps_for_running_avg

    if running_avg_vel < v_limit :
      inst_velocity_low.velocity[i-int(steps_for_running_avg/2)] = running_avg_vel
  
    else :
      inst_velocity_high.velocity[i-int(steps_for_running_avg/2)] = running_avg_vel

#   I also compute the running average of the velocity direction
    x_of_running_avg = 0.0
    y_of_running_avg = 0.0
      
  print("Ottenute le running avg della velocità")


  high_not_reset_streak = 0
  low_not_reset_streak = 0
  
  for i in range (0, n_division) :
    
    not_reset_high_variables = 0
    not_reset_low_variables = 0

    if not_reset_high_variables == 0 :

      avg_temp_high = 0.0
      counter_high = 0
      square_diff_sum_high = 0.0

    if not_reset_low_variables == 0 :

      avg_temp_low = 0.0
      counter_low = 0
      square_diff_sum_low = 0.0
  
    higher = -math.pi*2 + math.pi*4*(i+1)/n_division
    lower = -math.pi*2 + math.pi*4*i/n_division

#    print("divisione ", i+1, " calcolo le medie")
    
#   I compute the average
    for j in range (int(steps_for_running_avg/2), len(phi)-int(steps_for_running_avg/2)-1) :
      
      if phi["phi difference running avg " + drug][j] <= higher and phi["phi difference running avg " + drug][j] > lower :
        
        if inst_velocity_high.velocity[j-int(steps_for_running_avg/2)] >= v_limit :
        
          avg_temp_high += inst_velocity_high.velocity[j-int(steps_for_running_avg/2)]
          counter_high += 1
  
        else :
  
          avg_temp_low += inst_velocity_low.velocity[j-int(steps_for_running_avg/2)]
          counter_low += 1

#   I can't do statistics unless I have 30 events
    if counter_high > 30 or i == 0 :
        
      stats_of_bars[avg_high_header][i] = avg_temp_high/counter_high
      
      for fill_before in range (1, high_not_reset_streak+1) :
        stats_of_bars[avg_high_header][i-fill_before] = avg_temp_high/counter_high
        
    else :
      
      not_reset_high_variables = 1
      high_not_reset_streak += 1
  
    if counter_low > 30 or i == 0 :
  
      stats_of_bars[avg_low_header][i] = avg_temp_low/counter_low

      for fill_before in range (1, low_not_reset_streak+1) :
        stats_of_bars[avg_low_header][i-fill_before] = avg_temp_low/counter_low

    else :
      
      not_reset_low_variables = 1
      low_not_reset_streak += 1

#    print("divisione ", i+1, " calcolo le std")
      
#   I compute the std
    for j in range (int(steps_for_running_avg/2), len(phi)-int(steps_for_running_avg/2)-1) :
      
      if phi["phi difference running avg " + drug][j] <= higher and phi["phi difference running avg " + drug][j] > lower :
        
        if inst_velocity_high.velocity[j-int(steps_for_running_avg/2)] >= v_limit :
        
          square_diff_sum_high += math.pow(inst_velocity_high.velocity[j-int(steps_for_running_avg/2)] - stats_of_bars[avg_high_header][i - high_not_reset_streak], 2)
  
        else :
  
          square_diff_sum_low += math.pow(inst_velocity_low.velocity[j-int(steps_for_running_avg/2)] - stats_of_bars[avg_low_header][i - low_not_reset_streak], 2)

    if counter_high > 30 or i == 0 :
        
      stats_of_bars[std_high_header][i] = math.sqrt(square_diff_sum_high/(counter_high-1))

      for fill_before in range (1, high_not_reset_streak+1) :
        stats_of_bars[std_high_header][i-fill_before] = math.sqrt(square_diff_sum_high/(counter_high-1))
        stats_of_bars[counter_high_header][i-fill_before] = int(counter_high/(high_not_reset_streak+1))

      stats_of_bars[counter_high_header][i] = int(counter_high/(high_not_reset_streak+1))

      not_reset_high_variables = 0
      high_not_reset_streak = 0


    if counter_low > 30 or i == 0 :
  
      stats_of_bars[std_low_header][i] = math.sqrt(square_diff_sum_low/(counter_low-1))

      for fill_before in range (1, low_not_reset_streak+1) :
        stats_of_bars[std_low_header][i-fill_before] = math.sqrt(square_diff_sum_low/(counter_low-1))
        stats_of_bars[counter_low_header][i-fill_before] = int(counter_low/(low_not_reset_streak+1))

      stats_of_bars[counter_low_header][i] = int(counter_low/(low_not_reset_streak+1))

      not_reset_low_variables = 0
      low_not_reset_streak = 0

    print("Divisione ", i+1, drug, ":")
    print("Eventi high: ", stats_of_bars[counter_high_header][i], "eventi low: ", stats_of_bars[counter_low_header][i])
    print("avg high: ",stats_of_bars[avg_high_header][i], "avg low: ", stats_of_bars[avg_low_header][i])
    print("std high: ", stats_of_bars[std_high_header][i], "std low: ", stats_of_bars[std_low_header][i])

stats_of_bars["prob (high)- caf"] = np.nan
stats_of_bars["prob (high)- eth"] = np.nan
stats_of_bars["prob (high)- sug"] = np.nan
stats_of_bars["prob (low)- caf"] = np.nan
stats_of_bars["prob (low)- eth"] = np.nan
stats_of_bars["prob (low)- sug"] = np.nan


for exp in range(1,4) :

  counter_high = 0
  counter_low = 0
  is_it_1_high = 0.0
  is_it_1_low = 0.0
  
  if exp == 1 :

    for i in range(0, len(stats_of_bars)) :
      
      counter_high += stats_of_bars["counter (high)- caf"][i]
      counter_low += stats_of_bars["counter (low)- caf"][i]
      
    for i in range(0, len(stats_of_bars)) :
      
      stats_of_bars["prob (high)- caf"][i] = stats_of_bars["counter (high)- caf"][i]/counter_high
      stats_of_bars["prob (low)- caf"][i] = stats_of_bars["counter (low)- caf"][i]/counter_low
    
    for i in range(0, len(stats_of_bars)) :
      
      is_it_1_high += stats_of_bars["prob (high)- caf"][i]
      is_it_1_low += stats_of_bars["prob (low)- caf"][i]
      
    print(is_it_1_high, is_it_1_low)
      
  if exp == 2 :

    for i in range(0, len(stats_of_bars)) :
      
      counter_high += stats_of_bars["counter (high)- eth"][i]
      counter_low += stats_of_bars["counter (low)- eth"][i]
      
    for i in range(0, len(stats_of_bars)) :
      
      stats_of_bars["prob (high)- eth"][i] = stats_of_bars["counter (high)- eth"][i]/counter_high
      stats_of_bars["prob (low)- eth"][i] = stats_of_bars["counter (low)- eth"][i]/counter_low
    
    for i in range(0, len(stats_of_bars)) :
      
      is_it_1_high += stats_of_bars["prob (high)- eth"][i]
      is_it_1_low += stats_of_bars["prob (low)- eth"][i]
      
    print(is_it_1_high, is_it_1_low)
      
  if exp == 3 :

    for i in range(0, len(stats_of_bars)) :
      
      counter_high += stats_of_bars["counter (high)- sug"][i]
      counter_low += stats_of_bars["counter (low)- sug"][i]
      
    for i in range(0, len(stats_of_bars)) :
      
      stats_of_bars["prob (high)- sug"][i] = stats_of_bars["counter (high)- sug"][i]/counter_high
      stats_of_bars["prob (low)- sug"][i] = stats_of_bars["counter (low)- sug"][i]/counter_low
    
    for i in range(0, len(stats_of_bars)) :
      
      is_it_1_high += stats_of_bars["prob (high)- sug"][i]
      is_it_1_low += stats_of_bars["prob (low)- sug"][i]
      
    print(is_it_1_high, is_it_1_low)
      

stats_of_bars.to_csv('./random_walk/stats_of_bars.csv')
