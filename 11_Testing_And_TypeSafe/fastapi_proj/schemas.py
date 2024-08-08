from pydantic import BaseModel,Field
from  typing import Annotated,Literal


class ModelRequest(BaseModel):
    prompt : str
    
class TextModelRequest(ModelRequest):
    model: Literal["tinyllama", "gemma2b"]
    temperature: float = 0.0


class TextModelResponse(BaseModel):
    execution_time : int = 0
    result : str =""