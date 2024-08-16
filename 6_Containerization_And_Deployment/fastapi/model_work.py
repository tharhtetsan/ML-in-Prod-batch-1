import os
import cv2
import numpy as np
import tensorflow as tf
from CustomModel import MyModel

class CustomModelWork:
    def __init__(self):
        self.model_path = os.getcwd()+"/training_1/custom_model.weights.h5"
        self.class_list =   ['Melanoma', 'Benign keratosis-like lesions', 'Melanocytic nevi']
        self.IMG_SIZE = 128
        self.input_shape = (128,128,3)
        self.output_shape = 3
        self.model = None
        self.optimizer = tf.keras.optimizers.Adam()
        
    def load_Model(self):
        self.model = MyModel(input_shape = self.input_shape,output_shape=self.output_shape)
        self.model.compile(loss="categorical_crossentropy",optimizer=self.optimizer, metrics=["accuracy"])
        self.model.load_weights(self.model_path)

    def preprocess_img(self,input_img):
        image = tf.cast(input_img, tf.float32)
        image = tf.image.resize(image, [self.IMG_SIZE, self.IMG_SIZE])
        image = (image / 255.0)
        image = np.array([image])
        return image

    def pred_img(self,input_img):
        pred_ = self.model.predict(input_img)[0]
        max_index = np.argmax(pred_)
        pred_label = self.class_list[max_index]
        pred_confidence = pred_[max_index]*100
        return pred_label,pred_confidence


