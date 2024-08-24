from tensorflow.keras.layers import Dense,MaxPooling2D,Flatten,Conv2D,Dropout,BatchNormalization
from tensorflow.keras.models import Model
import keras

class MyModel(Model):
    def __init__(self,input_shape, output_shape):
        super().__init__()
        self.input_layer = Conv2D(32, kernel_size=(3,3), activation='relu', padding='same', input_shape= input_shape,kernel_regularizer='l1')
        
        self.conv2d_32 = Conv2D(32, kernel_size=(3,3), activation='relu',)
        self.conv1d_64 = Conv2D(64, kernel_size=(3,3), activation='relu', padding='same')
        self.conv2d_64 = Conv2D(64, kernel_size=(3,3), activation='relu')
        self.conv2d_128 = Conv2D(128, kernel_size=(3,3), activation='relu', padding='same')
        self.maxPool_2d =  MaxPooling2D(pool_size=(2,2))
        
        self.f1 = Flatten()
        self.d1 = Dense(256, activation='relu',kernel_regularizer='l1')
        self.dropout_1 = Dropout(0.3)
        self.d2 = Dense(256, activation='relu')
        self.dropout_2 = Dropout(0.3)
        self.d3 = Dense(128, activation='relu')

        

        self.output_layer = Dense(output_shape, activation="sigmoid")
    
    def call(self, x):
        x = self.input_layer(x)
        x = self.conv2d_32(x)
        x = self.maxPool_2d(x)
        x = self.conv1d_64(x)
        x = self.conv2d_64(x)
        x = self.maxPool_2d(x)
        x = self.conv2d_128(x)
        x = self.f1(x)
        x = self.d1(x)
        x = self.dropout_1(x)
        x = self.d2(x)
        x = self.dropout_2(x)
        x = self.d3(x)
        x = self.output_layer(x)
        return x
