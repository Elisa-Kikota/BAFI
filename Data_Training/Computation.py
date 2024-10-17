from datetime import datetime
import numpy as np
import os
import pandas as pd
import re
import time

# ANSI escape codes for colors
BLUE = '\033[94m'
BOLD = '\033[1m'
GREEN = '\033[92m'
RED = '\033[31m'
RESET = '\033[0m'
YELLOW = '\033[93m'

# Get today's date
today_date = datetime.now().date()
#formatted_date = datetime.date.today().strftime("%Y-%m-%d")

# Specifing file location
file_path = "C:\\Users\\Pavilion\\Documents\\Programming\\Python\\Projects\\Football\\BAFI\\Data_Training\\"
file_path_origin = file_path + "Matches Data.csv"

# Predicted data dataframe
predicted_data = pd.DataFrame(columns=["Team_A", "Team_A_Av(GD)", "Team_A_C(GF)", "Team_B", "Team_B_Av(GD)", "Team_B_C(GF)"])

# Importing the file
data = pd.read_csv(file_path_origin)

# Convert the 'Date' column to datetime format
data['Date'] = pd.to_datetime(data['Date'])

# Filter the data for today's date
today_matches = data[data['Date'].dt.date == today_date]
today_matches = data[data['Date'] == '2024-01-29']

# Function for extracting goals only from goals and penalties
def extract_regular_goals(score_value):
    if pd.isna(score_value):
        return 0  # Return 0 for NaN values
    elif isinstance(score_value, (int, float)):
        return int(score_value)  # If it's already an integer or float, convert to int
    elif isinstance(score_value, str):
        goals_match = re.match(r'^(\d+)', score_value)
        if goals_match:
            return int(goals_match.group(1))
    return 0  # Return 0 if no match is found or if the value is not convertible
    
# Apply the function to 'GF' and 'GA' columns using direct assignment
today_matches.loc[:, 'GF'] = today_matches['GF'].apply(extract_regular_goals)
today_matches.loc[:, 'GA'] = today_matches['GA'].apply(extract_regular_goals)

# Convert the 'GF' and 'GA' columns to numeric to ensure they are integers
today_matches.loc[:, 'GF'] = pd.to_numeric(today_matches['GF'])
today_matches.loc[:, 'GA'] = pd.to_numeric(today_matches['GA'])

# Looping today's matches for goal difference average
for index, row in today_matches.iterrows():
    # Now 'row' is a pandas Series, and you can access the values using column names
    club_name = row['Club_name']
    opponent_name = row['Opponent']

    # Filter data for all matches of 'club_name'
    club_matches = data[data['Club_name'] == club_name]
    club_matches = club_matches[club_matches['Date'] < '2024-01-09']

    # Filter data for all matches of 'opponent'
    opponent_matches = data[data['Club_name'] == opponent_name]
    opponent_matches = opponent_matches[opponent_matches['Date'] < '2024-01-09']

    # Apply the function to 'GF' and 'GA' columns using direct assignment
    club_matches['GF'] = club_matches['GF'].apply(extract_regular_goals)
    club_matches['GA'] = club_matches['GA'].apply(extract_regular_goals)
    opponent_matches['GF'] = opponent_matches['GF'].apply(extract_regular_goals)
    opponent_matches['GA'] = opponent_matches['GA'].apply(extract_regular_goals)

    # Convert the 'GF' and 'GA' columns to numeric to ensure they are integers
    club_matches['GF'] = pd.to_numeric(club_matches['GF'])
    club_matches['GA'] = pd.to_numeric(club_matches['GA'])
    opponent_matches['GF'] = pd.to_numeric(opponent_matches['GF'])
    opponent_matches['GA'] = pd.to_numeric(opponent_matches['GA'])

    # Calculating average goal difference for club_name
    if len(club_matches) > 0:  # Check if there are matches for the club
        club_name_GD_Total = club_matches["GF"].sum() - club_matches["GA"].sum()
        num_matches_played_club = len(club_matches)
        club_name_GD_Average = club_name_GD_Total / num_matches_played_club
    else:
        club_name_GD_Average = 0

    # Calculating average goal difference for opponent
    if len(opponent_matches) > 0:  # Check if there are matches for the opponent
        opponent_GD_Total = opponent_matches["GF"].sum() - opponent_matches["GA"].sum()
        num_matches_played_opponent = len(opponent_matches)
        opponent_GD_Average = opponent_GD_Total / num_matches_played_opponent
    else:
        opponent_GD_Average = 0


    # Collecting data
    match = [
        {
            "Team_A"       : club_name,
            "Team_A_Av(GD)": club_name_GD_Average,
            "Team_A_C(GF)" : 0,
            "Team_B"       : opponent_name,
            "Team_B_Av(GD)": opponent_GD_Average,
            "Team_B_C(GF)" : 0
        }
    ]

    # appending predicted matches
    predicted_data = pd.concat([predicted_data, pd.DataFrame(match)], ignore_index=True)   



