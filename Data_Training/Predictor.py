import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Specifing file location
file_path = "C:\\Users\\Pavilion\\Documents\\Programming\\Python\\Projects\\Football\\BAFI\\Data_Training\\"
file_path_origin = file_path + "raw data.csv"

# Predicted data dataframe
#predicted_data = pd.DataFrame(columns=["Team_A", "Team_A_Av(GD)", "Team_A_C(GF)","Team_B", "Team_B_Av(GD)", "Team_B_C(GF)","Team_A_Last","Team_B_Last"])

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

print(predicting_data)
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

'''

# Using other matches to make prediction
new_data = pd.read_csv(file_path + "for prediction data.csv")

# Drop rows with missing values for simplicity
new_data = new_data.dropna()

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
new_data.to_csv(file_path + "already predicted data.csv", index=False)'''

# Plotting the relationship between each feature and the target variable
'''# Creating subplots
fig, axs = plt.subplots(2, 3, figsize=(15, 10))

# Plotting each feature against the target variable
for i, feature in enumerate(X.columns):
    row = i // 3
    col = i % 3
    axs[row, col].scatter(X[feature], y, alpha=0.5)
    axs[row, col].set_title(feature)
    axs[row, col].set_xlabel(feature)
    axs[row, col].set_ylabel('Result')
    
plt.tight_layout()
plt.show()'''

# Plotting all features against the target variable on the same graph
'''plt.figure(figsize=(10, 6))

# Plotting each feature against the target variable
for feature in X.columns:
    plt.scatter(X[feature], y, alpha=0.5, label=feature)

plt.title('Features vs. Result')
plt.xlabel('Feature Values')
plt.ylabel('Result')
plt.legend()
plt.grid(True)
plt.show()'''