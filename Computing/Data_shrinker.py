from datetime import datetime
import numpy as np
import pandas as pd
import re

# Specifing file location
file_path = "C:\\Users\\Pavilion\\Documents\\Programming\\Python\\Projects\\Football\\BAFI\\Computing\\"
file_path_origin = file_path + "today's data.csv"

# Importing the file
data = pd.read_csv(file_path_origin)

# Looping through the "Team_B_Av(GD)"
for index, row in data.iterrows():

    # Looking for Team_B_Av(GD) with zeros
    if row["Team_B_Av(GD)"] == 0:
        
        # Taking the team's name with the zero
        team = row["Team_B"]

        # Looping the whole data again to find the team
        for index_again, row_again in data.iterrows():

            # Looking if the team is in Team_A(s)
            if team in row_again["Team_A"]:

                # Updating Team_B name
                data.at[index, "Team_B"] = row_again["Team_A"]

                # Updating GD Average
                data.at[index_again, "Team_B_Av(GD)"] = row["Team_A_Av(GD)"]
                


# Saving data
#data.to_csv(file_path + "Updated data.csv", index=False)

#print(data)

found = 0
# REMOVING DUPLICATES
restart_iteration = True

while restart_iteration:
    restart_iteration = False

    # Looping rows
    for index, row in data.iterrows():
        
        # Taking Name and Average GD
        team_A_name = row["Team_A"]
        team_A_Av_GD = row["Team_A_Av(GD)"]
        team_B_name = row["Team_B"]
        team_B_Av_GD = row["Team_B_Av(GD)"]

        # Looking for similiars, by Looping
        for index_again, row_again in data.iterrows():
            if team_A_name == row_again["Team_B"]:
                if team_B_name == row_again["Team_A"]:
                    if team_A_Av_GD == row_again["Team_B_Av(GD)"]:
                        if team_B_Av_GD == row_again["Team_A_Av(GD)"]:
                            
                            data = data.drop(index)
                            
                            restart_iteration = True
                            break

        
print(f"Found: {found}")
#data.to_csv(file_path + "Shrinked data.csv", index=False)