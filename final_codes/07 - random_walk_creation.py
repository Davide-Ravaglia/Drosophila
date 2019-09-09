# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import pandas as pd
import pylab as plt
import math
import numpy as np
import random
from itertools import chain


__package__ = "Production of random walk based on the statistics from the real data"
__author__  = "Davide Ravaglia (davide.ravaglia3@studio.unibo.it)"

#%%

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

stats_of_bars = pd.read_csv('./random_walk/stats_of_bars.csv', sep=',', header=0, index_col='Unnamed: 0')

duration_high_low = pd.read_csv('./random_walk/duration_high_low.csv', sep=',', header=0, index_col='Unnamed: 0')

changes_of_theta = pd.read_csv('./random_walk/changes_of_theta.csv', sep=',', header=0, index_col='Unnamed: 0')

stats_of_bars = stats_of_bars.fillna(0)

entries_high = [0.0, 0.0, 0.0]
entries_low = [0.0, 0.0, 0.0]
entries_tot = [0.0, 0.0, 0.0]

cum_prob = pd.DataFrame(pd.DataFrame(index=range(0,len(stats_of_bars))))

prob_high = [0.0, 0.0, 0.0]
prob_low = [0.0, 0.0, 0.0]

counter_high_header = "counter (high)"
counter_low_header = "counter (low)"

prob_high_header = "prob (high)"
prob_low_header = "prob (low)"

for exp in range(0, 3) :

  if exp == 0 :
    drug = "- caf"
  if exp == 1 :
    drug = "- eth"
  if exp == 2 :
    drug = "- sug"

  high = "high "
  low = "low "

  cumulative_prob_high = 0.0
  cumulative_prob_low = 0.0
  cum_prob[high + drug] = np.nan
  cum_prob[low + drug] = np.nan

  high_header = prob_high_header + drug
  low_header = prob_low_header + drug
  
  for i in range(0, len(stats_of_bars)) :
    
    cumulative_prob_high += stats_of_bars[high_header][i]
    cum_prob[high + drug][i] = cumulative_prob_high
    
    cumulative_prob_low += stats_of_bars[low_header][i]
    cum_prob[low + drug][i] = cumulative_prob_low
  
  high_header = counter_high_header + drug
  low_header = counter_low_header + drug
  
  for i in range(0, len(stats_of_bars)) :
    
    entries_high[exp] += stats_of_bars[high_header][i]
    entries_low[exp] += stats_of_bars[low_header][i]
  
  entries_tot[exp] = entries_high[exp] + entries_low[exp]
  
  prob_low[exp] = entries_low[exp]/entries_tot[exp]
  prob_high[exp] = entries_high[exp]/entries_tot[exp]

