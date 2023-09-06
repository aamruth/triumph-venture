import streamlit as st
from streamlit_option_menu import option_menu
import datetime
import requests
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

from methods.preprocess_input import preproc_input
from methods.prediction_interp import prediction_interp

list_of_names = pd.read_csv('data/company_names.csv', encoding='unicode_escape')['0'].to_list()


with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "Prediction Input", "Forecast Input", "Upload CSV"],
        icons=["house", "pencil", "graph-up","filetype-csv"]
    )

def set_background_image(image_url):
    # css for bg image? -> not working -> opacity
    image_url = "https://i.ibb.co/9gxfp5b/istockphoto-619253992-1024x1024.jpg"
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
    #st.title(f"You are now on {selected}")
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
    #st.title(f"You are now on {selected}")
    #search_query = st.text_input("Search for a company")
    search_query = st.selectbox("Select Company", list_of_names)
    # Button to trigger API request
    api_company_url = st.secrets.google_name.key_search

    if st.button("Submit company name"):
        if search_query:
            try:
                # Send the search_query to your API
                payload = {"name": search_query}
                response = requests.get(api_company_url, params=payload)


                result = response.json()
                #print(result)

                if (result['status'] == 'acquired'):
                    st.success("The status of the company is acquired, so it can be considered successful!")
                elif (result['status'] == 'closed'):
                    st.error("The status of the company is closed. Unfortunately, it failed...")
                elif (result['status'] == 'operating'):
                    del result['name']
                    del result['status']
                    #print(result)
                    #print(preproc_input(result))
                    url = st.secrets.google_api.key
                    response = requests.get(url, params=preproc_input(result)).json()['value'][0]
                    if response == 1:
                        st.success("The status is still operational. However, we think it will be a success! For better reference, look at the mean amount of funds for successful projects from your industry.")
                    elif response == 0:
                        st.error("The status is still operational. However, we think it might be failing... Try our forecasting feature to predict future success. Look at the mean amount of funds for successful projects from your industry.")
                    dir_name_streamlit = os.path.dirname(os.path.abspath(__file__))
                    analytics_data_csv = os.path.join(dir_name_streamlit,'data','02_data.csv')
                    df1 = pd.read_csv(analytics_data_csv, encoding='latin1')
                    print(df1.head(10))
                    # Generate some example data

                    df1_software = df1[df1["Industry_Group_x"] == result['Industry_Group']]

                    final_status = df1_software.sort_values('funded_at', ascending=False).groupby('company_name')['status'].last()

                    final_status.name = 'final status'

                    df1_software = df1_software.join(final_status, on='company_name')

                    funds_per_round = df1_software.groupby(by=['final status', 'funding_round_code']).agg(
                        {'time_between_founded_funded_at': "mean", "raised_amount_usd": 'mean'}
                    )
                    # Select the data for final status = acquired
                    acquired_data = funds_per_round.loc['acquired']

                    # Extract the time between founded and funded and raised amount data
                    time_data = acquired_data['time_between_founded_funded_at']
                    raised_data = acquired_data['raised_amount_usd']

                    acquired_cumsum = funds_per_round.loc['acquired'] \
                        .sort_values("time_between_founded_funded_at", ascending=True)['raised_amount_usd'].cumsum()

                    plt.plot(funds_per_round.loc['acquired', 'time_between_founded_funded_at'].sort_values(), acquired_cumsum)


                    plt.scatter(funds_per_round.loc["acquired", 'time_between_founded_funded_at'].sort_values(), acquired_cumsum)

                    funds_per_round = funds_per_round.reset_index()

                    # Extract the time between founded and funded and raised amount data
                    time_data = acquired_data['time_between_founded_funded_at']
                    raised_data = acquired_data['raised_amount_usd']

                    # Create a figure and axes
                    fig, ax = plt.subplots()

                    # Create a bar chart for time data
                    ax.bar(range(len(time_data)), time_data.values)

                    # Set the x-tick labels
                    ax.set_xticks(range(len(time_data)))
                    #ax.set_xticklabels(time_data.index)

                    # Set the y-axis label
                    ax.set_ylabel('Time between founded and funded')

                    # Create a second y-axis for raised amount data
                    ax2 = ax.twinx()
                    #ax2.plot(range(len(raised_data)), raised_data.values, color='red', marker='o')

                    # Set the y-axis label for the second y-axis
                    ax2.set_ylabel('Raised amount (USD)')

                    # Set the title
                    ax.set_title('Funding data for companies with final status = acquired')

                    # Show the plot
                    #plt.show()
                    st.pyplot(fig)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a company name or input your company data manually.")

