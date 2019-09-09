# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import pandas as pd
import pylab as plt
import numpy as np

__package__ = "I create moving_stats which contains infos on the movement and stop part and then a df which has the probability of stop and movement duration, of which I graph the PDFs as well."
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

#   I divide all of the moving tracks into moving and "staying still" parts
#   based on weather they are moving faster then v_limit

#   I create a df(moving_stats) which will contain: speed, distance and duration
#   of the movement, based on a minimum duration and a velocity trigger which
#   I define as parameters

#   Lower than this velocity (mm/s) it's not considered movement.
#   This velocity is needed also in the second part of the program
v_limit = 2.0

#   I have to use a running avg for the velocity otherwise it changes too fast
#   so I define how many steps of 1/15 s I consider in the running average
steps_for_running_avg = 7


#   I make it long but some will be empty
moving_stats = pd.DataFrame(pd.DataFrame(index=range(0, 2500)))

exp_counter = 0

for exp in data.exp.unique() :

  id_counter = 1
  exp_counter += 1 

  if exp_counter == 1 :
    drug = "- caf"
  if exp_counter == 2 :
    drug = "- eth"
  if exp_counter == 3 :
    drug = "- sug"

  time_name_high = 'time (high)' + drug
  distance_name_high = 'distance (high)' + drug
  speed_name_high = 'speed (high)' + drug
  moving_stats[time_name_high] = np.nan
  moving_stats[distance_name_high] = np.nan
  moving_stats[speed_name_high] = np.nan

  time_name_low = 'time (low)' + drug
  distance_name_low = 'distance (low)' + drug
  speed_name_low = 'speed (low)' + drug
  moving_stats[time_name_low] = np.nan
  moving_stats[distance_name_low] = np.nan
  moving_stats[speed_name_low] = np.nan

  index_counter_high = 0
  index_counter_low = 0

  data_exp = data.loc[min(data.index[data['exp'] == exp]):max(data.index[data['exp'] == exp])]

  for id in data_exp.id.unique() :

    print('Exp : ', exp_counter, '  Id : ', id_counter)

    id_counter += 1
    
    data_id = data_exp.loc[min(data_exp.index[data_exp['id'] == id]):max(data_exp.index[data_exp['id'] == id])]
    new_index = pd.Series(data_id.frame)-1
    data_id.set_index(new_index, inplace=True)

    distance_moving = 0
    distance_standing = 0
    start_moving = 0
    start_standing = 0

#   I compute the running average for the first frame
    running_avg_vel = 0.0
    for i in range (0, steps_for_running_avg) :
      running_avg_vel += data_id['velmag_ctr'][i+1]
    running_avg_vel = running_avg_vel/steps_for_running_avg

#   The shifts from 1 and len(data_id) are due to the fact that I need to
#   compute the running average
    for index in range (int(steps_for_running_avg/2)+1, len(data_id)-int(steps_for_running_avg/2)-1) :

#   I compute the running average for the next frame, I need it because
#   I need to see if in the next frame it start/stops moving
      next_running_avg_vel = 0.0
      
      for i in range (0, steps_for_running_avg) :
        next_running_avg_vel += data_id['velmag_ctr'][index-int(steps_for_running_avg/2)+i+1]
      next_running_avg_vel = next_running_avg_vel/steps_for_running_avg
      
#   If it was moving but it goes below the trigger velocity place here the start_standing
      if (start_standing == 0 and running_avg_vel < v_limit) :
        start_standing = index
      
#   If it was not moving but it surpasses the trigger velocity place here the start_moving
      if (start_moving == 0 and running_avg_vel >= v_limit) :
        start_moving = index

#   If it's moving sum the distance it just traveled
      if start_moving != 0 :
        distance_moving +=  np.sqrt(np.power(data_id['x_mm'][index]-data_id['x_mm'][index-1], 2) +
                             np.power(data_id['y_mm'][index]-data_id['y_mm'][index-1], 2))
  
#   If it's standing sum the distance it just traveled
      if start_standing != 0 :
        distance_standing +=  np.sqrt(np.power(data_id['x_mm'][index]-data_id['x_mm'][index-1], 2) +
                             np.power(data_id['y_mm'][index]-data_id['y_mm'][index-1], 2))

#   If it moved  but the next frames it stops
#   compute the statistics and reset moving counters and all
      if (start_moving != 0 and next_running_avg_vel <= v_limit) :
        moving_stats[time_name_high][index_counter_high] = (index+1-start_moving)/15
        moving_stats[distance_name_high][index_counter_high] = distance_moving
        moving_stats[speed_name_high][index_counter_high] = distance_moving/moving_stats[time_name_high][index_counter_high]

        start_moving = 0
        distance_moving = 0
        index_counter_high += 1

