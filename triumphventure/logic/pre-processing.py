import pandas as pd
import matplotlib.pyplot as plt
import ydata_profiling as pp
import seaborn as sns
import warnings
import os

def pre_processing():

    data = pd.read_csv('../data/Start_up_data.csv', encoding= 'unicode_escape')

    data = data.iloc[:49438]

    data.columns = data.columns.str.replace(' ', '')
    data.columns = data.columns.str.strip()
    data.columns = data.columns.str.replace('[^a-zA-Z0-9_]', '', regex=True)
    data = data.dropna(subset=['name'])
    data['homepage_url'] = data['homepage_url'].fillna('Website not Provided')
    columns_to_remove = [
        'permalink', 'state_code', 'region', 'city', 'founded_month',
        'founded_quarter', 'founded_year', 'seed', 'venture', 'equity_crowdfunding',
        'undisclosed', 'convertible_note', 'debt_financing', 'angel', 'grant',
        'private_equity', 'post_ipo_equity', 'post_ipo_debt', 'secondary_market',
        'product_crowdfunding', 'round_A', 'round_B', 'round_C', 'round_D', 'round_E',
        'round_F', 'round_G', 'round_H'
    ]
    data = data.drop(columns=columns_to_remove, axis=1)

    data.columns

    data = data.dropna(subset=['market'])
    data = data.dropna(subset=['status'])

    data['funding_total_usd'] = data['funding_total_usd'].str.replace(',', '')
    data.loc[data['country_code'] != 'USA', 'country_code'] = 'Other'

    admin_services = str('Employer Benefits Programs, Human Resource Automation, Corporate IT, Distribution, Service Providers, Archiving Service, Call Center, Collection Agency, College Recruiting, Courier Service, Debt Collections, Delivery, Document Preparation, Employee Benefits, Extermination Service, Facilities Support Services, Housekeeping Service, Human Resources, Knowledge Management, Office Administration, Packaging Services, Physical Security, Project Management, Staffing Agency, Trade Shows, Virtual Workforce').split(', ')
    advertising = str('Creative Industries, Promotional, Advertising Ad Exchange, Ad Network, Ad Retargeting, Ad Server, Ad Targeting, Advertising, Advertising Platforms, Affiliate Marketing, Local Advertising, Mobile Advertising, Outdoor Advertising, SEM, Social Media Advertising, Video Advertising').split(', ')
    agriculture = str('Agriculture, AgTech, Animal Feed, Aquaculture, Equestrian, Farming, Forestry, Horticulture, Hydroponics, Livestock').split(', ')
    app = str('Application Performance Monitoring, App Stores, Application Platforms, Enterprise Application, App Discovery, Apps, Consumer Applications, Enterprise Applications, Mobile Apps, Reading Apps, Web Apps').split(', ')
    artificial_intelli = str('Artificial Intelligence, Intelligent Systems, Machine Learning, Natural Language Processing, Predictive Analytics').split(', ')
    biotechnology = str('Synthetic Biology, Bio-Pharm, Bioinformatics, Biometrics, Biopharma, Biotechnology, Genetics, Life Science, Neuroscience, Quantified Self').split(', ')
    clothing = str('Fashion, Laundry and Dry-cleaning, Lingerie, Shoes').split(', ')
    shopping = str('Consumer Behavior, Customer Support Tools, Discounts, Reviews and Recommendations, Auctions, Classifieds, Collectibles, Consumer Reviews, Coupons, E-Commerce, E-Commerce Platforms, Flash Sale, Gift, Gift Card, Gift Exchange, Gift Registry, Group Buying, Local Shopping, Made to Order, Marketplace, Online Auctions, Personalization, Point of Sale, Price Comparison, Rental, Retail, Retail Technology, Shopping, Shopping Mall, Social Shopping, Sporting Goods, Vending and Concessions, Virtual Goods, Wholesale').split(', ')
    community = str("Self Development, Sex, Forums, Match-Making, Babies, Identity, Women, Kids, Entrepreneur, Networking, Adult, Baby, Cannabis, Children, Communities, Dating, Elderly, Family, Funerals, Humanitarian, Leisure, LGBT, Lifestyle, Men's, Online Forums, Parenting, Pet, Private Social Networking, Professional Networking, Q&A, Religion, Retirement, Sex Industry, Sex Tech, Social, Social Entrepreneurship, Teenagers, Virtual World, Wedding, Women's, Young Adults").split(', ')
    electronics  = str('Mac, iPod Touch, Tablets, iPad, iPhone, Computer, Consumer Electronics, Drones, Electronics, Google Glass, Mobile Devices, Nintendo, Playstation, Roku, Smart Home, Wearables, Windows Phone, Xbox').split(', ')
    consumer_goods= str('Commodities, Sunglasses, Groceries, Batteries, Cars, Beauty, Comics, Consumer Goods, Cosmetics, DIY, Drones, Eyewear, Fast-Moving Consumer Goods, Flowers, Furniture, Green Consumer Goods, Handmade, Jewelry, Lingerie, Shoes, Tobacco, Toys').split(', ')
    content = str('E-Books, MicroBlogging, Opinions, Blogging Platforms, Content Delivery Network, Content Discovery, Content Syndication, Creative Agency, DRM, EBooks, Journalism, News, Photo Editing, Photo Sharing, Photography, Printing, Publishing, Social Bookmarking, Video Editing, Video Streaming').split(', ')
    datagroup = str('Optimization, A/B Testing, Analytics, Application Performance Management, Artificial Intelligence, Big Data, Bioinformatics, Biometrics, Business Intelligence, Consumer Research, Data Integration, Data Mining, Data Visualization, Database, Facial Recognition, Geospatial, Image Recognition, Intelligent Systems, Location Based Services, Machine Learning, Market Research, Natural Language Processing, Predictive Analytics, Product Research, Quantified Self, Speech Recognition, Test and Measurement, Text Analytics, Usability Testing').split(', ')
    design = str('Visualization, Graphics, Design, Designers, CAD, Consumer Research, Data Visualization, Fashion, Graphic Design, Human Computer Interaction, Industrial Design, Interior Design, Market Research, Mechanical Design, Product Design, Product Research, Usability Testing, UX Design, Web Design').split(', ')
    education = str('Universities, College Campuses, University Students, High Schools, All Students, Colleges, Alumni, Charter Schools, College Recruiting, Continuing Education, Corporate Training, E-Learning, EdTech, Education, Edutainment, Higher Education, Language Learning, MOOC, Music Education, Personal Development, Primary Education, Secondary Education, Skill Assessment, STEM Education, Textbook, Training, Tutoring, Vocational Education').split(', ')
    energy = str('Gas, Natural Gas Uses, Oil, Oil & Gas, Battery, Biofuel, Biomass Energy, Clean Energy, Electrical Distribution, Energy, Energy Efficiency, Energy Management, Energy Storage, Fossil Fuels, Fuel, Fuel Cell, Oil and Gas, Power Grid, Renewable Energy, Solar, Wind Energy').split(', ')
    events = str('Concerts, Event Management, Event Promotion, Events, Nightclubs, Nightlife, Reservations, Ticketing, Wedding').split(', ')
    financial = str('Debt Collecting, P2P Money Transfer, Investment Management, Trading, Accounting, Angel Investment, Asset Management, Auto Insurance, Banking, Bitcoin, Commercial Insurance, Commercial Lending, Consumer Lending, Credit, Credit Bureau, Credit Cards, Crowdfunding, Cryptocurrency, Debit Cards, Debt Collections, Finance, Financial Exchanges, Financial Services, FinTech, Fraud Detection, Funding Platform, Gift Card, Health Insurance, Hedge Funds, Impact Investing, Incubators, Insurance, InsurTech, Leasing, Lending, Life Insurance, Micro Lending, Mobile Payments, Payments, Personal Finance, Prediction Markets, Property Insurance, Real Estate Investment, Stock Exchanges, Trading Platform, Transaction Processing, Venture Capital, Virtual Currency, Wealth Management').split(', ')
    food = str('Specialty Foods, Bakery, Brewing, Cannabis, Catering, Coffee, Confectionery, Cooking, Craft Beer, Dietary Supplements, Distillery, Farmers Market, Food and Beverage, Food Delivery, Food Processing, Food Trucks, Fruit, Grocery, Nutrition, Organic Food, Recipes, Restaurants, Seafood, Snack Food, Tea, Tobacco, Wine And Spirits, Winery').split(', ')
    gaming = str('Game, Games, Casual Games, Console Games, Contests, Fantasy Sports, Gambling, Gamification, Gaming, MMO Games, Online Games, PC Games, Serious Games, Video Games').split(', ')
    government = str('Polling, Governance, CivicTech, Government, GovTech, Law Enforcement, Military, National Security, Politics, Public Safety, Social Assistance').split(', ')
    hardware= str('Cable, 3D, 3D Technology, Application Specific Integrated Circuit (ASIC), Augmented Reality, Cloud Infrastructure, Communication Hardware, Communications Infrastructure, Computer, Computer Vision, Consumer Electronics, Data Center, Data Center Automation, Data Storage, Drone Management, Drones, DSP, Electronic Design Automation (EDA), Electronics, Embedded Systems, Field-Programmable Gate Array (FPGA), Flash Storage, Google Glass, GPS, GPU, Hardware, Industrial Design, Laser, Lighting, Mechanical Design, Mobile Devices, Network Hardware, NFC, Nintendo, Optical Communication, Playstation, Private Cloud, Retail Technology, RFID, RISC, Robotics, Roku, Satellite Communication, Semiconductor, Sensor, Sex Tech, Telecommunications, Video Conferencing, Virtual Reality, Virtualization, Wearables, Windows Phone, Wireless, Xbox').split(', ')
    health_care = str('Senior Health, Physicians, Electronic Health Records, Doctors, Healthcare Services, Diagnostics, Alternative Medicine, Assisted Living, Assistive Technology, Biopharma, Cannabis, Child Care, Clinical Trials, Cosmetic Surgery, Dental, Diabetes, Dietary Supplements, Elder Care, Electronic Health Record (EHR), Emergency Medicine, Employee Benefits, Fertility, First Aid, Funerals, Genetics, Health Care, Health Diagnostics, Home Health Care, Hospital, Medical, Medical Device, mHealth, Nursing and Residential Care, Nutraceutical, Nutrition, Outpatient Care, Personal Health, Pharmaceutical, Psychology, Rehabilitation, Therapeutics, Veterinary, Wellness').split(', ')
    it = str('Distributors, Algorithms, ICT, M2M, Technology, Business Information Systems, CivicTech, Cloud Data Services, Cloud Management, Cloud Security, CMS, Contact Management, CRM, Cyber Security, Data Center, Data Center Automation, Data Integration, Data Mining, Data Visualization, Document Management, E-Signature, Email, GovTech, Identity Management, Information and Communications Technology (ICT), Information Services, Information Technology, Intrusion Detection, IT Infrastructure, IT Management, Management Information Systems, Messaging, Military, Network Security, Penetration Testing, Private Cloud, Reputation, Sales Automation, Scheduling, Social CRM, Spam Filtering, Technical Support, Unified Communications, Video Chat, Video Conferencing, Virtualization, VoIP').split(', ')
    internet = str('Online Identity, Cyber, Portals, Web Presence Management, Domains, Tracking, Web Tools, Curated Web, Search, Cloud Computing, Cloud Data Services, Cloud Infrastructure, Cloud Management, Cloud Storage, Darknet, Domain Registrar, E-Commerce Platforms, Ediscovery, Email, Internet, Internet of Things, ISP, Location Based Services, Messaging, Music Streaming, Online Forums, Online Portals, Private Cloud, Product Search, Search Engine, SEM, Semantic Search, Semantic Web, SEO, SMS, Social Media, Social Media Management, Social Network, Unified Communications, Vertical Search, Video Chat, Video Conferencing, Visual Search, VoIP, Web Browsers, Web Hosting').split(', ')
    invest = str('Angel Investment, Banking, Commercial Lending, Consumer Lending, Credit, Credit Cards, Financial Exchanges, Funding Platform, Hedge Funds, Impact Investing, Incubators, Micro Lending, Stock Exchanges, Trading Platform, Venture Capital').split(', ')
    manufacturing = str('Innovation Engineering, Civil Engineers, Heavy Industry, Engineering Firms, Systems, 3D Printing, Advanced Materials, Foundries, Industrial, Industrial Automation, Industrial Engineering, Industrial Manufacturing, Machinery Manufacturing, Manufacturing, Paper Manufacturing, Plastics and Rubber Manufacturing, Textiles, Wood Processing').split(', ')
    media = str('Writers, Creative, Television, Entertainment, Media, Advice, Animation, Art, Audio, Audiobooks, Blogging Platforms, Broadcasting, Celebrity, Concerts, Content, Content Creators, Content Discovery, Content Syndication, Creative Agency, Digital Entertainment, Digital Media, DRM, EBooks, Edutainment, Event Management, Event Promotion, Events, Film, Film Distribution, Film Production, Guides, In-Flight Entertainment, Independent Music, Internet Radio, Journalism, Media and Entertainment, Motion Capture, Music, Music Education, Music Label, Music Streaming, Music Venues, Musical Instruments, News, Nightclubs, Nightlife, Performing Arts, Photo Editing, Photo Sharing, Photography, Podcast, Printing, Publishing, Reservations, Social Media, Social News, Theatre, Ticketing, TV, TV Production, Video, Video Editing, Video on Demand, Video Streaming, Virtual World').split(', ')
    message = str('Unifed Communications, Chat, Email, Meeting Software, Messaging, SMS, Unified Communications, Video Chat, Video Conferencing, VoIP, Wired Telecommunications').split(', ')
    mobile = str('Android, Google Glass, iOS, mHealth, Mobile, Mobile Apps, Mobile Devices, Mobile Payments, Windows Phone, Wireless').split(', ')
    music = str('Audio, Audiobooks, Independent Music, Internet Radio, Music, Music Education, Music Label, Music Streaming, Musical Instruments, Podcast').split(', ')
    resource = str('Biofuel, Biomass Energy, Fossil Fuels, Mineral, Mining, Mining Technology, Natural Resources, Oil and Gas, Precious Metals, Solar, Timber, Water, Wind Energy').split(', ')
    navigation = str('Maps, Geospatial, GPS, Indoor Positioning, Location Based Services, Mapping Services, Navigation').split(', ')
    other = str('Mass Customization, Monetization, Testing, Subscription Businesses, Mobility, Incentives, Peer-to-Peer, Nonprofits, Alumni, Association, B2B, B2C, Blockchain, Charity, Collaboration, Collaborative Consumption, Commercial, Consumer, Crowdsourcing, Customer Service, Desktop Apps, Emerging Markets, Enterprise, Ethereum, Franchise, Freemium, Generation Y, Generation Z, Homeless Shelter, Infrastructure, Knowledge Management, LGBT Millennials, Non Profit, Peer to Peer, Professional Services, Project Management, Real Time, Retirement, Service Industry, Sharing Economy, Small and Medium Businesses, Social Bookmarking, Social Impact, Subscription Service, Technical Support, Underserved Children, Universities').split(', ')
    payment = str('Billing, Bitcoin, Credit Cards, Cryptocurrency, Debit Cards, Fraud Detection, Mobile Payments, Payments, Transaction Processing, Virtual Currency').split(', ')
    platforms = str('Development Platforms, Android, Facebook, Google, Google Glass, iOS, Linux, macOS, Nintendo, Operating Systems, Playstation, Roku, Tizen, Twitter, WebOS, Windows, Windows Phone, Xbox').split(', ')
    privacy = str('Digital Rights Management, Personal Data, Cloud Security, Corrections Facilities, Cyber Security, DRM, E-Signature, Fraud Detection, Homeland Security, Identity Management, Intrusion Detection, Law Enforcement, Network Security, Penetration Testing, Physical Security, Privacy, Security').split(', ')
    services = str('Funeral Industry, English-Speaking, Spas, Plumbers, Service Industries, Staffing Firms, Translation, Career Management, Business Services, Services, Accounting, Business Development, Career Planning, Compliance, Consulting, Customer Service, Employment, Environmental Consulting, Field Support, Freelance, Intellectual Property, Innovation Management, Legal, Legal Tech, Management Consulting, Outsourcing, Professional Networking, Quality Assurance, Recruiting, Risk Management, Social Recruiting, Translation Service').split(', ')
    realestate= str('Office Space, Self Storage, Brokers, Storage, Home Owners, Self Storage , Realtors, Home & Garden, Utilities, Home Automation, Architecture, Building Maintenance, Building Material, Commercial Real Estate, Construction, Coworking, Facility Management, Fast-Moving Consumer Goods, Green Building, Home and Garden, Home Decor, Home Improvement, Home Renovation, Home Services, Interior Design, Janitorial Service, Landscaping, Property Development, Property Management, Real Estate, Real Estate Investment, Rental Property, Residential, Self-Storage, Smart Building, Smart Cities, Smart Home, Timeshare, Vacation Rental').split(', ')
    sales = str('Advertising, Affiliate Marketing, App Discovery, App Marketing, Brand Marketing, Cause Marketing, Content Marketing, CRM, Digital Marketing, Digital Signage, Direct Marketing, Direct Sales, Email Marketing, Lead Generation, Lead Management, Local, Local Advertising, Local Business, Loyalty Programs, Marketing, Marketing Automation, Mobile Advertising, Multi-level Marketing, Outdoor Advertising, Personal Branding, Public Relations, Sales, Sales Automation, SEM, SEO, Social CRM, Social Media Advertising, Social Media Management, Social Media Marketing, Sponsorship, Video Advertising').split(', ')
    science = str('Face Recognition, New Technologies, Advanced Materials, Aerospace, Artificial Intelligence, Bioinformatics, Biometrics, Biopharma, Biotechnology, Chemical, Chemical Engineering, Civil Engineering, Embedded Systems, Environmental Engineering, Human Computer Interaction, Industrial Automation, Industrial Engineering, Intelligent Systems, Laser, Life Science, Marine Technology, Mechanical Engineering, Nanotechnology, Neuroscience, Nuclear, Quantum Computing, Robotics, Semiconductor, Software Engineering, STEM Education').split(', ')
    software = str('Business Productivity, 3D Technology, Android, App Discovery, Application Performance Management, Apps, Artificial Intelligence, Augmented Reality, Billing, Bitcoin, Browser Extensions, CAD, Cloud Computing, Cloud Management, CMS, Computer Vision, Consumer Applications, Consumer Software, Contact Management, CRM, Cryptocurrency, Data Center Automation, Data Integration, Data Storage, Data Visualization, Database, Developer APIs, Developer Platform, Developer Tools, Document Management, Drone Management, E-Learning, EdTech, Electronic Design Automation (EDA), Embedded Software, Embedded Systems, Enterprise Applications, Enterprise Resource Planning (ERP), Enterprise Software, Facial Recognition, File Sharing, IaaS, Image Recognition, iOS, Linux, Machine Learning, macOS, Marketing Automation, Meeting Software, Mobile Apps, Mobile Payments, MOOC, Natural Language Processing, Open Source, Operating Systems, PaaS, Predictive Analytics, Presentation Software, Presentations, Private Cloud, Productivity Tools, QR Codes, Reading Apps, Retail Technology, Robotics, SaaS, Sales Automation, Scheduling, Sex Tech, Simulation, SNS, Social CRM, Software, Software Engineering, Speech Recognition, Task Management, Text Analytics, Transaction Processing, Video Conferencing, Virtual Assistant, Virtual Currency, Virtual Desktop, Virtual Goods, Virtual Reality, Virtual World, Virtualization, Web Apps, Web Browsers, Web Development').split(', ')
    sports = str('American Football, Baseball, Basketball, Boating, Cricket, Cycling, Diving, eSports, Fantasy Sports, Fitness, Golf, Hockey, Hunting, Outdoors, Racing, Recreation, Rugby, Sailing, Skiing, Soccer, Sporting Goods, Sports, Surfing, Swimming, Table Tennis, Tennis, Ultimate Frisbee, Volley Ball').split(', ')
    sustainability = str('Green, Wind, Biomass Power Generation, Renewable Tech, Environmental Innovation, Renewable Energies, Clean Technology, Biofuel, Biomass Energy, Clean Energy, CleanTech, Energy Efficiency, Environmental Engineering, Green Building, Green Consumer Goods, GreenTech, Natural Resources, Organic, Pollution Control, Recycling, Renewable Energy, Solar, Sustainability, Waste Management, Water Purification, Wind Energy').split(', ')
    transportation = str('Taxis, Air Transportation, Automotive, Autonomous Vehicles, Car Sharing, Courier Service, Delivery Service, Electric Vehicle, Ferry Service, Fleet Management, Food Delivery, Freight Service, Last Mile Transportation, Limousine Service, Logistics, Marine Transportation, Parking, Ports and Harbors, Procurement, Public Transportation, Railroad, Recreational Vehicles, Ride Sharing, Same Day Delivery, Shipping, Shipping Broker, Space Travel, Supply Chain Management, Taxi Service, Transportation, Warehousing, Water Transportation').split(', ')
    travel = str('Adventure Travel, Amusement Park and Arcade, Business Travel, Casino, Hospitality, Hotel, Museums and Historical Sites, Parks, Resorts, Timeshare, Tour Operator, Tourism, Travel, Travel Accommodations, Travel Agency, Vacation Rental').split(', ')
    video = str('Animation, Broadcasting, Film, Film Distribution, Film Production, Motion Capture, TV, TV Production, Video, Video Editing, Video on Demand, Video Streaming').split(', ')

    import re
    data['Industry_Group'] = pd.np.where(data.market.str.contains('|'.join(admin_services), flags=re.IGNORECASE), "Administrative Services",
                                pd.np.where(data.market.str.contains('|'.join(software), flags=re.IGNORECASE), "Software",
                                pd.np.where(data.market.str.contains('|'.join(advertising), flags=re.IGNORECASE), "Advertising",
                                pd.np.where(data.market.str.contains('|'.join(agriculture), flags=re.IGNORECASE), "Agriculture and Farming",
                                pd.np.where(data.market.str.contains('|'.join(app), flags=re.IGNORECASE), "Apps",
                                pd.np.where(data.market.str.contains('|'.join(artificial_intelli), flags=re.IGNORECASE), "Artificial Intelligence",
                                pd.np.where(data.market.str.contains('|'.join(biotechnology), flags=re.IGNORECASE), "Biotechnology",
                                pd.np.where(data.market.str.contains('|'.join(clothing), flags=re.IGNORECASE), "Clothing and Apparel",
                                pd.np.where(data.market.str.contains('|'.join(shopping), flags=re.IGNORECASE), "Commerce and Shopping",
                                pd.np.where(data.market.str.contains('|'.join(community), flags=re.IGNORECASE), "Community and Lifestyle",
                                pd.np.where(data.market.str.contains('|'.join(electronics), flags=re.IGNORECASE), "Consumer Electronics",
                                pd.np.where(data.market.str.contains('|'.join(consumer_goods), flags=re.IGNORECASE), "Consumer Goods",
                                pd.np.where(data.market.str.contains('|'.join(content), flags=re.IGNORECASE), "Content and Publishing",
                                pd.np.where(data.market.str.contains('|'.join(data), flags=re.IGNORECASE), "Data and Analytics",
                                pd.np.where(data.market.str.contains('|'.join(design), flags=re.IGNORECASE), "Design",
                                pd.np.where(data.market.str.contains('|'.join(education), flags=re.IGNORECASE), "Education",
                                pd.np.where(data.market.str.contains('|'.join(energy), flags=re.IGNORECASE), "Energy",
                                pd.np.where(data.market.str.contains('|'.join(events), flags=re.IGNORECASE), "Events",
                                pd.np.where(data.market.str.contains('|'.join(financial), flags=re.IGNORECASE), "Financial Services",
                                pd.np.where(data.market.str.contains('|'.join(food), flags=re.IGNORECASE), "Food and Beverage",
                                pd.np.where(data.market.str.contains('|'.join(gaming), flags=re.IGNORECASE), "Gaming",
                                pd.np.where(data.market.str.contains('|'.join(government), flags=re.IGNORECASE), "Government and Military",
                                pd.np.where(data.market.str.contains('|'.join(hardware), flags=re.IGNORECASE), "Hardware",
                                pd.np.where(data.market.str.contains('|'.join(health_care), flags=re.IGNORECASE), "Health Care",
                                pd.np.where(data.market.str.contains('|'.join(it), flags=re.IGNORECASE), "Information Technology",
                                pd.np.where(data.market.str.contains('|'.join(internet), flags=re.IGNORECASE), "Internet Services",
                                pd.np.where(data.market.str.contains('|'.join(invest), flags=re.IGNORECASE), "Lending and Investments",
                                pd.np.where(data.market.str.contains('|'.join(manufacturing), flags=re.IGNORECASE), "Manufacturing",
                                pd.np.where(data.market.str.contains('|'.join(media), flags=re.IGNORECASE), "Media and Entertainment",
                                pd.np.where(data.market.str.contains('|'.join(message), flags=re.IGNORECASE), "Messaging and Telecommunication",
                                pd.np.where(data.market.str.contains('|'.join(mobile), flags=re.IGNORECASE), "Mobile",
                                pd.np.where(data.market.str.contains('|'.join(music), flags=re.IGNORECASE), "Music and Audio",
                                pd.np.where(data.market.str.contains('|'.join(resource), flags=re.IGNORECASE), "Natural Resources",
                                pd.np.where(data.market.str.contains('|'.join(navigation), flags=re.IGNORECASE), "Navigation and Mapping",
                                pd.np.where(data.market.str.contains('|'.join(payment), flags=re.IGNORECASE), "Payments",
                                pd.np.where(data.market.str.contains('|'.join(platforms), flags=re.IGNORECASE), "Platforms",
                                pd.np.where(data.market.str.contains('|'.join(privacy), flags=re.IGNORECASE), "Privacy and Security",
                                pd.np.where(data.market.str.contains('|'.join(services), flags=re.IGNORECASE), "Professional Services",
                                pd.np.where(data.market.str.contains('|'.join(realestate), flags=re.IGNORECASE), "Real Estate",
                                pd.np.where(data.market.str.contains('|'.join(sales), flags=re.IGNORECASE), "Sales and Marketing",
                                pd.np.where(data.market.str.contains('|'.join(science), flags=re.IGNORECASE), "Science and Engineering",
                                pd.np.where(data.market.str.contains('|'.join(sports), flags=re.IGNORECASE), "Sports",
                                pd.np.where(data.market.str.contains('|'.join(sustainability), flags=re.IGNORECASE), "Sustainability",
                                pd.np.where(data.market.str.contains('|'.join(transportation), flags=re.IGNORECASE), "Transportation",
                                pd.np.where(data.market.str.contains('|'.join(travel), flags=re.IGNORECASE), "Travel and Tourism",
                                pd.np.where(data.market.str.contains('|'.join(video), flags=re.IGNORECASE), "Video",
                                pd.np.where(data.market.str.contains('|'.join(other), flags=re.IGNORECASE), "Other",  "Other")))))))))))))))))))))))))))))))))))))))))))))))

    data['Industry_Group'].nunique()

    data = data[data['funding_total_usd'] != ' -   ']
    data = data.reset_index(drop=True)
    data = data.drop_duplicates(subset=['name', 'homepage_url', 'Industry_Group'])

    #data[data[['name', 'homepage_url', 'Industry_Group']].duplicated()]

    data

    data.columns

    columns_to_save = ['funding_total_usd',
        'status', 'country_code', 'funding_rounds', 'founded_at',
        'first_funding_at', 'last_funding_at', 'Industry_Group']
    data = data[columns_to_save]

    data[['Industry_Group']].value_counts()

    data['time_between_first_last_funding'] = (pd.to_datetime(data['last_funding_at'], format='%m/%d/%y', errors="coerce") - pd.to_datetime(data['first_funding_at'], errors="coerce")).dt.days

    data.isna().sum()

    data['founded_at'].fillna(data['first_funding_at'], inplace=True)

    data.isna().sum()

    data.dropna(subset=['time_between_first_last_funding'], inplace=True)

    #most_recent_date = pd.to_datetime(data['last_funding_at'], format='%m/%d/%y', errors="coerce").max()
    #data['years_in_business'] = (pd.to_datetime(data['last_funding_at'], format='%m/%d/%y', errors="coerce") - pd.to_datetime(data['founded_at'], errors="coerce")).dt.days

    # Convert date columns to datetime with the correct format
    date_columns = ['founded_at', 'first_funding_at', 'last_funding_at']
    data[date_columns] = data[date_columns].apply(pd.to_datetime, format='%m/%d/%y', errors='coerce')
    # Filter out rows with NaT values (invalid dates)
    data = data.dropna(subset=date_columns, how='any')
    data

    #data[['founded_at']].hist()

    #data[data['time_between_first_last_funding'] >= 0]

    start_date = '1990-01-01'
    end_date = '2015-12-30'

    # Select DataFrame rows between two dates
    mask1 = (data['founded_at'] > start_date) & (data['founded_at'] <= end_date)
    data = data.loc[mask1]

    mask2 = (data['first_funding_at'] > start_date) & (data['first_funding_at'] <= end_date) & (data['last_funding_at'] > start_date) & (data['last_funding_at'] <= end_date)
    data = data.loc[mask2]

    data = data[data['first_funding_at'] <= data['last_funding_at']]

    reference_date = pd.to_datetime(end_date)

    data['days_in_business'] = (reference_date - data['founded_at']).dt.days

    data = data.reset_index(drop=True)

    data = data.drop(columns=['founded_at', 'first_funding_at', 'last_funding_at'])

    data

    data.dtypes

    #change to numeric
    data['funding_total_usd'] = pd.to_numeric(data['funding_total_usd'], errors='coerce')
    # Convert 'time_between_first_last_funding' column to integer
    data['time_between_first_last_funding'] = data['time_between_first_last_funding'].astype('Int64')
    data['funding_rounds'] = data['funding_rounds'].astype('Int64', errors='ignore')

    data

    data.dtypes

    plt.figure(figsize=(16, 6))

    # Plot distribution by Industry Group
    plt.subplot(1, 3, 1)
    industry_counts = data["Industry_Group"].value_counts()
    industry_counts.plot(kind="bar")
    plt.title("Distribution by Industry Group")
    plt.xlabel("Industry Group")
    plt.ylabel("Number of Startups")
    plt.xticks(rotation=45, ha="right")

    # Plot distribution by Country Code
    plt.subplot(1, 3, 2)
    country_counts = data["country_code"].value_counts()
    country_counts.plot(kind="bar")
    plt.title("Distribution by Country Code")
    plt.xlabel("Country Code")
    plt.ylabel("Number of Startups")
    plt.xticks(rotation=0)

    # Plot distribution by Status
    plt.subplot(1, 3, 3)
    status_counts = data["status"].value_counts()
    status_counts.plot(kind="bar")
    plt.title("Distribution by Status")
    plt.xlabel("Status")
    plt.ylabel("Number of Startups")
    plt.xticks(rotation=0)

    # Adjust spacing between subplots
    plt.tight_layout(w_pad=4)

    plt.show()

    pivot_table = data.pivot_table(index="country_code", columns="status", values="funding_total_usd", aggfunc="count", fill_value=0)

    # Create a stacked bar plot
    plt.figure(figsize=(10, 6))
    pivot_table.plot(kind="bar", stacked=True)
    plt.title("Distribution of Status by Country Code")
    plt.xlabel("Country Code")
    plt.ylabel("Number of Startups")
    plt.xticks(rotation=0)
    plt.legend(title="Status")

    plt.tight_layout()
    plt.show()

    data

    rounds_threshold_us = int(data.groupby(['country_code','status'])['funding_rounds'].describe().iloc[0][1])
    rounds_threshold_us

    data.groupby(['country_code','status'])['funding_rounds'].describe()

    rounds_threshold_us = int(data.groupby(['country_code','status'])['funding_rounds'].describe().iloc[3][1])
    rounds_threshold_other = int(data.groupby(['country_code','status'])['funding_rounds'].describe().iloc[0][1])
    fundings_threshold_us = data.groupby(['country_code','status'])['funding_total_usd'].describe().iloc[3][4]
    fundings_threshold_other = data.groupby(['country_code','status'])['funding_total_usd'].describe().iloc[0][4]

    data.loc[data['status'] == 'acquired', 'Success_failure'] = 1
    data.loc[data['status'] == 'closed', 'Success_failure'] = 0

    data.loc[(data['status'] == 'operating') & (data['country_code'] == 'USA') & (data['funding_total_usd'] >= int(fundings_threshold_us)) & (data['funding_rounds'] >= int(rounds_threshold_us)), 'Success_failure'] = 1
    data.loc[(data['status'] == 'operating') & (data['country_code'] == 'Other') & (data['funding_total_usd'] >= int(fundings_threshold_other)) & (data['funding_rounds'] >= int(rounds_threshold_other-1)), 'Success_failure'] = 1

    data['Success_failure'] = data['Success_failure'].fillna(0)

    encoded_data = pd.get_dummies(data, columns=["country_code"], prefix=["country"], drop_first=True)

    encoded_data = pd.get_dummies(data, columns=["Industry_Group"], prefix=["industry"])


    encoded_data.shape

    encoded_data

    encoded_data["Success_failure"] = encoded_data["Success_failure"].astype(int)

    from sklearn.preprocessing import MinMaxScaler

    # Select numerical features for standardization
    numerical_features = ["funding_total_usd", "funding_rounds", "time_between_first_last_funding", "days_in_business"]

    # Initialize StandardScaler
    scaler = MinMaxScaler()

    # Standardize the selected features
    encoded_data[numerical_features] = scaler.fit_transform(encoded_data[numerical_features])

    encoded_data

    #correlation_matrix = encoded_data.corr()

    # Create a heatmap of the correlation matrix
    #plt.figure(figsize=(40, 26
                    #))
    #sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", center=0)
    #plt.title("Correlation Matrix")
    #plt.show()

    #from sklearn.preprocessing import LabelEncoder
    # Perform label encoding for the 'status' column
    #label_encoder = LabelEncoder()
    #encoded_data["status_encoded"] = label_encoder.fit_transform(encoded_data["status"])

    # Perform one-hot encoding for the 'country_code' column
    encoded_data = pd.get_dummies(encoded_data, columns=["country_code"], prefix=["country"], drop_first=True)

    encoded_data.drop(columns=["status"])
    return encoded_data