# Make API request


    # collapsible box
    st.write("Alternatively, you can enter the company data yourself.")
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


        url = st.secrets.google_api.key
        # Make API request
        if st.button("Predict success"):
            url = st.secrets.google_api.key
            response = requests.get(url, params=preproc_input(api_input))
            result_dict = preproc_input(api_input)

            # Print the values of the dictionary
            print(result_dict.values())
            if response.status_code == 200:
                prediction = response.json()#['status_code']
                prediction_value = response.json()['value'][0]
                print(prediction)
                if prediction_value == 1:
                    st.success("We think your startup will be a success! For better reference, look at the mean amount of funds for successful projects from your industry.")
                elif prediction_value == 0:
                    st.error("We think your startup might be failing at the moment... Try our forecasting feature to predict future success. Look at the mean amount of funds for successful projects from your industry.")
                dir_name_streamlit = os.path.dirname(os.path.abspath(__file__))
                analytics_data_csv = os.path.join(dir_name_streamlit,'data','02_data.csv')
                df1 = pd.read_csv(analytics_data_csv, encoding='latin1')
                print(df1.head(10))
                # Generate some example data

                df1_software = df1[df1["Industry_Group_x"] == industry_category]

                final_status = df1_software.sort_values('funded_at', ascending=False).groupby('company_name')['status'].last()

                final_status.name = 'final status'

                df1_software = df1_software.join(final_status, on='company_name')

                funds_per_round = df1_software.groupby(by=['final status', 'funding_round_code']).agg(
                    {'time_between_founded_funded_at': "mean", "raised_amount_usd": 'mean'}
                )
                # Select the data for final status = acquired
                acquired_data = funds_per_round.loc['acquired']

                # Extract the time between founded and funded and raised amount data
                time_data = acquired_data['time_between_founded_funded_at']
                raised_data = acquired_data['raised_amount_usd']

                acquired_cumsum = funds_per_round.loc['acquired'] \
                    .sort_values("time_between_founded_funded_at", ascending=True)['raised_amount_usd'].cumsum()

                plt.plot(funds_per_round.loc['acquired', 'time_between_founded_funded_at'].sort_values(), acquired_cumsum)


                plt.scatter(funds_per_round.loc["acquired", 'time_between_founded_funded_at'].sort_values(), acquired_cumsum)

                funds_per_round = funds_per_round.reset_index()

                # Extract the time between founded and funded and raised amount data
                time_data = acquired_data['time_between_founded_funded_at']
                raised_data = acquired_data['raised_amount_usd']

                # Create a figure and axes
                fig, ax = plt.subplots()

                # Create a bar chart for time data
                ax.bar(range(len(time_data)), time_data.values)

                # Set the x-tick labels
                ax.set_xticks(range(len(time_data)))
                #ax.set_xticklabels(time_data.index)

                # Set the y-axis label
                ax.set_ylabel('Time between founded and funded')

                # Create a second y-axis for raised amount data
                ax2 = ax.twinx()
                #ax2.plot(range(len(raised_data)), raised_data.values, color='red', marker='o')

                # Set the y-axis label for the second y-axis
                ax2.set_ylabel('Raised amount (USD)')

                # Set the title
                ax.set_title('Funding data for companies with final status = acquired')

                # Show the plot
                #plt.show()
                st.pyplot(fig)
            else:
                st.error("Error fetching prediction from the API")
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

        url = "https://triumph-venture-fn7ljr6k4q-lz.a.run.app/predict"

        if st.button("Success forecast"):
            list_of_results = []

            for n in range(0,5):
                check = preproc_input(prediction_interp(list_of_round_dates, list_of_round_funds, api_input).drop(columns=['date']).iloc[n].to_dict())
                response = requests.get(url, params=check)
                list_of_results.append(response.json()['value'][0])

            list_of_future_dates = pd.to_datetime(prediction_interp(list_of_round_dates, list_of_round_funds, api_input)['date'].to_list(), format='%Y-%m-%d').values.astype(np.int64) // 10**9
            list_of_future_dates = list_of_future_dates//(60*60*24)
            list_current_dates = pd.to_datetime(list_of_round_dates, format='%Y-%m-%d').values.astype(np.int64) // 10**9
            list_current_dates = list_current_dates//(60*60*24)
            last_current_date = list_current_dates[-1]
            list_days_till_forecast = list_of_future_dates - last_current_date

            #print(list_of_round_dates)
            #print(list_of_round_funds)
            #st.success(prediction_interp(list_of_round_dates, list_of_round_funds, api_input)['date'])
            #st.success(list_of_results)
            #st.success(list_days_till_forecast)
            #print(prediction_interp(list_of_round_dates, list_of_round_funds, api_input))


            first_success_index = list_of_results.index(1) if 1 in list_of_results else len(list_of_results)

            #print(first_success_index)

            if first_success_index == len(list_of_results):
                st.error("You should significantly increase the funds you receive in the following rounds. Look at the mean amount of funds for successful projects from your industry.")
            elif first_success_index != len(list_of_results):
                st.success(f"You're on the right way. If all goes as before, you can become successful within {list_days_till_forecast[first_success_index]} days. For better reference, look at the mean amount of funds for successful projects from your industry.")

            dir_name_streamlit = os.path.dirname(os.path.abspath(__file__))
            analytics_data_csv = os.path.join(dir_name_streamlit,'data','02_data.csv')
            df1 = pd.read_csv(analytics_data_csv, encoding='latin1')
            #print(df1.head(10))
            # Generate some example data

            df1_software = df1[df1["Industry_Group_x"] == industry_category]

            final_status = df1_software.sort_values('funded_at', ascending=False).groupby('company_name')['status'].last()

            final_status.name = 'final status'

            df1_software = df1_software.join(final_status, on='company_name')

            funds_per_round = df1_software.groupby(by=['final status', 'funding_round_code']).agg(
    {'time_between_founded_funded_at': "mean", "raised_amount_usd": 'mean'})


            # Select the data for final status = acquired
            acquired_data = funds_per_round.loc['acquired'].sort_values(by='time_between_founded_funded_at')

            # Extract the time between founded and funded and raised amount data
            time_data = acquired_data['time_between_founded_funded_at']
            raised_data = acquired_data['raised_amount_usd']

            acquired_cumsum = funds_per_round.loc['acquired'] \
                .sort_values("time_between_founded_funded_at", ascending=True)['raised_amount_usd'].cumsum()

            plt.plot(funds_per_round.loc['acquired', 'time_between_founded_funded_at'].sort_values(), acquired_cumsum)


            plt.scatter(funds_per_round.loc["acquired", 'time_between_founded_funded_at'].sort_values(), acquired_cumsum)

            funds_per_round = funds_per_round.reset_index()

            # Extract the time between founded and funded and raised amount data
            time_data = acquired_data['time_between_founded_funded_at']
            raised_data = acquired_data['raised_amount_usd']
            rounds = []
            for element in list(time_data.index):
                rounds.append(" ".join(element.split("_")).capitalize())


                        # Create a figure and axes
            fig, ax = plt.subplots(figsize=(14,8))

            # Create a bar chart for time data
            ax.barh(range(len(time_data)), time_data.values)

            # Set the y-tick labels
            ax.set_yticks(range(len(time_data)))
            ax.set_yticklabels(rounds, fontsize=16);

            # Set the x-axis label
            ax.set_xlabel('Days lived by Startup', fontsize=16)

            # Create a second y-axis for raised amount data
            ax2 = ax.twiny()
            ax2.scatter(raised_data.values, range(len(raised_data)), color='red', marker='o')

            # Set the y-axis label for the second y-axis
            #ax2.set_xlabel('Raised amount (USD)')

            # Set the title
            ax.set_title('Funds raised by Acquired Startup(USD)', fontsize=16)

            # Show the plot
            plt.show()

            st.pyplot(fig)

        # check = prediction_interp(list_of_round_dates, list_of_round_funds, api_input)

        # #interpolation_data_frame = preproc_input(prediction_interp(list_of_round_dates, list_of_round_funds, api_input).drop(columns=['date']).to_dict())
        # for n in range(0,6):
        #     check = preproc_input(prediction_interp(list_of_round_dates, list_of_round_funds, api_input).drop(columns=['date']).iloc[0].to_dict())
        #     response = requests.get(url, params=check)
        #     list_of_results.append(response.json()['value'][0])

        # #print(list_of_round_dates)
        # #print(list_of_round_funds)
        # #print(list_of_dict)
        # st.success(check)

        # if st.button("Success forecast"):
        #     first_success_index = list_of_results.index(1) if 1 in list_of_results else len(list_of_results)
        #     #print(interpolation_data_frame)
        #     print(first_success_index)
        #     print(list_of_round_dates)
        #     print(list_of_round_funds)
        #     print(check)
            # failure_dates = interpolation_data_frame['date'][first_success_index]
            #print(interpolation_data_frame['date'])
            # if (len(failure_dates) != len(list_of_results)):
            #     new_date = interpolation_data_frame['date'][first_success_index]
            #     st.success(f"The project will be a success after{new_date}!")
            # elif (len(failure_dates) == len(list_of_results)):
            #         st.error("Unfortunatelly your rate of growth isn't enough. In order to be successfull increase the amount of funds...")
            # else:
            #     st.error("Error fetching prediction from the API")

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
# elif selected == "Visualization":
#     st.title(f"You are now on {selected}")
#     dir_name_streamlit = os.path.dirname(os.path.abspath(__file__))
#     analytics_data_csv = os.path.join(dir_name_streamlit,'data','02_data.csv')
#     df1 = pd.read_csv(analytics_data_csv, encoding='latin1')
#     print(df1.head(10))
#     # Generate some example data

