# -*- coding: utf-8 -*-
#!/usr/bin/env python

import pandas as pd
import pylab as plt
import numpy as np
import scipy
import math
from itertools import chain


__package__ = "Compute and graph the PDFs of the p-values of the meeting combinations both for the real data and the toy model, divided by drugs"
__author__  = "Davide Ravaglia (davide.ravaglia3@studio.unibo.it)"

plt.rcParams.update({'font.size': 15,
                    'xtick.major.size': 4,
                    'xtick.major.width': 2,
                    'ytick.major.size': 4,
                    'ytick.major.width': 2,
                    'axes.linewidth': 1.5})


#%%

stats_of_meeting_real = pd.read_csv('./network/stats_of_meeting_real.csv', sep=',', header=0, index_col='Unnamed: 0')
  
#   Here I compute the probability that the fly #N meets teh fly #M a
#   certain number of times
probability_of_meeting = pd.DataFrame(pd.DataFrame(index=range(0,45)))

#   FOR THE REAL DATA

data_chosen = stats_of_meeting_real
real_or_fake = " real"

for exp in range (0, 3) :

  j=0

  if exp == 0 :
    drug = " caf"
  if exp == 1 :
    drug = " eth"
  if exp == 2 :
    drug = " sug"
  
  probability_of_meeting["Id 1 -" + drug + real_or_fake] = 0
  probability_of_meeting["Id 2 -" + drug + real_or_fake] = 0
  probability_of_meeting["Occurences -" + drug + real_or_fake] = 0
  probability_of_meeting["Probability Id 1 -" + drug + real_or_fake] = 0.0
  probability_of_meeting["Probability Id 2 -" + drug + real_or_fake] = 0.0
  
  header_id_1 = "Id 1 -" + drug
  header_id_2 = "Id 2 -" + drug
  
#   I write for every possibile couple of Drosophila, the number of times they met
  for id_1 in range (1, 11):
    
    for id_2 in range (id_1+1, 11):

      probability_of_meeting["Id 1 -" + drug + real_or_fake][j] = id_1
      probability_of_meeting["Id 2 -" + drug + real_or_fake][j] = id_2
      
      print(j, id_1, id_2, drug, real_or_fake)
      
      for i in range (0, len(data_chosen)) :
        
        if ((data_chosen[header_id_1][i] == id_1 and data_chosen[header_id_2][i] == id_2) or
          (data_chosen[header_id_1][i] == id_2 and data_chosen[header_id_2][i] == id_1)):
          
          probability_of_meeting["Occurences -" + drug + real_or_fake][j] += 1
            
      j+=1

#   Now I sum all of the meetings the Dros id_1 did
    total_meetings_of_id_1 = 0
    for l in range (0, j):
      
      if (probability_of_meeting["Id 1 -" + drug + real_or_fake][l] == id_1 or
          probability_of_meeting["Id 2 -" + drug + real_or_fake][l] == id_1) :
        
        total_meetings_of_id_1 += probability_of_meeting["Occurences -" + drug + real_or_fake][l]

#      print(total_meetings_of_id_1)

#   Now I compute the probability as 1- (2*abs(difference between the cdf and 0.5))
    for l in range (0, j):

      if probability_of_meeting["Id 1 -" + drug + real_or_fake][l] == id_1 :
        probability_of_meeting["Probability Id 1 -" + drug + real_or_fake][l] = 1 - np.abs((0.5 - scipy.stats.binom.cdf(probability_of_meeting["Occurences -" + drug + real_or_fake][l], total_meetings_of_id_1, 1/9)) * 2)

      if probability_of_meeting["Id 2 -" + drug + real_or_fake][l] == id_1 :
        probability_of_meeting["Probability Id 2 -" + drug + real_or_fake][l] = 1 - np.abs((0.5 - scipy.stats.binom.cdf(probability_of_meeting["Occurences -" + drug + real_or_fake][l], total_meetings_of_id_1, 1/9)) * 2)


