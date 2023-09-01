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
    return 0.93
def test():
    pass


def pre_process_mydata():
    # Drop the unnamed column
    data = data.drop(columns=['Unnamed: 0'])
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
    data = pd.read_csv('../data/clean_data.csv', encoding='unicode_escape')
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
    # pickle_file_dir = os.path.dirname(os.path.abspath(os.getcwd()))
    # my_pickle_file = os.path.join(pickle_file_dir,'fitted_model_tv.pkl')
    print(os.getcwd())
    with open('./triumphventure/logic/fitted_model_tv.pkl',"rb") as model_pkl:
        model = pickle.load(model_pkl)
    return model

if __name__ == "__main__":
    load_model()
