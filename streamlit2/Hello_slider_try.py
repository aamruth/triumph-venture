import streamlit as st
from streamlit_option_menu import option_menu
import datetime
import requests
import pandas as pd

from methods.preprocess_input import preproc_input
list_of_names = pd.read_csv('../data/company_names.csv', encoding='unicode_escape')['0'].to_list()


with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "Prediction Input", "Visualization"],
        icons=["house", "pencil", "graph-up"]
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
                        st.success("The status is still operational, however we think it will be a success!")
                    elif response == 0:
                        st.error("The status is still operational, however we think might be failing...")
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
                    st.success("The status is still operational, however we think it will be a success!")
                elif prediction_value == 0:
                    st.error("The status is still operational, however we think might be failing...")
            else:
                st.error("Error fetching prediction from the API")

elif selected == "Visualization":
    st.title(f"You are now on {selected}")
    # Add your Visualization page content here.

# Close the sidebar
st.sidebar.markdown('</div>', unsafe_allow_html=True)
st.sidebar.markdown('</div>', unsafe_allow_html=True)
st.sidebar.markdown('</div>', unsafe_allow_html=True)