#   FOR THE RANDOM WALKS
concatenated = chain(range(1, 14), range(15, 16), range(17, 29), range(30, 33), range(34, 37), range(38, 40), range(41, 43), range(44, 48))
for seed in concatenated:

  path = './network/many_stats_of_meeting_fake/stats_of_meeting_fake (seed=' + str(seed) + ').csv'
  
  stats_of_meeting_fake = pd.read_csv(path, sep=',', header=0, index_col='Unnamed: 0')

  data_chosen = stats_of_meeting_fake
  real_or_fake = " fake (" + str(seed) + ")"
  
  for exp in range (0, 3) :

    j=0

    if exp == 0 :
      drug = " caf"
    if exp == 1 :
      drug = " eth"
    if exp == 2 :
      drug = " sug"
    
    probability_of_meeting["Id 1 -" + drug + real_or_fake] = 0
    probability_of_meeting["Id 2 -" + drug + real_or_fake] = 0
    probability_of_meeting["Occurences -" + drug + real_or_fake] = 0
    probability_of_meeting["Probability Id 1 -" + drug + real_or_fake] = 0.0
    probability_of_meeting["Probability Id 2 -" + drug + real_or_fake] = 0.0
    
    header_id_1 = "Id 1 -" + drug
    header_id_2 = "Id 2 -" + drug
    
#   I write for every possibile couple of Drosophila, the number of times they met
    for id_1 in range (1, 11):
      
      for id_2 in range (id_1+1, 11):

        probability_of_meeting["Id 1 -" + drug + real_or_fake][j] = id_1
        probability_of_meeting["Id 2 -" + drug + real_or_fake][j] = id_2
        
        print(j, id_1, id_2, drug, real_or_fake)
        
        for i in range (0, len(data_chosen)) :
          
          if ((data_chosen[header_id_1][i] == id_1 and data_chosen[header_id_2][i] == id_2) or
            (data_chosen[header_id_1][i] == id_2 and data_chosen[header_id_2][i] == id_1)):
            
            probability_of_meeting["Occurences -" + drug + real_or_fake][j] += 1
              
        j+=1

#   Now I sum all of the meetings the Dros id_1 did
      total_meetings_of_id_1 = 0
      for l in range (0, j):
        
        if (probability_of_meeting["Id 1 -" + drug + real_or_fake][l] == id_1 or
            probability_of_meeting["Id 2 -" + drug + real_or_fake][l] == id_1) :
          
          total_meetings_of_id_1 += probability_of_meeting["Occurences -" + drug + real_or_fake][l]

#      print(total_meetings_of_id_1)

#   Now I compute the probability as 1- (2*abs(difference between the cdf and 0.5))
      for l in range (0, j):

        if probability_of_meeting["Id 1 -" + drug + real_or_fake][l] == id_1 :
          probability_of_meeting["Probability Id 1 -" + drug + real_or_fake][l] = 1 - np.abs((0.5 - scipy.stats.binom.cdf(probability_of_meeting["Occurences -" + drug + real_or_fake][l], total_meetings_of_id_1, 1/9)) * 2)

        if probability_of_meeting["Id 2 -" + drug + real_or_fake][l] == id_1 :
          probability_of_meeting["Probability Id 2 -" + drug + real_or_fake][l] = 1 - np.abs((0.5 - scipy.stats.binom.cdf(probability_of_meeting["Occurences -" + drug + real_or_fake][l], total_meetings_of_id_1, 1/9)) * 2)


probability_of_meeting.to_csv('./network/probability_of_meeting.csv')


probability_of_meeting = pd.read_csv('./network/probability_of_meeting.csv', sep=',', header=0, index_col='Unnamed: 0')


