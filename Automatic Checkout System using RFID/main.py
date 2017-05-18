import rfid
import box
import numpy as np
import cv2
rfid.bill()
name,image=box.recognize()
#image=np.array('capture.pgm','uint8')
cv2.imshow(name,image)
cv2.waitKey(0)
input('Pressw enter to exit')
