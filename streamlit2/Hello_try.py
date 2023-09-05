import streamlit as st
from streamlit_option_menu import option_menu
import datetime
import requests
#import pandas as pd
#import statsmodels.api as sm
#import matplotlib.pyplot as plt
#from scipy.interpolate import interp1d
#import numpy as np
from methods.prediction_interp import prediction_interp
from methods.preprocess_input import preproc_input

with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "Prediction Input", "Forecast Input", "Visualization"],
        icons=["house", "pencil", "pencil", "graph-up"]
    )

def set_background_image(image_url):
    # css for bg image? -> not working -> opacity
    st.markdown(
        f"""
        <style>
            .stApp {{
                background-image: url("{image_url}");
                background-size: cover;
                background-repeat: no-repeat;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
# sections
if selected == "Home":
    st.title(f"You have selected {selected}")
    st.title(f"Welcome to the Le Wagon Berlin Data Science Batch 1307 Venture Success Prediction Website")
    st.write("We are a team of data scientists from Le Wagon Berlin Data Science Batch 1307, "
             "and we have built this website to help you predict the success of your venture.")
    st.write("Our website uses machine learning algorithms to provide insights into factors that "
             "impact the success of startups and businesses.")
    st.write("You can use the 'Prediction Input' section to input information about your venture, "
             "and we will provide you with a prediction of your venture's success.")
    st.write("Explore the 'Visualization' section to view data visualizations and gain a deeper "
             "understanding of the factors affecting venture success.")
elif selected == "Prediction Input":
    st.title(f"You have selected {selected}")

    # collapsible box
    expand_input = st.checkbox("Expand Prediction Input Details", False)
    if expand_input:
        # Dropdown field for selecting Country
        country_options = [
            'United States', 'Estonia', 'United Kingdom', 'Argentina', 'Hong Kong',
            'Chile', 'Germany', 'France', 'China', 'Canada', 'Australia', 'Romania',
            'Netherlands', 'Sweden', 'Russia', 'Denmark', 'India', 'Singapore',
            'Norway', 'Belgium', 'Ireland', 'Italy', 'Israel', 'Spain', 'Thailand',
            'New Zealand', 'Czech Republic', 'Switzerland', 'Brazil', 'Hungary',
            'Japan', 'Botswana', 'South Korea', 'Nigeria', 'Finland', 'Turkey',
            'Costa Rica', 'Portugal', 'Taiwan', 'Cambodia', 'Colombia', 'Ukraine',
            'Lithuania', 'South Africa', 'Austria', 'Philippines', 'Iceland',
            'Bulgaria', 'Uruguay', 'Croatia', 'Kenya', 'Mexico', 'Jordan', 'Vietnam',
            'Ghana', 'Peru', 'Poland', 'Indonesia', 'Panama', 'Latvia', 'Albania',
            'Uganda', 'Lebanon', 'Greece', 'United Arab Emirates', 'Pakistan',
            'Egypt', 'Slovakia', 'Luxembourg', 'Malaysia', 'Bahamas', 'Armenia',
            'Algeria', 'Moldova', 'Tunisia', 'Nicaragua', 'Tanzania', 'Cyprus',
            'Nepal', 'Bahrain', 'Cameroon', 'Serbia', 'Saudi Arabia', 'Cayman Islands',
            'Brunei', 'El Salvador', 'Ecuador', 'Malta', 'Slovenia', 'Laos',
            'Trinidad and Tobago', 'Morocco', 'Myanmar', 'Bangladesh',
            'Dominican Republic', 'Bermuda', 'Liechtenstein', 'Mozambique', 'Guatemala',
            'Azerbaijan', 'Monaco', 'Zimbabwe', 'Uzbekistan', 'Oman', 'Belarus',
            'Jersey', 'Jamaica', 'Kuwait', 'Mauritius', 'Ivory Coast', 'Somalia',
            'North Macedonia', 'Gibraltar', 'Seychelles', 'Saint Martin'
        ]
        selected_country = st.selectbox("Select Country", country_options)

        # Map selected country to output value
        output_value = "USA" if selected_country == "United States" else "Other"

        # Alphabetically sorted list of Industry Categories
        industry_categories = [
            'Administrative Services', 'Advertising', 'Agriculture and Farming',
            'Apps', 'Artificial Intelligence', 'Clothing and Apparel', 'Commerce and Shopping',
            'Community and Lifestyle', 'Consumer Electronics', 'Consumer Goods', 'Data and Analytics',
            'Design', 'Education', 'Energy', 'Events', 'Financial Services', 'Food and Beverage',
            'Gaming', 'Government and Military', 'Hardware', 'Health Care', 'Information Technology',
            'Internet Services', 'Manufacturing', 'Media and Entertainment', 'Messaging and Telecommunication',
            'Mobile', 'Natural Resources', 'Navigation and Mapping', 'Other', 'Platforms', 'Privacy and Security',
            'Professional Services', 'Real Estate', 'Sales and Marketing', 'Science and Engineering',
            'Software', 'Sports', 'Sustainability', 'Technology', 'Telecommunication', 'Tourism', 'Transportation'
        ]
        # Dropdown field for Industry Category
        industry_category = st.selectbox("Please select your Industry Category", industry_categories)

        # Calculate the default date in the middle of the specified range
        default_founding_date = datetime.date(2005, 1, 1)

        # Date input for Company founding date
        days_in_business = st.number_input("Days in Business", min_value=0)

        # Time between first and Last funding input
        time_between_first_last_funding = st.number_input("Time between first and last funding", min_value=0)

        # Input field for Total Investments in USD
        total_investments = st.number_input("Total Investments (USD)", min_value=0.0)

        # Mapping of slider values to labels
        investment_round_labels = {
            1: 1,
            2: 2,
            3: 3,
            4: 4,
            5: 5,
            6: 6,
            7: 7,
            8: 8
        }

        # Slider for Investment Round (labeled A to H)
        investment_round_value = st.slider("Investment Round", min_value=1, max_value=8, value=1)

        # Display the selected investment round label
        investment_round_label = investment_round_labels[investment_round_value]
        st.write("Investment Round:", investment_round_label)

        # Collect API input
        api_input = {
            "Industry_Group": industry_category,          # string
            "funding_total_usd": total_investments,      # float
            "country_code": output_value,                 # "USA" or "Other"
            "funding_rounds": investment_round_label,     # int 1-8
            "time_between_first_last_funding": time_between_first_last_funding,  # int
            "days_in_business": days_in_business,         # int
        }

        # Make API request
        if st.button("Predict success"):
            url = "https://triumph-venture-fn7ljr6k4q-lz.a.run.app/predict"
            response = requests.get(url, params=preproc_input(api_input))
            print(response)
            print(url)
            result_dict = preproc_input(api_input)

            if (investment_round_value == 1) & (time_between_first_last_funding > 0):
                st.success("It seems like the input data you provided is impossible!")
            else:

                # Print the values of the dictionary
                print(result_dict.values())
                if response.status_code == 200:
                    prediction = response.json()#['status_code']
                    print(prediction)
                    if prediction['value'][0] == 1:
                        st.success("Good job! You have a successful startup!")
                    else:
                        st.success("It seems like your startup is not there yet... Use the feature below for possible forecasts.")
                    #st.success(f"Predicted rate of success: {prediction}")
                else:
                    st.error("Something went wrong :)")
elif selected == "Forecast Input":
    st.title(f"You have selected {selected}")

    # collapsible box
    expand_input = st.checkbox("Expand Forecast Input Details", False)
    if expand_input:
        # Dropdown field for selecting Country
        country_options = [
            'United States', 'Estonia', 'United Kingdom', 'Argentina', 'Hong Kong',
            'Chile', 'Germany', 'France', 'China', 'Canada', 'Australia', 'Romania',
            'Netherlands', 'Sweden', 'Russia', 'Denmark', 'India', 'Singapore',
            'Norway', 'Belgium', 'Ireland', 'Italy', 'Israel', 'Spain', 'Thailand',
            'New Zealand', 'Czech Republic', 'Switzerland', 'Brazil', 'Hungary',
            'Japan', 'Botswana', 'South Korea', 'Nigeria', 'Finland', 'Turkey',
            'Costa Rica', 'Portugal', 'Taiwan', 'Cambodia', 'Colombia', 'Ukraine',
            'Lithuania', 'South Africa', 'Austria', 'Philippines', 'Iceland',
            'Bulgaria', 'Uruguay', 'Croatia', 'Kenya', 'Mexico', 'Jordan', 'Vietnam',
            'Ghana', 'Peru', 'Poland', 'Indonesia', 'Panama', 'Latvia', 'Albania',
            'Uganda', 'Lebanon', 'Greece', 'United Arab Emirates', 'Pakistan',
            'Egypt', 'Slovakia', 'Luxembourg', 'Malaysia', 'Bahamas', 'Armenia',
            'Algeria', 'Moldova', 'Tunisia', 'Nicaragua', 'Tanzania', 'Cyprus',
            'Nepal', 'Bahrain', 'Cameroon', 'Serbia', 'Saudi Arabia', 'Cayman Islands',
            'Brunei', 'El Salvador', 'Ecuador', 'Malta', 'Slovenia', 'Laos',
            'Trinidad and Tobago', 'Morocco', 'Myanmar', 'Bangladesh',
            'Dominican Republic', 'Bermuda', 'Liechtenstein', 'Mozambique', 'Guatemala',
            'Azerbaijan', 'Monaco', 'Zimbabwe', 'Uzbekistan', 'Oman', 'Belarus',
            'Jersey', 'Jamaica', 'Kuwait', 'Mauritius', 'Ivory Coast', 'Somalia',
            'North Macedonia', 'Gibraltar', 'Seychelles', 'Saint Martin'
        ]
        selected_country = st.selectbox("Select Country", country_options)

        # Map selected country to output value
        output_value = "USA" if selected_country == "United States" else "Other"

        # Alphabetically sorted list of Industry Categories
        industry_categories = [
            'Administrative Services', 'Advertising', 'Agriculture and Farming',
            'Apps', 'Artificial Intelligence', 'Clothing and Apparel', 'Commerce and Shopping',
            'Community and Lifestyle', 'Consumer Electronics', 'Consumer Goods', 'Data and Analytics',
            'Design', 'Education', 'Energy', 'Events', 'Financial Services', 'Food and Beverage',
            'Gaming', 'Government and Military', 'Hardware', 'Health Care', 'Information Technology',
            'Internet Services', 'Manufacturing', 'Media and Entertainment', 'Messaging and Telecommunication',
            'Mobile', 'Natural Resources', 'Navigation and Mapping', 'Other', 'Platforms', 'Privacy and Security',
            'Professional Services', 'Real Estate', 'Sales and Marketing', 'Science and Engineering',
            'Software', 'Sports', 'Sustainability', 'Technology', 'Telecommunication', 'Tourism', 'Transportation'
        ]
        # Dropdown field for Industry Category
        industry_category = st.selectbox("Please select your Industry Category", industry_categories)

        # Calculate the default date in the middle of the specified range
        #default_founding_date = datetime.date(2005, 1, 1)

        founding_date = st.date_input("Founding date", format = "YYYY/MM/DD")


        # Mapping of slider values to labels
        investment_round_labels = {
            1: 1,
            2: 2,
            3: 3,
            4: 4,
            5: 5,
            6: 6,
            7: 7,
            8: 8
        }

        # Slider for Investment Round (labeled A to H)
        investment_round_value = st.slider("Investment Round", min_value=1, max_value=8, value=1)

        # Display the selected investment round label
        investment_round_label = investment_round_labels[investment_round_value]
        st.write("Investment Round:", investment_round_label)

        list_of_round_dates = []
        list_of_round_funds = []

        for n_round in range(1,investment_round_label+1):
            round_date = st.date_input(f'Date of round {n_round}', format = "YYYY/MM/DD")
            round_money = st.number_input(f'Round {n_round} Investments (USD)', min_value=0.0)
            list_of_round_dates.append(round_date)
            list_of_round_funds.append(round_money)

                # Collect API input
        api_input = {
            "Industry_Group": industry_category,          # string
            "country_code": output_value,                 # "USA" or "Other"
            "funding_rounds": investment_round_label,     # int 1-8
            "founded_date": founding_date
        }

        # Collect API input
        #api_input = {
        #    "Industry_Group": industry_category,          # string
        #    "funding_total_usd": total_investments,      # float
        #    "country_code": output_value,                 # "USA" or "Other"
        #    "funding_rounds": investment_round_label,     # int 1-8
        #    "time_between_first_last_funding": time_between_first_last_funding,  # int
        #    "days_in_business": days_in_business,         # int
        #}
        url = "https://triumph-venture-fn7ljr6k4q-lz.a.run.app/predict"

        list_of_results = []

        for n in range(0,6):
            check = preproc_input(prediction_interp(list_of_round_dates, list_of_round_funds, api_input).drop(columns=['date']).iloc[0].to_dict())
            response = requests.get(url, params=check)
            list_of_results.append(response.json()['value'][0])

        print(list_of_round_dates)
        print(list_of_round_funds)
        print(prediction_interp(list_of_round_dates, list_of_round_funds, api_input))
        st.success(list_of_results)



        # # Make API request
        # if st.button("Forecast success"):

        #     dates = prediction_interp(list_of_round_dates, list_of_round_funds, api_input)['date']
        #     money_amounts = prediction_interp(list_of_round_dates, list_of_round_funds, api_input)['funding_total_usd']
        #     failure_success = list_of_results

        #     # Find the index of the first success
        #     first_success_index = failure_success.index(1) if 1 in failure_success else len(failure_success)

        #     # Separate data into failure and success portions
        #     failure_dates = dates[:first_success_index]
        #     failure_amounts = money_amounts[:first_success_index]

        #     # Create a scatter plot for failures
        #     fig, ax = plt.subplots()
        #     ax.scatter(failure_dates, failure_amounts, label='Failure', color='red', marker='x')

        #     # # If there are success data points after the first success, separate and plot them
        #     # if first_success_index < len(dates):
        #     #     success_dates = dates[first_success_index]
        #     #     success_amounts = money_amounts[first_success_index]
        #     #     fig = plt.scatter(success_dates, success_amounts, label='Success', color='green', marker='o')

        #     # Adding a legend
        #     #legend = plt.legend()

        #     st.pyplot(fig)

        #     st.success(list_of_results)

elif selected == "Visualization":
    st.title(f"You have selected {selected}")
    # Add your Visualization page content here.

# Close the sidebar
st.sidebar.markdown('</div>', unsafe_allow_html=True)
st.sidebar.markdown('</div>', unsafe_allow_html=True)
st.sidebar.markdown('</div>', unsafe_allow_html=True)
