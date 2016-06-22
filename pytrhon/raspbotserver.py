#!/usr/bin/python
#
# Motor Left: 
#  Pin 01: Port 13 = GPIO 27
#  Pin 02: Port 11 = GPIO 17
# Motor Right:
#  Pin 01: Port 5 = GPIO 03
#  Pin 02: Port 3 = GPIO 02
#

# Imports
import RPi.GPIO as gpio
import time
import sys
import SocketServer
import threading
import string
#  
#
def initialize():
  global isInit
  if not isInit:
    print "Init motor ..."
    initAll()
    print "Start moveIT thread ..."
    threading.Thread(target=moveIt).start()
    isInit = True

def initAll(): 
  gpio.setmode(gpio.BOARD)
  gpio.setup(motorLeftPin01, gpio.OUT)
  gpio.setup(motorLeftPin02, gpio.OUT)
  gpio.setup(motorRightPin01, gpio.OUT)
  gpio.setup(motorRightPin02, gpio.OUT)

def stopAll():
  gpio.output(motorLeftPin01, False)
  gpio.output(motorLeftPin02, False)
  gpio.output(motorRightPin01, False)
  gpio.output(motorRightPin02, False)
  gpio.cleanup()

def moveLeftForward():
  gpio.output(motorLeftPin01, True)
  gpio.output(motorLeftPin02, False)

def moveRightForward():
  gpio.output(motorRightPin01, False)
  gpio.output(motorRightPin02, True)

def moveLeftBackward():
  gpio.output(motorLeftPin01, False)
  gpio.output(motorLeftPin02, True)

def moveRightBackward():
  gpio.output(motorRightPin01, True)
  gpio.output(motorRightPin02, False)

def stopMovement():
  gpio.output(motorLeftPin01, False)
  gpio.output(motorLeftPin02, False)
  gpio.output(motorRightPin01, False)
  gpio.output(motorRightPin02, False)
  
def moveIt():
  global charMove, mytimer, runIt, server
  runIt=True
  while(runIt):
    time.sleep(0.4)
    # print("waiting for input...")
    if not charMove == None:
      # print("Exe command '{}'...".format(charMove))
      if string.find(charMove,"q")>=0:
          print("please stop!")
          runIt = False
      else:
          runIt = moveBot(charMove)
          time.sleep(0.05)
          mytimer += 0.05
          if mytimer > 0.2:
              mytimer = 0
              charMove = "."
  stopAll()
  server.shutdown()
  
      
def moveBot(charMove):
  if string.find(charMove,".")>=0:
    #print("Stopping...")
    stopMovement()
  
  if string.find(charMove,"w")>=0:
    print("moving forward...")
    moveLeftForward()
    moveRightForward()
  elif string.find(charMove,"s")>=0:
    print("moving backwards...")
    moveLeftBackward()
    moveRightBackward()
  
  if string.find(charMove,"a")>=0:
    print("moving left...")
    moveRightForward()
    moveLeftBackward()
  elif string.find(charMove,"d")>=0:
    print("moving right...")
    moveLeftForward()
    moveRightBackward()
  
  if string.find(charMove,"q")>=0:
    print("Quitting...")
    return False
  
  return True
#
# Server
#
class RaspBotServer(SocketServer.BaseRequestHandler):
  def handle(self):
    global charMove
    print "Handle myself ..."
    data = self.request[0].strip()
    socket = self.request[1]
    print("Got command '{data}'...".format(data=data))
    charMove = data
    socket.sendto(data, self.client_address)                
#
#
#
if __name__ == "__main__":
  print "Startup ..."
  motorLeftPin01 = 13
  motorLeftPin02 = 11
  motorRightPin01 = 5
  motorRightPin02 = 3
  charMove = None
  mytimer = 0
  print("We start up background thread...")
  isInit = False
  initialize()
  
  HOST, PORT = "0.0.0.0", 9999
  print "Server init ..."
  server = SocketServer.UDPServer((HOST, PORT), RaspBotServer)
  print "Serve forever ..."
  server.serve_forever()
