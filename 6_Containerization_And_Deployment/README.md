### Sample flask

```bash
pipenv shell --dev
python main.py
flask --app main run
```




```bash

docker build . -t simple_flask
docker run --env PORT=8888 simple_flask

python3 -c "import tensorflow as tf; print(tf.__version__)"
python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"



docker run --gpus all --env PORT=8888 -p 8888:8888 simple_flask

```



#### Gunicorn vs Uvicorn 
Gunicorn is an application server that interacts with your web-application using the WSGI protocol. This means that Gunicorn can serve applications written in synchronous web-frameworks such as Flask .

Uvicorn is an application server that supports the ASGI protocol. It also has an option to start and run several worker processes. Nevertheless, Uvicorn's capabilities for handling worker processes are more limited than Gunicorn's.




#### References
- ![Docker gpu](https://docs.docker.com/desktop/gpu/_)
- ![Colima MAC docker runtime](https://github.com/abiosoft/colima)
- ![Apple Silicon GPUs, Docker and Ollama](https://chariotsolutions.com/blog/post/apple-silicon-gpus-docker-and-ollama-pick-two/)


#### Ollama Testing
ollama serve
ollama run mistral