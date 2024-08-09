import tensorflow as tf
from fastapi import FastAPI
from fastapi import Query, Response, status, UploadFile
import io
import os
from PIL import Image
import uvicorn
import numpy as np



app = FastAPI()

@app.get("/")
def home():
    return "Hello there!"


@app.get("/check_gpu")
def check_gpu():
    gpu_status = tf.test.is_gpu_available()
    return {"gpu_status" : gpu_status}

@app.post("/predict_image" )
async def server_image_to_video_model_controller(file: UploadFile):
    input_size= (128,128)

    request_object_content = await file.read()
    image = Image.open(io.BytesIO(request_object_content))

    np_image = np.asanyarray(image)

    
    return {"image : ",np_image.shape}



if __name__ == "__main__":
    
    uvicorn.run("main:app", host='0.0.0.0', port=8888, reload=True)
