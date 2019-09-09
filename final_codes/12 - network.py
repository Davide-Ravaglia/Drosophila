# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import pandas as pd
import pylab as plt
import numpy as np
from itertools import chain


__package__ = "Find the meetings for the real data and all the rndm walks produced and write a df with the info about them"
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

#   I will use this df to make the search for an id skip if I have already looked
#   into that id for an interaction for a certain amount of time.
skip_until = pd.DataFrame(pd.DataFrame(index=range(1,11)))

#   I import the two df which have the information of the region in which a
#   Dros is at any time.
region_real = pd.read_csv('./network/region_real.csv', sep=',', header=0, index_col='Unnamed: 0')

#   What is a meeting between Drosophila?
#   Take a Dros in the region 19:
#   . If another Drosophila is in the extended region 19 (region 19 + border)
#   . If it they contemporary stay still (v < v_limit which now is 2.0 mm/s,
#     the velocity is computed as the running velocity with t = 7/15s)
#     in the region for some time (still to decide so make a bunch of trials and graph it all)
#   Then for each meeting we should also see the avg distance, how much
#   They are looking at each other and stuff like that

#   I create two df which will have the following statistics of the meeting:
#   . Id of both
#   . Beginning of meeting
#   . Simultaneous time spent in the box
#   (of this time:)
#   . Time spent staying still in the box for both
#   . Simultaneous time spent staying still in box

stats_of_meeting_real = pd.DataFrame(pd.DataFrame(index=range(0,1000)))


time_for_meeting = 0.5
v_limit = 2.0
division = 6

prev_region = 0


#   I find the meetings for the real data

data_chosen = region_real

for exp in range (0, 3) :

  if exp == 0 :
    drug = " caf"
  if exp == 1 :
    drug = " eth"
  if exp == 2 :
    drug = " sug"

  stats_of_meeting_real["Id 1 -" + drug] = np.nan
  stats_of_meeting_real["Id 2 -" + drug] = np.nan
  stats_of_meeting_real["Start -" + drug] = np.nan
  stats_of_meeting_real["Time tog. -" + drug] = np.nan
  stats_of_meeting_real["Time still 1 -" + drug] = np.nan
  stats_of_meeting_real["Time still 2 -" + drug] = np.nan
  stats_of_meeting_real["Time still tog. -" + drug] = np.nan
  stats_of_meeting_real["Region -" + drug] = np.nan
  
  meeting_counter = 0
  
  for id in range (1, 11) :
    
    print("EXP: ", exp, "  ID: ", id)
    
    header_x = str(exp) + " : " + str(id) + " x"
    header_y = str(exp) + " : " + str(id) + " y"
    header_vel = str(exp) + " : " + str(id) + " vel"
    header_theta = str(exp) + " : " + str(id) + " theta"
    
    start_col_name = str(exp) + " : " + str(id) + " ("

    skip_until["Here"] = np.nan
#   I will use this variable to elimanate the "twin" meetings since every
#   meeting will have a twin
    already_happened = 0

    for i in range (0, len(data_chosen)) :
      
#   The velocity I'm accessing to is already the running avg of the inst vel        
      if data_chosen[header_vel][i] < v_limit :
#   I keep in memory in which region the Dros. was the last frame, this way I
#   hope to speed up the process by looking first at that region.
        if data_chosen[start_col_name + str(prev_region) + ")"][i] == 1 :
#   I search for another Dros. in the same (extended) square
          for second_id in range (1, 11) :
#   Of course skip the id of the first Dros.
            if second_id == id : continue
#   If I already signaled to skip until a certain time a determined id
            if skip_until["Here"][second_id] > i : continue
#   > 0 and not == 1 because It's ok if it's 0.5, which means that is in the
#   extended square. I also want that the second Dros. is still.
            if (data_chosen[str(exp)+" : "+str(second_id)+" ("+str(prev_region)+")"][i] > 0
                and data_chosen[str(exp)+" : "+str(second_id)+" vel"][i] < v_limit):
#   I use a second index to see how long the interaction of which I have
#   just seen the start it is.
              for j in range (1, len(data_chosen)) :
#   Stop if I have reached the end of the df

                if (i+j == len(data_chosen)) :
                  
                  skip_until["Here"][second_id] = i+j
#   If the interaction has lasted long enough I save the statistics about it
                  if j/15 > time_for_meeting :
