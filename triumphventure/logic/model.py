from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
import numpy as np
import pandas as pd
from sklearn.model_selection import cross_validate
from sklearn.inspection import permutation_importance
import os
import pickle
import matplotlib.pyplot as plt
import ydata_profiling as pp
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import ydata_profiling as pp
import seaborn as sns
import warnings
import os
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import make_column_transformer, make_column_selector
from sklearn.ensemble import AdaBoostRegressor, VotingRegressor, GradientBoostingRegressor, StackingRegressor, RandomForestRegressor
from sklearn.feature_selection import SelectPercentile, mutual_info_regression, VarianceThreshold, SelectFromModel
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.linear_model import Ridge, LinearRegression,LogisticRegression
from sklearn.metrics import make_scorer, mean_squared_error, mean_squared_log_error
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, RandomizedSearchCV
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, OrdinalEncoder
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import RobustScaler

data = pd.read_csv('../triumphventure/data/clean_data.csv', encoding= 'unicode_escape')


def evaluate_model():
    model = RandomForestClassifier(random_state=42)
    permutation_score = permutation_importance(model, X_train, y_train, n_repeats=100) # Perform Permutation

    print("After feature permutation, here are the decreases in terms of scores:")
    importance_df = importance_df.sort_values(by="feature_importance", ascending = False) # Order by importance
    importance_df

    # I want to get rid of features which caused less than this  in terms of performance
    threshold = 0.01

    # Decompose this one-liner piece of code step by step if you don't understand it at first sight!
    weak_features = importance_df[importance_df.feature_importance <= threshold]["feature"].values

    ## Question 3 - Cross validating the model with strong features only
    X_strong_features = X_train.drop(columns=list(weak_features))
    model = initialise_model(X_strong_features)
    print(f"Our strong features are {list(X_strong_features.columns)}")
    scores = cross_val_score(model, X_strong_features, y_train, cv = 5)
    strong_model_score = scores.mean()
    print(f"The RandomForestClassifier fitted with the strong features only has a score of {round(strong_model_score,2)}")
    # Evaluate the model
    # Make predictions on the testing data
    y_pred = model.predict(X_strong_features_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)
    return strong_model_score
def test():
    pass
def pre_process_mydata():
    # Drop the unnamed column
    data = data.drop(columns=['Unnamed: 0'])

    class columnDropperTransformer(TransformerMixin, BaseEstimator):
        def __init__(self):
            self.weak_features = ['Industry_Group_Gaming', 'Industry_Group_Professional Services',
        'Industry_Group_Financial Services', 'Industry_Group_Advertising',
        'Industry_Group_Mobile', 'Industry_Group_Media and Entertainment',
        'Industry_Group_Privacy and Security', 'Industry_Group_Education',
        'Industry_Group_Content and Publishing',
        'Industry_Group_Sales and Marketing',
        'Industry_Group_Manufacturing',
        'Industry_Group_Consumer Electronics',
        'Industry_Group_Data and Analytics',
        'Industry_Group_Transportation', 'Industry_Group_Hardware',
        'Industry_Group_Clothing and Apparel',
        'Industry_Group_Real Estate', 'Industry_Group_Design',
        'Industry_Group_Food and Beverage',
        'Industry_Group_Travel and Tourism', 'Industry_Group_Platforms',
        'Industry_Group_Sports', 'Industry_Group_Events',
        'Industry_Group_Consumer Goods',
        'Industry_Group_Administrative Services', 'Industry_Group_Energy',
        'Industry_Group_Sustainability',
        'Industry_Group_Messaging and Telecommunication',
        'Industry_Group_Navigation and Mapping',
        'Industry_Group_Agriculture and Farming',
        'Industry_Group_Natural Resources',
        'Industry_Group_Government and Military', 'Industry_Group_Apps',
        'Industry_Group_Artificial Intelligence',
        'Industry_Group_Science and Engineering']

        def fit(self,X,y=None):
            self.encoder = OneHotEncoder(handle_unknown="ignore", sparse=False)
            self.encoder.fit(X)
            self.feature_names_ = self.encoder.get_feature_names_out(['country_code','Industry_Group'])
            return self
        def transform(self,X,y=None):
            encoded = self.encoder.transform(X)
            # Create a DataFrame with the transformed data and feature names
            transformed_df = pd.DataFrame(data=encoded, columns=self.feature_names_)
            return transformed_df.drop(self.weak_features, axis=1)

    preproc_numerical= make_pipeline(
        SimpleImputer(),
        RobustScaler()
    )

    preproc_categorical_Industry_Group_country = make_pipeline(
        SimpleImputer(strategy="most_frequent"),
        columnDropperTransformer()
    )

    preproc = make_column_transformer(
        (preproc_numerical, make_column_selector(dtype_include=["int64", "float64"])),
        (preproc_categorical_Industry_Group_country, make_column_selector(dtype_include=["object"]))
    )


    pipe_baseline = make_pipeline(preproc, RandomForestClassifier(random_state=42))
    return pipe_baseline

def create_pipeline():
    pass

def initialise_model():
    pipe_baseline = pre_process_mydata()
     #X_strong_features_test = X_test_new.drop(columns=list(weak_features))
    y_new = data["status"].astype(int)
    X_new = data.drop(columns=["status"])

 # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_new, y_new, test_size=0.2, random_state=42)
    pipe_baseline.fit(X_train,y_train)
    return pipe_baseline


def save_model():
    # YOUR CODE HERE
    pipe_baseline = initialise_model()
    # Export Pipeline as pickle file
    with open("fitted_model_tv.pkl", "wb") as file:
        pickle.dump(pipe_baseline, file)

    # Load Pipeline from pickle file in another notebook
def load_model():
    pickle_file_dir = os.path.dirname(os.path.abspath(os.getcwd()))
    my_pickle_file = os.path.join(pickle_file_dir,'fitted_model_tv.pkl')
    my_model = pickle.load(open(my_pickle_file,"rb"))
    return my_model

if __name__ == "__main__":
    save_model()