#   Hist of probability of meetings for the real data
numbins = 20
min_range = 0.0
max_range = 1.0
(n_real_caf, bins_caf, patches_caf) = plt.hist(pd.concat([probability_of_meeting["Probability Id 1 - caf real"], probability_of_meeting["Probability Id 2 - caf real"]]), numbins, range=(min_range, max_range), color='b', alpha=0.6, label="Caffeine")
(n_real_eth, bins_eth, patches_eth) = plt.hist(pd.concat([probability_of_meeting["Probability Id 1 - eth real"], probability_of_meeting["Probability Id 2 - eth real"]]), numbins, range=(min_range, max_range), color='g', alpha=0.6, label="Ethanol")
(n_real_sug, bins_sug, patches_sug) = plt.hist(pd.concat([probability_of_meeting["Probability Id 1 - sug real"], probability_of_meeting["Probability Id 2 - sug real"]]), numbins, range=(min_range, max_range), color='r', alpha=0.6, label="Sugar")
plt.xlabel("Probability")
plt.ylabel("Frequency")
plt.tight_layout()
plt.legend()
#plt.savefig('./Graphs/Probability of meeting (real).pdf')
plt.show()
plt.close()

#   I collect the info of all the hist of probability of meetings for
#   the fake data in one df.
bins_info = pd.DataFrame(pd.DataFrame(index=range(0,numbins)))

concatenated = chain(range(1, 14), range(15, 16), range(17, 29), range(30, 33), range(34, 37), range(38, 40), range(41, 43), range(44, 48))
for seed in concatenated:
  
  bins_info["n_fake_caf (" + str(seed) + ")"] = np.nan
  bins_info["n_fake_eth (" + str(seed) + ")"] = np.nan
  bins_info["n_fake_sug (" + str(seed) + ")"] = np.nan
  
  (bins_info["n_fake_caf (" + str(seed) + ")"], bins_caf, c) = plt.hist(pd.concat([probability_of_meeting["Probability Id 1 - caf fake" + " (" + str(seed) + ")"], probability_of_meeting["Probability Id 2 - caf fake" + " (" + str(seed) + ")"]]), numbins, range=(min_range, max_range), color='b', alpha=0.6, label="Caffeine")
  (bins_info["n_fake_eth (" + str(seed) + ")"], bins_sug, c) = plt.hist(pd.concat([probability_of_meeting["Probability Id 1 - eth fake" + " (" + str(seed) + ")"], probability_of_meeting["Probability Id 2 - eth fake" + " (" + str(seed) + ")"]]), numbins, range=(min_range, max_range), color='g', alpha=0.6, label="Ethanol")
  (bins_info["n_fake_sug (" + str(seed) + ")"], bins_eth, c) = plt.hist(pd.concat([probability_of_meeting["Probability Id 1 - sug fake" + " (" + str(seed) + ")"], probability_of_meeting["Probability Id 2 - sug fake" + " (" + str(seed) + ")"]]), numbins, range=(min_range, max_range), color='r', alpha=0.6, label="Sugar")

  plt.close()

#   Now I compute the average for each bin of all the histograms saved before.
bins_info["average_caf"] = np.nan
bins_info["average_eth"] = np.nan
bins_info["average_sug"] = np.nan

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
  center_of_bin.append(bins_caf[i] + (bins_caf[1]-bins_caf[0])/2)


#   I graph the PDF of p-value of the meeting combinations for caffeine

#   These are the real lines
plt.plot(center_of_bin, n_real_caf/90, color='b', marker='o', label="Caffeine (R)")

#   I use the legend here in order not to have the legend of the rndm walks
plt.legend()

#   These are the averages of the random walks
plt.plot(center_of_bin, bins_info["average_caf"]/90, color='b', linestyle = ':', markersize=0, label="Caffeine (T)")

#   These are the borders of the band, maybe I coul put the light but not as
#   light as the fill
plt.plot(center_of_bin, (bins_info["average_caf"]+bins_info["std_caf"])/90, color='b', markersize=0, alpha = 0.5)
plt.plot(center_of_bin, (bins_info["average_caf"]-bins_info["std_caf"])/90, color='b', markersize=0, alpha = 0.5)


#   These is the filling
high = (bins_info["average_caf"] + bins_info["std_caf"])/90
low = (bins_info["average_caf"] - bins_info["std_caf"])/90
plt.fill_between(center_of_bin, high, low, facecolor='b', alpha=0.2)