#   I check weather the interaction has already happened or not
                    for k in range (0, meeting_counter) :
#   If I find that it already happened I don't write it down and I reset
#   the variable already_happened
                      if (stats_of_meeting_real["Id 1 -" + drug][k] == second_id and
                          stats_of_meeting_real["Id 2 -" + drug][k] == id and
                          stats_of_meeting_real["Start -" + drug][k] == i/15):
                        already_happened = 1
                        break
                    if already_happened == 0 :
                      stats_of_meeting_real["Id 1 -" + drug][meeting_counter] = id
                      stats_of_meeting_real["Id 2 -" + drug][meeting_counter] = second_id
                      stats_of_meeting_real["Start -" + drug][meeting_counter] = i/15
                      stats_of_meeting_real["Time still tog. -" + drug][meeting_counter] = j/15
                      stats_of_meeting_real["Region -" + drug][meeting_counter] = prev_region
                      meeting_counter += 1
#                          print("Incontro 1 #", meeting_counter)
                    else : already_happened = 0
                    skip_until["Here"][second_id] = i+j
                  break
#   If one of the Dros. starts moving or leaves the extended region but they
#   have spent enough time together save the statistics of the interaction.
#   Since I don't want to fill the nan with 0 I have to do the opposite check
#   and then use the else if the if didin't work
                if (data_chosen[str(exp)+" : "+str(second_id)+" ("+str(prev_region)+")"][i+j] > 0
                    and data_chosen[str(exp)+" : "+str(second_id)+" vel"][i+j] < v_limit
                    and data_chosen[start_col_name + str(prev_region) + ")"][i+j] > 0
                    and data_chosen[header_vel][i+j] < v_limit) : continue
                elif j/15 > time_for_meeting :
                  for k in range (0, meeting_counter) :
                    if (stats_of_meeting_real["Id 1 -" + drug][k] == second_id and
                        stats_of_meeting_real["Id 2 -" + drug][k] == id and
                        stats_of_meeting_real["Start -" + drug][k] == i/15):
                      already_happened = 1
                      break
                  if already_happened == 0 :
                    stats_of_meeting_real["Id 1 -" + drug][meeting_counter] = id
                    stats_of_meeting_real["Id 2 -" + drug][meeting_counter] = second_id
                    stats_of_meeting_real["Start -" + drug][meeting_counter] = i/15
                    stats_of_meeting_real["Time still tog. -" + drug][meeting_counter] = j/15
                    stats_of_meeting_real["Region -" + drug][meeting_counter] = prev_region
                    meeting_counter += 1
#                        print("Incontro 3 #", meeting_counter)
                  else : already_happened = 0
                  skip_until["Here"][second_id] = i+j
                  break
                else :
                  skip_until["Here"][second_id] = i+j
                  break

#   If the Dros. changed region since the last time it was still search for
#   the region in which is now
        else:
          for region in range (0, division*division) :
            if data_chosen[start_col_name + str(region) + ")"][i] == 1 :
#   As soon as you find the region where is now do exactly the same stuff you
#   did above.
              prev_region = region
#   I search for another Dros. in the same (extended) square
              for second_id in range (1, 11) :
#   Of course skip the id of the first Dros.
                if second_id == id : continue
#   If I already signaled to skip until a certain time a determined id
                if skip_until["Here"][second_id] > i : continue
#   > 0 and not == 1 because It's ok if it's 0.5, which means that is in the
#   extended square. I also want that the second Dros. is still.
                if (data_chosen[str(exp)+" : "+str(second_id)+" ("+str(prev_region)+")"][i] > 0
                    and data_chosen[str(exp)+" : "+str(second_id)+" vel"][i] < v_limit):
#   I use a second index to see how long the interaction of which I have
#   just seen the start it is.
                  for j in range (1, len(data_chosen)) :
#   Stop if I have reached the end of the df

                    if (i+j == len(data_chosen)) :

                      skip_until["Here"][second_id] = i+j