#   If it stood but the next frames it moves
#   compute the statistics and reset standing counters and all
      if (start_standing != 0 and next_running_avg_vel > v_limit) :
        moving_stats[time_name_low][index_counter_low] = (index+1-start_standing)/15
        moving_stats[distance_name_low][index_counter_low] = distance_standing
        moving_stats[speed_name_low][index_counter_low] = distance_standing/moving_stats[time_name_low][index_counter_low]
        
        start_standing = 0
        distance_standing = 0
        index_counter_low += 1

#   I assign the running average of the next turn already computed
      running_avg_vel = next_running_avg_vel

moving_stats.to_csv('./moving_stats/moving_stats.csv')

moving_stats = pd.read_csv('./moving_stats/moving_stats.csv', sep=',', header=0, index_col='Unnamed: 0')

moving_stats = moving_stats.fillna(-10)

numbins = 60
max_range_high = 30

(n_high_caf, bins_high_caf, patches_high_caf) = plt.hist(moving_stats["time (high)- caf"], numbins, range = (0, max_range_high), color='b', alpha=0.6, label="Caffeine")
(n_high_eth, bins_high_eth, patches_high_eth) = plt.hist(moving_stats["time (high)- eth"], numbins, range = (0, max_range_high), color='g', alpha=0.6, label="Ethanol")
(n_high_sug, bins_high_sug, patches_high_sug) = plt.hist(moving_stats["time (high)- sug"], numbins, range = (0, max_range_high), color='r', alpha=0.6, label="Sugar")
plt.xlabel("Duration of movement (s)")
plt.ylabel("Frequency")
plt.legend()
plt.tight_layout()
plt.show()
plt.close()

tot_high_caf = np.sum(n_high_caf)
tot_high_eth = np.sum(n_high_eth)
tot_high_sug = np.sum(n_high_sug)

numbins = 60
max_range_low = 12.5

(n_low_caf, bins_low_caf, patches_low_caf) = plt.hist(moving_stats["time (low)- caf"], numbins, range = (0, max_range_low), color='b', alpha=0.6, label="Caffeine")
(n_low_eth, bins_low_eth, patches_low_eth) = plt.hist(moving_stats["time (low)- eth"], numbins, range = (0, max_range_low), color='g', alpha=0.6, label="Ethanol")
(n_low_sug, bins_low_sug, patches_low_sug) = plt.hist(moving_stats["time (low)- sug"], numbins, range = (0, max_range_low), color='r', alpha=0.6, label="Sugar")
plt.xlabel("Duration of stop (s)")
plt.ylabel("Frequency")
plt.legend()
plt.tight_layout()
plt.show()
plt.close()

tot_low_caf = np.sum(n_low_caf)
tot_low_eth = np.sum(n_low_eth)
tot_low_sug = np.sum(n_low_sug)


#   I fill the df which will have all of the  information of the above hist
duration_high_low = pd.DataFrame(pd.DataFrame(index=range(0, numbins)))

#   First I make two columns with the central value for each bin
duration_high_low["durat central (high)"] = np.nan
duration_high_low["durat central (low)"] = np.nan

for i in range (0, numbins) :
  duration_high_low["durat central (high)"][i] = max_range_high/numbins*i + max_range_high/(2*numbins)
  duration_high_low["durat central (low)"][i] = max_range_low/numbins*i + max_range_low/(2*numbins)

#   Then for each bin, each drug and high and low I compute the probability
#   and the cumulative probability

#   High part
duration_high_low["prob (high)- caf"] = n_high_caf/tot_high_caf
duration_high_low["cumprob (high)- caf"] = np.nan
cumulative_prob = 0.0

for i in range (0, numbins) :
  cumulative_prob += duration_high_low["prob (high)- caf"][i]
  duration_high_low["cumprob (high)- caf"][i] = cumulative_prob

duration_high_low["prob (high)- eth"] = n_high_eth/tot_high_eth
duration_high_low["cumprob (high)- eth"] = np.nan
cumulative_prob = 0.0

for i in range (0, numbins) :
  cumulative_prob += duration_high_low["prob (high)- eth"][i]
  duration_high_low["cumprob (high)- eth"][i] = cumulative_prob

duration_high_low["prob (high)- sug"] = n_high_sug/tot_high_sug
duration_high_low["cumprob (high)- sug"] = np.nan
cumulative_prob = 0.0

