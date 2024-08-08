from fastapi import FastAPI,Body,Request
from schemas import TextModelRequest,TextModelResponse
import uvicorn

app = FastAPI ()


@app.get("/")
def home():
    return "hello"


@app.post("/generate/text", response_model_exclude_defaults = True)
async def serve_text_generateModel(
    request : Request,
    body : TextModelRequest  = Body(...)) -> TextModelResponse:
    generated_text = "hello"
    return TextModelResponse(execution_time=0,result = generated_text)

if __name__ == "__main__":
    uvicorn.run("main:app",port=8000, reload=True)