plt.xlabel("P-value of encounter")
plt.ylabel("Probability")
#   ylim for 15 bins
#plt.ylim(0, 0.28)
#   ylim for 10 bins
plt.ylim(0, 0.31)
plt.tight_layout()
plt.savefig('./Graphs/Probability of meeting (caf).pdf')
plt.show()
plt.close()




#   I graph the PDF of p-value of the meeting combinations for ethanol

#   These are the real lines
plt.plot(center_of_bin, n_real_eth/90, color='g', marker='o', label="Ethanol (R)")

#   I use the legend here in order not to have the legend of the rndm walks
plt.legend()

#   These are the averages of the random walks
plt.plot(center_of_bin, bins_info["average_eth"]/90, color='g', linestyle = ':', markersize=0, label="Ethanol (T)")

#   These are the borders of the band, maybe I coul put the light but not as
#   light as the fill
plt.plot(center_of_bin, (bins_info["average_eth"]+bins_info["std_eth"])/90, color='g', markersize=0, alpha = 0.5)
plt.plot(center_of_bin, (bins_info["average_eth"]-bins_info["std_eth"])/90, color='g', markersize=0, alpha = 0.5)

#   These is the filling
high = (bins_info["average_eth"] + bins_info["std_eth"])/90
low = (bins_info["average_eth"] - bins_info["std_eth"])/90
plt.fill_between(center_of_bin, high, low, facecolor='g', alpha=0.2)

plt.xlabel("P-value of encounter")
plt.ylabel("Probability")
#   ylim for 15 bins
#plt.ylim(0, 0.28)
#   ylim for 10 bins
plt.ylim(0, 0.31)
plt.tight_layout()
plt.savefig('./Graphs/Probability of meeting (eth).pdf')
plt.show()
plt.close()




#   I graph the PDF of p-value of the meeting combinations for sugar

#   These are the real lines
plt.plot(center_of_bin, n_real_sug/90, color='r', marker='o', label="Sugar (R)")

#   I use the legend here in order not to have the legend of the rndm walks
plt.legend()

#   These are the averages of the random walks
plt.plot(center_of_bin, bins_info["average_sug"]/90, color='r', linestyle = ':', markersize=0, label="Sugar (T)")

#   These are the borders of the band, maybe I coul put the light but not as
#   light as the fill
plt.plot(center_of_bin, (bins_info["average_sug"]+bins_info["std_sug"])/90, color='r', markersize=0, alpha = 0.5)
plt.plot(center_of_bin, (bins_info["average_sug"]-bins_info["std_sug"])/90, color='r', markersize=0, alpha = 0.5)

#   These is the filling
high = (bins_info["average_sug"] + bins_info["std_sug"])/90
low = (bins_info["average_sug"] - bins_info["std_sug"])/90
plt.fill_between(center_of_bin, high, low, facecolor='r', alpha=0.2)

plt.xlabel("P-value of encounter")
plt.ylabel("Probability")
#   ylim for 15 bins
#plt.ylim(0, 0.28)
#   ylim for 10 bins
plt.ylim(0, 0.31)
plt.tight_layout()
plt.savefig('./Graphs/Probability of meeting (sug).pdf')
plt.show()
plt.close()




#   I graph the PDF of p-value of the meeting combinations for all the drugs

#   These are the real lines
plt.plot(center_of_bin, n_real_caf/90, color='b', marker='o', label="Caffeine (R)")
plt.plot(center_of_bin, n_real_eth/90, color='g', marker='o', label="Ethanol (R)")
plt.plot(center_of_bin, n_real_sug/90, color='r', marker='o', label="Sugar (R)")

#   I use the legend here in order not to have the legend of the rndm walks
plt.legend()

#   These are the averages of the random walks
plt.plot(center_of_bin, bins_info["average_caf"]/90, color='b', linestyle = ':', markersize=0, label="Caffeine (T)")
plt.plot(center_of_bin, bins_info["average_eth"]/90, color='g', linestyle = ':', markersize=0, label="Ethanol (T)")
plt.plot(center_of_bin, bins_info["average_sug"]/90, color='r', linestyle = ':', markersize=0, label="Sugar (T)")

