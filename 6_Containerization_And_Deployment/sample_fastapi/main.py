from fastapi import FastAPI, UploadFile
import uvicorn


app = FastAPI()


@app.get("/")
def home():
    return "hello"


if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8888, reload=True)
