#### sample_fastapi

```bash
docker build . -t sample_fastapi

docker run -p 8888:8888 --env PORT=8888 sample_fastapi
```