# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import pandas as pd
import pylab as plt
import numpy as np
import math


__package__ = "First look at the data: distance and velocity"
__author__  = "Davide Ravaglia (davide.ravaglia3@studio.unibo.it)"

#%%

def statistics(data_name):
  """
  A first look at the statistics of the Drosophila.
  
  Parameters
  ----------
  data_name : string
        Name of the file in which are the data.
  
  Returns
  -------
  Creates a folder named 'Graphs'. Note thatt will replace already exising
  files with the same name inside this folder.
  Inside it will place 7 graphs:
  1.'Av speed whole experiment.pdf': average speed of the different Drosophila
    during the whole experiment, divided by drugs.
  2,3,4.'Av speed for time interval ("Drug").pdf': average speed of the
    different Drosophila during the whole experiment for timestep chosen;
    divided into 3 graphs with different name ("Drug" changes).
  5.'Instant speed whole experiment.pdf': instant speed, divided by drugs.
  6.'Min dist between Drosophila's centers.pdf': distance to closest Drosophila,
    divided by drugs.
  7.'Vel. dir. angle - orient. angle.pdf': difference between the angle of
    velocity and the on which the Drosophila is facing, divided by drugs.
  8.'Angle to wall.pdf': angle to closest point on the arena wall, relative to
    the fly's orientation, divided by drugs.
  9.'Dist. and angle to wall.pdf': distance and angle to wall, divided by drugs.
  10.'Forward speed and angle to wall.pdf': forward velocity of the Drosophila's
    center and angle to wall, divided by drugs.
  11.'Angle diff. between closest Dros.pdf': absolute difference in orientation
    between closest Drosophila.
  12.'Maximum angle occluded.pdf': maximum total angle of Drosophila's view
    occluded by another Drosophila.
  13.'Network ("Drug").pdf': change of the Drosophila of interaction during a
    time interval; the interaction is determined by a minimun distance and an
    alignment of the Drosophila's bodies.
  """

#%%

  #Parameters which should be ignored if the function is called from terminal

#  data_name = 'data_original.csv'

  plt.rcParams.update({'font.size': 15,
                      'xtick.major.size': 4,
                      'xtick.major.width': 2,
                      'ytick.major.size': 4,
                      'ytick.major.width': 2,
                      'axes.linewidth': 1.5})

  if(os.path.isdir('./Graphs to show')):
    print('Folder already existing. The program will substitute existing files')
  else:
    os.mkdir('Graphs')
    print('Creating folder "Graphs"')

  data = pd.read_csv(data_name, sep=',', header=0, usecols=['exp', 'id',
         'theta', 'timestamps', 'x_mm', 'y_mm', 'phi', 'velmag_ctr','du_ctr',
         'dv_ctr', 'phisideways', 'dist2wall', 'theta2wall', 'dcenter',
         'anglesub', 'absthetadiff_center', 'closestfly_center'])
  
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
  
  #Average speed of the different Drosophila

  for exp in data.exp.unique() :
   
    data_exp = data.loc[min(data.index[data['exp'] == exp]):max(data.index[data['exp'] == exp])]
  
    groupby_id = data_exp['velmag_ctr'].groupby(data_exp['id'])
    
    IndexSeries = list(range(1, 1+len(data_exp['id'].unique())))
    av_by_Droso = groupby_id.mean().to_frame().set_index(pd.Index(IndexSeries))
    av_by_Droso['id'] = IndexSeries
    
    dros_number = av_by_Droso.as_matrix(columns=av_by_Droso.columns[1:2])
    vel_avg = av_by_Droso.as_matrix(columns=av_by_Droso.columns[0:1])
    
    if exp=='exp_1' :
      color_chosen = 'b'
      legend_chosen = 'Caffeine'
    if exp=='exp_101' :
      color_chosen = 'g'
      legend_chosen = 'Ethanol'
    if exp=='exp_201' :
      color_chosen = 'r'
      legend_chosen = 'Sugar'
    
    plt.plot(dros_number, vel_avg, 'ro', color=color_chosen, label=legend_chosen, marker='o', linestyle='dashed', linewidth=1, markersize=8)
  
  plt.legend()
  plt.xlabel('Drosophila Id')
  plt.ylabel('Average Speed (mm/s)')
  plt.xticks(np.arange(1, len(dros_number)+1, step=1))
  plt.tight_layout()
  plt.savefig('./Graphs/Av speed whole experiment.pdf')
  plt.show()
  plt.close()