for i in range (0, numbins) :
  cumulative_prob += duration_high_low["prob (high)- sug"][i]
  duration_high_low["cumprob (high)- sug"][i] = cumulative_prob
  
#   Low part
duration_high_low["prob (low)- caf"] = n_low_caf/tot_low_caf
duration_high_low["cumprob (low)- caf"] = np.nan
cumulative_prob = 0.0

for i in range (0, numbins) :
  cumulative_prob += duration_high_low["prob (low)- caf"][i]
  duration_high_low["cumprob (low)- caf"][i] = cumulative_prob

duration_high_low["prob (low)- eth"] = n_low_eth/tot_low_eth
duration_high_low["cumprob (low)- eth"] = np.nan
cumulative_prob = 0.0

for i in range (0, numbins) :
  cumulative_prob += duration_high_low["prob (low)- eth"][i]
  duration_high_low["cumprob (low)- eth"][i] = cumulative_prob

duration_high_low["prob (low)- sug"] = n_low_sug/tot_low_sug
duration_high_low["cumprob (low)- sug"] = np.nan
cumulative_prob = 0.0

for i in range (0, numbins) :
  cumulative_prob += duration_high_low["prob (low)- sug"][i]
  duration_high_low["cumprob (low)- sug"][i] = cumulative_prob

duration_high_low.to_csv('./random_walk/duration_high_low.csv')

duration_high_low = pd.read_csv('./random_walk/duration_high_low.csv', sep=',', header=0, index_col='Unnamed: 0')

#   Graph of duration of movement
plt.plot(duration_high_low["durat central (high)"], duration_high_low["prob (high)- caf"], color='b', label="Caffeine", marker='o', markersize=3)
plt.plot(duration_high_low["durat central (high)"], duration_high_low["prob (high)- eth"], color='g', label="Ethanol", marker='o', markersize=3)
plt.plot(duration_high_low["durat central (high)"], duration_high_low["prob (high)- sug"], color='r', label="Sugar", marker='o', markersize=3)
plt.ylabel('Probability')
plt.xlabel('Duration of movement (s)')
plt.xlim(0, 10)
plt.tight_layout()
plt.legend()
plt.savefig('./Graphs/Duration of movement.pdf')
plt.show()
plt.close()

#   Graph of duration of movement in log scale
plt.plot(duration_high_low["durat central (high)"], duration_high_low["prob (high)- caf"], color='b', label="Caffeine", marker='o', markersize=3)
plt.plot(duration_high_low["durat central (high)"], duration_high_low["prob (high)- eth"], color='g', label="Ethanol", marker='o', markersize=3)
plt.plot(duration_high_low["durat central (high)"], duration_high_low["prob (high)- sug"], color='r', label="Sugar", marker='o', markersize=3)
plt.ylabel('Probability')
plt.xlabel('Duration of movement (s)')
plt.xlim(0, 10)
plt.yscale("log")
plt.ylim(0.005, 0.205)
plt.tight_layout()
plt.legend()
plt.savefig('./Graphs/Duration of movement (log).pdf')
plt.show()
plt.close()

#   Graph of duration of stop
plt.plot(duration_high_low["durat central (low)"], duration_high_low["prob (low)- caf"], color='b', label="Caffeine", marker='o', markersize=3)
plt.plot(duration_high_low["durat central (low)"], duration_high_low["prob (low)- eth"], color='g', label="Ethanol", marker='o', markersize=3)
plt.plot(duration_high_low["durat central (low)"], duration_high_low["prob (low)- sug"], color='r', label="Sugar", marker='o', markersize=3)
plt.ylabel('Probability')
plt.xlabel('Duration of stasis (s)')
plt.xlim(0, 5)
plt.tight_layout()
plt.legend()
plt.savefig('./Graphs/Duration of stop.pdf')
plt.show()
plt.close()


#   Graph of duration of stop in log scale
plt.plot(duration_high_low["durat central (low)"], duration_high_low["prob (low)- caf"], color='b', label="Caffeine", marker='o', markersize=3)
plt.plot(duration_high_low["durat central (low)"], duration_high_low["prob (low)- eth"], color='g', label="Ethanol", marker='o', markersize=3)
plt.plot(duration_high_low["durat central (low)"], duration_high_low["prob (low)- sug"], color='r', label="Sugar", marker='o', markersize=3)
plt.ylabel('Probability')
plt.xlabel('Duration of stasis (s)')
plt.xlim(0, 5)
plt.yscale("log")
plt.ylim(0.005, 0.205)
plt.tight_layout()
plt.legend()
plt.savefig('./Graphs/Duration of stop (log).pdf')
plt.show()
plt.close()
  
