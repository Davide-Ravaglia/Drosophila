# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import pandas as pd
import pylab as plt
import numpy as np


__package__ = "Graphs of comparison of different running averages. Histograms of differences between running averages and instant speed/instant velocity direction. Graph of values of instant speed in log and normal speed"
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


list_velocity_complete = []
mov_avg_vel_complete = []

list_vel_dir_complete = []
mov_avg_vel_dir_complete = []

list_orientation_complete = []
mov_avg_orient_complete = []

for exp in data.exp.unique() :

  data_exp = data.loc[min(data.index[data['exp'] == exp]):max(data.index[data['exp'] == exp])]

  for id in data_exp.id.unique() :

    data_id = data_exp.loc[min(data_exp.index[data_exp['id'] == id]):max(data_exp.index[data_exp['id'] == id])]
    list_time = data_id.timestamps
    list_velocity = data_id.velmag_ctr
    list_velocity_direction = data_id.phi
    list_orientation = data_id.theta

#   N is the number of frames to use for the running avg
#   cumsum is
#   moving_aves is
    N = 7
    if N%2 == 0: M = N-1
    if N%2 == 1: M = N

#   VELOCITY
    cumsum, moving_aves = [0], []

    for i, x in enumerate(list_velocity, 1):
        cumsum.append(cumsum[i-1] + x)
        if i>=N:
            moving_ave = (cumsum[i] - cumsum[i-N])/N
            moving_aves.append(moving_ave)

#   Here I trim the first and last part of the original data so I have two
#   arrays with the same lenght          
    list_velocity = list_velocity[:(len(list_velocity)-int(M/2))]
    list_velocity = list_velocity[int(N/2):]
    
    list_velocity_complete.extend(list_velocity)
    mov_avg_vel_complete.extend(moving_aves)

#   VELOCITY DIRECTION
    cumsum, moving_aves = [0], []

    for i, x in enumerate(list_velocity_direction, 1):
        cumsum.append(cumsum[i-1] + x)
        if i>=N:
            moving_ave = (cumsum[i] - cumsum[i-N])/N
            moving_aves.append(moving_ave)

#   Here I trim the first and last part of the original data so I have two
#   arrays with the same lenght          
    list_velocity_direction = list_velocity_direction[:(len(list_velocity_direction)-int(M/2))]
    list_velocity_direction = list_velocity_direction[int(N/2):]
    
    list_vel_dir_complete.extend(list_velocity_direction)
    mov_avg_vel_dir_complete.extend(moving_aves)
    
#   ORIENTATION
    cumsum, moving_aves = [0], []

    for i, x in enumerate(list_orientation, 1):
        cumsum.append(cumsum[i-1] + x)
        if i>=N:
            moving_ave = (cumsum[i] - cumsum[i-N])/N
            moving_aves.append(moving_ave)

#   Here I trim the first and last part of the original data so I have two
#   arrays with the same lenght          
    list_orientation = list_orientation[:(len(list_orientation)-int(M/2))]
    list_orientation = list_orientation[int(N/2):]
    
    list_orientation_complete.extend(list_orientation)
    mov_avg_orient_complete.extend(moving_aves)

#   I trim the time in order to plot time vs velocity
    list_time = list_time[:(len(list_time)-int(M/2))]
    list_time = list_time[int(N/2):]

    if id == 'fly#_001_1' : break

  if exp == 'exp_1' : break

moving_aves_vel_7 = mov_avg_vel_complete
moving_aves_vel_dir_7 = mov_avg_vel_dir_complete
moving_aves_orient_7 = mov_avg_orient_complete
list_time_7 = list_time

list_velocity_complete = []
mov_avg_vel_complete = []

list_vel_dir_complete = []
mov_avg_vel_dir_complete = []

list_orientation_complete = []
mov_avg_orient_complete = []

