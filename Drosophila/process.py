#!/usr/bin/env python

import pandas as pd
import pylab as plt
import numpy as np
from scipy.spatial.distance import pdist, squareform
import matplotlib.animation as animation # animation plot
from viewer.dynplot import dynplot

__package__ = "Distance time evolution"
__author__  = "Nico Curti (nico.curit2@unibo.it)"



if __name__ == '__main__':

  filename = '../data/experiment_0.csv'
  data = pd.read_csv(filename, sep=',', header=0, usecols=['timestamps',
                                                           'id',
                                                           'x', 'y'
                                                           ])

  #%%
  flies = data.groupby('id')
  coords = [d[['x', 'y']] for _, d in flies]
  for i in range(len(coords)): coords[i].index = np.arange(0, len(coords[i]))
  movie = dynplot(coords[0][:200])

#%%
  times = data.groupby('timestamps')
  coords = [d[['x', 'y']] for _, d in times]
  colors = np.arange(10)
  npts = 1000
  minx, maxx = data.x.min(), data.x.max()
  miny, maxy = data.y.min(), data.y.max()

  ims = np.empty(npts, dtype=np.object)

  fig = plt.figure(figsize=(10,10))
  fig.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.15)
  ax = fig.gca()
  ax.grid()
  ax.set_xlim(minx, maxx)
  ax.set_ylim(miny, maxy)
  ax.set_ylabel('y', fontsize=24)
  ax.set_xlabel('x', fontsize=24)

  for t in range(npts):
    pts = ax.scatter(coords[t].x, coords[t].y,
                     s=50, c=colors)
    ims[t] = [pts]
  movie = animation.ArtistAnimation(fig,
                                    ims,
                                    interval=50,
                                    blit=True,
                                    repeat_delay=100)


#%%


  times = data.groupby('timestamps')
  distances = [pdist(d[['x', 'y']], metric='euclidean')
               for _, d in times]
  nframe = len(distances)
  del data

  fig = plt.figure(figsize=(8,8))
  sizes = squareform(distances[0]).shape
  fig.set_size_inches(1. * sizes[0] / sizes[1], 1, forward=False)
  ax = plt.Axes(fig, [0., 0., 1., 1.])
  ax.set_axis_off()
  fig.add_axes(ax)

  ims = [[plt.imshow(squareform(d), animated=True, cmap='hot'),
          ]#plt.colorbar()]
         for d in distances[:2000]]

  movie = animation.ArtistAnimation(fig,
                                    ims,
                                    interval=50,
                                    blit=True,
                                    repeat_delay=100)