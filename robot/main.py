
import glob

from glob import BOT_OFF
from glob import BOT_ON
from glob import BOT_ERROR
from glob import BOT_WON
from glob import BOT_STATES
from glob import UP
from glob import RIGHT
from glob import LEFT
from glob import DOWN
from glob import DIRECTIONS
from glob import MOVES


from world import World
from gamedefs import GAME_SETUPS
from gamedefs import EMPTY
from gamedefs import PICKUP
from gamedefs import DEPOSIT
from gamedefs import END
from gamedefs import WALL

# Students code
import robot

# Student Functions:
def TurnOn():
  glob.GAME.TurnOn()
def TurnOff():
  glob.GAME.TurnOff()
def TurnLeft():
  glob.GAME.TurnLeft()
def Move():
  glob.GAME.Move()
def PickUp():
  glob.GAME.PickUp()
def PutDown():
  glob.GAME.PutDown()


def isAtPickUp():
  return glob.GAME.isAtPickUp()
def isAtDeposit():
  return glob.GAME.isAt(DEPOSIT)
def isAtEnd():
  return glob.GAME.isAt(END)
def isClearAhead():
  return glob.GAME.isClear(0)
def isClearLeft():
  return glob.GAME.isClear(-1)
def isClearRight():
  return glob.GAME.isClear(1)
def hasPickUps():
  return glob.GAME.hasPickUps()
def hasError():
  return glob.GAME.hasError()