#%%
  
  #Average speed in a time interval of all the Drosophila in different graphs
  #determined by the drug
  
  seconds_for_step = 240
  timestep = (data['timestamps']/seconds_for_step).astype(int)
  data['timestep'] = timestep
  IndexSeries = list(range(0, len(data.timestep.unique())))
  
  for exp in data.exp.unique() :
     
    data_exp = data.loc[min(data.index[data['exp'] == exp]):max(data.index[data['exp'] == exp])]
  
    for id in data_exp.id.unique() :
  
      data_id = data_exp.loc[min(data_exp.index[data_exp['id'] == id]):max(data_exp.index[data_exp['id'] == id])]
      groupby_timestep = data_id['velmag_ctr'].groupby(data_id['timestep'])
      av_by_timestep = groupby_timestep.mean().to_frame().set_index(pd.Index(IndexSeries))
      av_by_timestep['timestep'] = IndexSeries
      
      time = av_by_timestep.as_matrix(columns=av_by_timestep.columns[1:2])
      time = time*seconds_for_step/60
      vel_timestep = av_by_timestep.as_matrix(columns=av_by_timestep.columns[0:1])
  
      plt.plot(time, vel_timestep)
      
    if exp=='exp_1' :
      path = './Graphs/Av speed for time interval (caffeine).pdf'
    if exp=='exp_101' :
      path = './Graphs/Av speed for time interval (ethanol).pdf'
    if exp=='exp_201' :
      path = './Graphs/Av speed for time interval (sugar).pdf'
    plt.xlabel('Minute')
    plt.ylabel('Average Speed Interval (mm/s)')
    plt.xticks(np.arange(0, (len(time)-1)*seconds_for_step/60+1, step=int(len(time)*seconds_for_step/60/5)-1))
    plt.tight_layout()
    plt.savefig(path)
    plt.show()
    plt.close()

#%%
  
  #Instant speed for all the Drosophila

  for exp in data.exp.unique() :
     
    data_exp = data.loc[min(data.index[data['exp'] == exp]):max(data.index[data['exp'] == exp])]
  
    if exp=='exp_1' :
      color_chosen = 'b'
      legend_chosen = 'Caffeine'
    if exp=='exp_101' :
      color_chosen = 'g'
      legend_chosen = 'Ethanol'
    if exp=='exp_201' :
      color_chosen = 'r'
      legend_chosen = 'Sugar'
    
    numbins=120
    y, x, _ = plt.hist(data_exp.velmag_ctr, numbins, range = (0, 40), color=color_chosen, label=legend_chosen, alpha=0.6)
  plt.xlabel('Instant Speed (mm/s)')
  plt.ylabel('Frequency')
  max_bin_content = y[int(numbins/8):numbins].max()
  plt.ylim((0,max_bin_content*1.2))
  plt.legend()
  plt.tight_layout()
  plt.savefig('./Graphs/Instant speed whole experiment.pdf')
  plt.show()
  plt.close()

#%%

  #Data selection based on ID and EXP given as parameters
  #Omitted because not very significant after a first look

#  list_of_exp = data['exp'].unique()
#  code_exp = list_of_exp[exp_number]
#  data_exp = data.loc[min(data.index[data['exp'] == code_exp]):max(data.index[data['exp'] == code_exp])]
#  list_of_id = data_exp['id'].unique()
#  code_id = list_of_id[id_number]
#  data_id = data_exp.loc[min(data_exp.index[data_exp['id'] == code_id]):max(data_exp.index[data_exp['id'] == code_id])]

  
  #Trail followed by one Drosophila during the experiment

#  plt.plot(data_id.x_mm, data_id.y_mm)
#  plt.xlabel('x (mm)')
#  plt.ylabel('y (mm)')
#  plt.tight_layout()
#  plt.savefig('./Graphs/Trail of one Drosophila.pdf')
#  plt.show()
#  plt.close()

