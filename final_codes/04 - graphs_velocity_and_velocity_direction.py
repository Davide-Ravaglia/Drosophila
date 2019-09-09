# -*- coding: utf-8 -*-
#!/usr/bin/env python

import pandas as pd
import pylab as plt
import numpy as np

__package__ = "Graphs of probability of variation of velocity direction. Graphs of averages, std, std of the mean of the velocities related to certain velocity direction changes."
__author__  = "Davide Ravaglia (davide.ravaglia3@studio.unibo.it)"

#%%


stats_of_bars = pd.read_csv('./random_walk/stats_of_bars.csv', sep=',', header=0, index_col='Unnamed: 0')


#   PROBABILITY GRAPH HIGH ZOOM
plt.plot(stats_of_bars["phi central"], stats_of_bars["prob (high)- caf"], color='b', label="Caffeine", marker='o', markersize=3, alpha=0.7)
plt.plot(stats_of_bars["phi central"], stats_of_bars["prob (high)- eth"], color='g', label="Ethanol", marker='o', markersize=3,  alpha=0.7)
plt.plot(stats_of_bars["phi central"], stats_of_bars["prob (high)- sug"], color='r', label="Sugar", marker='o', markersize=3,  alpha=0.7)
plt.xlim(-1.1, 1.1)
plt.ylabel('Probability')
plt.xlabel('Variation of Velocity Direction (rad)')
plt.tight_layout()
plt.legend()
plt.savefig('./Graphs/Probability - Inst variation of Vel Dir (high) (zoom).pdf')
plt.show()
plt.close()

#   PROBABILITY GRAPH LOW ZOOM
plt.plot(stats_of_bars["phi central"], stats_of_bars["prob (low)- caf"], color='b', label="Caffeine", marker='o', markersize=3, alpha=0.7)
plt.plot(stats_of_bars["phi central"], stats_of_bars["prob (low)- eth"], color='g', label="Ethanol", marker='o', markersize=3,  alpha=0.7)
plt.plot(stats_of_bars["phi central"], stats_of_bars["prob (low)- sug"], color='r', label="Sugar", marker='o', markersize=3,  alpha=0.7)
plt.xlim(-1.1,1.1)
plt.ylabel('Probability')
plt.xlabel('Variation of Velocity Direction (rad)')
plt.tight_layout()
plt.legend()
plt.savefig('./Graphs/Probability - Inst variation of Vel Dir (low) (zoom).pdf')
plt.show()
plt.close()


#   AVG VELOCITY AND STD GRAPH HIGH ZOOM
plt.errorbar(stats_of_bars["phi central"], stats_of_bars["average (high)- caf"], yerr=stats_of_bars["std (high)- caf"], fmt='o', color='b', ecolor='steelblue', elinewidth=3, capsize=0, label="Caff.", alpha=0.7)
plt.errorbar(stats_of_bars["phi central"], stats_of_bars["average (high)- eth"], yerr=stats_of_bars["std (high)- eth"], fmt='o', color='g', ecolor='yellowgreen', elinewidth=3, capsize=0, label="Eth.", alpha=0.7)
plt.errorbar(stats_of_bars["phi central"], stats_of_bars["average (high)- sug"], yerr=stats_of_bars["std (high)- sug"], fmt='o', color='r', ecolor='lightcoral', elinewidth=3, capsize=0, label="Sug.", alpha=0.7)
plt.ylim(0, 35)
plt.xlim(-0.8,0.8)
plt.ylabel('Instant Speed (mm/s)')
plt.xlabel('Variation of Velocity Direction (rad)')
plt.tight_layout()
plt.legend()
plt.savefig('./Graphs/Inst Vel - Inst variation of Vel Dir (high) (zoom).pdf')
plt.show()
plt.close()


#   AVG VELOCITY AND STD GRAPH LOW ZOOM
plt.errorbar(stats_of_bars["phi central"], stats_of_bars["average (low)- caf"], yerr=stats_of_bars["std (low)- caf"], fmt='o', color='b', ecolor='steelblue', elinewidth=3, capsize=0, label="Caff.", alpha=0.7)
plt.errorbar(stats_of_bars["phi central"], stats_of_bars["average (low)- eth"], yerr=stats_of_bars["std (low)- eth"], fmt='o', color='g', ecolor='yellowgreen', elinewidth=3, capsize=0, label="Eth.", alpha=0.7)
plt.errorbar(stats_of_bars["phi central"], stats_of_bars["average (low)- sug"], yerr=stats_of_bars["std (low)- sug"], fmt='o', color='r', ecolor='lightcoral', elinewidth=3, capsize=0, label="Sug.", alpha=0.7)
plt.xlim(-1.5,1.5)
plt.ylabel('Instant Velocity (mm/s)')
plt.xlabel('Variation of Velocity Direction (rad)')
plt.ylim(0, 1.25)
plt.tight_layout()
plt.legend()
plt.savefig('./Graphs/Inst Vel - Inst variation of Vel Dir (low) (zoom).pdf')
plt.show()
plt.close()

