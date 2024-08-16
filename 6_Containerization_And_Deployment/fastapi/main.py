import tensorflow as tf
from fastapi import FastAPI
from fastapi import Query, Response, status, UploadFile
import io
import os
from PIL import Image
import uvicorn
import numpy as np
from contextlib import asynccontextmanager
from model_work import CustomModel_work,catAndDogModel_work



ml_models = {}

@asynccontextmanager
async def lifesapn(app : FastAPI):
    """
    device_name = None
    if torch.backends.mps.is_available():
        device_name = "cpu"
    else:
        device_name = "cpu"

    ml_models["text"] = m_text.load_text_model(device_name= device_name)
    """
    
    custom_model = CustomModel_work()
    custom_model.load_model()
    
    catAnddog_model = catAndDogModel_work()
    catAnddog_model.load_model()

    ml_models["custom_skincancer_model"] = custom_model

    ml_models["cat_and_dog_model"] = catAnddog_model


    yield
    ml_models.clear()



app = FastAPI(lifespan= lifesapn)

@app.get("/")
def home():
    return "Hello there!"


@app.get("/check_gpu")
def check_gpu():
    gpu_status = tf.test.is_gpu_available()
    return {"gpu_status" : gpu_status}

@app.post("/predict_skincancer" )
async def server_image_to_video_model_controller(file: UploadFile):
    request_object_content = await file.read()
    image = Image.open(io.BytesIO(request_object_content))

    np_image = np.asanyarray(image)

    custom_model = (ml_models["custom_skincancer_model"])
    input_image = custom_model.preprocess_img(np_image)
    pred_label,conf = custom_model.pred_img(input_img=input_image)
    pred_response = {"predicted_result": pred_label,"confidence":conf}

    return pred_response


@app.post("/predict_catAnddog" )
async def server_image_to_video_model_controller(file: UploadFile):
    request_object_content = await file.read()
    image = Image.open(io.BytesIO(request_object_content))

    np_image = np.asanyarray(image)
    catdog_model = (ml_models["cat_and_dog_model"])
    input_image = catdog_model.preprocess_img(np_image)
    pred_label = catdog_model.pred_img(input_image)
    pred_response = {"predicted_result": pred_label}

    return pred_response


if __name__ == "__main__":
    
    uvicorn.run("main:app", host='0.0.0.0', port=8888, reload=True)
