from fastapi import FastAPI, UploadFile
import uvicorn
import tensorflow as tf
from contextlib import asynccontextmanager
from model_work import CatAndDogModel_work, SkinCancerModel_work,m_text,m_autio
from PIL import Image
import io
import numpy as np
import torch

from fastapi.responses import StreamingResponse
from fastapi import Query,status,Response



ml_models = {}

@asynccontextmanager
async def lifespan (app : FastAPI):

    CatAndDogModel_obj = CatAndDogModel_work()
    CatAndDogModel_obj.load_model()
    ml_models["cat_and_dog_model"] = CatAndDogModel_obj


    #skincancer_obj = SkinCancerModel_work()
    #skincancer_obj.load_model()
    #ml_models["skincancer_model"] = skincancer_obj
    

    audio_obj = m_autio()
    audio_obj.load_model()
    ml_models["m_audio"] = audio_obj

    yield
    ml_models.clear()
    


app = FastAPI(lifespan=lifespan)



@app.get("/")
def home():
    return "hello"


@app.get("/check_gpu")
def check_gpu():
    tf_gpu_status = tf.test.is_gpu_available()
    troch_gpu_status  = torch.backends.mps.is_available()
    _response =  {"tf_gpu_status" : tf_gpu_status,
                  "torch_gpu_status" : troch_gpu_status}

    return _response


@app.post("/predict_catdog")
async def serve_catAnddo(file : UploadFile):
    object_content = await file.read()
    image = Image.open(io.BytesIO(object_content))

    np_image = np.asanyarray(image)

    cat_and_dog_model_obj = ml_models["cat_and_dog_model"]

    input_image =cat_and_dog_model_obj.preprocess_img(np_image)
    pred_class = cat_and_dog_model_obj._predict(input_image)
    response_ = {"predicted_label ": pred_class}
    return response_



@app.post("/predict_skincancer")
async def serve_catAnddo(file : UploadFile):
    object_content = await file.read()
    image = Image.open(io.BytesIO(object_content))

    np_image = np.asanyarray(image)

    skincancer_obj = ml_models["skincancer_model"]
    input_image =skincancer_obj.preprocess_img(np_image)
    pred_class = skincancer_obj._predict(input_image)
    response_ = {"predicted_label ": pred_class}
    return response_




@app.get("/text_audio",
          responses={status.HTTP_200_OK:{"content" : {"audio/wav":{}}}},
          response_class=StreamingResponse,)

def serve_text_to_audio(prompt = Query(...),prest : m_autio.VoicePresets = Query(default="v2/en_speaker_9")):
    #print("user prompt : ",prompt)
    #print("prest : ",prest)

    output_buffer = ml_models["m_audio"]._predict(data_input = prompt)
    
    return StreamingResponse(output_buffer, media_type="audio/wav")






if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8888, reload=True)