# Delay to display computing status
#time.sleep(3)
os.system('cls' if os.name == 'nt' else 'clear')    
print(f"{GREEN}Average goal difference Calculation successful{RESET}")



# SHRINKING DATA
# Looping through the "Team_B_Av(GD)"
for index, row in predicted_data.iterrows():

    # Looking for Team_B_Av(GD) with zeros
    if row["Team_B_Av(GD)"] == 0:
        
        # Taking the team's name with the zero
        team = row["Team_B"]

        # Looping the whole data again to find the team
        for index_again, row_again in predicted_data.iterrows():

            # Looking if the team is in Team_A(s)
            if team in row_again["Team_A"]:

                # Updating Team_B name
                predicted_data.at[index, "Team_B"] = row_again["Team_A"]

                # Updating GD Average
                predicted_data.at[index_again, "Team_B_Av(GD)"] = row["Team_A_Av(GD)"]



# Delay to display computing status
#time.sleep(3)
print(f"{GREEN}Shrinking data successful{RESET}")



# REMOVING DUPLICATES
restart_iteration = True
while restart_iteration:
    restart_iteration = False

    # Looping rows
    for index, row in predicted_data.iterrows():
        
        # Taking Name and Average GD
        team_A_name = row["Team_A"]
        team_A_Av_GD = row["Team_A_Av(GD)"]
        team_B_name = row["Team_B"]
        team_B_Av_GD = row["Team_B_Av(GD)"]

        # Looking for similiars, by Looping
        for index_again, row_again in predicted_data.iterrows():
            if team_A_name == row_again["Team_B"]:
                if team_B_name == row_again["Team_A"]:
                    if team_A_Av_GD == row_again["Team_B_Av(GD)"]:
                        if team_B_Av_GD == row_again["Team_A_Av(GD)"]:
                            
                            predicted_data = predicted_data.drop(index)
                            
                            restart_iteration = True
                            break



# Delay to display computing status
#time.sleep(3)
print(f"{GREEN}Removing duplicates successful{RESET}")



