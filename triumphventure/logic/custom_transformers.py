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
