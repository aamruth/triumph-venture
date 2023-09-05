import pandas as pd

def preproc_input(input_dict):
    data = pd.DataFrame(input_dict, index=[0])
    list_of_ind = ['Industry_Group_Biotechnology', 'Industry_Group_Commerce_and_Shopping',
                'Industry_Group_Community_and_Lifestyle',
                'Industry_Group_Health_Care',
                    'Industry_Group_Information_Technology',
                    'Industry_Group_Internet_Services',
                    'Industry_Group_Other',
                    'Industry_Group_Software']
    list_of_ind_stripped = ['Biotechnology', 'Commerce and Shopping',
                'Community and Lifestyle',
                'Health Care',
                    'Information Technology',
                    'Internet Services',
                    'Other',
                    'Software']
    for industry in list_of_ind:
        data[industry] = 0.0
    for industry in list_of_ind_stripped:
        if data['Industry_Group'][0] == industry:
            data[f'Industry_Group_{industry.replace(" ", "_")}'] = 1.0
    return data.drop(columns=['Industry_Group']).iloc[0].to_dict()
