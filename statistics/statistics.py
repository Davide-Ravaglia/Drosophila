# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import pandas as pd
import pylab as plt
import numpy as np


__package__ = "First look at the data: distance and velocity"
__author__  = "Davide Ravaglia (davide.ravaglia3@studio.unibo.it)"


def statistics(data_name, exp_number=2, id_number=1):
  """
  A first look at the statistics of the Drosophila.
  
  Parameters
  ----------
  data_name : string
        Name of the file in which are the data.
  exp_number : integer
        From 0 to 2, which corrensponds to the different drugs: caffeine, ethanol, sugar.
  id_number : integer
        From 1 to 10, Id of the fly which will be used for graph 6 and 7.
  
  Returns
  -------
  Creates a folder named 'Graphs' (note that it will crash if a folder with
  this name already exists).
  Inside it will place 7 graphs:
  1.'Average_Speed.pdf': average speed of the different Drosophila
    during the whole experiment, divided by drugs.
  2,3,4.'Average_Speed_Timestep_"Drug".pdf': average speed of the different
    Drosophila during the whole experiment for timestep chosen; divided
    in 3 graphs with different name ("Drug" changes).
  5.'Instant_Speed.pdf': instant speed between consecutive shots for all
    of the Drosophila during the whole experiment, divided by drugs.
  6.'Trail.pdf': trail followed by the chosen Drosophila in the arena during
    the whole experiment.
  7.'Correlation_Phi_Theta.pdf': points with coordinates the angle which the
    Drosophila faces and the angle which determines its position in the arena.
  """

  if(os.path.isdir('./Graphs')):
    print('Folder already existing. The program will substitute existing files')
  else:
    os.mkdir("Graphs")
    print('Creating folder "Graphs"')

  data = pd.read_csv(data_name, sep=',', header=0, usecols=['exp', 'id', 'theta', 'timestamps', 'x_mm', 'y_mm', 'phi', 'velmag_ctr'])
  
  #Sostituisco 1 con 01... in modo che l'id 10 risulti in ordine dopo la 9
  #Necessario solo per la exp_1 in quanto le altre hanno nome fly#_205_1
  data['id'] = data['id'].replace('fly#_1_1', 'fly#_01_1')
  data['id'] = data['id'].replace('fly#_2_1', 'fly#_02_1')
  data['id'] = data['id'].replace('fly#_3_1', 'fly#_03_1')
  data['id'] = data['id'].replace('fly#_4_1', 'fly#_04_1')
  data['id'] = data['id'].replace('fly#_5_1', 'fly#_05_1')
  data['id'] = data['id'].replace('fly#_6_1', 'fly#_06_1')
  data['id'] = data['id'].replace('fly#_7_1', 'fly#_07_1')
  data['id'] = data['id'].replace('fly#_8_1', 'fly#_08_1')
  data['id'] = data['id'].replace('fly#_9_1', 'fly#_09_1')
  
  #Ora posso ordinare il file
  data = data.sort_values(['exp', 'id', 'timestamps'])
  
  #Velocità medie delle Drosophila per le 3 diverse droghe
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
  plt.title('Average Speed for All Drosophila and All Drugs')
  plt.xlabel('Drosophila')
  plt.ylabel('Average Speed (mm/s)')
  plt.xticks(np.arange(1, len(dros_number)+1, step=1))
  plt.savefig('./Graphs/Average_Speed.pdf')
  plt.show()
  plt.close()
  
  #Velocità medie per un certo intervallo di tempo di tutte le Drosophila
  #In grafici distinti per tipo di droga
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
      title_chosen='Average Speed for Different Minutues (Drug:Caffeine)'
      drug_name='_Caffeine'
    if exp=='exp_101' :
      title_chosen='Average Speed for Different Minutues (Drug:Ethanol)'
      drug_name='_Ethanol'
    if exp=='exp_201' :
      title_chosen='Average Speed for Different Minutues (Drug:Sugar)'
      drug_name='_Sugar'
    path = './Graphs/Average_Speed_Timestep.pdf'
    newpath = path[:31] + drug_name + path[31:]
    plt.title(title_chosen)
    plt.xlabel('Minute')
    plt.ylabel('Speed (mm/s)')
    plt.xticks(np.arange(0, (len(time)-1)*seconds_for_step/60+1, step=int(len(time)*seconds_for_step/60/5)-1))
    plt.savefig(newpath)
    plt.show()
    plt.close()
  
  #Velocità istantanee per tutte le Drosophila
  #In grafici distinti per tipo di droga
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
    y, x, _ = plt.hist(data_exp.velmag_ctr, numbins, range = (0, 40), color=color_chosen, label=legend_chosen, alpha=0.8)
    plt.title('Instant Speed for All Drosophila and All Drugs')
    plt.xlabel('Speed (mm/s)')
    plt.ylabel('Frequency')
    max_bin_content = y[int(numbins/8):numbins].max()
    plt.ylim((0,max_bin_content*1.2))
  plt.legend()
  plt.savefig('./Graphs/Instant_Speed.pdf')
  plt.show()
  plt.close()

  #Selezione dei dati in base ai parametri di ingresso di ID e EXP
  list_of_exp = data['exp'].unique()
  code_exp = list_of_exp[exp_number]
  data_exp = data.loc[min(data.index[data['exp'] == code_exp]):max(data.index[data['exp'] == code_exp])]
  list_of_id = data_exp['id'].unique()
  code_id = list_of_id[id_number]
  data_id = data_exp.loc[min(data_exp.index[data_exp['id'] == code_id]):max(data_exp.index[data_exp['id'] == code_id])]

  #Velocità medie per un certo intervallo di tempo di una Drosophila
  #Per un solo tipo di droga
  #Commentato in quanto abbastanza ridondante
  
  #  seconds_for_step = 60
  #  timestep = (data['timestamps']/seconds_for_step).astype(int)
  #  data['timestep'] = timestep
  #  IndexSeries = list(range(0, len(data.timestep.unique())))
  #  
  #  groupby_timestep = data_id['velmag_ctr'].groupby(data_id['timestep'])
  #  av_by_timestep = groupby_timestep.mean().to_frame().set_index(pd.Index(IndexSeries))
  #  av_by_timestep['timestep'] = IndexSeries
  #  
  #  time = av_by_timestep.as_matrix(columns=av_by_timestep.columns[1:2])
  #  time = time*seconds_for_step/60
  #  vel_timestep = av_by_timestep.as_matrix(columns=av_by_timestep.columns[0:1])
  #  
  #  plt.plot(time, vel_timestep)
  #  
  #  
  #  plt.title('Average Speed for different minutes')
  #  plt.xlabel('Minute')
  #  plt.ylabel('Speed (mm/s)')
  #  plt.xticks(np.arange(0, (len(time)-1)*seconds_for_step/60+1, step=int(len(time)*seconds_for_step/60/6)))
  #  #plt.savefig('./Graphs/Average_Speed_Minute.pdf
  #  plt.close()
  
  #Percorso seguito da una Drosophila durante un esperimento
  plt.plot(data_id.x_mm, data_id.y_mm)
  plt.title('Plot of x_mm and y_mm')
  plt.xlabel('x (mm)')
  plt.ylabel('y (mm)')
  plt.savefig('./Graphs/Trail.pdf')
  plt.show()
  plt.close()

  #Correlazione tra l'angolo che forma con l'asse y e la direzione della
  #Drosophila con l'angolo che ne determina la posizione nell'arena
  #(0° sull'asse x negativo)
  plt.plot(data_id.phi, data_id.theta, 'ro', markersize=1)
  plt.title('Correlation between Phi and Theta')
  plt.xlabel('Phi (rad)')
  plt.ylabel('Theta (rad)')
  plt.savefig('./Graphs/Correlation_Phi_Theta.pdf')
  plt.show()
  plt.close()

if __name__ == '__main__':
  
  data_name = 'data_original.csv'
  exp_number=0
  id_number=9
  
  statistics(data_name, exp_number, id_number)
