#!/usr/bin/env python

import pandas as pd
import pylab as plt
import numpy as np
from collections import deque
import matplotlib.animation as animation
import seaborn as sns
sns.set_context("paper", font_scale=3)

__package__ = "2D Dynamic Viewer"
__author__  = "Nico Curti (nico.curit2@unibo.it)"


def dynplot(data, buff_size = 10, npt_stat = 5, color='k'):
  """
  Plot 2D dynamics with animation support.

  Parameters
  ----------
  data : Pandas DataFrame
         The coordinates are supposed must be labelled as 'x' and 'y'
         respectivelly.
  buff_size : integer, optional
         Size of the deque for the line plot. The value must be less than
         the total number of points.
  npt_stat : integer, optional
         Number of points to estimate the dynamic directions.
  color : str, optional
         Color of the line plot.

  Returns
  -------
  movie : matplotlib animation
         Animation obtained by the line plot of the dynamic coordinates.
  """

  assert (isinstance(data,      pd.DataFrame))
  assert (isinstance(buff_size, int))
  assert (isinstance(npt_stat,  int))
  assert (isinstance(color,     str))

  minx, maxx = data.x.min(), data.x.max()
  miny, maxy = data.y.min(), data.y.max()

  npt, dim = data.shape

  assert (buff_size <= npt)
  pts = deque(maxlen=buff_size)
  counter = 0
  (dX, dY) = (0, 0)
  direction = ""

  ims = np.empty(npt, dtype=np.object)

  fig = plt.figure(figsize=(10,10))
  fig.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.15)
  ax = fig.gca()
  ax.grid()
  ax.set_xlim(minx, maxx)
  ax.set_ylim(miny, maxy)
  ax.set_ylabel('y', fontsize=24)
  ax.set_xlabel('x', fontsize=24)

  for t, d in data.iterrows():

    x, y = d
    pts.append( (x, y) )
    lines = []
    frame_cnt = ax.text(maxx - 20, maxy - 5,
                        'Frame: {}'.format(t),
                        fontsize=16, fontweight='bold')

    for i in range(1, len(pts)):
      if pts[i - 1] is None or pts[i] is None:
        continue

      if len(pts) > npt_stat:
        if counter >= npt_stat and i == 1 and pts[-npt_stat] is not None:
          dX = pts[-npt_stat][0] - pts[i][0]
          dY = pts[-npt_stat][1] - pts[i][1]
          (dirX, dirY) = ('', '')

          if abs(dX) > 20:
            dirX = 'East' if np.sign(dX) == 1 else 'West'
          if abs(dY) > 20:
            dirY = 'North' if np.sign(dY) == 1 else 'South'

          if dirX != '' and dirY != '':
            direction = '{}-{}'.format(dirY, dirX)
          else:
            direction = dirX if dirX != '' else dirY
      thickness = int(np.sqrt(buff_size * float(i + 1)) / 3.5)
      xprev, yprev = pts[i - 1]
      xnow,  ynow  = pts[i]
      line, = ax.plot([xprev, xnow], [yprev, ynow],
                      color=color,
                      linewidth=thickness,
#                      linestyle='dashed',
                      animated=True)
      lines.append(line)

      if i == len(pts) - 1:
        scatter, = ax.plot(xnow, ynow,
                           'h',
                           color=color,
                           markersize=15,
                           animated=True)
        lines.append(scatter)


    direction_fmt = ax.text(minx + 2, miny + 2,
                            direction,
                            fontsize=16,
                            fontweight='bold'
                            )
    delta_fmt     = ax.text(maxx - 30, miny + 2,
                            'dx: {0:.2f}, dy: {0:.2f}'.format(dX, dY),
                            fontsize=16,
                            fontweight='bold'
                            )

    counter += 1

    ims[t] = [*lines, frame_cnt, direction_fmt, delta_fmt]

  movie = animation.ArtistAnimation(fig, ims, interval=150, blit=True, repeat_delay=100)
  return movie


if __name__ == '__main__':

  np.random.seed(123)
  data = pd.DataFrame(np.random.uniform(low=0.,
                                        high=100.,
                                        size=(100, 2)),
                      columns=['x', 'y'])

  movie = dynplot(data, buff_size=10, npt_stat=5, color='k')

#  movie.save('./animation.gif', writer='imagemagick', fps=60)
