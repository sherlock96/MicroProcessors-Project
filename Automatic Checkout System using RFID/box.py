"""Raspberry Pi Face Recognition Treasure Box
Treasure Box Script
Copyright 2013 Tony DiCola 
"""
import cv2
import numpy as np
import config
import face
import hardware

import glob
import os
import sys
import select


def is_letter_input(letter):
	# Utility function to check if a specific character is available on stdin.
	# Comparison is case insensitive.
	if select.select([sys.stdin,],[],[],0.0)[0]:
		input_char = sys.stdin.read(1)
		return input_char.lower() == letter.lower()
	return False


def recognize():
	# Load training data into model
	print 'Loading training data...'
	
	training_file1='./training/xml/training1.xml'
	model1 = cv2.createEigenFaceRecognizer()
	model1.load(training_file1)

	training_file2='./training/xml/training2.xml'
	model2 = cv2.createEigenFaceRecognizer()
	model2.load(training_file2)

	training_file3='./training/xml/training3.xml'
	model3 = cv2.createEigenFaceRecognizer()
	model3.load(training_file3)
##
##	training_file4='./training/xml/training4.xml'
##	model4 = cv2.createEigenFaceRecognizer()
##	model4.load(training_file4)
	
	print 'Training data loaded!'
	# Initialize camer and box.
	camera = config.get_camera()
	box = hardware.Box()
	# Move box to locked position.
	box.lock()
	print 'Running box...'
	print 'Press button to lock (if unlocked), or unlock if the correct face is detected.'
	print 'Press Ctrl-C to quit.'
	while True:
		# Check if capture should be made.
		# TODO: Check if button is pressed.
		#if box.is_button_up() or is_letter_input('c'):
                        #cv2.destroyAllWindows()
                if not box.is_locked:
                        # Lock the box if it is unlocked
                        box.lock()
                        print 'Box is now locked.'
                else:
                        print 'Button pressed, looking for face...'
                        # Check for the positive face and unlock if found.
                        image = camera.read()
                        # Convert image to grayscale.
                        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
                        # Get coordinates of single face in captured image.
                        result = face.detect_single(image)
                        if result is None:
                                print 'Could not detect single face!  Check the image in capture.pgm' \
                                          ' to see what was captured and try again with only one face visible.'
                                continue
                        x, y, w, h = result
                        # Crop and resize image to face.
                        crop = face.resize(face.crop(image, x, y, w, h))

                        # Test face against model.
                        label1, confidence1 = model1.predict(crop)
                        label2, confidence2 = model2.predict(crop)
                        label3, confidence3 = model3.predict(crop)
##                              label4, confidence4 = model4.predict(crop)

                        if (label1 == config.POSITIVE_LABEL):
                                print 'Predicted POSITIVE face with confidence {0} (lower is more confident).'.format(confidence1)
                        elif  (label2 == config.POSITIVE_LABEL):
                                print 'Predicted POSITIVE face with confidence {0} (lower is more confident).'.format(confidence2)
                        elif  (label3 == config.POSITIVE_LABEL):
                                print 'Predicted POSITIVE face with confidence {0} (lower is more confident).'.format(confidence3)
                        else : print 'Predicted NEGATIVE face with confidence {0} (lower is more confident).'.format(confidence2)

                        crop=np.array(crop,'uint8')
                        #cv2.imshow('VAIBHAV',crop)
                        #cv2.waitKey(500)
                        if label1 == config.POSITIVE_LABEL and confidence1 < config.POSITIVE_THRESHOLD:
                                print 'Its VAIBHAV!'
                                print 'Confidence : {0}'.format(confidence1)
                                cv2.imshow('VAIBHAV',crop)
                                cv2.waitKey(1000)
                                box.unlock()
                                return 'VAIBHAV',crop
                                #break
                        elif label2 == config.POSITIVE_LABEL and confidence2 < config.POSITIVE_THRESHOLD:
                                print 'Its SHIVAM!'
                                print 'Confidence : {0}'.format(confidence2)
                                cv2.imshow('SHIVAM',crop)
                                cv2.waitKey(1000)
                                box.unlock()
                                return 'SHIVAM',crop
                                #break
                        elif label3 == config.POSITIVE_LABEL and confidence3 < config.POSITIVE_THRESHOLD:
                                print 'Its ANSHAL!'
                                print 'Confidence : {0}'.format(confidence3)
                                cv2.imshow('ANSHAL',crop)
                                cv2.waitKey(1000)
                                box.unlock()
                                return 'ANSHAL',crop
                                #break
##				elif label4 == config.POSITIVE_LABEL and confidence4 < config.POSITIVE_THRESHOLD:
##					print 'UTKARSH face!'
##                                      print 'Confidence : {0}'.format(confidence4)
##					cv2.imshow('UTKARSH',crop)
##                                      cv2.waitKey(1000)
##					box.unlock()
                        else:
                                print 'Did not recognize face!'