for exp in data.exp.unique() :

  data_exp = data.loc[min(data.index[data['exp'] == exp]):max(data.index[data['exp'] == exp])]

  for id in data_exp.id.unique() :

    data_id = data_exp.loc[min(data_exp.index[data_exp['id'] == id]):max(data_exp.index[data_exp['id'] == id])]
    list_time = data_id.timestamps
    list_velocity = data_id.velmag_ctr
    list_velocity_direction = data_id.phi
    list_orientation = data_id.theta

#   N is the number of frames to use for the running avg
#   cumsum is
#   moving_aves is
    N = 15
    if N%2 == 0: M = N-1
    if N%2 == 1: M = N

#   VELOCITY
    cumsum, moving_aves = [0], []

    for i, x in enumerate(list_velocity, 1):
        cumsum.append(cumsum[i-1] + x)
        if i>=N:
            moving_ave = (cumsum[i] - cumsum[i-N])/N
            moving_aves.append(moving_ave)

#   Here I trim the first and last part of the original data so I have two
#   arrays with the same lenght          
    list_velocity = list_velocity[:(len(list_velocity)-int(M/2))]
    list_velocity = list_velocity[int(N/2):]
    
    list_velocity_complete.extend(list_velocity)
    mov_avg_vel_complete.extend(moving_aves)

#   VELOCITY DIRECTION
    cumsum, moving_aves = [0], []

    for i, x in enumerate(list_velocity_direction, 1):
        cumsum.append(cumsum[i-1] + x)
        if i>=N:
            moving_ave = (cumsum[i] - cumsum[i-N])/N
            moving_aves.append(moving_ave)

#   Here I trim the first and last part of the original data so I have two
#   arrays with the same lenght          
    list_velocity_direction = list_velocity_direction[:(len(list_velocity_direction)-int(M/2))]
    list_velocity_direction = list_velocity_direction[int(N/2):]
    
    list_vel_dir_complete.extend(list_velocity_direction)
    mov_avg_vel_dir_complete.extend(moving_aves)
    
#   ORIENTATION
    cumsum, moving_aves = [0], []

    for i, x in enumerate(list_orientation, 1):
        cumsum.append(cumsum[i-1] + x)
        if i>=N:
            moving_ave = (cumsum[i] - cumsum[i-N])/N
            moving_aves.append(moving_ave)

#   Here I trim the first and last part of the original data so I have two
#   arrays with the same lenght          
    list_orientation = list_orientation[:(len(list_orientation)-int(M/2))]
    list_orientation = list_orientation[int(N/2):]
    
    list_orientation_complete.extend(list_orientation)
    mov_avg_orient_complete.extend(moving_aves)

#   I trim the time in order to plot time vs velocity
    list_time = list_time[:(len(list_time)-int(M/2))]
    list_time = list_time[int(N/2):]

    if id == 'fly#_001_1' : break

  if exp == 'exp_1' : break

moving_aves_vel_15 = mov_avg_vel_complete
moving_aves_vel_dir_15 = mov_avg_vel_dir_complete
moving_aves_orient_15 = mov_avg_orient_complete
list_time_15 = list_time


list_velocity_complete = []
mov_avg_vel_complete = []

list_vel_dir_complete = []
mov_avg_vel_dir_complete = []

list_orientation_complete = []
mov_avg_orient_complete = []

for exp in data.exp.unique() :

  data_exp = data.loc[min(data.index[data['exp'] == exp]):max(data.index[data['exp'] == exp])]

  for id in data_exp.id.unique() :

    data_id = data_exp.loc[min(data_exp.index[data_exp['id'] == id]):max(data_exp.index[data_exp['id'] == id])]
    list_time = data_id.timestamps
    list_velocity = data_id.velmag_ctr
    list_velocity_direction = data_id.phi
    list_orientation = data_id.theta

#   N is the number of frames to use for the running avg
#   cumsum is
#   moving_aves is
    N = 30
    if N%2 == 0: M = N-1
    if N%2 == 1: M = N

#   VELOCITY
    cumsum, moving_aves = [0], []

    for i, x in enumerate(list_velocity, 1):
        cumsum.append(cumsum[i-1] + x)
        if i>=N:
            moving_ave = (cumsum[i] - cumsum[i-N])/N
            moving_aves.append(moving_ave)

