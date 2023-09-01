###########################################################################################################
###########################################################################################################
###########################################################################################################
######## authors = Aamruth Shankar, India Dearlove, Deepa Tamraparani, Yan Brodskyi, Timothy Williams
######## insitution = Le Wagon Berlin Data-Science-Batch-1307
######## website = <---- ADD GITHUB PROFILES OF MEMBERS -->
######## version = 1.0
######## status = WIP
######## deployed at =  https://1307-venture-success-prediction.streamlit.app/
###########################################################################################################
###########################################################################################################
###########################################################################################################


import streamlit as st
import requests
import datetime
from PIL import Image
# Set the page width
st.set_page_config(layout="wide")

# Include the external CSS file
st.markdown('<link rel="stylesheet" type="text/css" href="styles.css">', unsafe_allow_html=True)

# Create the main content
st.title("Venture Success Prediction Project Batch-1307")

# Create the sidebar
sidebar_width = 0.3  #0.3 ratio

# Apply the CSS class to the sidebar content
st.sidebar.markdown('<h2 class="data-input-title" style="padding-top: 0;">Data Input</h2>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-container">', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-content">', unsafe_allow_html=True)

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

selected_country = st.sidebar.selectbox("Select Country", country_options)
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
industry_category = st.sidebar.selectbox("Please select your Industry Category", industry_categories)

# Calculate the default date in the middle of the specified range
default_founding_date = datetime.date(2005, 1, 1)

# Date input for Company founding date
#founding_date = st.sidebar.date_input("Company founding date", value=default_founding_date, min_value=datetime.date(1995, 1, 1), max_value=datetime.date(2023, 8, 31))

# Date input for Time between First and Last Funding
#time_between_funding_dates = st.sidebar.date_input("Time between First and Last Funding", value=default_founding_date, min_value=datetime.date(1995, 1, 1), max_value=datetime.date(2023, 8, 31))

# Date input for Days in Business
#days_in_business = st.sidebar.date_input("Days in Business", value=default_founding_date, min_value=datetime.date(1995, 1, 1), max_value=datetime.date(2023, 8, 31))
days_in_business = st.sidebar.number_input("Days in Business", min_value=0)

# Check if the input date is within the defined range
#if founding_date < datetime.date(1995, 1, 1) or founding_date > datetime.date(2023, 8, 31):
#    st.sidebar.warning("Date not in defined range between 1995 and 2023")

# Input field for Total Investments in USD
total_investments = st.sidebar.number_input("Total Investments (USD)", min_value=0.0)

# Mapping of slider values to labels
investment_round_labels = {
    1: 'A',
    2: 'B',
    3: 'C',
    4: 'D',
    5: 'E',
    6: 'F',
    7: 'G',
    8: 'H'
}

# Slider for Investment Round (labeled A to H)
investment_round_value = st.sidebar.slider("Investment Round", min_value=1, max_value=8, value=1)

# Display the selected investment round label
investment_round_label = investment_round_labels[investment_round_value]
st.sidebar.write("Investment Round:", investment_round_label)


# Collect API input
api_input = {
    "Industry_Group": industry_category,          #string
    "days_in_business": days_in_business,         #int
    "funding_total_usd ": total_investments,      #float
    "funding_rounds": investment_round_label,     #int 1-8
    "country_code": output_value                  #"USA" or "Other"
}

# Make API request
if st.sidebar.button("Predict success"):
    url = "http://127.0.0.1:8000/predict?funding_rounds=1&time_between_first_last_funding=89&days_in_business=300&country_usa=true"
    response = requests.get(url, params=api_input)

    if response.status_code == 200:
        prediction = response.json()['success']
        st.success(f"Predicted rate of success: {prediction:.2f}")
    else:
        st.error("Error fetching prediction from the API")

st.sidebar.markdown('</div>', unsafe_allow_html=True)
st.sidebar.markdown('</div>', unsafe_allow_html=True)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Main content of the page
# Main content of the page with background image

# Main content of the page with background image
st.markdown(
    '<div style="background-image: url(\'https://fastly.picsum.photos/id/277/536/354.jpg\'); background-size: cover;">',
    unsafe_allow_html=True
)
st.write("Content???")


st.markdown('</div>', unsafe_allow_html=True)
