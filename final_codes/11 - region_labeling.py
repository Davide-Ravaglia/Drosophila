# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import pandas as pd
import pylab as plt
import numpy as np
from itertools import chain


__package__ = "Labeling of the region in which the fly is"
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

#   I create two df, region_real e region_fake one for the real data and one for the rndm walks.
#   Each df will have 30 column for each part of the arena.
#   30 because 1 for each id
#   The index indicate, as usual, the frames.
#   Each box can have 3 values: 0, 0.5 and 1
#   1 if the id is in that part of the arena
#   0.5 if the id is in the part of the arena if I exend the part a bit
#   0 if it's not in the part of the arena even with the extension

#   I define the number of parts into which to divide the lenght of the
#   diameter. This parts will be the sides of the squares which will divide
#   the arena.
division = 6

steps_for_running_avg = 7
v_limit = 2.0

#   I know the max and min of the data aren't 50 but a bit more, don't know why.
#   So I find the maximum (in abs value) of x and y. If it's less then 50
#   I use 50. This will be the half lenght of the side of the square which
#   confines the circular arena.
half_side = max(np.abs(data.x_mm.max()), np.abs(data.x_mm.min()), np.abs(data.y_mm.max()), np.abs(data.y_mm.min()), 50)
print(half_side)

#   I create a df which will have the coordinates of the max and min x and y
#   coords for each square. It will contain also those coords incremented
#   by the value of the border width. Now I define the border with ad 1/4
#   of the square side.
#   Of course the center of the coords will be the center of the arena.
borders_coords = pd.DataFrame(pd.DataFrame(index=range(0,division*division)))

#   The 8 columns the df will have: the coords of the side and of the extended sides
borders_coords["x min"] = np.nan
borders_coords["x max"] = np.nan
borders_coords["y min"] = np.nan
borders_coords["y max"] = np.nan
borders_coords["x min ext"] = np.nan
borders_coords["x max ext"] = np.nan
borders_coords["y min ext"] = np.nan
borders_coords["y max ext"] = np.nan

#   Side of the square into which I divide the arena
square_side = half_side*2/division
border_width = square_side/5

for y_div in range(0, division) :

  y_min = -half_side + 2*half_side*y_div/division
  y_max = -half_side + 2*half_side*(y_div+1)/division
  y_min_ext = -half_side - border_width + 2*half_side*y_div/division
  y_max_ext = -half_side + border_width + 2*half_side*(y_div+1)/division

  for x_div in range(0, division) :
    
    x_min = -half_side + 2*half_side*x_div/division
    x_max = -half_side + 2*half_side*(x_div+1)/division
    x_min_ext = -half_side - border_width + 2*half_side*x_div/division
    x_max_ext = -half_side + border_width + 2*half_side*(x_div+1)/division

    borders_coords["x min"][y_div*division + x_div] = x_min
    borders_coords["x max"][y_div*division + x_div] = x_max
    borders_coords["y min"][y_div*division + x_div] = y_min
    borders_coords["y max"][y_div*division + x_div] = y_max
    borders_coords["x min ext"][y_div*division + x_div] = x_min_ext
    borders_coords["x max ext"][y_div*division + x_div] = x_max_ext
    borders_coords["y min ext"][y_div*division + x_div] = y_min_ext
    borders_coords["y max ext"][y_div*division + x_div] = y_max_ext

#   FOR THE REAL DATA
region_real = pd.DataFrame(pd.DataFrame(index=range(0,22000)))

#   I fill the region_real df
exp_counter = -1

for exp in data.exp.unique() :

  id_counter = 1
  exp_counter += 1 

  data_exp = data.loc[min(data.index[data['exp'] == exp]):max(data.index[data['exp'] == exp])]

  for id in data_exp.id.unique() :

    print('Exp: ', exp_counter,'  Id: ', id_counter)

    start_col_name = str(exp_counter) + " : " + str(id_counter) + " ("
    id_counter += 1
    
#   Cycle in which I create the n columns for each id (one for each region)
    for region in range (0, division*division) :

      region_real[start_col_name + str(region) + ")"] = np.nan
    
    data_id = data_exp.loc[min(data_exp.index[data_exp['id'] == id]):max(data_exp.index[data_exp['id'] == id])]
    new_index = pd.Series(data_id.frame) -1
    data_id.set_index(new_index, inplace=True)

    for i in range (0, len(data_id)) :
    
      for region in range (0, division*division) :