class Game:
  def __init__(self, index, showGui):
    if index < 0 or index >= len(GAME_SETUPS):
      print 'Error: Invalid integer set for CURRENT_GAME.'
      print 'Must be between 0 and ' + str(len(GAME_SETUPS)-1) + '.'
      exit(0)

    # Set the global variable.
    glob.GAME = self

    print 'Starting game' + str(index)
    self.game = GAME_SETUPS[index]
    self.gameNum = index
    self.showGui = showGui
    self.currX = self.game['start'][0]
    self.currY = self.game['start'][1]
    self.currDir = UP
    self.botState = BOT_OFF
    self.errorMessage = ''
    self.pickupCount = 0


    self.pickupSpots = []
    board = self.game["board"]
    for i in range(len(board)):
      if board[i] == PICKUP:
        x = i % self.game['size']
        y = i / self.game['size']
        self.pickupSpots.append((x,y))

    self.state = []
    self.logState()

  def logState(self):
    pickSpots = self.pickupSpots[:]

    currState = ((self.currX, self.currY),
                 self.botState,
                 self.currDir,
                 self.pickupCount,
                 self.errorMessage,
                 pickSpots)

    self.state.append(currState)
    self.errorMessage = ''

  def DumpState(self):
    stateStr = ''
    for state in self.state:
      stateStr += '[' + BOT_STATES[state[1]] + '] '
      stateStr += "Position: " + str(state[0]) + ' '
      stateStr += "Dir: " + DIRECTIONS[state[2]] + ' '
      stateStr += "Pickups: " + str(state[3]) + "\n"
      if state[4] != '':
        stateStr += "   Error Message: " + state[4] + "\n"

    return stateStr

  def makeWorld(self):
    print "Creating GUI"
    world = World(self.game, self.state, self.DumpState(), robot.STEP_TIME)
    world.start()
    return world

  def run(self):
    print 'Running Your Solution'
    studentSolution = getattr(robot, 'solve' + str(self.gameNum))
    studentSolution()
    self.CheckWin()
    print self.DumpState()
    if self.showGui:
      self.world = self.makeWorld()


  def isAtPickUp(self):
    pos = (self.currX, self.currY)
    return pos in self.pickupSpots


  def isAt(self, blockType):
    pos = self.currX + self.currY * self.game['size']
    return self.game['board'][pos] == blockType


  def isClear(self, dmod):
    clearDir = (self.currDir + dmod) % 4
    nextX = self.currX + MOVES[clearDir][0]
    nextY = self.currY + MOVES[clearDir][1]
    maxIndex = self.game['size'] - 1

    if nextX > maxIndex or nextX < 0 or nextY > maxIndex or nextY < 0:
      return False

    bpos = nextX + nextY * self.game["size"]
    return self.game['board'][bpos] != WALL


  def hasPickUps(self):
    return self.pickupCount > 0


  def hasError(self):
    return self.botState == BOT_ERROR


  def TurnOn(self):
    if self.botState == BOT_ERROR:
      return

    self.botState = BOT_ON
    self.logState()

  def TurnOff(self):
    if self.botState == BOT_ERROR:
      return

    self.botState = BOT_OFF
    self.logState()

  def TurnLeft(self):
    if self.botState == BOT_ERROR:
      return
    elif self.botState == BOT_OFF:
      self.botState = BOT_ERROR
      self.errorMessage = 'Tried to turn while the bot is off.'
      self.logState()
      return

    self.currDir = (self.currDir - 1) % 4
    self.logState()

  def Move(self):
    if self.botState == BOT_ERROR:
      return
    elif self.botState == BOT_OFF:
      self.botState = BOT_ERROR
      self.errorMessage = 'Tried to move while the bot is off.'
      self.logState()
      return

    nextX = self.currX + MOVES[self.currDir][0]
    nextY = self.currY + MOVES[self.currDir][1]
    maxIndex = self.game['size'] - 1

    if nextX > maxIndex or nextX < 0 or nextY > maxIndex or nextY < 0:
      self.botState = BOT_ERROR
      self.errorMessage = 'Attempted to move the bot off the game board to (' + str(nextX) + ', ' + str(nextY) + ').'
      self.logState()
      return

    nextPos = nextX + (nextY * self.game['size'])
    if self.game['board'][nextPos] == WALL:
      self.botState = BOT_ERROR
      self.errorMessage = 'Attempted to move the bot through a wall to (' + str(nextX) + ', ' + str(nextY) + ').'
      self.logState()
      return

    self.currX = nextX
    self.currY = nextY
    self.logState()

  def PickUp(self):
    if self.botState == BOT_ERROR:
      return
    elif self.botState == BOT_OFF:
      self.botState = BOT_ERROR
      self.errorMessage = 'Tried to pick up while the bot is off.'
      self.logState()
      return

    currPos = (self.currX, self.currY)
    if currPos in self.pickupSpots:
      self.pickupCount += 1
      self.pickupSpots.remove(currPos)
    else:
      self.botState = BOT_ERROR
      self.errorMessage = 'Tried to pick nothing.'

    self.logState()

  def PutDown(self):
    if self.botState == BOT_ERROR:
      return
    elif self.botState == BOT_OFF:
      self.botState = BOT_ERROR
      self.errorMessage = 'Tried to put down while the bot is off.'
      self.logState()
      return

    if self.pickupCount == 0:
      self.botState = BOT_ERROR
      self.errorMessage = 'Tried to put down nothing.'
      self.logState()
      return

    currPos = (self.currX, self.currY)
    self.pickupCount -= 1
    self.pickupSpots.append(currPos)
    self.logState()

  def CheckWin(self):
    if self.botState == BOT_ERROR:
      return

    if self.botState != BOT_OFF:
      self.botState = BOT_ERROR
      self.errorMessage = 'Finished wihtout turning the bot off.'
      self.logState()

    pos = self.currX + (self.currY * self.game['size'])
    if self.game['board'][pos] != END:
      self.botState = BOT_ERROR
      self.errorMessage = 'The bot did not finish at the end point.'
      self.logState()

    if self.pickupCount > 0:
      self.botState = BOT_ERROR
      self.errorMessage = 'The bot is carring pickups at the end point.'
      self.logState()

    for pickup in self.pickupSpots:
      pos = pickup[0] + (pickup[1] * self.game['size'])
      if self.game['board'][pos] != DEPOSIT:
        self.botState = BOT_ERROR
        self.errorMessage = 'A pickup is not on a deposit.'
        self.logState()

    for i in range(self.game['size']**2):
      if self.game['board'][i] == DEPOSIT:
        pos = (i % self.game['size'], i / self.game['size'])
        if not pos in self.pickupSpots:
          self.botState = BOT_ERROR
          self.errorMessage = 'Some deposits are empty.'
          self.logState()

    if self.botState != BOT_ERROR:
      self.botState = BOT_WON
      self.logState()

if __name__ == '__main__':
  print "Welcome to the robot"
  gameNum = robot.CURRENT_GAME
  if robot.SHOW_GUI:
    game = Game(gameNum, True)
    game.run()
  else:
    for i in range(len(GAME_SETUPS)):
      game = Game(i, False)
      game.run()
