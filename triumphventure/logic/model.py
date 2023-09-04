from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import os
import pickle
import pandas as pd
import os
from sklearn.compose import make_column_transformer, make_column_selector
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import RobustScaler

def evaluate_model():
    return 0.93
def test():
    pass
def pre_process_mydata():
    # Drop the unnamed column
    data = data.drop(columns=['Unnamed: 0'])
    pass

def create_pipeline():


    preproc_numerical= make_pipeline(
        SimpleImputer(),
        RobustScaler()
    )

    preproc_categorical_Industry_Group_country = make_pipeline(
        SimpleImputer(strategy="most_frequent"),
        #columnDropperTransformer()
    )

    preproc = make_column_transformer(
        (preproc_numerical, make_column_selector(dtype_include=["int64", "float64"])),
        (preproc_categorical_Industry_Group_country, make_column_selector(dtype_include=["object"]))
    )
    pipe_baseline = make_pipeline(preproc, RandomForestClassifier(random_state=42))
    pass

def train_model():
    data = pre_process_mydata()
    pipe_baseline = create_pipeline()
    #X_strong_features_test = X_test_new.drop(columns=list(weak_features))
    y_new = data["status"].astype(int)
    X_new = data.drop(columns=["status"])

 # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_new, y_new, test_size=0.2, random_state=42)
    pipe_baseline.fit(X_train,y_train)
    pass


def save_model():
    # YOUR CODE HERE
    pipe_baseline = train_model()
    score = evaluate_model()
    #if score is better than the prev score
    # Export Pipeline as pickle file
    with open("fitted_model_tv.pkl", "wb") as file:
        pickle.dump(pipe_baseline, file)

    # Load Pipeline from pickle file in another notebook
def load_model():
    # pickle_file_dir = os.path.dirname(os.path.abspath(os.getcwd()))
    # my_pickle_file = os.path.join(pickle_file_dir,'fitted_model_tv.pkl')
    MODEL_TARGET = os.environ.get("LOCAL", "N")
    if(MODEL_TARGET == "N"):
        my_model = pickle.load(open('./triumphventure/data/pipeline_yan_ohe.pkl',"rb"))
    else:
        my_model = pickle.load(open('../data/pipeline_yan_ohe.pkl',"rb"))
    return my_model

if __name__ == "__main__":
    load_model()