#   If my point is inside an extended region I give the box value 0.5
        if (data_id.x_mm[i] >= borders_coords["x min ext"][region] and
            data_id.x_mm[i] <= borders_coords["x max ext"][region] and
            data_id.y_mm[i] >= borders_coords["y min ext"][region] and
            data_id.y_mm[i] <= borders_coords["y max ext"][region]) :
             
          region_real[start_col_name + str(region) + ")"][i] = 0.5

#   If my point is inside the extended region and is inside the region I
#   give the box value 1
          if (data_id.x_mm[i] >= borders_coords["x min"][region] and
              data_id.x_mm[i] <= borders_coords["x max"][region] and
              data_id.y_mm[i] >= borders_coords["y min"][region] and
              data_id.y_mm[i] <= borders_coords["y max"][region]) :

           region_real[start_col_name + str(region) + ")"][i] = 1



#   Since I will need the actual coordinates, the velocity (done with running
#   average with t = 7/15 s) and their orientation,
#   I put all of this info into the two df: region_real and region_fake
#   so they will be the only thing I need later

#   For the real data
exp_counter = -1
for exp in data.exp.unique() :

  id_counter = 1
  exp_counter += 1

  data_exp = data.loc[min(data.index[data['exp'] == exp]):max(data.index[data['exp'] == exp])]

  for id in data_exp.id.unique() :

    print('Exp: ', exp_counter,'  Id: ', id_counter)

    start_col_name = str(exp_counter) + " : " + str(id_counter)
    id_counter += 1
          
    data_id = data_exp.loc[min(data_exp.index[data_exp['id'] == id]):max(data_exp.index[data_exp['id'] == id])]
    new_index = pd.Series(data_id.frame) -1
    data_id.set_index(new_index, inplace=True)

    region_real[start_col_name + " x"] = data_id.x_mm
    region_real[start_col_name + " y"] = data_id.y_mm
    region_real[start_col_name + " vel"] = np.nan
    region_real[start_col_name + " theta"] = data_id.theta

    for i in range (int(steps_for_running_avg/2), len(data_id)-int(steps_for_running_avg/2)-1) :

#   I compute the running avg of the velocity
      sum_of_vel = 0.0

      for j in range (0, steps_for_running_avg) :
        sum_of_vel += data_id.velmag_ctr[i+j-int(steps_for_running_avg/2)]
        
      region_real[start_col_name + " vel"][i] = sum_of_vel/steps_for_running_avg

region_real.to_csv('./network/region_real.csv')
      
#   FOR THE RANDOM WALKS