#   Here I trim the first and last part of the original data so I have two
#   arrays with the same lenght          
    list_velocity = list_velocity[:(len(list_velocity)-int(M/2))]
    list_velocity = list_velocity[int(N/2):]
    
    list_velocity_complete.extend(list_velocity)
    mov_avg_vel_complete.extend(moving_aves)

#   VELOCITY DIRECTION
    cumsum, moving_aves = [0], []

    for i, x in enumerate(list_velocity_direction, 1):
        cumsum.append(cumsum[i-1] + x)
        if i>=N:
            moving_ave = (cumsum[i] - cumsum[i-N])/N
            moving_aves.append(moving_ave)

#   Here I trim the first and last part of the original data so I have two
#   arrays with the same lenght          
    list_velocity_direction = list_velocity_direction[:(len(list_velocity_direction)-int(M/2))]
    list_velocity_direction = list_velocity_direction[int(N/2):]
    
    list_vel_dir_complete.extend(list_velocity_direction)
    mov_avg_vel_dir_complete.extend(moving_aves)
    
#   ORIENTATION
    cumsum, moving_aves = [0], []

    for i, x in enumerate(list_orientation, 1):
        cumsum.append(cumsum[i-1] + x)
        if i>=N:
            moving_ave = (cumsum[i] - cumsum[i-N])/N
            moving_aves.append(moving_ave)

#   Here I trim the first and last part of the original data so I have two
#   arrays with the same lenght          
    list_orientation = list_orientation[:(len(list_orientation)-int(M/2))]
    list_orientation = list_orientation[int(N/2):]
    
    list_orientation_complete.extend(list_orientation)
    mov_avg_orient_complete.extend(moving_aves)

#   I trim the time in order to plot time vs velocity
    list_time = list_time[:(len(list_time)-int(M/2))]
    list_time = list_time[int(N/2):]

    if id == 'fly#_001_1' : break

  if exp == 'exp_1' : break


moving_aves_vel_30 = mov_avg_vel_complete
moving_aves_vel_dir_30 = mov_avg_vel_dir_complete
moving_aves_orient_30 = mov_avg_orient_complete
list_time_30 = list_time


#   Graphs of Velocity, velocity direction and orientation in comparison with
#   different running averages  
#   These Graphs only work if you take out the #%% mark above where it's written:
#   Take out the  #%% above if you want...

plt.plot(np.asarray(list_time), np.asarray(list_velocity), label='Instant')
plt.plot(np.asarray(list_time_7), np.asarray(moving_aves_vel_7), label='R.A. (t=0.47s)', linewidth = 3)
plt.plot(np.asarray(list_time_15), np.asarray(moving_aves_vel_15), label='R.A. (t=1.0s)', linewidth = 3)
plt.plot(np.asarray(list_time_30), np.asarray(moving_aves_vel_30), label='R.A. (t=2.0s)', linewidth = 3)
plt.xlabel('Time (s)')
plt.ylabel('Velocity (mm/s)')
plt.xlim(40, 50)
plt.tight_layout()
plt.legend()
#plt.savefig('./Graphs/Velocity and running avg.pdf')
plt.show()
plt.close()

  
plt.plot(np.asarray(list_time), np.asarray(list_velocity_direction), label='Instant')
plt.plot(np.asarray(list_time_7), np.asarray(moving_aves_vel_dir_7), label='R.A. (t=0.47s)', linewidth = 3)
plt.plot(np.asarray(list_time_15), np.asarray(moving_aves_vel_dir_15), label='R.A. (t=1.0s)', linewidth = 3)
plt.plot(np.asarray(list_time_30), np.asarray(moving_aves_vel_dir_30), label='R.A. (t=2.0s)', linewidth = 3)
plt.xlabel('Time (s)')
plt.ylabel('Velocity Direction (rad)')
plt.xlim(100, 110)
plt.ylim(-5, 3.14)
plt.tight_layout()
plt.legend()
plt.savefig('./Graphs/Vel. Direction and running avg.pdf')
plt.show()
plt.close()





