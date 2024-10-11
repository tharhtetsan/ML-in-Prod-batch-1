import os
import numpy as np
import mlflow
from mlflow.models.signature import infer_signature

import tensorflow as tf
from tensorflow.keras.layers import Dense,GlobalAveragePooling2D,Dropout,Flatten,Conv2D,Input,MaxPooling2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.python.saved_model import signature_constants
from tensorflow.keras.callbacks import LearningRateScheduler
from tensorflow.keras.models import Model
from tensorflow.keras.applications import ResNet50
from sklearn.model_selection import train_test_split


from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
from hyperopt.pyll import scope
from prefect import flow,task
from prefect.task_runners import SequentialTaskRunner
#prefect orion start


img_width,img_height = 256,256
model_input = (img_width,img_height,3)
img_size = (img_width,img_height)
batch_size = 16
epochs = 0






def create_model(input_size,drop_rate,num_perceptron,num_layers,num_output):

    base_model = ResNet50(
    include_top=False,
    input_shape=input_size,
    weights='imagenet')

    x=base_model.output
    x = GlobalAveragePooling2D()(x)
    for i in range(num_layers):
        x = Dense(num_perceptron, activation="relu")(x)
        x = Dropout(drop_rate)(x)
        num_perceptron = num_perceptron+num_perceptron

    preds=Dense(num_output,activation='softmax')(x)
    model=Model(inputs=base_model.input,outputs=preds)

    return model



def image_read(img_path,img_size = (256,256)):
    import cv2
    image = cv2.imread(img_path)
    resized_img = cv2.resize(image,img_size)
    return resized_img 




#@task
def load_data_generator(data_path = r"E:\data_share_ths\dataset\cat_and_dog\cats_and_dogs_filtered"):
    train_imgs,train_label= [],[]
    
    for foldername in os.listdir(data_path+"\\train"):
        for filename in os.listdir(data_path+"\\train\\"+foldername):
            if foldername.strip() == "cats":
                train_label.append(0)
            else:
                train_label.append(1)

            read_path = data_path+"\\train\\"+foldername+"\\"+filename
            train_imgs.append(image_read(img_path=read_path))
        
    for foldername in os.listdir(data_path+"\\validation"):
        for filename in os.listdir(data_path+"\\validation\\"+foldername):
            if foldername.strip() == "cats":
                train_label.append(0)
            else:
                train_label.append(1)
        
            read_path = data_path+"\\validation\\"+foldername+"\\"+filename
            train_imgs.append(image_read(img_path=read_path))

    train_imgs,val_imgs = train_test_split(train_imgs,train_size=0.9,random_state = 10)
    train_label,val_lable = train_test_split(train_label,train_size=0.9,random_state = 10)
    
    
    train_imgs,train_label = np.array(train_imgs),np.array(train_label)
    val_imgs,val_lable = np.array(val_imgs),np.array(val_lable)

    print("train images : ",train_imgs.shape)
    print("train Label : ",train_label.shape)
    print("val images : ",train_imgs.shape)
    print("val Label : ",train_label.shape)


    return train_imgs,train_label,val_imgs,val_lable