concatenated = chain(range(1, 14), range(15, 16), range(17, 29), range(30, 33), range(34, 37), range(38, 40), range(41, 43), range(44, 48))
for seed in concatenated:
  
  print(seed)
  
  extraction_path = './random_walk/many_walks/rndm_walks (seed=' + str(seed) + ').csv'
  
  #   For the random walks
  region_fake = pd.DataFrame(pd.DataFrame(index=range(0,22000)))
  
  #   First off I extract the random_walks
  rndm_walks = pd.read_csv(extraction_path, sep=',', header=0, index_col='Unnamed: 0')
        
  
  
  #   I fill the region_fake df
  for exp in range(0, 3) :
  
    for id in range(1, 11) :
  
      print('Exp: ', exp,'  Id: ', id)
  
      start_col_name = str(exp) + " : " + str(id) + " ("
      
  #   Cycle in which I create the n columns for each id (one for each region)
      for region in range (0, division*division) :
  
        region_fake[start_col_name + str(region) + ")"] = np.nan
  
  #   I extract the x and y coords from the rndm_walks df
      column_x = rndm_walks[str(exp) + " - " + str(id-1) + " x"]
      column_y = rndm_walks[str(exp) + " - " + str(id-1) + " y"]
  
      for i in range (0, len(column_x)) :
      
        for region in range (0, division*division) :
  
  #   If my point is inside an extended region I give the box value 0.5
          if (column_x[i] >= borders_coords["x min ext"][region] and
              column_x[i] <= borders_coords["x max ext"][region] and
              column_y[i] >= borders_coords["y min ext"][region] and
              column_y[i] <= borders_coords["y max ext"][region]) :
               
            region_fake[start_col_name + str(region) + ")"][i] = 0.5
  
  #   If my point is inside the extended region and is inside the region I
  #   give the box value 1
            if (column_x[i] >= borders_coords["x min"][region] and
                column_x[i] <= borders_coords["x max"][region] and
                column_y[i] >= borders_coords["y min"][region] and
                column_y[i] <= borders_coords["y max"][region]) :
  
             region_fake[start_col_name + str(region) + ")"][i] = 1
  
    
        
  for exp in range(0, 3) :
  
    if exp == 0 :
      drug = " caf"
    if exp == 1 :
      drug = " eth"
    if exp == 2 :
      drug = " sug"
  
    for id in range(1, 11) :
  
      print('Exp: ', exp,'  Id: ', id)
  
      start_col_name = str(exp) + " : " + str(id)
      
  #   I extract the x and y coords from the rndm_walks df
      column_x = rndm_walks[str(exp) + " - " + str(id-1) + " x"]
      column_y = rndm_walks[str(exp) + " - " + str(id-1) + " y"]
      column_phi = rndm_walks[str(exp) + " - " + str(id-1) + " phi"]
  
      region_fake[start_col_name + " x"] = column_x
      region_fake[start_col_name + " y"] = column_y
      region_fake[start_col_name + " vel"] = np.nan
  #    region_fake[start_col_name + " theta"] = np.nan
  
      for i in range (int(steps_for_running_avg/2), len(column_x)-int(steps_for_running_avg/2)-1) :
  
  #   I compute the running average of the velocity
        sum_of_vel = 0.0
        for j in range (0, steps_for_running_avg) :
          sum_of_vel += np.sqrt(np.power(column_x[i+j-int(steps_for_running_avg/2)+1]-column_x[i+j-int(steps_for_running_avg/2)],2)
                                +np.power(column_y[i+j-int(steps_for_running_avg/2)+1]-column_y[i+j-int(steps_for_running_avg/2)],2))/(1/15)
        region_fake[start_col_name + " vel"][i] = sum_of_vel/steps_for_running_avg
  
  #   When I have the running average I can say if it's still or moving
  #   If it's moving the orientation will be the velocity direction. If it's still
  #   it will be the last velocity direction before moving + a little variation each time
  
    #   I comment this part because the orientation is not actually used
  #      if region_fake[start_col_name + " vel"][i] < v_limit :
  
  #   It could happen that the previous orientation (which I later need) is nan.
  #   In this case the orientation will be the velocity direction
  #        if math.isnan(region_fake[start_col_name + " vel"][i-1]) :
  #          print("Succede")
  #          region_fake[start_col_name + " theta"][i] = column_phi[i]
  #
  #        else :
  #          which_bin = random.uniform(0, 1)
    #   I use the cumulative probability to choose the bin
  #          for j in range(0, len(changes_of_theta)) :
  #  
  #            if changes_of_theta["cumprob" + drug][j] > which_bin :
  #              change_of_orientation = random.uniform(changes_of_theta["dtheta central"][j]-0.1/(numbins), changes_of_theta["dtheta central"][j]+0.1/(numbins))
  #              break
  #
  #          region_fake[start_col_name + " theta"][i] = region_fake[start_col_name + " theta"][i-1] + change_of_orientation
  #          if region_fake[start_col_name + " theta"][i] > math.pi :
  #            print(region_fake[start_col_name + " theta"][i])
  #            region_fake[start_col_name + " theta"][i] -= math.pi*2
  #            print(region_fake[start_col_name + " theta"][i])
  #          if region_fake[start_col_name + " theta"][i] < -math.pi :
  #            print(region_fake[start_col_name + " theta"][i])
  #            region_fake[start_col_name + " theta"][i] += math.pi*2
  #            print(region_fake[start_col_name + " theta"][i])
  #
  #      else :
  #         region_fake[start_col_name + " theta"][i] = column_phi[i]

  path = './network/many_region_fake/region_fake (seed=' + str(seed) + ').csv'
  
  region_fake.to_csv(path)
