arfrom bs4 import BeautifulSoup
import csv
import datetime
import os
import pandas as pd
import random
import requests
import time

# ANSI escape codes for colors
BLUE = '\033[94m'
BOLD = '\033[1m'
GREEN = '\033[92m'
RED = '\033[31m'
RESET = '\033[0m'
YELLOW = '\033[93m'

#Emoji set
emojis = ["~_~","U_U","X_X","*_*","=_=","-_-","> <","Y.Y"]

#Time delays between pages
t=3             #5 seconds

#file path for storage      #os.path.abspath(__file__)             #.replace("Scraper.py","")
file_path = 'C:\\Users\\Pavilion\\Documents\\Programming\\Python\\Projects\\Football\\BAFI\\Records_Taken\\'
#file_path_for_all_data = file_path + 'Matches Data.csv'
file_path_for_all_data = file_path + datetime.date.today().strftime("%Y-%m-%d") + '.csv'

file_path_for_last_data = file_path + 'Last Match Data.csv'

#Creating matches data frame
matches_data = pd.DataFrame(columns=["Country","Club_name", "Date", "GF", "GA", "Opponent"])

#Creating last match saved data frame
last_match_data = pd.DataFrame(columns=["Country","Club_name", "Date", "GF", "GA", "Opponent"])

#All Countries Page URL
url_All_Countries = "https://fbref.com/en/squads/"

#Total percentage
percentage = 0
countries = 0

#Header for identification
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Getting the All Countries Page
response_Countries = requests.get(url_All_Countries, headers=header)