# Now showing the error on the mean
# I want a column which will have sqrt(entries) as value

stats_of_bars["sqrt(counter) (high)- caf"] = np.sqrt(stats_of_bars["counter (high)- caf"])
stats_of_bars["sqrt(counter) (low)- caf"] = np.sqrt(stats_of_bars["counter (low)- caf"])
stats_of_bars["sqrt(counter) (high)- eth"] = np.sqrt(stats_of_bars["counter (high)- eth"])
stats_of_bars["sqrt(counter) (low)- eth"] = np.sqrt(stats_of_bars["counter (low)- eth"])
stats_of_bars["sqrt(counter) (high)- sug"] = np.sqrt(stats_of_bars["counter (high)- sug"])
stats_of_bars["sqrt(counter) (low)- sug"] = np.sqrt(stats_of_bars["counter (low)- sug"])

#   AVG VELOCITY AND STD ON THE MEAN GRAPH HIGH ZOOM
plt.errorbar(stats_of_bars["phi central"], stats_of_bars["average (high)- caf"], yerr=stats_of_bars["std (high)- caf"]/stats_of_bars["sqrt(counter) (high)- caf"], fmt='o', color='b', ecolor='steelblue', elinewidth=3, capsize=0, label="Caff.", alpha=0.7)
plt.errorbar(stats_of_bars["phi central"], stats_of_bars["average (high)- eth"], yerr=stats_of_bars["std (high)- eth"]/stats_of_bars["sqrt(counter) (high)- eth"], fmt='o', color='g', ecolor='yellowgreen', elinewidth=3, capsize=0, label="Eth.", alpha=0.7)
plt.errorbar(stats_of_bars["phi central"], stats_of_bars["average (high)- sug"], yerr=stats_of_bars["std (high)- sug"]/stats_of_bars["sqrt(counter) (high)- sug"], fmt='o', color='r', ecolor='lightcoral', elinewidth=3, capsize=0, label="Sug.", alpha=0.7)
plt.ylim(5.7, 18.3)
plt.xlim(-1.1, 1.1)
plt.ylabel('Instant Speed (mm/s)')
plt.xlabel('Variation of Velocity Direction (rad)')
plt.tight_layout()
plt.legend()
plt.savefig('./Graphs/Inst Vel - Inst variation of Vel Dir (high) (zoom) (mean).pdf')
plt.show()
plt.close()

#   AVG VELOCITY AND STD ON THE MEAN GRAPH LOW ZOOM
plt.errorbar(stats_of_bars["phi central"], stats_of_bars["average (low)- caf"], yerr=stats_of_bars["std (low)- caf"]/stats_of_bars["sqrt(counter) (low)- caf"], fmt='o', color='b', ecolor='steelblue', elinewidth=3, capsize=0, label="Caff.", alpha=0.7)
plt.errorbar(stats_of_bars["phi central"], stats_of_bars["average (low)- eth"], yerr=stats_of_bars["std (low)- eth"]/stats_of_bars["sqrt(counter) (low)- caf"], fmt='o', color='g', ecolor='yellowgreen', elinewidth=3, capsize=0, label="Eth.", alpha=0.7)
plt.errorbar(stats_of_bars["phi central"], stats_of_bars["average (low)- sug"], yerr=stats_of_bars["std (low)- sug"]/stats_of_bars["sqrt(counter) (low)- caf"], fmt='o', color='r', ecolor='lightcoral', elinewidth=3, capsize=0, label="Sug.", alpha=0.7)
plt.xlim(-1.1,1.1)
plt.ylabel('Instant Velocity (mm/s)')
plt.xlabel('Variation of Velocity Direction (rad)')
plt.ylim(0.2, 0.6)
plt.tight_layout()
plt.legend()
plt.savefig('./Graphs/Inst Vel - Inst variation of Vel Dir (low) (zoom) (mean).pdf')
plt.show()
plt.close()


