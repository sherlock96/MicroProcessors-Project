"""Raspberry Pi Face Recognition Treasure Box
Face Recognition Training Script
Copyright 2013 Tony DiCola 

Run this script to train the face recognition system with positive and negative
training images.  The face recognition model is based on the eigen faces
algorithm implemented in OpenCV.  You can find more details on the algorithm
and face recognition here:
  http://docs.opencv.org/modules/contrib/doc/facerec/facerec_tutorial.html
"""
import fnmatch
import os

import cv2
import numpy as np

import config
import face



def walk_files(directory, match='*'):
	"""Generator function to iterate through all files in a directory recursively
	which match the given filename match parameter.
	"""
	for root, dirs, files in os.walk(directory):
		for filename in fnmatch.filter(files, match):
			yield os.path.join(root, filename)

def prepare_image(filename):
	"""Read an image as grayscale and resize it to the appropriate size for
	training the face recognition model.
	"""
	return face.resize(cv2.imread(filename, cv2.IMREAD_GRAYSCALE))

def normalize(X, low, high, dtype=None):
	"""Normalizes a given array in X to a value between low and high.
	Adapted from python OpenCV face recognition example at:
	  https://github.com/Itseez/opencv/blob/2.4/samples/python2/facerec_demo.py
	"""
	X = np.asarray(X)
	minX, maxX = np.min(X), np.max(X)
	# normalize to [0...1].
	X = X - float(minX)
	X = X / float((maxX - minX))
	# scale to [low...high].
	X = X * (high-low)
	X = X + low
	if dtype is None:
		return np.asarray(X)
	return np.asarray(X, dtype=dtype)

if __name__ == '__main__':
        i=raw_input('for which user to train? (enter number): ')
        print 'Reading training images...'
        faces = []
        labels = []
        pos_count = 0
        neg_count = 0
        positive_path='./training/positive/u{0}'.format(i)
        training_file='./training/xml/training{0}.xml'.format(i)
        MEAN_FILE = './training/mean/mean{0}.png'.format(i)
        POSITIVE_EIGENFACE_FILE = './training/eigen/positive_eigenface{0}.png'.format(i)
        NEGATIVE_EIGENFACE_FILE = './training/eigen/negative_eigenface{0}.png'.format(i)
        # Read all positive images
        for filename in walk_files(positive_path, '*.pgm'):
                faces.append(prepare_image(filename))
                labels.append(config.POSITIVE_LABEL)
                pos_count += 1
        # Read all negative images
        for filename in walk_files(config.NEGATIVE_DIR, '*.pgm'):
                faces.append(prepare_image(filename))
                labels.append(config.NEGATIVE_LABEL)
                neg_count += 1
        print 'Read', pos_count, 'positive images and', neg_count, 'negative images.'

        # Train model
        print 'Training model...'
        model = cv2.createEigenFaceRecognizer()
        model.train(np.asarray(faces), np.asarray(labels))

        # Save model results
        model.save(training_file)
        print 'Training data saved to', training_file
                    
        # Save mean and eignface images which summarize the face recognition model.
        mean = model.getMat("mean").reshape(faces[0].shape)
        cv2.imwrite(MEAN_FILE, normalize(mean, 0, 255, dtype=np.uint8))
        eigenvectors = model.getMat("eigenvectors")
        pos_eigenvector = eigenvectors[:,0].reshape(faces[0].shape)
        cv2.imwrite(POSITIVE_EIGENFACE_FILE, normalize(pos_eigenvector, 0, 255, dtype=np.uint8))
        neg_eigenvector = eigenvectors[:,1].reshape(faces[0].shape)
        cv2.imwrite(NEGATIVE_EIGENFACE_FILE, normalize(neg_eigenvector, 0, 255, dtype=np.uint8))
