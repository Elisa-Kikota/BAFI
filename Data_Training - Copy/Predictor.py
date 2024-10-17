import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Specifing file location
file_path = "C:\\Users\\Pavilion\\Documents\\Programming\\Python\\Projects\\Football\\BAFI\\Computing\\"
file_path_origin = file_path + "predicting data.csv"

# Predicted data dataframe
#predicted_data = pd.DataFrame(columns=["Team_A", "Team_A_Av(GD)", "Team_A_C(GF)", "Team_B", "Team_B_Av(GD)", "Team_B_C(GF)","Team_A_Last","Team_B_Last"])

# Importing the file
predicting_data = pd.read_csv(file_path_origin)

# Drop rows with missing values for simplicity
predicting_data = predicting_data.dropna()

# Convert 'Team_A_Last' and 'Team_B_Last' to numeric values
predicting_data['Team_A_Last'] = pd.to_numeric(predicting_data['Team_A_Last'])
predicting_data['Team_B_Last'] = pd.to_numeric(predicting_data['Team_B_Last'])

# Adding result column
predicting_data['Result'] = np.where(predicting_data['Team_A_Last'] > predicting_data['Team_B_Last'], 1,
                                   np.where(predicting_data['Team_A_Last'] == predicting_data['Team_B_Last'], 0, -1))


# Create feature matrix (X) and target variable (y)
X = predicting_data[['Team_A_Av(GD)', 'Team_A_C(GF)', 'Team_A_Last', 'Team_B_Av(GD)', 'Team_B_C(GF)', 'Team_B_Last']]
y = predicting_data['Result']  # Assuming you have a 'Result' column indicating the outcome (e.g., 1 for Team_A wins, 0 for draw, -1 for Team_B wins)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a Random Forest Classifier
model = RandomForestClassifier()

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
predictions = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, predictions)
print(f'Model Accuracy: {accuracy}')

# Adding prediction column
predicting_data['Prediction'] = None

# Using other matches to make prediction
new_data = pd.read_csv(file_path + "raw data.csv")

# Adding prediction column
new_data['Prediction'] = None

# Making the predictions using the model
for index, row in new_data.iterrows():
    new_data.at[index, "Prediction"] = model.predict(pd.DataFrame({
        'Team_A_Av(GD)': [row['Team_A_Av(GD)']], 
        'Team_A_C(GF)' : [row['Team_A_C(GF)']], 
        'Team_A_Last'  : [row['Team_A_Last']],
        'Team_B_Av(GD)': [row['Team_B_Av(GD)']], 
        'Team_B_C(GF)' : [row['Team_B_C(GF)']], 
        'Team_B_Last'  : [row['Team_B_Last']]
    }))

# Saving data
new_data.to_csv(file_path + "new stuff data.csv", index=False)