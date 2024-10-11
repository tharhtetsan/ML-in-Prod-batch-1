from ast import Pass
import os
import numpy as np
import cv2
import mlflow
from tensorflow.keras.preprocessing.image import ImageDataGenerator





import mlflow
MLFLOW_TRACKING_URI = "sqlite:///mlflow_ths.db"
model_name = "cat-dog-classification"
model_stage =  "Staging"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)




def image_read(img_path,img_size = (128,128)):
    image = cv2.imread(img_path)
    resized_img = cv2.resize(image,img_size)
    return resized_img 


def load_test_data(data_path = r"E:\data_share_ths\dataset\cat_and_dog\cats_and_dogs_filtered"):
    test_imgs,test_label = [],[]
    for foldername in os.listdir(data_path+"\\validation"):
        for filename in os.listdir(data_path+"\\validation\\"+foldername):
            
            if foldername.strip() == "cats":
                test_label.append(0)
            else:
                test_label.append(1)
        
            read_path = data_path+"\\validation\\"+foldername+"\\"+filename
            test_imgs.append(image_read(img_path=read_path))


    test_imgs,test_label = np.array(test_imgs),np.array(test_label)
    print("Test images : ",test_imgs.shape)
    print("Test Label : ",test_label.shape)
    
    return test_imgs,test_label



def load_model(model_name,stage):
    model_path = f"models:/{model_name}/{stage}"
    tf_model = mlflow.keras.load_model(model_path)
    return tf_model


def model_predict(test_imgs,tf_model):
    predicted_result = tf_model.predict(test_imgs)
    return predicted_result


def calculate_accuracy(test_labels,predicted_labels):
    pred_labels = [np.argmax(x) for x in predicted_labels]
    accuracy = np.sum(pred_labels==test_labels)/len(test_labels) * 100
    print("accuracy : ",accuracy)


def evaluation_process():

    
    test_imgs,test_label = load_test_data(data_path = r"E:\data_share_ths\dataset\cat_and_dog\cats_and_dogs_filtered")
    tf_model = load_model(model_name=model_name,stage=model_stage)
    predicted_result = model_predict(test_imgs=test_imgs,tf_model=tf_model)
    calculate_accuracy(test_labels=test_label,predicted_labels=predicted_result)


evaluation_process()