#%%
  
  #Histogram of all of the minimum distance between fly's center and
  #other flies' centers
  
  for exp in data.exp.unique() :
     
    data_exp = data.loc[min(data.index[data['exp'] == exp]):max(data.index[data['exp'] == exp])]
  
    if exp=='exp_1' :
      color_chosen = 'b'
      legend_chosen = 'Caffeine'
    if exp=='exp_101' :
      color_chosen = 'g'
      legend_chosen = 'Ethanol'
    if exp=='exp_201' :
      color_chosen = 'r'
      legend_chosen = 'Sugar'
    
    numbins=120
    y, x, _ = plt.hist(data_exp.dcenter, numbins, range=(0, 50), color=color_chosen, label=legend_chosen, alpha=0.6)
  plt.xlabel('Minimum Distance Between Center of Dros. (mm)')
  plt.ylabel('Frequency')
  plt.legend()
  plt.tight_layout()
  plt.savefig("./Graphs/Min dist between Drosophila's centers.pdf")
  plt.show()
  plt.close()

#%%

  #Histogram of the difference between the velocity direction and the
  #orientation of fly
  
  for exp in data.exp.unique() :
     
    data_exp = data.loc[min(data.index[data['exp'] == exp]):max(data.index[data['exp'] == exp])]
  
    if exp=='exp_1' :
      color_chosen = 'b'
      legend_chosen = 'Caffeine'
    if exp=='exp_101' :
      color_chosen = 'g'
      legend_chosen = 'Ethanol'
    if exp=='exp_201' :
      color_chosen = 'r'
      legend_chosen = 'Sugar'
    
    numbins=240
    y, x, _ = plt.hist(abs(data_exp.phi)-abs(data_exp.theta), numbins, color=color_chosen, label=legend_chosen, alpha=0.6)
  plt.xlabel('|Vel. Direct. Angle| - |Orient. Angle| (rad)')
  plt.ylabel('Frequency')
  plt.legend()
  plt.tight_layout()
  plt.savefig('./Graphs/Vel. dir. angle - orient. angle.pdf')
  plt.show()
  plt.close()
  
#%%
  
  #Histogram of all of the angle to closest point on the arena wall,
  #relative to the fly's orientation.
  #NOTE: for ethanol and sugar it's not symmetrical
  
  for exp in data.exp.unique() :
     
    data_exp = data.loc[min(data.index[data['exp'] == exp]):max(data.index[data['exp'] == exp])]
  
    if exp=='exp_1' :
      color_chosen = 'b'
      legend_chosen = 'Caffeine'
    if exp=='exp_101' :
      color_chosen = 'g'
      legend_chosen = 'Ethanol'
    if exp=='exp_201' :
      color_chosen = 'r'
      legend_chosen = 'Sugar'
    
    numbins=120
    y, x, _ = plt.hist(data_exp.theta2wall, numbins, color=color_chosen, label=legend_chosen, alpha=0.6)
  plt.xlabel('Theta to Closest Wall (rad)')
  plt.ylabel('Frequency')
  plt.legend()
  plt.tight_layout()
  plt.savefig('./Graphs/Angle to wall.pdf')
  plt.show()
  plt.close()

#%%

  #Correlation between the distance to the closest wall and the angle to
  #closest point on the arena wall, relative to the fly's orientation
  #NOTE: some points have d2wall > 45.5mm which is the radius

  for exp in data.exp.unique() :
     
    data_exp = data.loc[min(data.index[data['exp'] == exp]):max(data.index[data['exp'] == exp])]
  
    if exp=='exp_1' :
      color_chosen = 'b'
      legend_chosen = 'Caffeine'
      id='fly#_001_1'
    if exp=='exp_101' :
      color_chosen = 'g'
      legend_chosen = 'Ethanol'
      id='fly#_101_1'
    if exp=='exp_201' :
      color_chosen = 'r'
      legend_chosen = 'Sugar'
      id='fly#_201_1'
    
    data_id = data_exp.loc[min(data_exp.index[data_exp['id'] == id]):max(data_exp.index[data_exp['id'] == id])]
    plt.plot(data_id.dist2wall, data_id.theta2wall, color=color_chosen, label=legend_chosen, alpha=0.6, markersize=1, linewidth=0, marker='o')
  plt.xlabel('Distance to closest wall (mm)')
  plt.ylabel('Theta to Closest Wall (rad)')
  lgnd = plt.legend()
  for i in range(0, (len(data.exp.unique()))):
    lgnd.legendHandles[i]._legmarker.set_markersize(8)
  plt.tight_layout()
  plt.savefig('./Graphs/Dist. and angle to wall.pdf')
  plt.show()
  plt.close()

