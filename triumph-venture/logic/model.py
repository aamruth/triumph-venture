y = encoded_data["Success_failure"]
X = encoded_data.drop(columns=["Success_failure"])
from sklearn.model_selection import train_test_split
# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Create a Random Forest classifier as the base model
base_model = RandomForestClassifier(random_state=42)

# Train the model on the training data
base_model.fit(X_train, y_train)


# Make predictions on the testing data
y_pred = base_model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

import numpy as np
from sklearn.model_selection import cross_validate
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression

model = RandomForestClassifier(random_state=42)

cv_results = cross_validate(model, X_train, y_train, cv = 5)

score = cv_results["test_score"].mean()
print(f"Before any feature permutation, the cross-validated accuracy is equal to {round(score,2)}")

## Question 1 - Permutation importance
model = LogisticRegression().fit(X_train,y_train) # Fit the model

permutation_score = permutation_importance(model, X_train, y_train, n_repeats=100) # Perform Permutation

importance_df = pd.DataFrame(np.vstack((X_train.columns,
                                        permutation_score.importances_mean)).T, # Unstack results
                            columns = ['feature','feature_importance'])

print("After feature permutation, here are the decreases in terms of scores:")
importance_df = importance_df.sort_values(by="feature_importance", ascending = False) # Order by importance
importance_df

# I want to get rid of features which caused less than this  in terms of performance
threshold = 0.01

# Decompose this one-liner piece of code step by step if you don't understand it at first sight!
weak_features = importance_df[importance_df.feature_importance <= threshold]["feature"].values
weak_features

from sklearn.model_selection import cross_val_score

## Question 3 - Cross validating the model with strong features only
X_strong_features = X_train.drop(columns=list(weak_features))

print(f"Our strong features are {list(X_strong_features.columns)}")

model = RandomForestClassifier(random_state=42)

scores = cross_val_score(model, X_strong_features, y_train, cv = 5)
strong_model_score = scores.mean()

print(f"Before removing weak features, the cross-validated accuracy was equal to {round(score,2)}")

print(f"The RandomForestClassifier fitted with the strong features only has a score of {round(strong_model_score,2)}")

X_strong_features_test = X_test.drop(columns=list(weak_features))

model.fit(X_strong_features, y_train)

# Make predictions on the testing data
y_pred = model.predict(X_strong_features_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