#     df1_software = df1[df1["Industry_Group_x"] == 'Software']

#     final_status = df1_software.sort_values('funded_at', ascending=False).groupby('company_name')['status'].last()

#     final_status.name = 'final status'

#     df1_software = df1_software.join(final_status, on='company_name')

#     funds_per_round = df1_software.groupby(by=['final status', 'funding_round_code']).agg(
#         {'time_between_founded_funded_at': "mean", "raised_amount_usd": 'mean'}
#     )
#     # Select the data for final status = acquired
#     acquired_data = funds_per_round.loc['acquired']

#     # Extract the time between founded and funded and raised amount data
#     time_data = acquired_data['time_between_founded_funded_at']
#     raised_data = acquired_data['raised_amount_usd']

#     acquired_cumsum = funds_per_round.loc['acquired'] \
#         .sort_values("time_between_founded_funded_at", ascending=True)['raised_amount_usd'].cumsum()

#     plt.plot(funds_per_round.loc['acquired', 'time_between_founded_funded_at'].sort_values(), acquired_cumsum)


#     plt.scatter(funds_per_round.loc["acquired", 'time_between_founded_funded_at'].sort_values(), acquired_cumsum)

#     funds_per_round = funds_per_round.reset_index()

#     # Extract the time between founded and funded and raised amount data
#     time_data = acquired_data['time_between_founded_funded_at']
#     raised_data = acquired_data['raised_amount_usd']

