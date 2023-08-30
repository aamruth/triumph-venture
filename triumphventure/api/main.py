import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from triumphventure.logic.model import load_model

app = FastAPI()

app.state.model = load_model()

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# http://127.0.0.1:8000/predict?funding_rounds=1&time_between_first_last_funding=89&days_in_business=300&country_usa=true
@app.get("/predict")
def predict(
        funding_rounds: int,
        time_between_first_last_funding: int,
        days_in_business: int,
        country_usa: bool,
    ):
    """
    Make a single course prediction.
    """
    model = app.state.model
    df = pd.DataFrame(locals(), index=[0])
    value = model.predict(df)

    return value

@app.get("/")
def read_root():
    return {"Hello": "World"}
