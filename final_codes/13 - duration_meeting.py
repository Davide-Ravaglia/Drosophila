# -*- coding: utf-8 -*-
#!/usr/bin/env python

import pandas as pd
import pylab as plt
import numpy as np
import math
from itertools import chain


__package__ = "Frequencies and PDFs of duration of meetings for both real data and toy model, divided by drugs"
__author__  = "Davide Ravaglia (davide.ravaglia3@studio.unibo.it)"

#%%

extraction_path = './network/stats_of_meeting_real.csv'
stats_of_meeting_real = pd.read_csv(extraction_path, sep=',', header=0, index_col='Unnamed: 0')


#   Hist of duration of meetings for the real data
numbins = 15
min_range = 0.5
max_range = 8

(n_real_eth, bins_eth, patches_eth) = plt.hist(stats_of_meeting_real["Time still tog. - eth"].fillna(-1), numbins, range=(min_range, max_range), color='g', alpha=0.6, label="Ethanol")
(n_real_sug, bins_sug, patches_sug) = plt.hist(stats_of_meeting_real["Time still tog. - sug"].fillna(-1), numbins, range=(min_range, max_range), color='r', alpha=0.6, label="Sugar")
(n_real_caf, bins_caf, patches_caf) = plt.hist(stats_of_meeting_real["Time still tog. - caf"].fillna(-1), numbins, range=(min_range, max_range), color='b', alpha=0.6, label="Caffeine")
plt.xlabel("Duration of meeting (s)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.legend()
plt.savefig('./Graphs/Duration of meeting (real).pdf')
plt.show()
plt.close()


#   I want to graph the duration of meeting, both real and fake
#   but for the fake meetings I want the average and std plotted


numbins = 15
min_range = 0.0
max_range = 8.0
(n_real_caf, bins_caf, patches_caf) = plt.hist(stats_of_meeting_real["Time still tog. - caf"], numbins, range=(min_range, max_range), color='b', alpha=0.6, label="Caffeine")
(n_real_eth, bins_eth, patches_eth) = plt.hist(stats_of_meeting_real["Time still tog. - eth"], numbins, range=(min_range, max_range), color='g', alpha=0.6, label="Ethanol")
(n_real_sug, bins_sug, patches_sug) = plt.hist(stats_of_meeting_real["Time still tog. - sug"], numbins, range=(min_range, max_range), color='r', alpha=0.6, label="Sugar")
plt.xlabel("Duration")
plt.ylabel("Frequency")
plt.tight_layout()
plt.legend()
plt.show()
plt.close()

#   I collect the info of all the hist of probability of meetings for
#   the fake data in one df.
bins_info = pd.DataFrame(pd.DataFrame(index=range(0,numbins)))

concatenated = chain(range(1, 14), range(15, 16), range(17, 29), range(30, 33), range(34, 37), range(38, 40), range(41, 43), range(44, 48))
for seed in concatenated:

  extraction_path = './network/many_stats_of_meeting_fake/stats_of_meeting_fake (seed=' + str(seed) + ').csv'
  stats_of_meeting_fake = pd.read_csv(extraction_path, sep=',', header=0, index_col='Unnamed: 0')

  bins_info["n_fake_caf (" + str(seed) + ")"] = np.nan
  bins_info["n_fake_eth (" + str(seed) + ")"] = np.nan
  bins_info["n_fake_sug (" + str(seed) + ")"] = np.nan
  bins_info["bins_caf (" + str(seed) + ")"] = np.nan
  bins_info["bins_eth (" + str(seed) + ")"] = np.nan
  bins_info["bins_sug (" + str(seed) + ")"] = np.nan
  bins_info["patches_caf (" + str(seed) + ")"] = np.nan
  bins_info["patches_eth (" + str(seed) + ")"] = np.nan
  bins_info["patches_sug (" + str(seed) + ")"] = np.nan
  
  (bins_info["n_fake_caf (" + str(seed) + ")"], bins_caf, c) = plt.hist(stats_of_meeting_fake["Time still tog. - caf"], numbins, range=(min_range, max_range), color='b', alpha=0.6, label="Caffeine")
  (bins_info["n_fake_eth (" + str(seed) + ")"], bins_eth, c) = plt.hist(stats_of_meeting_fake["Time still tog. - eth"], numbins, range=(min_range, max_range), color='g', alpha=0.6, label="Ethanol")
  (bins_info["n_fake_sug (" + str(seed) + ")"], bins_sug, c) = plt.hist(stats_of_meeting_fake["Time still tog. - sug"], numbins, range=(min_range, max_range), color='r', alpha=0.6, label="Sugar")
  #plt.xlabel("Probability")
  #plt.ylabel("Frequency")
  #plt.tight_layout()
  #plt.legend()
  #plt.savefig('./Graphs/Probability of meeting (fake).pdf')
  #plt.show()
  plt.close()

#   Now I compute the average for each bin of all the histograms saved before.
bins_info["average_caf"] = np.nan
bins_info["average_eth"] = np.nan
bins_info["average_sug"] = np.nan

concatenated = chain(range(1, 14), range(15, 16), range(17, 29), range(30, 33), range(34, 45))

for bin_number in range (0, numbins) :
  
  sum_caf = 0.0
  sum_eth = 0.0
  sum_sug = 0.0
  
  how_many_seed = 0
  
  concatenated = chain(range(1, 14), range(15, 16), range(17, 29), range(30, 33), range(34, 37), range(38, 40), range(41, 43), range(44, 48))
  for seed in concatenated:
    
    sum_caf += bins_info["n_fake_caf (" + str(seed) + ")"][bin_number]
    sum_eth += bins_info["n_fake_eth (" + str(seed) + ")"][bin_number]
    sum_sug += bins_info["n_fake_sug (" + str(seed) + ")"][bin_number]
    how_many_seed += 1
    
  bins_info["average_caf"][bin_number] = sum_caf/how_many_seed
  bins_info["average_eth"][bin_number] = sum_eth/how_many_seed
  bins_info["average_sug"][bin_number] = sum_sug/how_many_seed


#   Now I compute the std for each bin of all the histograms saved before.
bins_info["std_caf"] = np.nan
bins_info["std_eth"] = np.nan
bins_info["std_sug"] = np.nan

for bin_number in range (0, numbins) :
  
  square_diff_caf = 0.0
  square_diff_eth = 0.0
  square_diff_sug = 0.0
  
  how_many_seed = 0

  concatenated = chain(range(1, 14), range(15, 16), range(17, 29), range(30, 33), range(34, 37), range(38, 40), range(41, 43), range(44, 48))
  for seed in concatenated:
    
    square_diff_caf += math.pow(bins_info["n_fake_caf (" + str(seed) + ")"][bin_number] -  bins_info["average_caf"][bin_number], 2)
    square_diff_eth += math.pow(bins_info["n_fake_eth (" + str(seed) + ")"][bin_number] -  bins_info["average_eth"][bin_number], 2)
    square_diff_sug += math.pow(bins_info["n_fake_sug (" + str(seed) + ")"][bin_number] -  bins_info["average_sug"][bin_number], 2)
    how_many_seed += 1
    
  bins_info["std_caf"][bin_number] = math.sqrt(square_diff_caf/(how_many_seed-1))
  bins_info["std_eth"][bin_number] = math.sqrt(square_diff_eth/(how_many_seed-1))
  bins_info["std_sug"][bin_number] = math.sqrt(square_diff_sug/(how_many_seed-1))
  
center_of_bin = []
for i in range (0, numbins) :
  center_of_bin.append(bins_sug[i] + (bins_sug[1]-bins_sug[0])/2)



#   I plot the graph for caffeine

#   These are the real lines
plt.plot(center_of_bin, n_real_caf, color='b', marker='o', label="Caffeine (R)")

#   I use the legend here in order not to have the legend of the rndm walks
plt.legend()


#   These are the averages of the random walks
plt.plot(center_of_bin, bins_info["average_caf"], color='b', linestyle = ':', markersize=0, label="Caffeine (T)")

#   These are the borders of the band, maybe I coul put the light but not as
#   light as the fill
plt.plot(center_of_bin, (bins_info["average_caf"]+bins_info["std_caf"]), color='b', markersize=0, alpha = 0.5)
plt.plot(center_of_bin, (bins_info["average_caf"]-bins_info["std_caf"]), color='b', markersize=0, alpha = 0.5)

#   These is the filling
high = (bins_info["average_caf"] + bins_info["std_caf"])
low = (bins_info["average_caf"] - bins_info["std_caf"])
plt.fill_between(center_of_bin, high, low, facecolor='b', alpha=0.2)

plt.xlabel("Duration of encounters")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig('./Graphs/Duration of meeting (caff) (freq).pdf')
plt.show()
plt.close()



#   I plot the graph for ethanol

#   These are the real lines
plt.plot(center_of_bin, n_real_eth, color='g', marker='o', label="Ethanol (R)")

#   I use the legend here in order not to have the legend of the rndm walks
plt.legend()

#   These are the averages of the random walks
plt.plot(center_of_bin, bins_info["average_eth"], color='g', linestyle = ':', markersize=0, label="Ethanol (T)")

#   These are the borders of the band, maybe I coul put the light but not as
#   light as the fill
plt.plot(center_of_bin, (bins_info["average_eth"]+bins_info["std_eth"]), color='g', markersize=0, alpha = 0.5)
plt.plot(center_of_bin, (bins_info["average_eth"]-bins_info["std_eth"]), color='g', markersize=0, alpha = 0.5)

#   These is the filling
high = (bins_info["average_eth"] + bins_info["std_eth"])
low = (bins_info["average_eth"] - bins_info["std_eth"])
plt.fill_between(center_of_bin, high, low, facecolor='g', alpha=0.2)

plt.xlabel("Duration of encounters")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig('./Graphs/Duration of meeting (eth) (freq).pdf')
plt.show()
plt.close()



#   I plot the graph for sugar

#   These are the real lines
plt.plot(center_of_bin, n_real_sug, color='r', marker='o', label="Sugar (R)")

#   I use the legend here in order not to have the legend of the rndm walks
plt.legend()

#   These are the averages of the random walks
plt.plot(center_of_bin, bins_info["average_sug"], color='r', linestyle = ':', markersize=0, label="Sugar (T)")

#   These are the borders of the band, maybe I coul put the light but not as
#   light as the fill
plt.plot(center_of_bin, (bins_info["average_sug"]+bins_info["std_sug"]), color='r', markersize=0, alpha = 0.5)
plt.plot(center_of_bin, (bins_info["average_sug"]-bins_info["std_sug"]), color='r', markersize=0, alpha = 0.5)

#   These is the filling
high = (bins_info["average_sug"] + bins_info["std_sug"])
low = (bins_info["average_sug"] - bins_info["std_sug"])
plt.fill_between(center_of_bin, high, low, facecolor='r', alpha=0.2)

plt.xlabel("Duration of encounters")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig('./Graphs/Duration of meeting (sug) (freq).pdf')
plt.show()
plt.close()


#   I plot the graph for all of the drugs combined

#   These are the real lines
plt.plot(center_of_bin, n_real_caf, color='b', marker='o', label="Caffeine (R)")
plt.plot(center_of_bin, n_real_eth, color='g', marker='o', label="Ethanol (R)")
plt.plot(center_of_bin, n_real_sug, color='r', marker='o', label="Sugar (R)")

#   I use the legend here in order not to have the legend of the rndm walks
plt.legend()


#   These are the averages of the random walks
plt.plot(center_of_bin, bins_info["average_caf"], color='b', linestyle = ':', markersize=0, label="Caffeine (T)")
plt.plot(center_of_bin, bins_info["average_eth"], color='g', linestyle = ':', markersize=0, label="Ethanol (T)")
plt.plot(center_of_bin, bins_info["average_sug"], color='r', linestyle = ':', markersize=0, label="Sugar (T)")

#   These are the borders of the band, maybe I coul put the light but not as
#   light as the fill
plt.plot(center_of_bin, (bins_info["average_caf"]+bins_info["std_caf"]), color='b', markersize=0, alpha = 0.5)
plt.plot(center_of_bin, (bins_info["average_eth"]+bins_info["std_eth"]), color='g', markersize=0, alpha = 0.5)
plt.plot(center_of_bin, (bins_info["average_sug"]+bins_info["std_sug"]), color='r', markersize=0, alpha = 0.5)
plt.plot(center_of_bin, (bins_info["average_caf"]-bins_info["std_caf"]), color='b', markersize=0, alpha = 0.5)
plt.plot(center_of_bin, (bins_info["average_eth"]-bins_info["std_eth"]), color='g', markersize=0, alpha = 0.5)
plt.plot(center_of_bin, (bins_info["average_sug"]-bins_info["std_sug"]), color='r', markersize=0, alpha = 0.5)

#   These is the filling
high = (bins_info["average_caf"] + bins_info["std_caf"])
low = (bins_info["average_caf"] - bins_info["std_caf"])
plt.fill_between(center_of_bin, high, low, facecolor='b', alpha=0.2)

high = (bins_info["average_eth"] + bins_info["std_eth"])
low = (bins_info["average_eth"] - bins_info["std_eth"])
plt.fill_between(center_of_bin, high, low, facecolor='g', alpha=0.2)

high = (bins_info["average_sug"] + bins_info["std_sug"])
low = (bins_info["average_sug"] - bins_info["std_sug"])
plt.fill_between(center_of_bin, high, low, facecolor='r', alpha=0.2)

plt.xlabel("Duration of encounters")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig('./Graphs/Duration of meeting (all) (freq).pdf')
plt.show()
plt.close()



#   The same graphs as before but done with probability and not frequency  


center_of_bin = []
for i in range (0, numbins) :
  center_of_bin.append(bins_sug[i] + (bins_sug[1]-bins_sug[0])/2)



#   I plot the graph for caffeine

#   These are the real lines
plt.plot(center_of_bin, n_real_caf/n_real_caf.sum(), color='b', marker='o', label="Caffeine (R)")

#   I use the legend here in order not to have the legend of the rndm walks
plt.legend()

#   These are the averages of the random walks
plt.plot(center_of_bin, bins_info["average_caf"]/bins_info["average_caf"].sum(), color='b', linestyle = ':', markersize=0, label="Caffeine (T)")

#   These are the borders of the band, maybe I coul put the light but not as
#   light as the fill
plt.plot(center_of_bin, (bins_info["average_caf"]+bins_info["std_caf"])/bins_info["average_caf"].sum(), color='b', markersize=0, alpha = 0.5)
plt.plot(center_of_bin, (bins_info["average_caf"]-bins_info["std_caf"])/bins_info["average_caf"].sum(), color='b', markersize=0, alpha = 0.5)

#   These is the filling
high = (bins_info["average_caf"] + bins_info["std_caf"])/bins_info["average_caf"].sum()
low = (bins_info["average_caf"] - bins_info["std_caf"])/bins_info["average_caf"].sum()
plt.fill_between(center_of_bin, high, low, facecolor='b', alpha=0.2)

plt.xlabel("Duration of encounters")
plt.ylabel("Probability")
plt.ylim(0, 0.52)
plt.tight_layout()
plt.savefig('./Graphs/Duration of meeting (caf) (prob).pdf')
plt.show()
plt.close()




#   I plot the graph for ethanol

#   These are the real lines
plt.plot(center_of_bin, n_real_eth/n_real_eth.sum(), color='g', marker='o', label="Ethanol (R)")

#   I use the legend here in order not to have the legend of the rndm walks
plt.legend()

#   These are the averages of the random walks
plt.plot(center_of_bin, bins_info["average_eth"]/bins_info["average_eth"].sum(), color='g', linestyle = ':', markersize=0, label="Ethanol (T)")

#   These are the borders of the band, maybe I coul put the light but not as
#   light as the fill
plt.plot(center_of_bin, (bins_info["average_eth"]+bins_info["std_eth"])/bins_info["average_eth"].sum(), color='g', markersize=0, alpha = 0.5)
plt.plot(center_of_bin, (bins_info["average_eth"]-bins_info["std_eth"])/bins_info["average_eth"].sum(), color='g', markersize=0, alpha = 0.5)

#   These is the filling
high = (bins_info["average_eth"] + bins_info["std_eth"])/bins_info["average_eth"].sum()
low = (bins_info["average_eth"] - bins_info["std_eth"])/bins_info["average_eth"].sum()
plt.fill_between(center_of_bin, high, low, facecolor='g', alpha=0.2)

plt.xlabel("Duration of encounters")
plt.ylabel("Probability")
plt.ylim(0, 0.52)
plt.tight_layout()
plt.savefig('./Graphs/Duration of meeting (eth) (prob).pdf')
plt.show()
plt.close()




#   I plot the graph for sugar

#   These are the real lines
plt.plot(center_of_bin, n_real_sug/n_real_sug.sum(), color='r', marker='o', label="Sugar (R)")

#   I use the legend here in order not to have the legend of the rndm walks
plt.legend()

#   These are the averages of the random walks
plt.plot(center_of_bin, bins_info["average_sug"]/bins_info["average_sug"].sum(), color='r', linestyle = ':', markersize=0, label="Sugar (T)")

#   These are the borders of the band, maybe I coul put the light but not as
#   light as the fill
plt.plot(center_of_bin, (bins_info["average_sug"]+bins_info["std_sug"])/bins_info["average_sug"].sum(), color='r', markersize=0, alpha = 0.5)
plt.plot(center_of_bin, (bins_info["average_sug"]-bins_info["std_sug"])/bins_info["average_sug"].sum(), color='r', markersize=0, alpha = 0.5)

#   These is the filling
high = (bins_info["average_sug"] + bins_info["std_sug"])/bins_info["average_sug"].sum()
low = (bins_info["average_sug"] - bins_info["std_sug"])/bins_info["average_sug"].sum()
plt.fill_between(center_of_bin, high, low, facecolor='r', alpha=0.2)

plt.xlabel("Duration of encounters")
plt.ylabel("Probability")
plt.ylim(0, 0.52)
plt.tight_layout()
plt.savefig('./Graphs/Duration of meeting (sug) (prob).pdf')
plt.show()
plt.close()




#   I plot the graph for all of the drugs combined

#   These are the real lines
plt.plot(center_of_bin, n_real_caf/n_real_caf.sum(), color='b', marker='o', label="Caffeine (R)")
plt.plot(center_of_bin, n_real_eth/n_real_eth.sum(), color='g', marker='o', label="Ethanol (R)")
plt.plot(center_of_bin, n_real_sug/n_real_sug.sum(), color='r', marker='o', label="Sugar (R)")

#   I use the legend here in order not to have the legend of the rndm walks
plt.legend()


#   These are the averages of the random walks
plt.plot(center_of_bin, bins_info["average_caf"]/bins_info["average_caf"].sum(), color='b', linestyle = ':', markersize=0, label="Caffeine (T)")
plt.plot(center_of_bin, bins_info["average_eth"]/bins_info["average_eth"].sum(), color='g', linestyle = ':', markersize=0, label="Ethanol (T)")
plt.plot(center_of_bin, bins_info["average_sug"]/bins_info["average_sug"].sum(), color='r', linestyle = ':', markersize=0, label="Sugar (T)")

#   These are the borders of the band, maybe I coul put the light but not as
#   light as the fill
plt.plot(center_of_bin, (bins_info["average_caf"]+bins_info["std_caf"])/bins_info["average_caf"].sum(), color='b', markersize=0, alpha = 0.5)
plt.plot(center_of_bin, (bins_info["average_eth"]+bins_info["std_eth"])/bins_info["average_eth"].sum(), color='g', markersize=0, alpha = 0.5)
plt.plot(center_of_bin, (bins_info["average_sug"]+bins_info["std_sug"])/bins_info["average_sug"].sum(), color='r', markersize=0, alpha = 0.5)
plt.plot(center_of_bin, (bins_info["average_caf"]-bins_info["std_caf"])/bins_info["average_caf"].sum(), color='b', markersize=0, alpha = 0.5)
plt.plot(center_of_bin, (bins_info["average_eth"]-bins_info["std_eth"])/bins_info["average_eth"].sum(), color='g', markersize=0, alpha = 0.5)
plt.plot(center_of_bin, (bins_info["average_sug"]-bins_info["std_sug"])/bins_info["average_sug"].sum(), color='r', markersize=0, alpha = 0.5)

#   These is the filling
high = (bins_info["average_caf"] + bins_info["std_caf"])/bins_info["average_caf"].sum()
low = (bins_info["average_caf"] - bins_info["std_caf"])/bins_info["average_caf"].sum()
plt.fill_between(center_of_bin, high, low, facecolor='b', alpha=0.2)

high = (bins_info["average_eth"] + bins_info["std_eth"])/bins_info["average_eth"].sum()
low = (bins_info["average_eth"] - bins_info["std_eth"])/bins_info["average_eth"].sum()
plt.fill_between(center_of_bin, high, low, facecolor='g', alpha=0.2)

high = (bins_info["average_sug"] + bins_info["std_sug"])/bins_info["average_sug"].sum()
low = (bins_info["average_sug"] - bins_info["std_sug"])/bins_info["average_sug"].sum()
plt.fill_between(center_of_bin, high, low, facecolor='r', alpha=0.2)

plt.xlabel("Duration of encounters")
plt.ylabel("Probability")
plt.ylim(0, 0.52)
plt.tight_layout()
plt.savefig('./Graphs/Duration of meeting (all) (prob).pdf')
plt.show()
plt.close()
