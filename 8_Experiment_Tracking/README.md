## Getting Start with MLflow
```bash
pip install mlflow

# Run locally
mlflow server --host 127.0.0.1 --port 8080

```



### MLflow with Custom database backend
```bash
mlflow ui  --host 127.0.0.1 --port 8080 --backend-store-uri sqlite:///mlruns.db


mlflow ui  --host 127.0.0.1 --port 8080 --backend-store-uri postgresql+pg8000://DB_USERNAME:DB_PASSWORD@DB_IP:5432/DB_NAME

```