#   These are the borders of the band, maybe I coul put the light but not as
#   light as the fill
plt.plot(center_of_bin, (bins_info["average_caf"]+bins_info["std_caf"])/90, color='b', markersize=0, alpha = 0.5)
plt.plot(center_of_bin, (bins_info["average_eth"]+bins_info["std_eth"])/90, color='g', markersize=0, alpha = 0.5)
plt.plot(center_of_bin, (bins_info["average_sug"]+bins_info["std_sug"])/90, color='r', markersize=0, alpha = 0.5)
plt.plot(center_of_bin, (bins_info["average_caf"]-bins_info["std_caf"])/90, color='b', markersize=0, alpha = 0.5)
plt.plot(center_of_bin, (bins_info["average_eth"]-bins_info["std_eth"])/90, color='g', markersize=0, alpha = 0.5)
plt.plot(center_of_bin, (bins_info["average_sug"]-bins_info["std_sug"])/90, color='r', markersize=0, alpha = 0.5)


#   These is the filling
high = (bins_info["average_caf"] + bins_info["std_caf"])/90
low = (bins_info["average_caf"] - bins_info["std_caf"])/90
plt.fill_between(center_of_bin, high, low, facecolor='b', alpha=0.2)

high = (bins_info["average_eth"] + bins_info["std_eth"])/90
low = (bins_info["average_eth"] - bins_info["std_eth"])/90
plt.fill_between(center_of_bin, high, low, facecolor='g', alpha=0.2)

high = (bins_info["average_sug"] + bins_info["std_sug"])/90
low = (bins_info["average_sug"] - bins_info["std_sug"])/90
plt.fill_between(center_of_bin, high, low, facecolor='r', alpha=0.2)

plt.xlabel("P-value of encounter")
plt.ylabel("Probability")
#   ylim for 15 bins
#plt.ylim(0, 0.28)
#   ylim for 10 bins
plt.ylim(0, 0.31)
plt.tight_layout()
plt.savefig('./Graphs/Probability of meeting (all).pdf')
plt.show()
plt.close()




#   Here I graph the cumulative probability of the probability distribution
cumprobs = pd.DataFrame(pd.DataFrame(index=range(0, numbins)))

#   First I make two columns with the central value for each bin
cumprobs["central"] = np.nan

for i in range (0, numbins) :
  cumprobs["central"][i] = max_range/numbins*i + max_range/(2*numbins)
  
#   Then for each bin, each drug and high and low I compute the probability
#   and the cumulative probability

#   Real part
cumprobs["prob (real) - caf"] = n_real_caf/n_real_caf.sum()
cumprobs["cumprob (real) - caf"] = np.nan
cumulative_prob = 0.0

for i in range (0, numbins) :
  cumulative_prob += cumprobs["prob (real) - caf"][i]
  cumprobs["cumprob (real) - caf"][i] = cumulative_prob

cumprobs["prob (real) - eth"] = n_real_eth/n_real_eth.sum()
cumprobs["cumprob (real) - eth"] = np.nan
cumulative_prob = 0.0

for i in range (0, numbins) :
  cumulative_prob += cumprobs["prob (real) - eth"][i]
  cumprobs["cumprob (real) - eth"][i] = cumulative_prob

cumprobs["prob (real) - sug"] = n_real_sug/n_real_sug.sum()
cumprobs["cumprob (real) - sug"] = np.nan
cumulative_prob = 0.0

for i in range (0, numbins) :
  cumulative_prob += cumprobs["prob (real) - sug"][i]
  cumprobs["cumprob (real) - sug"][i] = cumulative_prob

#   Fake part
cumprobs["prob (fake) - caf"] = bins_info["average_caf"]/bins_info["average_caf"].sum()
cumprobs["cumprob (fake) - caf"] = np.nan
cumulative_prob = 0.0

for i in range (0, numbins) :
  cumulative_prob += cumprobs["prob (fake) - caf"][i]
  cumprobs["cumprob (fake) - caf"][i] = cumulative_prob

