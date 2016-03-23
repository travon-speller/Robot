
import Tkinter as tk

from time import sleep

import threading

from droid import Droid
from pickup import Pickup

from gamedefs import EMPTY
from gamedefs import PICKUP
from gamedefs import DEPOSIT
from gamedefs import END
from gamedefs import WALL


WIDTH = 940
HEIGHT = 620

BOARD_SIZE = 600

STEP_TIME = 0


class World(tk.Frame):
  def __init__(self, game, states, resultStr, stepTime):
    self.game = game
    self.divs = game['size']
    self.root = root = tk.Tk(className = " SYCS 100 Robots! ")
    self.root.geometry(newGeometry = str(WIDTH)+'x'+str(HEIGHT)+'+100+0')
    # Initialize the parent class.
    tk.Frame.__init__(self, master=root, cnf={})
    self.grid(sticky=tk.N+tk.S+tk.E+tk.W)

    canvas = tk.Canvas(self.root, height = BOARD_SIZE, width = BOARD_SIZE, bg = 'white')
    self.canvas = canvas
    canvas.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

    self.makeBoard()
    self.showResults(resultStr)
    self.showGuide()
    self.droid = Droid(canvas, BOARD_SIZE/self.divs)
    self.states = states
    self.stateIndex = 0
    self.pickups = []

    global STEP_TIME
    STEP_TIME = max(100, stepTime)
    STEP_TIME = min(3000, STEP_TIME)

  def draw(self):
    self.updateState()
    self.droid.show()
    self.drawPickups()

    if len(self.states) > self.stateIndex:
      self.after(STEP_TIME, self.draw)

  def drawPickups(self):
    for pickup in self.pickups:
      pickup.destroy()

    for pickupSpot in self.pickupSpots:
      pickup = Pickup(self.canvas, BOARD_SIZE/self.divs)
      pickup.pos = pickupSpot
      pickup.show()
      self.pickups.append(pickup)

  def updateState(self):
    state = self.states[self.stateIndex]

    self.droid.pos = state[0]
    self.droid.status = state[1]
    self.droid.dir = state[2]
    self.droid.pickups = state[3]

    self.pickupSpots = state[5]
    self.stateIndex += 1

  def makeBoard(self):
    canvas = self.canvas
    divSize = BOARD_SIZE/self.divs

    board = self.game['board']
    for i in range(len(board)):
      x = i % self.divs * divSize
      y = i / self.divs * divSize
      if board[i] == END:
        # Draw the Finish
        self.canvas.create_rectangle(x, y, x + divSize, y + divSize,
                                outline = 'white',
                                fill = 'yellow',
                                width=divSize/2,
                                )
      elif board[i] == DEPOSIT:
        # Draw the Walls
        self.canvas.create_rectangle(x, y, x + divSize, y + divSize,
                                outline = 'white',
                                fill = 'orange',
                                width=divSize/2,
                                )
      elif board[i] == WALL:
        # Draw the Walls
        self.canvas.create_rectangle(x, y, x + divSize, y + divSize,
                                outline = 'white',
                                fill = 'grey',
                                width=divSize/2,
                                )
    # Draw the Border walls
    self.canvas.create_rectangle(0, 0, BOARD_SIZE, BOARD_SIZE,
                            outline = 'grey',
                            # fill = 'clear',
                            width=divSize/4,
                            )

    for i in range(divSize/2, BOARD_SIZE, divSize):
      canvas.create_line(i, 0, i, BOARD_SIZE, width = 2)
      canvas.create_line(0, i, BOARD_SIZE, i, width = 2)

  def showResults(self, resultStr):
    text = tk.Text(self.root, width=48, height=16, bg='grey')
    if resultStr.find('Error'):
      text.configure(fg='red')

    text.insert(tk.INSERT, "Resutls: (scroll down)\n\n")
    text.insert(tk.END, resultStr)

    text.configure(state=tk.DISABLED)
    text.grid(row=0, column=1, sticky=tk.N+tk.W)

  def showGuide(self):
    text = tk.Text(self.root, width=13, height=20)
    text.insert(tk.INSERT, "SYMBOL GUIDE:\n\n\n")
    text.insert(tk.INSERT, " Your Avatar:\n")
    text.insert(tk.INSERT, "  (Off: Grey)\n")
    text.insert(tk.INSERT, "  (On: Green)\n")
    text.insert(tk.INSERT, " (Error: Red)\n")
    text.insert(tk.INSERT, "  (Won: Blue)\n\n")
    text.insert(tk.INSERT, "      Pickup:\n\n\n")
    text.insert(tk.INSERT, "        Wall:\n\n\n")
    text.insert(tk.INSERT, "     Deposit:\n\n\n")
    text.insert(tk.INSERT, "        Exit:\n\n\n")
    text.configure(state=tk.DISABLED)
    text.grid(row=0, column=1, sticky=tk.S+tk.W)

    canvas = tk.Canvas(self.root, height = 250, width = 220)
    canvas.grid(row=0, column=1, sticky=tk.S+tk.E)
    droid = Droid(canvas, 80)
    droid.pos = (-.20, -.20)
    droid.show()
    pickup = Pickup(canvas, 60)
    pickup.pos = (-.18, 1.0)
    pickup.show()

    canvas.create_rectangle(5, 125, 35, 155,
                            fill = 'grey',
                            width=0,
                            )

    canvas.create_rectangle(5, 170, 35, 200,
                            fill = 'orange',
                            width=0,
                            )

    canvas.create_rectangle(5, 215, 35, 250,
                            fill = 'yellow',
                            width=0,
                            )

  def start(self, *pargs):
    mainThread = threading.Thread(target = self.draw, args=pargs)
    mainThread.start()
    self.mainloop()