#   If the interaction has lasted long enough I save the statistics about it
                      if j/15 > time_for_meeting :
                        for k in range (0, meeting_counter) :
                          if (stats_of_meeting_real["Id 1 -" + drug][k] == second_id and
                              stats_of_meeting_real["Id 2 -" + drug][k] == id and
                              stats_of_meeting_real["Start -" + drug][k] == i/15):
                            already_happened = 1
                            break
                        if already_happened == 0 :
                          stats_of_meeting_real["Id 1 -" + drug][meeting_counter] = id
                          stats_of_meeting_real["Id 2 -" + drug][meeting_counter] = second_id
                          stats_of_meeting_real["Start -" + drug][meeting_counter] = i/15
                          stats_of_meeting_real["Time still tog. -" + drug][meeting_counter] = j/15
                          stats_of_meeting_real["Region -" + drug][meeting_counter] = prev_region
                          meeting_counter += 1
#                              print("Incontro 5 #", meeting_counter)
                        else : already_happened = 0

                        skip_until["Here"][second_id] = i+j

                        break
#   If one of the Dros. starts moving or leaves the extended region but they
#   have spent enough time together save the statistics of the interaction.
#   Since I don't want to fill the nan with 0 I have to do the opposite check
#   and then use the else if the if didin't work
                    if (data_chosen[str(exp)+" : "+str(second_id)+" ("+str(prev_region)+")"][i+j] > 0
                        and data_chosen[str(exp)+" : "+str(second_id)+" vel"][i+j] < v_limit
                        and data_chosen[start_col_name + str(prev_region) + ")"][i+j] > 0
                        and data_chosen[header_vel][i+j] < v_limit) : continue
                    elif j/15 > time_for_meeting :
                      for k in range (0, meeting_counter) :
                        if (stats_of_meeting_real["Id 1 -" + drug][k] == second_id and
                            stats_of_meeting_real["Id 2 -" + drug][k] == id and
                            stats_of_meeting_real["Start -" + drug][k] == i/15):
                          already_happened = 1
                          break
                      if already_happened == 0 :
                        stats_of_meeting_real["Id 1 -" + drug][meeting_counter] = id
                        stats_of_meeting_real["Id 2 -" + drug][meeting_counter] = second_id
                        stats_of_meeting_real["Start -" + drug][meeting_counter] = i/15
                        stats_of_meeting_real["Time still tog. -" + drug][meeting_counter] = j/15
                        stats_of_meeting_real["Region -" + drug][meeting_counter] = prev_region
                        meeting_counter += 1
#                            print("Incontro 7 #", meeting_counter)
                      else : already_happened = 0

                      skip_until["Here"][second_id] = i+j

                      break

                    else :

                      skip_until["Here"][second_id] = i+j

                      break

#   Now, if a meeting has the same start time and the same two id of another
#   one, is of course the same duplicated. So I have to eliminate the twins.

stats_of_meeting_real.to_csv('./network/stats_of_meeting_real.csv')


#   I find the meetings for the fake data

