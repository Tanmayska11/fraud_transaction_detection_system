from fastapi import FastAPI
from app.predict import predict

# 👇 THIS LINE IS CRITICAL
app = FastAPI(title="Fraud Detection API")


@app.get("/")
def home():
    return {"message": "Fraud Detection API Running"}


@app.post("/predict")
def predict_fraud(data: dict):
    return predict(data)