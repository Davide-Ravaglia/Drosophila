# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import pandas as pd
import pylab as plt
import numpy as np

__package__ = "Rectifiability of the trails, so measure of the trails measured with different minimal units of lenght"
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


#   I import the file witht the random walks
rndm_walks = pd.read_csv('./random_walk/many_walks/rndm_walks (seed=1).csv', sep=',', header=0, index_col='Unnamed: 0')

#   time_min and time_max are really only useful when I check the program
#   in order not to wait too long (max time is 1467 s)
time_min = 0
time_max = 1467
lines_of_df = int(time_max-time_min)
#   below min_meter the rectifiability is just straight and above
#   max_meter there are no tracks
min_meter = 1
max_meter = 100
#   how much do I increase the meter each time
#   only integers steps please! It's not even useful to have so many
step = 1

#   This df will contain the avg distance travelled for the different ids
#   for the different meters
meter_stats = pd.DataFrame(pd.DataFrame(index=range(0,int((max_meter-min_meter)/step)+1)))
meter_stats['meter'] = np.nan

for meter in range(min_meter, max_meter+1, step) :
  
  meter_stats['meter'][meter-min_meter] = meter

#   I compute the avg movement lenght for the real data
exp_counter = -1
for exp in data.exp.unique() :

  id_counter = 1
  exp_counter += 1 

  data_exp = data.loc[min(data.index[data['exp'] == exp]):max(data.index[data['exp'] == exp])]

  for id in data_exp.id.unique() :

    col_name = str(exp_counter)+ ' : ' +str(id_counter) + " real"
    
    print('Exp: ', exp_counter,'  Id: ', id_counter)

    id_counter += 1
    
    data_id = data_exp.loc[min(data_exp.index[data_exp['id'] == id]):max(data_exp.index[data_exp['id'] == id])]
    data_id = data_id.loc[min(data_id.index[data_id['timestamps'] >= time_min]) : max(data_id.index[data_id['timestamps'] <= time_max])]
    new_index = pd.Series(data_id.frame) -1
    data_id.set_index(new_index, inplace=True)

    meter_stats[col_name] = np.nan
      
    for meter in range(min_meter, max_meter+1, step) :
    
      unit = 0
      distance = 0
      first_point_of_ruler = 0
  
      for internal_index in range (1, len(data_id)) :
        
        distance =  np.sqrt(np.power(data_id['x_mm'][internal_index]-data_id['x_mm'][first_point_of_ruler], 2) +
                             np.power(data_id['y_mm'][internal_index]-data_id['y_mm'][first_point_of_ruler], 2))
        
        if distance >= meter :
          
          first_point_of_ruler = internal_index
          unit += int(distance/meter)
      
      meter_stats[col_name][meter-min_meter] = unit*meter
      
#   I compute the avg movement lenght for the fake data
for exp in range(0, 3) :

  for id in range(0, 10) :

    col_name = str(exp)+ ' : ' +str(id+1) + " fake"
    header_x = str(exp) + " - " + str(id) + " x"
    header_y = str(exp) + " - " + str(id) + " y"

    print('Exp: ', exp,'  Id: ', id)

    meter_stats[col_name] = np.nan
      
    for meter in range(min_meter, max_meter+1, step) :
    
      unit = 0
      distance = 0
      first_point_of_ruler = 0
  
      for internal_index in range (1, (time_max-time_min)*15) :

        if internal_index == len(rndm_walks)-1 : break
        
        distance =  np.sqrt(np.power(rndm_walks[header_x][internal_index]-rndm_walks[header_x][first_point_of_ruler], 2) +
                             np.power(rndm_walks[header_y][internal_index]-rndm_walks[header_y][first_point_of_ruler], 2))
        
        if distance >= meter :
          
          first_point_of_ruler = internal_index
          unit += int(distance/meter)
      
      meter_stats[col_name][meter-min_meter] = unit*meter


meter_stats.to_csv('./moving_stats/meter_stats.csv')

meter_stats = pd.read_csv('./moving_stats/meter_stats.csv', sep=',', header=0, index_col='Unnamed: 0')

meter_stats = meter_stats.fillna(0)

#   I do the avg of the different ids
#   When fake == 0 I use the real data, when fake == 1 I use the fake data
for fake in range (0, 2) :

  if fake == 0 :
    real_or_fake = " real"
  if fake == 1 :
    real_or_fake = " fake"

  for exp in range (0, 3) :
  
    meter_stats[str(exp) + real_or_fake] = np.nan
    
    for meter in range(min_meter, max_meter+1, step) :
  
      sum_of_ids = 0.0
  
      for id in range (1, 11) :
  
        col_name = str(exp)+ ' : ' +str(id) + real_or_fake
        sum_of_ids += meter_stats[col_name][meter-min_meter]
  
      meter_stats[str(exp) + real_or_fake][meter-min_meter] = sum_of_ids/10

#   FOR THE NEXT GRAPHS I NEED THE CYCLE ABOVE
#   GRAPH RECTIFIABILITY
plt.plot(meter_stats["0 real"], meter_stats.meter, color='b', label = "Caffeine")
plt.plot(meter_stats["1 real"], meter_stats.meter, color='g', label = "Ethanol")
plt.plot(meter_stats["2 real"], meter_stats.meter, color='r', label = "Sugar")
#   I have to put the legend here othrwhise it gets the column name of the
#   next plot as label.
plt.legend()
plt.plot(meter_stats["0 fake"], meter_stats.meter, color='b', linestyle=':')
plt.plot(meter_stats["1 fake"], meter_stats.meter, color='g', linestyle=':')
plt.plot(meter_stats["2 fake"], meter_stats.meter, color='r', linestyle=':')
plt.xlabel('Average lenght of trail (mm)')
plt.ylabel('Lenght of meter (mm)')
plt.ylim(0, max_meter)
plt.tight_layout()
#plt.savefig('./Graphs/Rectifiability.pdf')
plt.show()
plt.close()

#   GRAPH RECTIFIABILITY NORMALIZED
plt.plot(meter_stats["0 real"]/meter_stats["0 real"].max(), meter_stats.meter, color='b', label = "Caffeine")
plt.plot(meter_stats["1 real"]/meter_stats["1 real"].max(), meter_stats.meter, color='g', label = "Ethanol")
plt.plot(meter_stats["2 real"]/meter_stats["2 real"].max(), meter_stats.meter, color='r', label = "Sugar")
#   I have to put the legend here othrwhise it gets the column name of the
#   next plot as label.
plt.legend()
plt.plot(meter_stats["0 fake"]/meter_stats["0 fake"].max(), meter_stats.meter, color='b', linestyle=':')
plt.plot(meter_stats["1 fake"]/meter_stats["1 fake"].max(), meter_stats.meter, color='g', linestyle=':')
plt.plot(meter_stats["2 fake"]/meter_stats["2 fake"].max(), meter_stats.meter, color='r', linestyle=':')
plt.xlabel('Average lenght of the trail normalized')
plt.ylabel('Minimal unit of length (mm)')
plt.ylim(7, max_meter)
plt.tight_layout()
plt.savefig('./Graphs/Rectifiability Normalized.pdf')
plt.show()
plt.close()

