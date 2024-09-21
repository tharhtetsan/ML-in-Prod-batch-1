## Getting Start with MLflow
```bash
pip install mlflow

# Run locally
mlflow server --host 127.0.0.1 --port 8080

```



### MLflow with Custom database backend
```bash
mlflow server --port 8080 --backend-store-uri sqlite:///mlruns.db

```
