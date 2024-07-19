from pydantic import BaseModel
from  typing import Literal

class ModelRequest(BaseModel):
    prompt : str
    
class TextModelRequest(ModelRequest):
    model: Literal["tinyllama", "gemma2b"]
    temperature: float = 0.0
