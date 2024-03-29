# -*- coding: utf-8 -*-
"""Mask_detection2.0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-XtoPSJ-BbfxyCErDAEWO81MW0ExLu-I
"""

!pip install kaggle

!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

!kaggle datasets download -d omkargurav/face-mask-dataset

from zipfile import ZipFile
dataset='/content/face-mask-dataset.zip'
with ZipFile(dataset,'r') as zip:
  zip.extractall()
  print('datast extracted')

!ls

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
from google.colab.patches import cv2_imshow
from PIL import Image
from sklearn.model_selection import train_test_split

with_mask_files=os.listdir('/content/data/with_mask')
print(with_mask_files[0:5])
print(with_mask_files[-5:])

without_mask_files=os.listdir('/content/data/without_mask')
print(without_mask_files[0:5])
print(without_mask_files[-5:])

print('no. of with mask images',len(with_mask_files))
print('no. of without mask images',len(without_mask_files))

"""Creating label for 2 class images
with mask-->1
without mask-->0
"""

with_mask_labels=[1]*len(with_mask_files)
without_mask_labels=[0]*len(without_mask_files)

print(with_mask_labels[0:5])
print(without_mask_labels[0:5])

labels=with_mask_labels+without_mask_labels

print(len(labels))

# printing images
img=mpimg.imread('/content/data/with_mask/with_mask_1894.jpg')
imgplot=plt.imshow(img)
plt.show()

img=mpimg.imread('/content/data/without_mask/without_mask_3743.jpg')
imgplot=plt.imshow(img)
plt.show()

"""**image processing 1.resizing 2. convert images to numpy array**"""

with_mask_path='/content/data/with_mask/'
data=[]

for img_file in with_mask_files:

 image = Image.open(with_mask_path+img_file)
 image = image.resize((128,128))
 image = image.convert('RGB')
 image = np.array(image)
 data.append(image)

without_mask_path='/content/data/without_mask/'


for img_file in without_mask_files:

 image = Image.open(without_mask_path+img_file)
 image = image.resize((128,128))
 image = image.convert('RGB')
 image = np.array(image)
 data.append(image)

len(data)

type(data[0])

# converting imagelist and labellist to numpy array
X=np.array(data)
Y=np.array(labels)

print(X.shape)

print(Y.shape)

print(X)
print(Y)

# train test splitting
X_train, X_test, Y_train, Y_test=train_test_split(X,Y,test_size=0.2,random_state=2)
print(X_train.shape,X_test.shape,Y_train.shape,Y_test.shape)

# scaling data
X_train_scaled=X_train/255
X_test_scaled=X_test/255

"""Building **CNN**"""

import tensorflow as tf
from tensorflow import keras

num_of_classes=2
model=keras.Sequential()

model.add(keras.layers.Conv2D(32,kernel_size=(3,3),activation='relu',input_shape=(128,128,3)))
model.add(keras.layers.MaxPooling2D(pool_size=(2,2)))

model.add(keras.layers.Conv2D(64,kernel_size=(3,3),activation='relu'))
model.add(keras.layers.MaxPooling2D(pool_size=(2,2)))

model.add(keras.layers.Flatten())  #converts 2D data to 1D

model.add(keras.layers.Dense(128,activation='relu'))

model.add(keras.layers.Dropout(0.5))

model.add(keras.layers.Dense(num_of_classes,activation='sigmoid'))

# compile neural network
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['acc'])

#training the neural network
history=model.fit(X_train_scaled,Y_train,validation_split=0.1,epochs=5)

# model evaluation
loss, accuracy=model.evaluate(X_test_scaled,Y_test)
print('Test accuracy=',accuracy)

h=history
#Plot the loss value
plt.plot(h.history['loss'],label='Train loss')
plt.plot(h.history['val_loss'],label='validation Loss')
plt.legend()
plt.show()

#Plot the accuracy value
plt.plot(h.history['acc'],label='Train accuracy')
plt.plot(h.history['val_acc'],label='Validation accuracy')
plt.legend()
plt.show()

input_image_path=input('Path of image to be predicted')
input_image=cv2.imread(input_image_path)
cv2_imshow(input_image)
input_image_resized=cv2.resize(input_image,(128,128))
input_image_scaled=input_image_resized/255
input_image_reshaped=np.reshape(input_image_scaled,[1,128,128,3])
input_prediction=model.predict(input_image_reshaped)
print(input_prediction)
input_pred_label=np.argmax(input_prediction)
print(input_pred_label)
if input_pred_label == 1:
  print('Person is wearing mask')
else:
  print('Person is not wearing mask')