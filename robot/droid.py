import Tkinter as tk

from glob import BOT_OFF
from glob import BOT_ON
from glob import BOT_ERROR

from glob import UP
from glob import RIGHT
from glob import LEFT
from glob import DOWN



droid_green = '#41FD34'
status_colors = [
  'grey',
  droid_green,
  'red',
  'blue',
]

class Droid:
  def __init__(self, canvas, size):
    self.canvas = canvas
    self.size = size
    self.tag = "droid"
    self.status = 1
    self.pos = (0,0)
    self.dir = 0
    self.pickups = 0


  def show(self):
    self.canvas.delete(self.tag)
    x = self.pos[0] * self.size + self.size/2
    y = self.pos[1] * self.size + self.size/2
    radius = self.size/4
    # Draw Circle
    self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                            outline = 'grey',
                            fill = status_colors[self.status],
                            width=3,
                            tags = self.tag
                            )

    if self.pickups > 0:
        self.canvas.create_oval(x-radius, y+radius, x -radius + 12, y + radius -12,
                                outline = 'grey',
                                fill = '#792DEB',
                                width=2,
                                tags = self.tag
                                )

    # Defulted UP
    xend = x
    yend = y - radius
    if self.dir == LEFT:
      xend = x - radius
      yend = y
    elif self.dir == RIGHT:
      xend = x + radius
      yend = y
    elif self.dir == DOWN:
      xend = x
      yend = y + radius

    self.canvas.create_line(x, y, xend, yend,
                            fill = 'black',
                            width=4,
                            tags = self.tag
                            )




    # Android Bot.
    # # Draw Head
    # self.canvas.create_arc(self.size*0.2, 0, self.size*0.8, self.size*0.45,
    #                         start = 0,
    #                         extent = 180,
    #                         style = tk.CHORD,
    #                         outline = status_colors[self.status],
    #                         fill = droid_green,
    #                         width=3,
    #                         tags = self.tag
    #                         )

    # # Draw Body
    # self.canvas.create_rectangle(self.size*0.2, self.size*0.225 + 6, self.size*0.8, self.size*0.75,
    #                         outline = status_colors[self.status],
    #                         fill = droid_green,
    #                         width=3,
    #                         tags = self.tag
    #                         )

    # # Draw Arms
    # self.canvas.create_rectangle(self.size*0.08, self.size*0.225 + 6, self.size*0.16, self.size*0.6,
    #                         outline = status_colors[self.status],
    #                         fill = droid_green,
    #                         width=3,
    #                         tags = self.tag
    #                         )
    # self.canvas.create_rectangle(self.size*0.84, self.size*0.225 + 6, self.size*0.92, self.size*0.6,
    #                         outline = status_colors[self.status],
    #                         fill = droid_green,
    #                         width=3,
    #                         tags = self.tag
    #                         )

    # # Draw Legs
    # self.canvas.create_rectangle(self.size*0.3, self.size*0.75 + 6, self.size*0.4, self.size,
    #                         outline = status_colors[self.status],
    #                         fill = droid_green,
    #                         width=3,
    #                         tags = self.tag
    #                         )
    # self.canvas.create_rectangle(self.size*0.6, self.size*0.75 + 6, self.size*0.7, self.size,
    #                         outline = status_colors[self.status],
    #                         fill = droid_green,
    #                         width=3,
    #                         tags = self.tag
    #                         )
