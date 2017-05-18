#!/usr/bin/python3
import sys
import cv2
sys.path.insert(0, "/home/pi/pi-rc522/ChipReader")
from pirc522 import RFID
import signal
import time

def bill():
    rdr = RFID()
    util = rdr.util()
    util.debug = False
    cost=0
    print 'Press Ctrl+C when done.\n'
    try:
        while True:
            #Request tag
            (error, data) = rdr.request()
            if not error:
                print ("\nDetected")
                (error, uid) = rdr.anticoll()
                if not error:
                    #Print UID
                    print ("Card read UID: "+str(uid[0])+"."+str(uid[1])+"."+str(uid[2])+"."+str(uid[3]))
                    if uid[0]==240 and uid[1]==250 and uid[2]==143 and uid[3]==124 :
                        print("item 1 purchased")
                        cost=cost+100
                    time.sleep(1)
    except KeyboardInterrupt:
        print '\n'
        print "Total Cost :", cost
        print '***** Thank You ******'
        print '\n'
 
