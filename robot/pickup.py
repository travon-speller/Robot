import Tkinter as tk

PICKUP_ID = 0

class Pickup:
  def __init__(self, canvas, size):
    global PICKUP_ID
    self.canvas = canvas
    self.size = size
    self.tag = "pickup" + str(PICKUP_ID)
    self.pos = (0,0)
    PICKUP_ID += 1


  def show(self):
    self.canvas.delete(self.tag)
    x = self.pos[0] * self.size + self.size/2
    y = self.pos[1] * self.size + self.size/2
    radius = self.size/6
    # Draw Circle
    self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                            outline = 'grey',
                            fill = '#792DEB',
                            width=3,
                            tags = self.tag
                            )


  def destroy(self):
    self.canvas.delete(self.tag)
