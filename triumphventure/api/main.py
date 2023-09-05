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

# http://127.0.0.1:8000/predict?Industry_Group_Other=0&Industry_Group_Health_Care=0&days_in_business=350&funding_rounds=2&country_code=USA&funding_total_usd=1000&time_between_first_last_funding=100&Industry_Group_Information_Technology=1&Industry_Group_Commerce_and_Shopping=0&Industry_Group_Community_and_Lifestyle=0&Industry_Group_Software=0&Industry_Group_Biotechnology=0&Industry_Group_Internet_Services=0
# {'funding_total_usd ': 0.0, 'country_code': 'USA', 'funding_rounds': 'A', 'time_between_first_last_funding': 0, 'days_in_business': 0, 'Industry_Group_Biotechnology': 0.0, 'Industry_Group_Commerce and Shopping': 0.0, 'Industry_Group_Community and Lifestyle': 0.0, 'Industry_Group_Health Care': 0.0, 'Industry_Group_Information Technology': 0.0, 'Industry_Group_Internet Services': 0.0, 'Industry_Group_Other': 0.0, 'Industry_Group_Software': 0.0}
# http://127.0.0.1:8000/predict?funding_rounds=1&time_between_first_last_funding=89&days_in_business=300&country_usa=true
@app.get("/predict")
def predict(
        funding_total_usd,
        country_code,
        funding_rounds,
        time_between_first_last_funding,
        days_in_business,
        Industry_Group_Biotechnology,
        Industry_Group_Commerce_and_Shopping,
        Industry_Group_Community_and_Lifestyle,
        Industry_Group_Health_Care,
        Industry_Group_Information_Technology,
        Industry_Group_Internet_Services,
        Industry_Group_Other,
        Industry_Group_Software
    ):
    """
    Make a single course prediction.
    """
    # find difference between founding_date and todays date
    # founding_date - timezone.now()

    print("reached")

    print(locals())
    df = pd.DataFrame({
        'funding_total_usd': funding_total_usd,
        'country_code': country_code,
        'funding_rounds': funding_rounds,
        'time_between_first_last_funding': time_between_first_last_funding,
        'days_in_business': days_in_business,
        'Industry_Group_Biotechnology': Industry_Group_Biotechnology,
        'Industry_Group_Commerce and Shopping': Industry_Group_Commerce_and_Shopping,
        'Industry_Group_Community and Lifestyle': Industry_Group_Community_and_Lifestyle,
        'Industry_Group_Health Care': Industry_Group_Health_Care,
        'Industry_Group_Information Technology': Industry_Group_Information_Technology,
        'Industry_Group_Internet Services': Industry_Group_Internet_Services,
        'Industry_Group_Other': Industry_Group_Other,
        'Industry_Group_Software': Industry_Group_Software,
    }
    , index=[0])
    model = app.state.model
    value = model.predict(df)
    print(value)

    return {"value": value.tolist()}

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/search")
def read_root(
        name: str
):
    companies = pd.read_csv('./triumphventure/data/companies.csv', encoding="utf-8", encoding_errors='replace')
    company = companies[companies["name"] == name].iloc[0]
    return {
        "name": company["name"],
        "status": company["status"],
        "Industry_Group": company["Industry_Group"],
        "country_code": company["country_code"],
        "funding_total_usd": float(company["funding_total_usd"]),
        "days_in_business": float(company["days_in_business"]),
        "funding_rounds": float(company["funding_rounds"]),
        "time_between_first_last_funding": float(company["time_between_first_last_funding"]),
    }


@app.get("/search_rounds")
def read_root(
        name: str
):
    companies = pd.read_csv('./triumphventure/data/companies.csv', encoding="utf-8", encoding_errors='replace')
    rounds = pd.read_csv('./triumphventure/data/rounds.csv', encoding="utf-8", encoding_errors='replace')
    company = companies[companies["name"] == name].fillna('').iloc[0]
    company_rounds = rounds[rounds["company_name"] == name].fillna('')
    all_rounds = []
    for _, round in company_rounds.iterrows():
        all_rounds.append({
            "raised_amount_usd": round["raised_amount_usd"],
            "round_type": round["funding_round_type"],
            "funded_at": round["funded_at"],
            "funding_round_code": round["funding_round_code"],
        })
    return {
        "name": company["name"],
        "status": company["status"],
        "Industry_Group": company["Industry_Group"],
        "country_code": company["country_code"],
        "funding_total_usd": company["funding_total_usd"],
        "days_in_business": company["days_in_business"],
        "funding_rounds": company["funding_rounds"],
        "time_between_first_last_funding": company["time_between_first_last_funding"],
        "rounds": all_rounds,
    }