#%%

  #Correlation between the forward velocity and the angle to closest point
  #on the arena wall, relative to the fly's orientation

  for exp in data.exp.unique() :
     
    data_exp = data.loc[min(data.index[data['exp'] == exp]):max(data.index[data['exp'] == exp])]
  
    if exp=='exp_1' :
      color_chosen = 'b'
      legend_chosen = 'Caffeine'
      id='fly#_001_1'
    if exp=='exp_101' :
      color_chosen = 'g'
      legend_chosen = 'Ethanol'
      id='fly#_101_1'
    if exp=='exp_201' :
      color_chosen = 'r'
      legend_chosen = 'Sugar'
      id='fly#_201_1'
    
    data_id = data_exp.loc[min(data_exp.index[data_exp['id'] == id]):max(data_exp.index[data_exp['id'] == id])]
    plt.plot(data_id.du_ctr, data_id.theta2wall, color=color_chosen, label=legend_chosen, alpha=0.6, markersize=1, linewidth=0, marker='o')
  plt.xlabel('Forward Velocity (mm/s)')
  plt.ylabel('Theta to Closest Wall (rad)')
  plt.xlim(-10,50)
  lgnd = plt.legend()
  lgnd.legendHandles[0]._legmarker.set_markersize(8)
  lgnd.legendHandles[1]._legmarker.set_markersize(8)
  lgnd.legendHandles[2]._legmarker.set_markersize(8)
  plt.tight_layout()
  plt.savefig('./Graphs/Forward speed and angle to wall.pdf')
  plt.show()
  plt.close()

#%%
  
  #Histogram of all of the absolute difference in orientation between a Drosophila
  #and the closest Drosophila (based on dcenter)
  #NOTE: both for caffeine and ethanol the fly have the same orientation
  #i.e. they often follow each other and not just meet
  
  for exp in data.exp.unique() :
     
    data_exp = data.loc[min(data.index[data['exp'] == exp]):max(data.index[data['exp'] == exp])]
  
    if exp=='exp_1' :
      color_chosen = 'b'
      legend_chosen = 'Caffeine'
    if exp=='exp_101' :
      color_chosen = 'g'
      legend_chosen = 'Ethanol'
    if exp=='exp_201' :
      color_chosen = 'r'
      legend_chosen = 'Sugar'
    
    numbins=120
    y, x, _ = plt.hist(data_exp.absthetadiff_center, numbins, color=color_chosen, label=legend_chosen, alpha=0.6)
  plt.xlabel('|Theta| Difference between Closest Dros. (rad)')
  plt.ylabel('Frequency')
  plt.legend()
  plt.tight_layout()
  plt.savefig('./Graphs/Angle diff. between closest Dros.pdf')
  plt.show()
  plt.close()

#%%
  
  #Histogram of all of the maximum total angle of fly's view occluded by another fly
  
  for exp in data.exp.unique() :
     
    data_exp = data.loc[min(data.index[data['exp'] == exp]):max(data.index[data['exp'] == exp])]
  
    if exp=='exp_1' :
      color_chosen = 'b'
      legend_chosen = 'Caffeine'
    if exp=='exp_101' :
      color_chosen = 'g'
      legend_chosen = 'Ethanol'
    if exp=='exp_201' :
      color_chosen = 'r'
      legend_chosen = 'Sugar'
    
    numbins=60
    y, x, _ = plt.hist(data_exp.anglesub, numbins, range=(0, 0.1), color=color_chosen, label=legend_chosen, alpha=0.6)
  plt.xlabel('Maximum Angle Occluded by another Dros. (rad)')
  plt.ylabel('Frequency')
  plt.legend()
  plt.tight_layout()
  plt.savefig('./Graphs/Maximum angle occluded.pdf')
  plt.show()
  plt.close()