#     # Create a figure and axes
#     fig, ax = plt.subplots()

#     # Create a bar chart for time data
#     ax.bar(range(len(time_data)), time_data.values)

#     # Set the x-tick labels
#     ax.set_xticks(range(len(time_data)))
#     #ax.set_xticklabels(time_data.index)

#     # Set the y-axis label
#     ax.set_ylabel('Time between founded and funded')

#     # Create a second y-axis for raised amount data
#     ax2 = ax.twinx()
#     #ax2.plot(range(len(raised_data)), raised_data.values, color='red', marker='o')

#     # Set the y-axis label for the second y-axis
#     ax2.set_ylabel('Raised amount (USD)')

#     # Set the title
#     ax.set_title('Funding data for companies with final status = acquired')

#     # Show the plot
#     #plt.show()
#     st.pyplot(fig)


#     @st.cache_resource
#     def get_plotly_data():

#         z_data = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/api_docs/mt_bruno_elevation.csv')
#         z = z_data.values
#         sh_0, sh_1 = z.shape
#         x, y = np.linspace(0, 1, sh_0), np.linspace(0, 1, sh_1)
#         return x, y, z

#     import plotly.graph_objects as go

#     x, y, z = get_plotly_data()

#     fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])
#     fig.update_layout(title='IRR', autosize=False, width=800, height=800, margin=dict(l=40, r=40, b=40, t=40))
#     st.plotly_chart(fig)


#     @st.cache_resource
#     def get_altair_data():

#         return pd.DataFrame(
#                 np.random.randn(200, 3),
#                 columns=['a', 'b', 'c']
#             )

#     import altair as alt

#     df = get_altair_data()

#     c = alt.Chart(df).mark_circle().encode(
#         x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])

#     st.write(c)
elif selected == "Upload CSV":
    st.title(f"You have selected {selected}")

    st.write("Please upload your CSV file below:")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    if uploaded_file is not None:
        try:
            # Read the uploaded CSV file
            df = pd.read_csv(uploaded_file)

            # Display the first few rows of the uploaded data
            st.write("Uploaded data:")
            st.write(df.head())

            # You can perform further data analysis or visualization here

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
# Close the sidebar
st.sidebar.markdown('</div>', unsafe_allow_html=True)
st.sidebar.markdown('</div>', unsafe_allow_html=True)
st.sidebar.markdown('</div>', unsafe_allow_html=True)