list_velocity_complete = []
mov_avg_vel_complete = []

list_vel_dir_complete = []
mov_avg_vel_dir_complete = []

list_orientation_complete = []
mov_avg_orient_complete = []

for exp in data.exp.unique() :

  data_exp = data.loc[min(data.index[data['exp'] == exp]):max(data.index[data['exp'] == exp])]

  for id in data_exp.id.unique() :

    data_id = data_exp.loc[min(data_exp.index[data_exp['id'] == id]):max(data_exp.index[data_exp['id'] == id])]
    list_time = data_id.timestamps
    list_velocity = data_id.velmag_ctr
    list_velocity_direction = data_id.phi
    list_orientation = data_id.theta

#   N is the number of frames to use for the running avg
#   cumsum is
#   moving_aves is
    N = 7
    if N%2 == 0: M = N-1
    if N%2 == 1: M = N

#   VELOCITY
    cumsum, moving_aves = [0], []

    for i, x in enumerate(list_velocity, 1):
        cumsum.append(cumsum[i-1] + x)
        if i>=N:
            moving_ave = (cumsum[i] - cumsum[i-N])/N
            moving_aves.append(moving_ave)

#   Here I trim the first and last part of the original data so I have two
#   arrays with the same lenght          
    list_velocity = list_velocity[:(len(list_velocity)-int(M/2))]
    list_velocity = list_velocity[int(N/2):]
    
    list_velocity_complete.extend(list_velocity)
    mov_avg_vel_complete.extend(moving_aves)

#   VELOCITY DIRECTION
    cumsum, moving_aves = [0], []

    for i, x in enumerate(list_velocity_direction, 1):
        cumsum.append(cumsum[i-1] + x)
        if i>=N:
            moving_ave = (cumsum[i] - cumsum[i-N])/N
            moving_aves.append(moving_ave)

#   Here I trim the first and last part of the original data so I have two
#   arrays with the same lenght          
    list_velocity_direction = list_velocity_direction[:(len(list_velocity_direction)-int(M/2))]
    list_velocity_direction = list_velocity_direction[int(N/2):]
    
    list_vel_dir_complete.extend(list_velocity_direction)
    mov_avg_vel_dir_complete.extend(moving_aves)
    
#   ORIENTATION
    cumsum, moving_aves = [0], []

    for i, x in enumerate(list_orientation, 1):
        cumsum.append(cumsum[i-1] + x)
        if i>=N:
            moving_ave = (cumsum[i] - cumsum[i-N])/N
            moving_aves.append(moving_ave)

#   Here I trim the first and last part of the original data so I have two
#   arrays with the same lenght          
    list_orientation = list_orientation[:(len(list_orientation)-int(M/2))]
    list_orientation = list_orientation[int(N/2):]
    
    list_orientation_complete.extend(list_orientation)
    mov_avg_orient_complete.extend(moving_aves)

#   I trim the time in order to plot time vs velocity
    list_time = list_time[:(len(list_time)-int(M/2))]
    list_time = list_time[int(N/2):]

diff_velocity_complete_7 = np.asarray(list_velocity_complete) - np.asarray(mov_avg_vel_complete)

numbins = 30

plt.hist(diff_velocity_complete_7, numbins, range = (-15, 15), label="0.47 s", color='b')
plt.xlabel('Speed - Running Avg. of speed (mm/s)')
plt.ylabel('Frequency')
plt.ylim(0, 60000)
plt.tight_layout()
plt.legend()
plt.gca().set_aspect(0.0005, adjustable='box')
plt.savefig('./Graphs/Diff. bw vel. and running avg for 0.47s (zoom).pdf')
plt.show()
plt.close()






list_velocity_complete = []
mov_avg_vel_complete = []

list_vel_dir_complete = []
mov_avg_vel_dir_complete = []

list_orientation_complete = []
mov_avg_orient_complete = []

