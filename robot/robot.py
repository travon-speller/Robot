# Name:

# See the README file for instructions.

from main import TurnOn
from main import TurnOff
from main import TurnLeft
from main import Move
from main import PickUp
from main import PutDown

from main import isAtPickUp
from main import isAtDeposit
from main import isAtEnd
from main import isClearAhead
from main import isClearLeft
from main import isClearRight
from main import hasPickUps
from main import hasError


from glob import UP
from glob import RIGHT
from glob import LEFT
from glob import DOWN

# This can be any value 0-7.  Change it to test each function.
CURRENT_GAME = 7

# Set this to False to just test all your results without a GUI.  When set to True
# it will test one puzzle at a time.
SHOW_GUI = True

# The number of miliseconds between each step.  Raise it to slow things down.
# Lower it to speed it up.
STEP_TIME = 500

def TurnRight():
	TurnLeft()
	TurnLeft()
	TurnLeft()

def moveRight():
	Move()
	TurnRight()

def rightMove():
	TurnRight()
	Move()

def moveLeft():
  TurnLeft()
  Move()

def finish():
	Move()
	TurnOff()

def tripleMove():
  Move()
  Move()
  Move()

def doubleMove():
  Move()
  Move()

def pickupChain():
	while isAtPickUp():
		PickUp()
		if isClearAhead():
			Move()
		else:
			TurnLeft()

def dropAll():
	while hasPickUps():
		PutDown()

def zigzag():
	moveRight()
	Move()
	TurnLeft()
	if isAtPickUp():
		PickUp()
	elif isAtDeposit():
		dropAll()

def solve0():
  TurnOn()
  rightMove()
  moveRight()
  finish()

def solve1():
  TurnOn()
  rightMove()
  PickUp()
  Move()
  PutDown()
  TurnRight()
  finish()

def solve2():
  TurnOn()
  TurnLeft()
  for x in range(2):
    tripleMove()
    rightMove()  
  doubleMove()
  TurnOff()

def solve3():	
  TurnOn()
  rightMove()
  for x in range(2):
    tripleMove()
    TurnLeft()
  pickupChain()
  doubleMove()
  dropAll()
  moveLeft()
  finish()

def solve4():
  TurnOn()
  TurnRight()
  tripleMove()
  moveRight()
  doubleMove()
  pickupChain()
  Move()
  dropAll()
  TurnRight()
  tripleMove()
  TurnOff()

def solve5():
  TurnOn()
  TurnRight()
  for x in range(5):
    zigzag()
  moveRight()
  finish()

def solve6():
  TurnOn()
  while isClearAhead() or isClearRight():
  	if isClearAhead():
  		Move()
  	else:
  		rightMove()
  	if isAtPickUp():
  		PickUp()
  	elif isAtDeposit():
  		dropAll()
  	elif isAtEnd():
  		TurnOff()

def solve7():
  TurnOn()
  rightMove()
  pickupChain()
  Move()
  pickupChain()
  tripleMove()
  PickUp()
  moveLeft()
  for x in range(2):
    PutDown()
    Move()
  pickupChain()
  PutDown()
  doubleMove()
  PutDown()
  moveLeft()
  moveLeft()
  for x in range(2):
    tripleMove()
    rightMove()
  dropAll()
  Move()
  finish()