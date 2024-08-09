```bash
pipenv run fastapi dev main.py

docker build . -t fastapi

docker run --env PORT=8888 -p 8888:8888 fastapi

```