for exp in data.exp.unique() :

  data_exp = data.loc[min(data.index[data['exp'] == exp]):max(data.index[data['exp'] == exp])]

  for id in data_exp.id.unique() :

    data_id = data_exp.loc[min(data_exp.index[data_exp['id'] == id]):max(data_exp.index[data_exp['id'] == id])]
    list_time = data_id.timestamps
    list_velocity = data_id.velmag_ctr
    list_velocity_direction = data_id.phi
    list_orientation = data_id.theta

#   N is the number of frames to use for the running avg
#   cumsum is
#   moving_aves is
    N = 15
    if N%2 == 0: M = N-1
    if N%2 == 1: M = N

#   VELOCITY
    cumsum, moving_aves = [0], []

    for i, x in enumerate(list_velocity, 1):
        cumsum.append(cumsum[i-1] + x)
        if i>=N:
            moving_ave = (cumsum[i] - cumsum[i-N])/N
            moving_aves.append(moving_ave)

#   Here I trim the first and last part of the original data so I have two
#   arrays with the same lenght          
    list_velocity = list_velocity[:(len(list_velocity)-int(M/2))]
    list_velocity = list_velocity[int(N/2):]
    
    list_velocity_complete.extend(list_velocity)
    mov_avg_vel_complete.extend(moving_aves)

#   VELOCITY DIRECTION
    cumsum, moving_aves = [0], []

    for i, x in enumerate(list_velocity_direction, 1):
        cumsum.append(cumsum[i-1] + x)
        if i>=N:
            moving_ave = (cumsum[i] - cumsum[i-N])/N
            moving_aves.append(moving_ave)

#   Here I trim the first and last part of the original data so I have two
#   arrays with the same lenght          
    list_velocity_direction = list_velocity_direction[:(len(list_velocity_direction)-int(M/2))]
    list_velocity_direction = list_velocity_direction[int(N/2):]
    
    list_vel_dir_complete.extend(list_velocity_direction)
    mov_avg_vel_dir_complete.extend(moving_aves)
    
#   ORIENTATION
    cumsum, moving_aves = [0], []

    for i, x in enumerate(list_orientation, 1):
        cumsum.append(cumsum[i-1] + x)
        if i>=N:
            moving_ave = (cumsum[i] - cumsum[i-N])/N
            moving_aves.append(moving_ave)

#   Here I trim the first and last part of the original data so I have two
#   arrays with the same lenght          
    list_orientation = list_orientation[:(len(list_orientation)-int(M/2))]
    list_orientation = list_orientation[int(N/2):]
    
    list_orientation_complete.extend(list_orientation)
    mov_avg_orient_complete.extend(moving_aves)

#   I trim the time in order to plot time vs velocity
    list_time = list_time[:(len(list_time)-int(M/2))]
    list_time = list_time[int(N/2):]

diff_velocity_complete_7 = np.asarray(list_velocity_complete) - np.asarray(mov_avg_vel_complete)

numbins = 30

plt.hist(diff_velocity_complete_7, numbins, range = (-15, 15), label="0.47 s", color='b')
plt.xlabel('Speed - Running Avg. of speed (mm/s)')
plt.ylabel('Frequency')
plt.ylim(0, 60000)
plt.tight_layout()
plt.legend()
plt.gca().set_aspect(0.0005, adjustable='box')
plt.savefig('./Graphs/Diff. bw vel. and running avg for 1.0s (zoom).pdf')
plt.show()
plt.close()






list_velocity_complete = []
mov_avg_vel_complete = []

list_vel_dir_complete = []
mov_avg_vel_dir_complete = []

list_orientation_complete = []
mov_avg_orient_complete = []

for exp in data.exp.unique() :

  data_exp = data.loc[min(data.index[data['exp'] == exp]):max(data.index[data['exp'] == exp])]

  for id in data_exp.id.unique() :

    data_id = data_exp.loc[min(data_exp.index[data_exp['id'] == id]):max(data_exp.index[data_exp['id'] == id])]
    list_time = data_id.timestamps
    list_velocity = data_id.velmag_ctr
    list_velocity_direction = data_id.phi
    list_orientation = data_id.theta