#@task
def train_model_search(train_imgs,train_label,val_imgs,val_lable):
    
    drop_rate = [0.5,0.35,0.2,0.5]
    num_perceptron=[512,256,128]
    learning_rate = [0.01,0.001,0.0001,0.00001]
    max_num_layers = 4 
    num_output=1
   
    max_epochs = 30

    search_space = {
    "num_layers" : scope.int(hp.quniform("num_layers",2,max_num_layers,1)),
    "num_perceptron" : scope.int(hp.choice("num_perceptron",num_perceptron)),
    "drop_rate" : hp.choice("drop_rate",drop_rate),
    "learning_rate" : hp.choice("learning_rate",learning_rate),
    "epochs" : scope.int(hp.quniform("epochs",2,max_epochs,1)),
    }

    def objective(params):
        with mlflow.start_run():
            print("####train_model_search####")  
            mlflow.set_tag("developer","tharhtet")
            mlflow.log_params(params)

            epochs = params["epochs"]

            """
            datagen = ImageDataGenerator(
                        featurewise_center=True,
                        featurewise_std_normalization=True,
                        rotation_range=20,
                        width_shift_range=0.2,
                        height_shift_range=0.2,
                        horizontal_flip=True)
            train_generator = datagen.flow(train_imgs, train_label,shuffle=True,batch_size=32,subset='training')
            val_generator = datagen.flow(train_imgs, train_label,shuffle=True,batch_size=8, subset='validation')
            """

            steps_per_epoch=int(len(train_imgs) / batch_size)
            model = create_model(input_size = model_input,
                drop_rate =params["drop_rate"],
                num_perceptron=params["num_perceptron"],
                num_layers=params["num_layers"],
                num_output=num_output)
      
             
            model.compile(loss='binary_crossentropy',
                        optimizer=Adam(lr=params["learning_rate"]),
                        metrics=['accuracy'])


            print(model.summary())
            
            history = model.fit(train_imgs,train_label,
                                steps_per_epoch=steps_per_epoch, epochs=epochs,
                                batch_size = batch_size,
                                validation_data = (val_imgs,val_lable),
                                validation_steps=int(len(val_imgs) / 8))

            train_acc = history.history['accuracy']
            val_acc = history.history['val_accuracy']
            train_loss = history.history['loss']
            val_loss = history.history['val_loss']
            final_valLoss = 0
            for t_acc,t_loss,v_acc,v_loss in zip(train_acc,train_loss,val_acc,val_loss):
                mlflow.log_metric("train_accuracy", t_acc)
                mlflow.log_metric("train_loss", t_loss)
                mlflow.log_metric("val_accuracy", v_acc)
                mlflow.log_metric("val_loss", v_loss)
                final_valLoss = v_loss
            #results[0]=val_loss, results[1] = val_acc
            

            test_img = np.array([val_imgs[0]])
            signature = infer_signature(test_img, model.predict(test_img,batch_size=1))
            mlflow.keras.log_model(model, "scc_cnn", signature=signature)

        return {'loss' :final_valLoss,'status':STATUS_OK }

    best_result = fmin(
    fn=objective,
    space=search_space,
    algo=tpe.suggest,
    max_evals=3,
    trials=Trials()
    )

    return best_result

#@task
def train_best_model(best_model_config:dict,train_imgs,train_label,val_imgs,val_lable):
    print("#### train the best model ####")  
    mlflow.set_tag("developer","tharhtet")
    mlflow.log_params(best_model_config)
    epochs = int(best_model_config["epochs"])
    model = create_model(input_size = model_input,
            drop_rate =best_model_config["drop_rate"],
            num_perceptron=best_model_config["num_perceptron"],
            num_layers=best_model_config["num_layers"],
            num_output=1)
    
            
    model.compile(loss='binary_crossentropy',
                optimizer=Adam(lr=best_model_config["learning_rate"]),
                metrics=['accuracy'])


    steps_per_epoch=int(len(train_imgs) / batch_size)

    history = model.fit(train_imgs,train_label,
                                steps_per_epoch=steps_per_epoch, epochs=epochs,
                                batch_size = batch_size,
                                validation_data = (val_imgs,val_lable),
                                validation_steps=int(len(val_imgs) / 8))

    train_acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    train_loss = history.history['loss']
    val_loss = history.history['val_loss']
    final_valLoss = 0
    for t_acc,t_loss,v_acc,v_loss in zip(train_acc,train_loss,val_acc,val_loss):
        mlflow.log_metric("train_accuracy", t_acc)
        mlflow.log_metric("train_loss", t_loss)
        mlflow.log_metric("val_accuracy", v_acc)
        mlflow.log_metric("val_loss", v_loss)
        final_valLoss = v_loss
    #results[0]=val_loss, results[1] = val_acc
    

    test_img = np.array([val_imgs[0]])
    signature = infer_signature(test_img, model.predict(test_img,batch_size=1))
    mlflow.keras.log_model(model, "best_cnn_model", signature=signature)









#@flow
def prefect_proj():
    mlflow.set_tracking_uri("sqlite:///mlflow_ths.db")
    mlflow.set_experiment("ths-cat-and-dog-new-exp")
    train_imgs,train_label,val_imgs,val_lable = load_data_generator(data_path =  r"E:\data_share_ths\dataset\cat_and_dog\cats_and_dogs_filtered")
    best_model_config = train_model_search(train_imgs,train_label,val_imgs,val_lable)
    
    #train_best_model(best_model_config,train_imgs,train_label,test_imgs,test_label)


prefect_proj()
