## Getting Start with MLflow
```bash
pip install mlflow

# Run locally
mlflow server --host 127.0.0.1 --port 8080

```



### MLflow with Custom database backend
```bash
mlflow ui  --host 127.0.0.1 --port 8080 --backend-store-uri sqlite:///mlruns.db


## Postgres SQL backend with  pg8000 driver
mlflow ui  --host 127.0.0.1 --port 8080 --backend-store-uri postgresql+pg8000://DB_USERNAME:DB_PASSWORD@DB_IP:5432/DB_NAME

## Postgres SQL backend with  psycopg2 driver
mlflow ui  --host 127.0.0.1 --port 8080 --backend-store-uri postgresql+psycopg2://postgres:admin@35.238.169.194:5432/mlflow


mlflow ui  --host 127.0.0.1 --port 8080 --default-artifact-root YOUR_BUCKED_NAME --backend-store-uri postgresql+psycopg2://postgres:admin@Database_IP:5432/mlflow


```