# COMMON OPPONENTS MATCHING        
# Looping today's matches
for index, row in predicted_data.iterrows():
    # Now 'row' is a pandas Series, and you can access the values using column names
    club_name = row['Team_A']
    opponent_name = row['Team_B']

    # Filter data for all matches of 'club_name'
    club_matches = data[data['Club_name'] == club_name]
    club_matches = club_matches[club_matches['Date'] < '2024-01-09']

    # Filter data for all matches of 'opponent'
    opponent_matches = data[data['Club_name'] == opponent_name]
    opponent_matches = opponent_matches[opponent_matches['Date'] < '2024-01-09']

    # Apply the function to 'GF' and 'GA' columns using direct assignment
    club_matches['GF'] = club_matches['GF'].apply(extract_regular_goals)
    club_matches['GA'] = club_matches['GA'].apply(extract_regular_goals)
    opponent_matches['GF'] = opponent_matches['GF'].apply(extract_regular_goals)
    opponent_matches['GA'] = opponent_matches['GA'].apply(extract_regular_goals)

    # Convert the 'GF' and 'GA' columns to numeric to ensure they are integers
    club_matches['GF'] = pd.to_numeric(club_matches['GF'])
    club_matches['GA'] = pd.to_numeric(club_matches['GA'])
    opponent_matches['GF'] = pd.to_numeric(opponent_matches['GF'])
    opponent_matches['GA'] = pd.to_numeric(opponent_matches['GA'])

    club_common_GF = 0
    opponent_common_GF = 0
    
    # Looping through club
    for index_club, row_club in club_matches.iterrows():
        
        # Looping through opponent
        for index_opponent, row_opponent in opponent_matches.iterrows():
            
            # When both their opponents match
            if (row_club['Opponent'] in row_opponent['Opponent']) or (row_opponent['Opponent'] in row_club['Opponent']):

                # Finding who's GA is greater
                if row_club['GA'] > row_opponent['GA']:
                    club_common_GF = club_common_GF + row_club['GF']
                    opponent_common_GF = opponent_common_GF + row_opponent['GF'] + row_club['GA'] - row_opponent['GA']
                    
                elif row_opponent['GA'] > row_club['GA']:
                    club_common_GF = club_common_GF + row_club['GF'] + row_opponent['GA'] - row_club['GA']
                    opponent_common_GF = opponent_common_GF + row_opponent['GF']

    #Updating Club's Common Opponents Matching 
    predicted_data.at[index, "Team_A_C(GF)"] = club_common_GF

    #Updating Opponent's Common Opponents Matching 
    predicted_data.at[index, "Team_B_C(GF)"] = opponent_common_GF



# Delay to display computing status
#time.sleep(3)
print(f"{GREEN}Common Opponents Matching successful{RESET}")



# ADDING LAST ENCOUNTERED MATCH
predicted_data['Team_A_Last'] = None
predicted_data['Team_B_Last'] = None

for index, row in predicted_data.iterrows():
    # Taking names
    club_name = row['Team_A']
    opponent_name = row['Team_B']

    # Filter data for all matches of 'club_name'
    club_matches = data[data['Club_name'] == club_name]
    club_matches = club_matches[club_matches['Date'] < '2024-01-09']

    # Filter data for all matches of 'opponent'
    opponent_matches = data[data['Club_name'] == opponent_name]
    opponent_matches = opponent_matches[opponent_matches['Date'] < '2024-01-09']

    # Apply the function to 'GF' and 'GA' columns using direct assignment
    club_matches['GF'] = club_matches['GF'].apply(extract_regular_goals)
    club_matches['GA'] = club_matches['GA'].apply(extract_regular_goals)
    opponent_matches['GF'] = opponent_matches['GF'].apply(extract_regular_goals)
    opponent_matches['GA'] = opponent_matches['GA'].apply(extract_regular_goals)

    # Convert the 'GF' and 'GA' columns to numeric to ensure they are integers
    club_matches['GF'] = pd.to_numeric(club_matches['GF'])
    club_matches['GA'] = pd.to_numeric(club_matches['GA'])
    opponent_matches['GF'] = pd.to_numeric(opponent_matches['GF'])
    opponent_matches['GA'] = pd.to_numeric(opponent_matches['GA'])

    # Looping through club only
    for index_club, row_club in club_matches.iterrows():
        
        if (row_club['Club_name'] in club_name):
            if (row_club['Opponent'] in opponent_name):

                predicted_data.at[index, "Team_A_Last"] = row_club["GF"]
                predicted_data.at[index, "Team_B_Last"] = row_club["GA"]

            


# Saving data
predicted_data.to_csv(file_path + "for prediction data.csv", index=False)
print(f"{GREEN}Data Saved Successfully {YELLOW}(*^_^*){RESET}")
print(predicted_data.tail())