#%%
  
  #I create a column called proximity which will be 0 if dcenter > trigger_for_proximity
  #and 1 if dcenter < trigger_for_proximity
  
  trigger_for_proximity = 6
  proximity = (data['dcenter']/trigger_for_proximity).astype(int)
  proximity = proximity.astype(bool)
  proximity = ~proximity
  proximity = proximity.astype(int)
  data['proximity'] = proximity

  #I create a column called seen which will be 0 if:
  #trigger_for_view < absthetadiff_center < pi - trigger_for_view
  #and 1 otherwise
  
  trigger_for_view = 0.7
  seen_1 = (data.absthetadiff_center/trigger_for_view).astype(int)
  seen_1 = seen_1.astype(bool)
  seen_1 = ~seen_1
  seen_1 = seen_1.astype(int)
  seen_2 = ((data.absthetadiff_center-math.pi)/trigger_for_view).astype(int)
  seen_2 = seen_2.astype(bool)
  seen_2 = ~seen_2
  seen_2 = seen_2.astype(int)
  seen = seen_1 + seen_2
  data['seen'] = seen
  
  time_min = 0
  time_max = 100
  timespan = time_max-time_min

#%%  

  #First look at the network
  #Visual rapresentatio of the closest Dros.
  #Example:
  #On line 2 the colour light blue means that the Dros.1 sees the Dros.2
  #as the closest one.
  #NOTE: this doesn't mean that 2 sees 1 as the closest too!

  for exp in data.exp.unique() :
     
    data_exp = data.loc[min(data.index[data['exp'] == exp]):max(data.index[data['exp'] == exp])]

    #I reverse the order just to reverse the legend..
    #If you want to undo it remember to switch the min and max used in the loc
      
    data_exp = data_exp.reindex(index=data_exp.index[::-1])
  
    for id in data_exp.id.unique() :
  
      data_id = data_exp.loc[max(data_exp.index[data_exp['id'] == id]) : min(data_exp.index[data_exp['id'] == id])]

      data_id = data_id.loc[max(data_id.index[data_id['timestamps'] <= time_max]) : min(data_id.index[data_id['timestamps'] >= time_min])]
      
      if (id=='fly#_001_1' or id=='fly#_101_1' or id=='fly#_201_1'):
          legend_chosen = 'Dros. 1'
      if (id=='fly#_002_1' or id=='fly#_102_1' or id=='fly#_202_1'):
          legend_chosen = 'Dros. 2'
      if (id=='fly#_003_1' or id=='fly#_103_1' or id=='fly#_203_1'):
          legend_chosen = 'Dros. 3'
      if (id=='fly#_004_1' or id=='fly#_104_1' or id=='fly#_204_1'):
          legend_chosen = 'Dros. 4'
      if (id=='fly#_005_1' or id=='fly#_105_1' or id=='fly#_205_1'):
          legend_chosen = 'Dros. 5'
      if (id=='fly#_006_1' or id=='fly#_106_1' or id=='fly#_206_1'):
          legend_chosen = 'Dros. 6'
      if (id=='fly#_007_1' or id=='fly#_107_1' or id=='fly#_207_1'):
          legend_chosen = 'Dros. 7'
      if (id=='fly#_008_1' or id=='fly#_108_1' or id=='fly#_208_1'):
          legend_chosen = 'Dros. 8'
      if (id=='fly#_009_1' or id=='fly#_109_1' or id=='fly#_209_1'):
          legend_chosen = 'Dros. 9'
      if (id=='fly#_010_1' or id=='fly#_110_1' or id=='fly#_210_1'):
          legend_chosen = 'Dros. 10'

      plt.plot(data_id.timestamps, data_id.closestfly_center*data_id.proximity*data_id.seen,
               marker="|", markersize=12, linewidth=0, label=legend_chosen)
         
    if exp=='exp_1' :
      path = './Graphs/Network (caffeine).pdf'
    if exp=='exp_101' :
      path = './Graphs/Network (ethanol).pdf'
    if exp=='exp_201' :
      path = './Graphs/Network (sugar).pdf'
    lgnd = plt.legend(fontsize = 13)
    for i in range(0, (len(data_exp.id.unique()))):
      lgnd.legendHandles[i]._legmarker.set_markersize(8)
      lgnd.legendHandles[i]._legmarker.set_marker('o')
    plt.xlabel('Time (s)')
    plt.ylabel('Drosophila Id')
    plt.xlim(time_min-timespan*0.05,time_max+timespan*0.6)
    plt.ylim(0.3,10.7)
    plt.xticks(np.arange(time_min, time_max+1, step=timespan/5))
    plt.yticks(np.arange(1, 11, step=1))
    plt.tight_layout()
    plt.savefig(path)
    plt.show()
    plt.close()

#%%

if __name__ == '__main__':
  
  data_name = 'data_original.csv'
  
  statistics(data_name)