# Check if the request was successful (status code 200)
if response_Countries.status_code == 200:
 
    #Checking if file already exists
    if os.path.exists(file_path_for_all_data):
        
        #Booling the continue process
        resume_data_extract = True

        #Loading data from the CSV file into pandas DataFrame
        matches_data = pd.read_csv(file_path_for_all_data)

        #checking last record
        last_match_data = pd.read_csv(file_path_for_last_data)

        #Showing continue from last save data all new
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"The file in {file_path_for_all_data}{RED} exists, {YELLOW}continued data extract.{RESET}")

        #Passing the all countries html page by bs4
        allCountriesPage = BeautifulSoup(response_Countries.text, 'html.parser')

        #taking number of countries
        number_of_countries = len(allCountriesPage.find("table",{"id":"countries"}).find("tbody").find_all("tr"))
        percentage_for_each_country = 100/number_of_countries

        #Taking the last country and its index
        start_index = 0
        if resume_data_extract == True:
            last_country = last_match_data.iloc[0]["Country"]
            for index, country in enumerate(allCountriesPage.find("table",{"id":"countries"}).find("tbody").find_all("tr")):
                if last_country == country.find("th").text:
                    start_index = index + 1
                    percentage = 100/number_of_countries*(index+1)
                    countries = start_index+1
                    resume_data_extract = False


        #Looping through countries
        for country in allCountriesPage.find("table",{"id":"countries"}).find("tbody").find_all("tr")[start_index:]:
                
            #Taking country name
            country_name = country.find("th").text

            #Single Country URL
            url_Country = 'https://fbref.com'+country.find("th",{"data-stat":"country"}).find("a").get('href')

            # Getting the Single Country Page
            response_Country = requests.get(url_Country, headers=header)

            #Delay of 3 seconds before entering respective country page
            time.sleep(t)

            #Check if the request was successful (status code 200)
            if response_Country.status_code == 200:
                    
                #Passing the country html page by bs4
                CountryPage = BeautifulSoup(response_Country.text, 'html.parser')

                #taking number of clubs
                number_of_clubs = len(CountryPage.find("table",{"id":"clubs"}).find("tbody").find_all("tr"))
                percentage_for_each_club = percentage_for_each_country/number_of_clubs

                #Looping through clubs in the country
                for index, Club in enumerate(CountryPage.find("table",{"id":"clubs"}).find("tbody").find_all("tr")):

                    #Checking if the club max season has 2024
                    if "2024" in Club.find("td",{"data-stat":"max_season"}).text:

                        #Taking club name
                        club_name = Club.find("th").text

                        #Club url
                        url_Club='https://fbref.com'+Club.find("th").find("a").get('href').replace("/history/","/").replace("-and-History","")

                        # Getting the Single Country Page
                        response_Club = requests.get(url_Club, headers=header)

                        #Delay of 3 seconds before entering respective club page
                        time.sleep(t)

                        #Check if the request was successful (status code 200)
                        if response_Club.status_code == 200:
                                
                            #Passing the country html page by bs4
                            ClubPage = BeautifulSoup(response_Club.text, 'html.parser')

                            try:
                                #Looping for matches in Club
                                for Match in ClubPage.find("table",{"id":"matchlogs_for"}).find("tbody").find_all("tr"):
                                
                                    #taking match data
                                    new_match = [
                                        {"Country"  : country_name,
                                         "Club_name": club_name,
                                         "Date"     : Match.find("th",{"data-stat":"date"}).text,
                                         "GF"       : Match.find("td",{"data-stat":"goals_for"}).text,
                                         "GA"       : Match.find("td",{"data-stat":"goals_against"}).text,
                                         "Opponent" : Match.find("td",{"data-stat":"opponent"}).text
                                        }
                                    ]
                        
                                    #appending match data
                                    matches_data = pd.concat([matches_data, pd.DataFrame(new_match)], ignore_index=True)
                            except AttributeError:
                                os.system('cls' if os.name == 'nt' else 'clear')
                                print(f"{RED}Skipping a match of {club_name}, because of no data{RESET}")
                                continue

                        else:
                            print(f"Failed to retrieve Single Club page. Status code: {response_Country.status_code}")           
                    

                    #Saving data after completing all clubs in a country
                    if index == len(CountryPage.find("table",{"id":"clubs"}).find("tbody").find_all("tr")) - 1:
                        countries = countries + 1

                        #Saving the last match
                        last_match_data = pd.DataFrame(new_match)

                        #Checking progress
                        percentage = percentage + percentage_for_each_country

                        #Showing progress
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print(f"{BLUE}Data taken and saved!{RESET}\n")    
                        print(f"{YELLOW}Contries extracted: {countries}/{number_of_countries}\n")
                        print(f"{YELLOW}Percentage        : {percentage:.3}%\n")
                        print(f"\t{RED}"+random.choice(emojis)+f"{RESET}\n\n")

                        # Save to CSV
                        matches_data.to_csv(file_path_for_all_data, index=False)
                        last_match_data.to_csv(file_path_for_last_data, index=False)

            
            else:
                print(f"Failed to retrieve Single Country page. Status code: {response_Country.status_code}")           

    else:
        #Showing saving data all new
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"The file in {file_path_for_all_data} {RED}doesn't exist, {YELLOW}creating new one.{RESET}")

        #Passing the all countries html page by bs4
        allCountriesPage = BeautifulSoup(response_Countries.text, 'html.parser')

        #taking number of countries
        number_of_countries = len(allCountriesPage.find("table",{"id":"countries"}).find("tbody").find_all("tr"))
        percentage_for_each_country = 100/number_of_countries

        start_index = 0

        #Looping through countries
        for country in allCountriesPage.find("table",{"id":"countries"}).find("tbody").find_all("tr"):
                
            #Taking country name
            country_name = country.find("th").text

            #Single Country URL
            url_Country = 'https://fbref.com'+country.find("th",{"data-stat":"country"}).find("a").get('href')

            # Getting the Single Country Page
            response_Country = requests.get(url_Country, headers=header)

            #Delay of 3 seconds before entering respective country page
            time.sleep(t)

            #Check if the request was successful (status code 200)
            if response_Country.status_code == 200:
                    
                #Passing the country html page by bs4
                CountryPage = BeautifulSoup(response_Country.text, 'html.parser')

                #taking number of clubs
                number_of_clubs = len(CountryPage.find("table",{"id":"clubs"}).find("tbody").find_all("tr"))
                percentage_for_each_club = percentage_for_each_country/number_of_clubs

                #Looping through clubs in the country
                for index, Club in enumerate(CountryPage.find("table",{"id":"clubs"}).find("tbody").find_all("tr")):

                    #Checking if the club max season has 2024
                    if "2024" in Club.find("td",{"data-stat":"max_season"}).text:

                        #Taking club name
                        club_name = Club.find("th").text

                        #Club url
                        url_Club='https://fbref.com'+Club.find("th").find("a").get('href').replace("/history/","/").replace("-and-History","")

                        # Getting the Single Country Page
                        response_Club = requests.get(url_Club, headers=header)

                        #Delay of 3 seconds before entering respective club page
                        time.sleep(t)

                        #Check if the request was successful (status code 200)
                        if response_Club.status_code == 200:
                                
                            #Passing the country html page by bs4
                            ClubPage = BeautifulSoup(response_Club.text, 'html.parser')

                            #Looping for matches in Club
                            for Match in ClubPage.find("table",{"id":"matchlogs_for"}).find("tbody").find_all("tr"):

                                #taking match data
                                new_match = [
                                    {"Country"  : country_name,
                                     "Club_name": club_name,
                                     "Date"     : Match.find("th",{"data-stat":"date"}).text,
                                     "GF"       : Match.find("td",{"data-stat":"goals_for"}).text,
                                     "GA"       : Match.find("td",{"data-stat":"goals_against"}).text,
                                     "Opponent" : Match.find("td",{"data-stat":"opponent"}).text
                                    }
                                ]
                        
                                #appending match data
                                matches_data = pd.concat([matches_data, pd.DataFrame(new_match)], ignore_index=True)

                        else:
                            print(f"Failed to retrieve Single Club page. Status code: {response_Country.status_code}")           
                    

                    #Saving data after completing all clubs in a country
                    if index == len(CountryPage.find("table",{"id":"clubs"}).find("tbody").find_all("tr")) - 1:
                        if(start_index>0):
                            countries = index
                        countries = countries + 1

                        #Saving the last match
                        last_match_data = pd.DataFrame(new_match)

                        #Checking progress
                        percentage = percentage + percentage_for_each_country

                        #Showing progress
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print(f"{BLUE}Data taken and saved!{RESET}\n")    
                        print(f"{YELLOW}Contries extracted: {countries}/{number_of_countries}\n")
                        print(f"{YELLOW}Percentage        : {percentage:.3}%\n")
                        print(f"\t{RED}"+random.choice(emojis)+f"{RESET}\n\n")

                        # Save to CSV
                        matches_data.to_csv(file_path_for_all_data, index=False)
                        last_match_data.to_csv(file_path_for_last_data, index=False)

            
            else:
                print(f"Failed to retrieve Single Country page. Status code: {response_Country.status_code}")           
                   

else:
    print(f"Failed to retrieve the All Countries page. Status code: {response_Countries.status_code}")

#Showing progress for all data saved
print(f"{GREEN}Data Successfully taken and saved!{RESET}")