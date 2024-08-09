import os
import cv2
import numpy as np
import tensorflow as tf
from CustomModel import MyModel

class ModelWork:
    def __init__(self):
        self.model_path = os.getcwd()+"/training_1/custom_model.weights.h5"
        self.class_list =  ['Melanocytic nevi', 'Melanoma', 'Benign keratosis-like lesions']
        self.input_size = (224,224)
        self.input_shape = (224,224,3)
        self.output_shape = 3
        self.model = None
        self.optimizer = tf.keras.optimizers.Adam(learning_rate=1e-3,decay=1e-4)
        
    def load_Model(self):
        self.model = MyModel(input_shape = self.input_shape,output_shape=self.output_shape)
        self.model.compile(loss="categorical_crossentropy",optimizer=self.optimizer, metrics=["accuracy"])
        self.model.load_weights(self.model_path)

    

    def load_img(self,img_path):
        img = cv2.imread(img_path)
        img =  img/255
        img_resize = cv2.resize(img,self.input_size)
        img_reshape = np.array([img_resize])
        return img_reshape 

    def pred_img(self,input_img):
        pred_ = self.model.predict(input_img)
        pred_label = self.class_list[np.argmax(pred_)]

        return pred_label