concatenated = chain(range(1, 14), range(15, 16), range(17, 29), range(30, 33), range(34, 37), range(38, 40), range(41, 43), range(44, 48))
for seed in concatenated:

  print(seed)
  
  extraction_path = './network/many_region_fake/region_fake (seed=' + str(seed) + ').csv'
  
  region_fake = pd.read_csv(extraction_path, sep=',', header=0, index_col='Unnamed: 0')
  
  stats_of_meeting_fake = pd.DataFrame(pd.DataFrame(index=range(0,1000)))
  
  data_chosen = region_fake
  
  prev_region = 0

  
  prev_region = 0
  
  for exp in range (0, 3) :
  
    if exp == 0 :
      drug = " caf"
    if exp == 1 :
      drug = " eth"
    if exp == 2 :
      drug = " sug"
  
    stats_of_meeting_fake["Id 1 -" + drug] = np.nan
    stats_of_meeting_fake["Id 2 -" + drug] = np.nan
    stats_of_meeting_fake["Start -" + drug] = np.nan
    stats_of_meeting_fake["Time tog. -" + drug] = np.nan
    stats_of_meeting_fake["Time still 1 -" + drug] = np.nan
    stats_of_meeting_fake["Time still 2 -" + drug] = np.nan
    stats_of_meeting_fake["Time still tog. -" + drug] = np.nan
    stats_of_meeting_fake["Region -" + drug] = np.nan
    
    meeting_counter = 0
    
    for id in range (1, 11) :
      
      print("EXP: ", exp, "  ID: ", id)
      
      header_x = str(exp) + " : " + str(id) + " x"
      header_y = str(exp) + " : " + str(id) + " y"
      header_vel = str(exp) + " : " + str(id) + " vel"
      header_theta = str(exp) + " : " + str(id) + " theta"
      
      start_col_name = str(exp) + " : " + str(id) + " ("
  
      skip_until["Here"] = np.nan
  #   I will use this variable to elimanate the "twin" meetings since every
  #   meeting will have a twin
      already_happened = 0
      
      for i in range (0, len(data_chosen)) :
        
  #   The velocity I'm accessing to is already the running avg of the inst vel        
        if data_chosen[header_vel][i] < v_limit :
  #   I keep in memory in which region the Dros. was the last frame, this way I
  #   hope to speed up the process by looking first at that region.
          if data_chosen[start_col_name + str(prev_region) + ")"][i] == 1 :
  #   I search for another Dros. in the same (extended) square
            for second_id in range (1, 11) :
  #   Of course skip the id of the first Dros.
              if second_id == id : continue
  #   If I already signaled to skip until a certain time a determined id
              if skip_until["Here"][second_id] > i : continue
  #   > 0 and not == 1 because It's ok if it's 0.5, which means that is in the
  #   extended square. I also want that the second Dros. is still.
              if (data_chosen[str(exp)+" : "+str(second_id)+" ("+str(prev_region)+")"][i] > 0
                  and data_chosen[str(exp)+" : "+str(second_id)+" vel"][i] < v_limit):
  #   I use a second index to see how long the interaction of which I have
  #   just seen the start it is.
                for j in range (1, len(data_chosen)) :
  #   Stop if I have reached the end of the df
  
                  if (i+j == len(data_chosen)) :
                    
                    skip_until["Here"][second_id] = i+j
  #   If the interaction has lasted long enough I save the statistics about it
                    if j/15 > time_for_meeting :
                      for k in range (0, meeting_counter) :
                        if (stats_of_meeting_fake["Id 1 -" + drug][k] == second_id and
                            stats_of_meeting_fake["Id 2 -" + drug][k] == id and
                            stats_of_meeting_fake["Start -" + drug][k] == i/15):
                          already_happened = 1
                          break
                      if already_happened == 0 :
                        stats_of_meeting_fake["Id 1 -" + drug][meeting_counter] = id
                        stats_of_meeting_fake["Id 2 -" + drug][meeting_counter] = second_id
                        stats_of_meeting_fake["Start -" + drug][meeting_counter] = i/15
                        stats_of_meeting_fake["Time still tog. -" + drug][meeting_counter] = j/15
                        stats_of_meeting_fake["Region -" + drug][meeting_counter] = prev_region
                        meeting_counter += 1
  #                          print("Incontro 2 #", meeting_counter)
                      else : already_happened = 0
                      skip_until["Here"][second_id] = i+j
                    break
  #   If one of the Dros. starts moving or leaves the extended region but they
  #   have spent enough time together save the statistics of the interaction.
  #   Since I don't want to fill the nan with 0 I have to do the opposite check
  #   and then use the else if the if didin't work
                  if (data_chosen[str(exp)+" : "+str(second_id)+" ("+str(prev_region)+")"][i+j] > 0
                      and data_chosen[str(exp)+" : "+str(second_id)+" vel"][i+j] < v_limit
                      and data_chosen[start_col_name + str(prev_region) + ")"][i+j] > 0
                      and data_chosen[header_vel][i+j] < v_limit) : continue
                  elif j/15 > time_for_meeting :
                    for k in range (0, meeting_counter) :
                      if (stats_of_meeting_fake["Id 1 -" + drug][k] == second_id and
                          stats_of_meeting_fake["Id 2 -" + drug][k] == id and
                          stats_of_meeting_fake["Start -" + drug][k] == i/15):
                        already_happened = 1
                        break
                    if already_happened == 0 :
                      stats_of_meeting_fake["Id 1 -" + drug][meeting_counter] = id
                      stats_of_meeting_fake["Id 2 -" + drug][meeting_counter] = second_id
                      stats_of_meeting_fake["Start -" + drug][meeting_counter] = i/15
                      stats_of_meeting_fake["Time still tog. -" + drug][meeting_counter] = j/15
                      stats_of_meeting_fake["Region -" + drug][meeting_counter] = prev_region
                      meeting_counter += 1
  #                        print("Incontro 4 #", meeting_counter)
                    else : already_happened = 0
                    skip_until["Here"][second_id] = i+j
                    break
                  else :
                    skip_until["Here"][second_id] = i+j
                    break
  
  #   If the Dros. changed region since the last time it was still search for
  #   the region in which is now
          else:
            for region in range (0, division*division) :
              if data_chosen[start_col_name + str(region) + ")"][i] == 1 :
  #   As soon as you find the region where is now do exactly the same stuff you
  #   did above.
                prev_region = region
  #   I search for another Dros. in the same (extended) square
                for second_id in range (1, 11) :
  #   Of course skip the id of the first Dros.
                  if second_id == id : continue
  #   If I already signaled to skip until a certain time a determined id
                  if skip_until["Here"][second_id] > i : continue
  #   > 0 and not == 1 because It's ok if it's 0.5, which means that is in the
  #   extended square. I also want that the second Dros. is still.
                  if (data_chosen[str(exp)+" : "+str(second_id)+" ("+str(prev_region)+")"][i] > 0
                      and data_chosen[str(exp)+" : "+str(second_id)+" vel"][i] < v_limit):
  #   I use a second index to see how long the interaction of which I have
  #   just seen the start it is.
                    for j in range (1, len(data_chosen)) :
  #   Stop if I have reached the end of the df
  
                      if (i+j == len(data_chosen)) :
                        
                        skip_until["Here"][second_id] = i+j
  #   If the interaction has lasted long enough I save the statistics about it
                        if j/15 > time_for_meeting :
                          for k in range (0, meeting_counter) :
                            if (stats_of_meeting_fake["Id 1 -" + drug][k] == second_id and
                                stats_of_meeting_fake["Id 2 -" + drug][k] == id and
                                stats_of_meeting_fake["Start -" + drug][k] == i/15):
                              already_happened = 1
                              break
                          if already_happened == 0 :
                            stats_of_meeting_fake["Id 1 -" + drug][meeting_counter] = id
                            stats_of_meeting_fake["Id 2 -" + drug][meeting_counter] = second_id
                            stats_of_meeting_fake["Start -" + drug][meeting_counter] = i/15
                            stats_of_meeting_fake["Time still tog. -" + drug][meeting_counter] = j/15
                            stats_of_meeting_fake["Region -" + drug][meeting_counter] = prev_region
                            meeting_counter += 1
  #                              print("Incontro 6 #", meeting_counter)
                          else : already_happened = 0
                          skip_until["Here"][second_id] = i+j
                          break
  #   If one of the Dros. starts moving or leaves the extended region but they
  #   have spent enough time together save the statistics of the interaction.
  #   Since I don't want to fill the nan with 0 I have to do the opposite check
  #   and then use the else if the if didin't work
                      if (data_chosen[str(exp)+" : "+str(second_id)+" ("+str(prev_region)+")"][i+j] > 0
                          and data_chosen[str(exp)+" : "+str(second_id)+" vel"][i+j] < v_limit
                          and data_chosen[start_col_name + str(prev_region) + ")"][i+j] > 0
                          and data_chosen[header_vel][i+j] < v_limit) : continue
                      elif j/15 > time_for_meeting :
                        for k in range (0, meeting_counter) :
                          if (stats_of_meeting_fake["Id 1 -" + drug][k] == second_id and
                              stats_of_meeting_fake["Id 2 -" + drug][k] == id and
                              stats_of_meeting_fake["Start -" + drug][k] == i/15):
                            already_happened = 1
                            break
                        if already_happened == 0 :
                          stats_of_meeting_fake["Id 1 -" + drug][meeting_counter] = id
                          stats_of_meeting_fake["Id 2 -" + drug][meeting_counter] = second_id
                          stats_of_meeting_fake["Start -" + drug][meeting_counter] = i/15
                          stats_of_meeting_fake["Time still tog. -" + drug][meeting_counter] = j/15
                          stats_of_meeting_fake["Region -" + drug][meeting_counter] = prev_region
                          meeting_counter += 1
  #                            print("Incontro 8 #", meeting_counter)
                        else : already_happened = 0
                        skip_until["Here"][second_id] = i+j
                        break
                      else :
                        skip_until["Here"][second_id] = i+j
                        break
  
  #   Now, if a meeting has the same start time and the same two id of another
  #   one, is of course the same duplicated. So I have to eliminate the twins.

  path = './network/many_stats_of_meeting_fake/stats_of_meeting_fake (seed=' + str(seed) + ').csv'

  stats_of_meeting_fake.to_csv(path)

