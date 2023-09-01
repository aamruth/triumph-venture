import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from triumphventure.logic.model import load_model
from triumphventure.logic.custom_transformers import columnDropperTransformer

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
        Industry_Group: str,
        days_in_business: int,
        funding_rounds: int,
        funding_total_usd: int,
        country_usa: bool,
        time_between_first_last_funding: int,
    ):
    """
    Make a single course prediction.
    """
    # find difference between founding_date and todays date
    # founding_date - timezone.now()

    print("reached")

    model = app.state.model
    print(locals())
    df = pd.DataFrame(locals(), index=[0])
    value = model.predict(df)
    print(value)

    return value

@app.get("/")
def read_root():
    return {"Hello": "World"}


predict('Software',100,2,100,'Others',100)
