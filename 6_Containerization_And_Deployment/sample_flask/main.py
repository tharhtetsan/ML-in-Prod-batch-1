import tensorflow as tf
from flask import Flask

app = Flask(__name__)

@app.get("/")
def home():
    return "Hello there!"


@app.get("/check_gpu")
def check_gpu():
    gpu_status = tf.test.is_gpu_available()
    return {"gpu_status" : gpu_status}


if __name__ == "__main__":
    app.run(port=8888)