cumprobs["prob (fake) - eth"] = bins_info["average_eth"]/bins_info["average_eth"].sum()
cumprobs["cumprob (fake) - eth"] = np.nan
cumulative_prob = 0.0

for i in range (0, numbins) :
  cumulative_prob += cumprobs["prob (fake) - eth"][i]
  cumprobs["cumprob (fake) - eth"][i] = cumulative_prob

cumprobs["prob (fake) - sug"] = bins_info["average_sug"]/bins_info["average_sug"].sum()
cumprobs["cumprob (fake) - sug"] = np.nan
cumulative_prob = 0.0

for i in range (0, numbins) :
  cumulative_prob += cumprobs["prob (fake) - sug"][i]
  cumprobs["cumprob (fake) - sug"][i] = cumulative_prob

#   I add a row on top full of 0.0 to make the cumprob graph start from (0, 0)
new_row = pd.DataFrame({'central':0.0,
                        'prob (real) - caf':0.0, 'cumprob (real) - caf':0.0,
                        'prob (real) - eth':0.0, 'cumprob (real) - eth':0.0,
                        'prob (real) - sug':0.0, 'cumprob (real) - sug':0.0,
                        'prob (fake) - caf':0.0, 'cumprob (fake) - caf':0.0,
                        'prob (fake) - eth':0.0, 'cumprob (fake) - eth':0.0,
                        'prob (fake) - sug':0.0, 'cumprob (fake) - sug':0.0},
                                                            index =[0]) 

# simply concatenate both dataframes 
cumprobs = pd.concat([new_row, cumprobs]).reset_index(drop = True)

plt.plot(cumprobs["central"], cumprobs["cumprob (real) - caf"], color='b', label="Caffeine (R)")
plt.plot(cumprobs["central"], cumprobs["cumprob (real) - eth"], color='g', label="Ethanol (R)")
plt.plot(cumprobs["central"], cumprobs["cumprob (real) - sug"], color='r', label="Sugar (R)")
#   I use the legend here in order not to have the legend of the rndm walks
plt.legend()
plt.plot(cumprobs["central"], cumprobs["cumprob (fake) - caf"], color='b', mfc='none', linestyle=":", label="Caffeine (T)")
plt.plot(cumprobs["central"], cumprobs["cumprob (fake) - eth"], color='g', mfc='none', linestyle=":", label="Ethanol (T)")
plt.plot(cumprobs["central"], cumprobs["cumprob (fake) - sug"], color='r', mfc='none', linestyle=":", label="Sugar (T)")
plt.xlabel("Probability of encounters")
plt.ylabel("Cumulative Probability")
plt.tight_layout()
plt.savefig('./Graphs/C.D.F. of Probability meeting (all).pdf')
plt.show()
plt.close()


#   Here I want to graph the points with on the x axis the p-value and
#   on the y-axis the occurences divided by the avg of occurences expected

prob_and_occ = pd.DataFrame(pd.DataFrame(index=range(0,90)))

for exp in range (0, 3) :

  if exp == 0 :
    drug = ' - caf real'
    label_chosen = "Caffeine"
    color_chosen = 'b'
  if exp == 1 :
    drug = ' - eth real'
    label_chosen = "Ethanol"
    color_chosen = 'g'
  if exp == 2 :
    drug = ' - sug real'
    label_chosen = "Sugar"
    color_chosen = 'r'
    
  prob_and_occ[label_chosen + " - p-value"] = np.nan
  prob_and_occ[label_chosen + " - occ/avg_occ"] = np.nan
  j = 0
