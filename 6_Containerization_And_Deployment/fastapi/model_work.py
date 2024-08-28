import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Dense,MaxPooling2D,Flatten,Conv2D,Dropout,BatchNormalization
from tensorflow.keras.models import Model
from skin_cancer.model import MyModel
import torch
from transformers import pipeline,Pipeline
import cv2
from typing import Literal
from io import BytesIO
from transformers import AutoProcessor, AutoModel, Pipeline, pipeline
import soundfile
import utils
from modelWork_template import BaseTemplate

class SkinCancerModel_work(BaseTemplate):
    def __init__(self):
        self.IMG_SIZE = 256
        self.output_node = 3
        self.model = None
        self.weight_only_path = os.getcwd()+"/skin_cancer/custom_model.weights.h5"
        self.class_names = ['Melanoma','Benign keratosis-like lesions','Melanocytic nevi']


    def load_model(self):
        self.model = MyModel(input_shape=(self.IMG_SIZE,self.IMG_SIZE,3),output_shape=self.output_node)
        optimizer = tf.keras.optimizers.Adam(learning_rate= 1e-3)
        self.model.compile(loss="categorical_crossentropy",optimizer=optimizer, metrics=["accuracy"])
        
        #need to predict sample image
        input_img = cv2.imread("test_imgs/bkl_902.jpg")
        image_reshape = self.preprocess_img(input_img=input_img)
        self.model.predict(image_reshape)

        self.model.load_weights(self.weight_only_path)
        print("########## skincancer model is loaded ##########")



    def preprocess_img(self,input_img):
        image = tf.cast(input_img, tf.float32)
        image = tf.image.resize(image, [self.IMG_SIZE, self.IMG_SIZE])
        image = (image / 255.0)
        image_reshape = np.array([image])
        return image_reshape
    


    def _predict(self, data_input):
        if self.model is None:
            return None
        preprocessed_img = data_input
        pred_ = self.model.predict(preprocessed_img)
        pred_label = self.class_names[np.argmax(pred_)]
        return pred_label













class CatAndDogModel_work(BaseTemplate):
    def __init__(self):
        self.IMG_SIZE = 150
        self.class_path = os.getcwd()+"/cat_and_dog/class_names.json"
        self.model_path = os.getcwd()+"/cat_and_dog/catAnddog_custom_model.h5"
        self.model = None
        self.class_names = {}



    def load_model(self):
        self.model = load_model(self.model_path)
        with open(self.class_path,"r") as f:
            self.class_names = json.load(f)
        print("########## cat_and_dog model is loaded ##########")
  

    def preprocess_img(self,input_img):
        image = tf.cast(input_img,tf.float32)
        image = tf.image.resize(image, [self.IMG_SIZE,self.IMG_SIZE])
        image /= 255.0
        image_reshape = np.array([image])
        return image_reshape
    


    def _predict(self, data_input):
        if self.model is None or self.class_names == {}:
            print("model is not loaded")
            return None

        preprocessed_img = data_input
        pred_ = self.model.predict(preprocessed_img)
        pred_class = (pred_ > 0.5).astype("int32")
    
        for k,v in self.class_names.items():
            if v == pred_class:
                return k
            
        return None
            

class m_text(BaseTemplate):
    def __init__(self) -> None:
        self.device_name = None
        if torch.backends.mps.is_available():
            self.device_name = "mps" #cuda
        else:
            self.device_name = "cpu"

        self.pipe = None


    def load_model(self):
        self.pipe = pipeline("text-generation",
                    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
                    torch_dtype=torch.bfloat16,
                    device= self.device_name)
        
    def _predict(self,data_input):

        if self.pipe is None:
            return None
        
        prompt = data_input
        temperature = 0.7
        system_prompt = """
        Your name is ML bot and you are a helpful
        chatbot responsible for teaching  machine learning system to your users.
        Always respond in markdown.
        """


        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ] 
        prompt = self.pipe.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        predictions = self.pipe(
            prompt,
            temperature=temperature,
            max_new_tokens=256,
            do_sample=True,
            top_k=50,
            top_p=0.95,
        ) 
        output = predictions[0]["generated_text"].split("</s>\n<|assistant|>\n")[-1]


        return output
        



class m_text(BaseTemplate):
    def __init__(self) -> None:

        self.device_name = None
        if torch.backends.mps.is_available():
            device_name = "mps" #cuda
        else:
            device_name = "cpu"

        self.pipe = None
        self.system_prompt = """
        Your name is ML bot and you are a helpful
        chatbot responsible for teaching  machine learning system to your users.
        Always respond in markdown.
        """
        self.temperature = 0.7
        
    




    def load_model(self):
        self.pipe = pipeline("text-generation",
                model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
                torch_dtype=torch.bfloat16,
                device= self.device_name)




    
    def _predict(self,data_input):
        if self.pipe is None:
            return None
        
        prompt = data_input
        messages = [
        {"role": "system", "content": self.system_prompt},
        {"role": "user", "content": prompt},
    ] 
        prompt = self.pipe.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        predictions = self.pipe(
            prompt,
            temperature=self.temperature,
            max_new_tokens=256,
            do_sample=True,
            top_k=50,
            top_p=0.95,
        ) 
        output = predictions[0]["generated_text"].split("</s>\n<|assistant|>\n")[-1]
        return output





class m_autio(BaseTemplate):
    VoicePresets = Literal["v2/en_speaker_1", "v2/en_speaker_9"]

       
    def __init__(self) -> None:
        self.preset = "v2/en_speaker_9"
        self.processor = None
        self.model = None
        

    def load_audio_model(self) -> tuple[AutoProcessor, AutoModel]:

        #Download the small bark processor which prepares input text prompt for the core model
        processor = AutoProcessor.from_pretrained("suno/bark-small")


        #Download the bark model which will be used to generate the output audio.
        model = AutoModel.from_pretrained("suno/bark-small")

        return processor, model


    def generate_audio(self,
        processor: AutoProcessor,
        model: AutoModel,
        prompt: str,
        preset ) -> tuple[np.array, int]:


        # Preprocess text prompt with a speaker voice preset embedding and return a Pytorch tensor array of tokenized inputs using return_tensors="pt"
        inputs = processor(text=[prompt], return_tensors="pt", voice_preset=preset)


        # Generate an audio array that contains amplitude values of the synthesized audio signal over time.
        output = model.generate(**inputs, do_sample=True).cpu().numpy().squeeze()

        # Obtain the sampling rate from model generating configurations which can be used to produce the audio.
        sample_rate = model.generation_config.sample_rate
        return output, sample_rate



    def load_model(self):
        self.processor,self.model = self.load_audio_model()
        

    
    def _predict(self,data_input):
        if self.model is None:
            return None
        
        prompt = data_input
        output, sample_rate = self.generate_audio(processor=self.processor,model=self.model,prompt=prompt,preset=self.preset)
        output_buffer = utils.audio_array_to_buffer(output,sample_rate)
        return output_buffer


