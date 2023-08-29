import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# app.state.model = load_model()

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# http://127.0.0.1:8000/predict?market=Legal&days=89
@app.get("/predict")
def predict(
        market: str,
        days: int
    ):
    """
    Make a single course prediction.
    """

    return {'predict': 'success'}

@app.get("/")
def read_root():
    return {"Hello": "World"}