#   These two variables tell me how many event under a p-value of some value are there
#   that are over or under the occ./avg occ. of 1
  threshold = 1.1
  how_many_high = 0
  how_many_low = 0
  
  for id in range (1, 11) :
    
    tot_occ_id = 0
    
    for i in range (0, 45) :
      if probability_of_meeting["Id 1" + drug][i] == id or probability_of_meeting["Id 2" + drug][i] == id :
        tot_occ_id += probability_of_meeting["Occurences" + drug][i]
    
    avg_occ_id = tot_occ_id/9

    for i in range (0, 45) :
      if probability_of_meeting["Id 1" + drug][i] == id :
        prob_and_occ[label_chosen + " - p-value"][j] = probability_of_meeting["Probability Id 1" + drug][i]
        prob_and_occ[label_chosen + " - occ/avg_occ"][j] = probability_of_meeting["Occurences" + drug][i]/avg_occ_id
        j += 1
        if probability_of_meeting["Probability Id 1" + drug][i] < threshold :
          if prob_and_occ[label_chosen + " - occ/avg_occ"][j-1] > 1 :
            how_many_high += 1
          else :
            how_many_low += 1
      if probability_of_meeting["Id 2" + drug][i] == id :
        prob_and_occ[label_chosen + " - p-value"][j] = probability_of_meeting["Probability Id 2" + drug][i]
        prob_and_occ[label_chosen + " - occ/avg_occ"][j] = probability_of_meeting["Occurences" + drug][i]/avg_occ_id
        j += 1
        if probability_of_meeting["Probability Id 2" + drug][i] < threshold :
          if prob_and_occ[label_chosen + " - occ/avg_occ"][j-1] > 1 :
            how_many_high += 1
          else :
            how_many_low += 1
        
  plt.plot(prob_and_occ[label_chosen + " - p-value"], prob_and_occ[label_chosen + " - occ/avg_occ"], color=color_chosen, label=label_chosen, linewidth = 0, marker = 'o', markersize = 3)
  print(label_chosen, ": High = ", how_many_high, " Low = ", how_many_low)
  
plt.legend()
plt.xlabel("P-value of the encounters")
plt.ylabel("Occ. / Average Occ.")
plt.xlim(-0.005, 0.105)
plt.tight_layout()
#plt.savefig('./Graphs/p-values and avg occurences.pdf')
plt.show()
plt.close()

#   Now I make it spit out the total number of meeting, with avg and std for the toy model
sum_caf = 0
sum_eth = 0
sum_sug = 0
concatenated = chain(range(1, 14), range(15, 16), range(17, 29), range(30, 33), range(34, 37), range(38, 40), range(41, 43), range(44, 48))
for seed in concatenated:
  
  sum_caf += probability_of_meeting["Occurences - caf fake (" + str(seed) + ")"].sum()
  sum_eth += probability_of_meeting["Occurences - eth fake (" + str(seed) + ")"].sum()
  sum_sug += probability_of_meeting["Occurences - sug fake (" + str(seed) + ")"].sum()

avg_caf = sum_caf/40
avg_eth = sum_eth/40
avg_sug = sum_sug/40

square_diff_caf = 0.0
square_diff_eth = 0.0
square_diff_sug = 0.0
concatenated = chain(range(1, 14), range(15, 16), range(17, 29), range(30, 33), range(34, 37), range(38, 40), range(41, 43), range(44, 48))
for seed in concatenated:
  
  square_diff_caf += math.pow(probability_of_meeting["Occurences - caf fake (" + str(seed) + ")"].sum() - avg_caf, 2)
  square_diff_eth += math.pow(probability_of_meeting["Occurences - eth fake (" + str(seed) + ")"].sum() - avg_eth, 2)
  square_diff_sug += math.pow(probability_of_meeting["Occurences - sug fake (" + str(seed) + ")"].sum() - avg_sug, 2)

std_caf = math.sqrt(square_diff_caf/39.0)
std_eth = math.sqrt(square_diff_eth/39.0)
std_sug = math.sqrt(square_diff_sug/39.0)


print("Tot. Real exp.1 : ", probability_of_meeting["Occurences - caf real"].sum())
print("Tot. Real exp.2 : ", probability_of_meeting["Occurences - eth real"].sum())
print("Tot. Real exp.3 : ", probability_of_meeting["Occurences - sug real"].sum())

print("Tot. Fake exp.1 : ", avg_caf, "+-", std_caf)
print("Tot. Fake exp.2 : ", avg_eth, "+-", std_eth)
print("Tot. Fake exp.3 : ", avg_sug, "+-", std_sug)

