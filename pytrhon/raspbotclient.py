#!/usr/bin/python
#
# Imports
import time
import sys
import usb.core
import usb.util
import socket
import threading
#
# Initial setup and basic methods
#
joyVendor=0x16c0
joyProduct=0x27dc
dev = usb.core.find(idVendor=joyVendor, idProduct=joyProduct)
interface = 0
endpoint = dev[0][(0,0)][0]
HOST, PORT = "10.52.200.185", 9999
#
# Init
#
def initAll():
    global sock, HOST, PORT
    if dev.is_kernel_driver_active(interface) is True:
        # tell the kernel to detach
        dev.detach_kernel_driver(interface)
        # claim the device
        usb.util.claim_interface(dev, interface)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setblocking(0)
#
# Startup
#
def main():
	initAll()
	moveIt()
	time.sleep(1)

#
# Move IT
#
def moveIt():
    global sock, sMove
    sMove = dev.read(endpoint.bEndpointAddress,endpoint.wMaxPacketSize)
    threading.Thread(target=moveItThread).start()
    runIt = True
    while(runIt):
        runIt = moveBot(sMove)
        time.sleep(0.02)
    sock.close()

def moveItThread():
    global sMove
    while (sMove[3] == 0):
        try:
            sMove = dev.read(endpoint.bEndpointAddress,endpoint.wMaxPacketSize)
        except usb.core.USBError as e:
            if e.args == ('Operation timed out',):
                continue    
        time.sleep(0.02)

def moveBot(data):
    global sock, HOST, PORT
    print data
    vVertical = data[2]
    vHorizontal = data[1]
    vButton = data[3]
    print "Got V=" + str(vVertical) +  " H=" + str(vHorizontal) + " B=" + str(vButton)
    success = None

    if vButton == 1:
        print "q"
        success = sock.sendto("q" + "\n", (HOST, PORT))       
        return False   

    if vVertical == 128 and vHorizontal == 128:
        print "."
        #success = sock.sendto("." + "\n", (HOST, PORT))
        return True

    sW = ""

    if vVertical == 0:
        print "w"
        sW += "w"
        #success = sock.sendto("w" + "\n", (HOST, PORT))
    elif vVertical == 255:
        print "s"
        sW += "s"
        #success = sock.sendto("s" + "\n", (HOST, PORT))

    if vHorizontal == 0:
        print "a"
        sW += "a"
        #success = sock.sendto("a" + "\n", (HOST, PORT))
    elif vHorizontal == 255:
        print "d"
        sW += "d"
        #success = sock.sendto("d" + "\n", (HOST, PORT))

    if len(sW) >= 1:
        success = sock.sendto(sW + "\n", (HOST, PORT))

    return True
#
# Call main
#
if __name__ == "__main__":
    sys.exit(main())
