import os
import cv2
import json
import numpy as np
import tensorflow as tf
from CustomModel import MyModel
from tensorflow.keras.models import load_model


class CustomModel_work:
    def __init__(self):
        self.model_path = os.getcwd()+"/training_1/custom_model.weights.h5"
        self.class_list =   ['Melanoma', 'Benign keratosis-like lesions', 'Melanocytic nevi']
        self.IMG_SIZE = 128
        self.input_shape = (self.IMG_SIZE,self.IMG_SIZE,3)
        self.output_shape = 3
        self.model = None
        self.optimizer = tf.keras.optimizers.Adam()
        
    def load_model(self):
        self.model = MyModel(input_shape = self.input_shape,output_shape=self.output_shape)
        self.model.compile(loss="categorical_crossentropy",optimizer=self.optimizer, metrics=["accuracy"])
        self.model.load_weights(self.model_path)

    def preprocess_img(self,input_img):
        image = tf.cast(input_img, tf.float32)
        image = tf.image.resize(image, [self.IMG_SIZE, self.IMG_SIZE])
        image = (image / 255.0)
        image = np.array([image])
        return image

    def pred_img(self,preprocessed_img):
        pred_ = self.model.predict(preprocessed_img)[0]
        max_index = np.argmax(pred_)
        pred_label = self.class_list[max_index]
        pred_confidence = pred_[max_index]*100
        return pred_label,pred_confidence
    

class catAndDogModel_work:
    def __init__(self):
        self.IMG_SIZE = 150
        self.class_path = os.getcwd()+"/cat_And_dog_model/catAndDog_class_names.json"
        self.model_path = os.getcwd()+"/cat_And_dog_model/my_tf_model.h5"
        self.model = None
        self.class_labels = {}

    
    def preprocess_img(self,input_img):
        image = tf.cast(input_img, tf.float32)
        image = tf.image.resize(image, [self.IMG_SIZE, self.IMG_SIZE])
        image /= 255.0  # Normalize if needed
        img_reshape = np.array([image])
        return img_reshape
            
    
    def binary_classification(self,predictions):
        if predictions.shape[1] == 1:  # Binary classification
            predicted_class = (predictions > 0.5).astype("int32")
        else:  # Multi-class classification
            predicted_class = np.argmax(predictions, axis=1)

        for k,v in self.class_labels.items():
            if v == predicted_class:
                return k


    def pred_img(self,preprocessed_img):
        if self.model is None or self.class_labels == {}:
            print("....Please load the model first....")
            return None
        

        predictions = self.model.predict(preprocessed_img)
        predicted_class = self.binary_classification(predictions)
        return predicted_class
        



    def load_model(self):
        self.model = load_model(self.model_path)
        with open(self.class_path, 'r') as f:
            class_names = json.load(f)
        self.class_labels = dict(class_names)
        
                    