concatenated = chain(range(1, 14), range(15, 16), range(17, 29), range(30, 33), range(34, 37), range(38, 40), range(41, 43), range(44, 48))
for seed in concatenated:

  random.seed(seed)

  badness = 0
  
  print(seed)
  
  timestep = 1/15
  number_of_exps = 3
  number_of_walks = 10
  interactions = 22000
  
  rndm_walks = pd.DataFrame(pd.DataFrame(index=range(0,interactions)))
  
  average_high = "average (high)"
  average_low = "average (low)"
  std_high = "std (high)"
  std_low = "std (low)"
  
  #   I define the half width of both the phi bar and the high and low
  #   duration bars. I will use them later to give a lil change to the value
  #   of the center of the bin that I choose
  half_width_of_phi_bar = np.abs(stats_of_bars["phi central"][1]-stats_of_bars["phi central"][0])/2
  half_width_of_durat_bar_high = np.abs(duration_high_low["durat central (high)"][1]-duration_high_low["durat central (high)"][0])/2
  half_width_of_durat_bar_low = np.abs(duration_high_low["durat central (low)"][1]-duration_high_low["durat central (low)"][0])/2
  
  for exp in range(0, number_of_exps) :
  
    if exp == 0 :
      drug = "- caf"
    if exp == 1 :
      drug = "- eth"
    if exp == 2 :
      drug = "- sug"
  
    for id in range(0, number_of_walks) :
  
      print(exp, id)
      #   I find a spot inside the circle where I can start
      for i in range(1, 100) :
      
        x_prev = random.uniform(-50.0, 50.0)
        y_prev = random.uniform(-50.0, 50.0)
        
        if math.pow(x_prev, 2) + math.pow(y_prev, 2) < 2500 : break
      
      #   I give a random orientation to the fly
      phi_prev = random.uniform(-math.pi, math.pi)
  
      header_x = str(exp) + " - " + str(id) + " x"
      header_y = str(exp) + " - " + str(id) + " y"
      header_phi = str(exp) + " - " + str(id) + " phi"
  
      rndm_walks[header_x] = np.nan
      rndm_walks[header_y] = np.nan
      rndm_walks[header_phi] = np.nan
      
  #    print("nan alle colonne: ",header_x, header_y, header_phi)
  
      rndm_walks[header_x][0] = x_prev
      rndm_walks[header_y][0] = y_prev
      rndm_walks[header_phi][0] = phi_prev
  
  #   Indicator which tells if we are in a high or low cycle
      high_1_low_0 = True
  #   Indicator which tells how many steps left are there to end the cycle.
      steps_left_for_cycle = 1
      
  #    print("0", "-1", rndm_walks[header_x][0], rndm_walks[header_y][0], rndm_walks[header_phi][0])
  
  #   The cycles high and low alternate, when is found that steps_left_for_cycle == 0
  #   The stats for the new cycle are extracted.
  
      for i in range(1, interactions) :
        
        steps_left_for_cycle -= 1
        
        if steps_left_for_cycle == 0 :
  
          high_1_low_0 = not high_1_low_0
          which_bin = random.uniform(0, 1)
  
          if high_1_low_0 :
            
            for j in range(0, len(duration_high_low)) :
    
              if duration_high_low["cumprob (high)" + drug][j] > which_bin :
  #   I actually don't extract between the mean and +- half width but
  #   from the mean to mean + 2*half width, otherwise I risk to choose a 0
  #   the first bin
                steps_left_for_cycle = int(random.uniform(duration_high_low["durat central (high)"][j], duration_high_low["durat central (high)"][j]+2*half_width_of_durat_bar_high)*15)
                break
  
          else :
            
            for j in range(0, len(duration_high_low)) :
    
              if duration_high_low["cumprob (low)" + drug][j] > which_bin :
  #   I actually don't extract between the mean and +- half width but
  #   from the mean to mean + 2*half width, otherwise I risk to choose a 0
  #   the first bin
                steps_left_for_cycle = int(random.uniform(duration_high_low["durat central (low)"][j], duration_high_low["durat central (low)"][j]+2*half_width_of_durat_bar_low)*15)
                break
  
        if high_1_low_0 :
  
          high = "high "
  #        print(high)
          average_header = average_high + drug
          std_header = std_high + drug
          cum_header = high + drug
  
  #   I extract a number to choose in which bin to go into
          which_bin = random.uniform(0, 1)
          
  #   I use the cumulative probability to choose the bin
          for j in range(0, len(cum_prob)) :
  
            if cum_prob[cum_header][j] > which_bin :
              instant_velocity = random.gauss(stats_of_bars[average_header][j], stats_of_bars[std_header][j])
              vel_dir_variation = random.uniform(stats_of_bars["phi central"][j]-half_width_of_phi_bar, stats_of_bars["phi central"][j]+half_width_of_phi_bar)
  
  #   A velocity < 0 changes the distribution of the angles
              if instant_velocity <= 0 : instant_velocity = 0.1
  #
  #            print("HIGH:\n  J=", j, "WB=", which_bin, "IV=", instant_velocity,"VDV=",vel_dir_variation)
  #
              rndm_walks[header_phi][i] = phi_prev + vel_dir_variation
  #   If phi < -pi or phi > pi add or subtract 2pi
              if rndm_walks[header_phi][i] < -math.pi :
                rndm_walks[header_phi][i] += 2*math.pi
              if rndm_walks[header_phi][i] > math.pi :
                rndm_walks[header_phi][i] -= 2*math.pi
              rndm_walks[header_x][i] = x_prev + instant_velocity*timestep*math.cos(rndm_walks[header_phi][i])
              rndm_walks[header_y][i] = y_prev + instant_velocity*timestep*math.sin(rndm_walks[header_phi][i])
  
              break
        
        else :
  
          low = "low "
          average_header = average_low + drug
          std_header = std_low + drug
          cum_header = low + drug
  
  #   I extract a number to choose in which bin to go into
          which_bin = random.uniform(0, 1)
          
  #   I use the cumulative probability to choose the bin
          for j in range(0, len(cum_prob)) :
            
            if cum_prob[cum_header][j] > which_bin :
              
              instant_velocity = random.gauss(stats_of_bars[average_header][j], stats_of_bars[std_header][j])
              vel_dir_variation_from_direction = random.uniform(stats_of_bars["phi central"][j]-half_width_of_phi_bar, stats_of_bars["phi central"][j]+half_width_of_phi_bar)
  
  #   A velocity < 0 changes the distribution of the angles
              if instant_velocity <= 0 : instant_velocity = 0.1
  #
  #            print("LOW:\n  J=", j, "WB=", which_bin, "IV=", instant_velocity,"VDV=",vel_dir_variation)
  #
              rndm_walks[header_phi][i] = phi_prev
              rndm_walks[header_x][i] = x_prev + instant_velocity*timestep*math.cos(vel_dir_variation_from_direction)
              rndm_walks[header_y][i] = y_prev + instant_velocity*timestep*math.sin(vel_dir_variation_from_direction)
              
              break
  
  #   If my point is out of the circle or radius 50
        if rndm_walks[header_x][i]*rndm_walks[header_x][i] + rndm_walks[header_y][i]*rndm_walks[header_y][i] > 2500 :
        
  #   I find the two intersection between the circle of radius 50 and the circle
  #   having the center my point on the previos iteration and radius the distance
  #   just traveled
          x_incr = rndm_walks[header_x][i]-rndm_walks[header_x][i-1]
          y_incr = rndm_walks[header_y][i]-rndm_walks[header_y][i-1]
          
          K = (2500 - x_incr*x_incr - y_incr*y_incr + y_prev*y_prev - x_prev*x_prev)/(2*y_prev)
          a = 1 + (x_prev*x_prev)/(y_prev*y_prev)
          beta = -(K+(x_prev*x_prev)/(y_prev))
          c = K*K - x_prev*x_prev*((x_incr*x_incr + y_incr*y_incr)/(y_prev*y_prev)-1)            
          
  #   I don't want it to crash but to just to skip to the next seed
  #   So when it encounters a badness, signal it and exit          
          if beta*beta - a*c < 0 :
            badness = 1
            print("beta = ", beta, "  a = ", a, "  c = ", c)
            print("beta*beta - a*c =", beta*beta - a*c)
            break

          y1 = (-beta + math.sqrt(beta*beta - a*c))/a
          y2 = (-beta - math.sqrt(beta*beta - a*c))/a

  #   I don't want it to crash but to just to skip to the next seed
  #   So when it encounters a badness, signal it and exit          
          if 2500 - y1*y1 < 0 :
            badness = 1
            print("y1 = ", y1)
            print("2500 - y1*y1", 2500 - y1*y1)
            break
          if 2500 - y2*y2 < 0 :
            badness = 1
            print("y2 = ", y2)
            print("2500 - y2*y2", 2500 - y2*y2)
            break
          
          x11 = math.sqrt(2500 - y1*y1)
          x12 = -x11
          x21 = math.sqrt(2500 - y2*y2)
          x22 = -x21
            
  #   Of x11 and x12 I choose the one closest to the starting point
          if min(math.hypot(x11 - x_prev, y1 - y_prev), math.hypot(x12 - x_prev, y1 - y_prev)) == math.hypot(x11 - x_prev, y1 - y_prev) :
            x1 = x11
            
          else :
            x1 = x12
  
  #   Of x21 and x22 I choose the one closest to the starting point
          if min(math.hypot(x21 - x_prev, y2 - y_prev), math.hypot(x22 - x_prev, y2 - y_prev)) == math.hypot(x21 - x_prev, y2 - y_prev) :
            x2 = x21
            
          else :
            x2 = x22
  
  #   Of x1,y1 and x2,y2, I choose the one closest to the point outside the circle
  #   This way I keep the orientation of movement
          if min(math.hypot(x1 - rndm_walks[header_x][i], y1 - rndm_walks[header_y][i]), math.hypot(x2 - rndm_walks[header_x][i], y2 - rndm_walks[header_y][i])) == math.hypot(x1 - rndm_walks[header_x][i], y1 - rndm_walks[header_y][i]) :
            rndm_walks[header_x][i] = x1
            rndm_walks[header_y][i] = y1
  #   I also need to change the direction I previosly assigned since it was
  #   based on a point out of the circle
            rndm_walks[header_phi][i] = np.arctan2(y1-y_prev, x1-x_prev)
  
            
          else :
            rndm_walks[header_x][i] = x2
            rndm_walks[header_y][i] = y2
  #   I also need to change the direction I previosly assigned since it was
  #   based on a point out of the circle
            rndm_walks[header_phi][i] = np.arctan2(y2-y_prev, x2-x_prev)
            
        if badness == 1 : break
  
        x_prev = rndm_walks[header_x][i]
        y_prev = rndm_walks[header_y][i]
        phi_prev = rndm_walks[header_phi][i]

      if badness == 1 : break

    if badness == 1 : break

#   I save the walk only if there were no badness
  if badness == 0 :
  
    path = './random_walk/many_walks/rndm_walks (seed=' + str(seed) + ').csv'
    rndm_walks.to_csv(path)


#   I graph one of the trails

header_x = "0 - 0 x"
header_y = "0 - 0 y"
hom_many_points = 22000
column_extraction = pd.DataFrame(pd.DataFrame(index=range(0,hom_many_points)))
column_extraction["x"] = rndm_walks[header_x]
column_extraction["y"] = rndm_walks[header_y]

plt.plot(column_extraction["x"], column_extraction["y"])
plt.xlabel("x (mm)")
plt.ylabel("y (mm)")
plt.tight_layout()
path = './Graphs/Trail ' + str(hom_many_points) + '__2.pdf'
plt.savefig(path)
plt.show()
plt.close()

