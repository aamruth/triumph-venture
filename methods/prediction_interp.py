import pandas as pd
import numpy as np


def prediction_interp(date_strings, rounds_funds, inp_params):

    len_r = len(rounds_funds)

    cum_list = [sum(rounds_funds[0:x:1]) for x in range(0, len_r+1)]

    cumulative_sum = cum_list[1:]

    # Convert the list of strings to a DatetimeIndex
    date_index = pd.to_datetime(date_strings, format='%Y-%m-%d')

    founded_date = pd.to_datetime(inp_params["founded_date"], format='%Y-%m-%d')

    # Convert dates to numerical values (e.g., timestamps)
    numeric_dates = date_index.values.astype(np.int64) // 10**9

    # Fit a polynomial to the data
    degree = 1  # Linear interpolation
    coefficients = np.polyfit(numeric_dates, cumulative_sum, degree)

    future_dates = pd.date_range(start=date_index[-1] + pd.DateOffset(months=6), periods=5, freq="6M")

    # Define a date for forecasting
    forecast_dates = pd.to_datetime(future_dates, format='%Y-%m-%d').values.astype(np.int64) // 10**9

    # Evaluate the polynomial at the forecast date
    forecasted_values = [np.polyval(coefficients, forecast_date) for forecast_date in forecast_dates]

    # Create a DataFrame for the forecast
    forecast_df = pd.DataFrame({"date": future_dates, "funding_total_usd": forecasted_values})

    forecast_df['Industry_Group'] = inp_params['Industry_Group']

    forecast_df['country_code'] = inp_params['country_code']

    forecast_df['time_between_first_last_funding'] = (pd.to_datetime(forecast_df['date'], format='%Y-%m-%d') - date_index[0]).dt.days

    forecast_df['days_in_business'] = (pd.to_datetime(forecast_df['date'], format='%Y-%m-%d') - founded_date).dt.days

    number_of_rounds = [*range(inp_params["funding_rounds"]+1,inp_params["funding_rounds"] + 6)]

    forecast_df["funding_rounds"] = number_of_rounds

    print(cumulative_sum)
    print(date_index)
    print(future_dates)

    return forecast_df.reset_index(drop=True)