#   N is the number of frames to use for the running avg
#   cumsum is
#   moving_aves is
    N = 30
    if N%2 == 0: M = N-1
    if N%2 == 1: M = N

#   VELOCITY
    cumsum, moving_aves = [0], []

    for i, x in enumerate(list_velocity, 1):
        cumsum.append(cumsum[i-1] + x)
        if i>=N:
            moving_ave = (cumsum[i] - cumsum[i-N])/N
            moving_aves.append(moving_ave)

#   Here I trim the first and last part of the original data so I have two
#   arrays with the same lenght          
    list_velocity = list_velocity[:(len(list_velocity)-int(M/2))]
    list_velocity = list_velocity[int(N/2):]
    
    list_velocity_complete.extend(list_velocity)
    mov_avg_vel_complete.extend(moving_aves)

#   VELOCITY DIRECTION
    cumsum, moving_aves = [0], []

    for i, x in enumerate(list_velocity_direction, 1):
        cumsum.append(cumsum[i-1] + x)
        if i>=N:
            moving_ave = (cumsum[i] - cumsum[i-N])/N
            moving_aves.append(moving_ave)

#   Here I trim the first and last part of the original data so I have two
#   arrays with the same lenght          
    list_velocity_direction = list_velocity_direction[:(len(list_velocity_direction)-int(M/2))]
    list_velocity_direction = list_velocity_direction[int(N/2):]
    
    list_vel_dir_complete.extend(list_velocity_direction)
    mov_avg_vel_dir_complete.extend(moving_aves)
    
#   ORIENTATION
    cumsum, moving_aves = [0], []

    for i, x in enumerate(list_orientation, 1):
        cumsum.append(cumsum[i-1] + x)
        if i>=N:
            moving_ave = (cumsum[i] - cumsum[i-N])/N
            moving_aves.append(moving_ave)

#   Here I trim the first and last part of the original data so I have two
#   arrays with the same lenght          
    list_orientation = list_orientation[:(len(list_orientation)-int(M/2))]
    list_orientation = list_orientation[int(N/2):]
    
    list_orientation_complete.extend(list_orientation)
    mov_avg_orient_complete.extend(moving_aves)

#   I trim the time in order to plot time vs velocity
    list_time = list_time[:(len(list_time)-int(M/2))]
    list_time = list_time[int(N/2):]

diff_velocity_complete_7 = np.asarray(list_velocity_complete) - np.asarray(mov_avg_vel_complete)

numbins = 30

plt.hist(diff_velocity_complete_7, numbins, range = (-15, 15), label="0.47 s", color='b')
plt.xlabel('Speed - Running Avg. of speed (mm/s)')
plt.ylabel('Frequency')
plt.ylim(0, 60000)
plt.tight_layout()
plt.legend()
plt.gca().set_aspect(0.0005, adjustable='box')
plt.savefig('./Graphs/Diff. bw vel. and running avg for 2.0s (zoom).pdf')
plt.show()
plt.close()







#Here I want to graph the frequencies of the values of the running avg
numbins = 30
max_range = 3

(n, bins, patches) = plt.hist(data.velmag_ctr, numbins, range = (0, max_range), color='gold', weights=np.ones(len(data))/len(data))
plt.xlabel("Speed (mm/s)")
plt.ylabel("Probability")
plt.tight_layout()
plt.savefig('./Graphs/Instant speed.pdf')
plt.show()
plt.close()

#   I do the same graph in log scale

(n, bins, patches) = plt.hist(data.velmag_ctr, numbins, range = (0, max_range), color='gold', weights=np.ones(len(data))/len(data))
plt.xlabel("Speed (mm/s)")
plt.ylabel("Probability")
plt.yscale('log')
plt.tight_layout()
plt.savefig('./Graphs/Instant speed (log).pdf')
plt.show()
plt.close()
