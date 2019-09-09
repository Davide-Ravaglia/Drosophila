# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import pandas as pd
import pylab as plt
import numpy as np

__package__ = "Graph of trails, both single trail and all the 10 trails simultaneous"
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

#   I extract the data of the first Dros.

stop_at_id = 1

id_counter = 0
for exp in data.exp.unique() :

  data_exp = data.loc[min(data.index[data['exp'] == exp]):max(data.index[data['exp'] == exp])]

  for id in data_exp.id.unique() :
    
    id_counter += 1
    data_id = data_exp.loc[min(data_exp.index[data_exp['id'] == id]):max(data_exp.index[data_exp['id'] == id])]
    
    if id_counter == stop_at_id : break
  
  if exp == exp : break

hom_many_points = 100
tick_interval = 20
start_frame = 100

column_extraction = pd.DataFrame(pd.DataFrame(index=range(22000*(stop_at_id-1) + start_frame,hom_many_points + 22000*(stop_at_id-1) + start_frame)))
column_extraction["x"] = data_id.x_mm
column_extraction["y"] = data_id.y_mm

plt.plot(column_extraction["y"], column_extraction["x"])
plt.xlabel("X (mm)")
plt.ylabel("Y (mm)")
#plt.xticks(np.arange(-50, 50+tick_interval, tick_interval))
#plt.yticks(np.arange(-50, 50+tick_interval, tick_interval))
plt.tight_layout()
plt.gca().set_aspect('equal', adjustable='box')
path = './Graphs/Trail ' + str(hom_many_points) + ' (real).pdf'
#plt.savefig(path)
plt.savefig('./Graphs/Trail for rectifiability explanation.pdf')
plt.show()
plt.close()


rndm_walks = pd.read_csv('./random_walk/many_walks/rndm_walks (seed=1).csv', sep=',', header=0, index_col='Unnamed: 0')


header_x = "0 - 5 x"
header_y = "0 - 5 y"

hom_many_points = 5000
tick_interval = 20

column_extraction = pd.DataFrame(pd.DataFrame(index=range(0,hom_many_points)))
column_extraction["x"] = rndm_walks[header_x]
column_extraction["y"] = rndm_walks[header_y]

plt.plot(column_extraction["x"], column_extraction["y"])
plt.xlabel("X (mm)")
plt.ylabel("Y (mm)")
plt.xticks(np.arange(-50, 50+tick_interval, tick_interval))
plt.yticks(np.arange(-50, 50+tick_interval, tick_interval))
plt.tight_layout()
plt.gca().set_aspect('equal', adjustable='box')
path = './Graphs/Trail ' + str(hom_many_points) + ' (toy).pdf'
plt.savefig(path)
plt.show()
plt.close()


#   Here I extract all of the 10 trails in a certain time frame
#   The start and end parameters show meeting betwee


#   This start coordinate is for a very long meeting bewtween 2 Dros
#start_extraction = 750
#   This start coordinate is for a meeting between 3 Dros
start_extraction = 791
end_extraction = 826
column_extraction = pd.DataFrame(pd.DataFrame(index=range(start_extraction, end_extraction)))


for stop_at_id in range (1, 11) :
  
  id_counter = 0
  for exp in data.exp.unique() :
  
    data_exp = data.loc[min(data.index[data['exp'] == exp]):max(data.index[data['exp'] == exp])]
  
    for id in data_exp.id.unique() :
      
      id_counter += 1
      print(id_counter)
      
      data_id = data_exp.loc[min(data_exp.index[data_exp['id'] == id]):max(data_exp.index[data_exp['id'] == id])]
      new_index = pd.Series(data_id.frame)-1
      data_id.set_index(new_index, inplace=True)
      
      if id_counter == stop_at_id : break
    
    if exp == exp : break

  column_extraction["x " + str(stop_at_id)] = data_id.x_mm
  column_extraction["y " + str(stop_at_id)] = data_id.y_mm


tick_interval = 20

plt.plot(column_extraction["x 1"], column_extraction["y 1"], color = 'gray')
plt.plot(column_extraction["x 2"], column_extraction["y 2"], color = 'firebrick')
plt.plot(column_extraction["x 3"], column_extraction["y 3"], color = 'red')
plt.plot(column_extraction["x 4"], column_extraction["y 4"], color = 'sandybrown')
plt.plot(column_extraction["x 5"], column_extraction["y 5"], color = 'olivedrab')
plt.plot(column_extraction["x 6"], column_extraction["y 6"], color = 'gold')
plt.plot(column_extraction["x 7"], column_extraction["y 7"], color = 'chartreuse')
plt.plot(column_extraction["x 8"], column_extraction["y 8"], color = 'blue')
plt.plot(column_extraction["x 9"], column_extraction["y 9"], color = 'm')
plt.plot(column_extraction["x 10"], column_extraction["y 10"], color = 'darkturquoise')
plt.xlabel("X (mm)")
plt.ylabel("Y (mm)")
plt.xlim(-50, 50)
plt.ylim(-50, 50)
plt.xticks(np.arange(-50, 50+tick_interval, tick_interval))
plt.yticks(np.arange(-50, 50+tick_interval, tick_interval))
plt.tight_layout()
plt.gca().set_aspect('equal', adjustable='box')
path = './Graphs/Trails encounter (long 3 Dros).pdf'
plt.savefig(path)
plt.show()
plt.close()


