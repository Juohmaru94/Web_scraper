#imports
from collections import Counter
from bs4 import BeautifulSoup
import requests
import pandas as pd

# X= first game Y= last game
# X AND Y ARE PART OF THE LINKS THAT ARE TO BE SCRAPED 
x = 12480
y = 12481
final_list = []

#Combine the two lists/This is for the end, but has to be placed here
def combine():
    combined_list = home_minutes + away_minutes
    return combined_list


for game_number in range(x,y):
    
    url = f'https://www.premierleague.com/match/{game_number}'
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'lxml')
    
    #This is for extra info about each game if necessary
    '''
    home_team = soup.find('div', class_='team home').find('a', class_='teamName').find('span', class_='long').text
    away_team = soup.find('div', class_='team away').find('a', class_='teamName').find('span', class_='long').text
    referee = soup.find('div', class_='referee').text.strip()
    attendance = soup.find('div', class_='attendance hide-m').text.replace('Att:','')
    matchweek = soup.find('div', class_='current').find('div', class_='long').text 
    home_scorers = soup.find('div', class_='matchEvents matchEventsContainer').find_all('div', class_='home')
    away_scorers = soup.find('div', class_='matchEvents matchEventsContainer').find_all('div', class_='away')
    match_score = soup.find('div', class_= 'score fullTime').text
    
    
    print(f'{matchweek}: {home_team} vs {away_team}: {match_score}')
    print(f'Referee: {referee}')
    print(f'Attendance:{attendance}\n')
    '''
    home_scorers = soup.find('div', class_='matchEvents matchEventsContainer').find_all('div', class_='home')
    away_scorers = soup.find('div', class_='matchEvents matchEventsContainer').find_all('div', class_='away')
    
    #Obtain a splited list of names and minutes of goals/cards
    def home_stats():
        for j in home_scorers:
            return (j.text.split())
    
    def away_stats():
        for i in away_scorers:
            return(i.text.split())
    
    #Replace ' from the minute, to make it an int for home and away
    def replace_home():
        new_list_home = [element.replace("'", "") for element in home_stats()]
        return new_list_home
        
    
    def replace_away():
        new_list_away = [element.replace("'", "") for element in away_stats()]
        return new_list_away
    
    #Remove minutes that yellow/red cards were given (home)
    def remove_home_cards(home_card):
        home2 = [i for i in range(len(replace_home())) if replace_home()[i] =='Red' or replace_home()[i] =='Second']
        home2.sort(reverse=True)
       
        for x in home2:
            home_card.pop(x-1)
            home_card.pop(x-2)
        
        return home_card
     
    #Remove minutes that yellow/red cards were given (away)
    def remove_away_cards(away_card):
        away2 = [i for i in range(len(replace_away())) if replace_away()[i] =='Red' or replace_away()[i] =='Second']
        away2.sort(reverse=True)
       
        for x in away2:
            away_card.pop(x-1)
            away_card.pop(x-2)
        return away_card
    
    
    #Replace the (,) because it collided when the same person scored twice or more
    def check_comas_home():    
        home_comas = [x.replace(",","") for x in remove_home_cards(replace_home())]
        return home_comas
    
    
    def check_comas_away():    
        away_comas = [x.replace(",","") for x in remove_away_cards(replace_away())]
        return away_comas
    
    
    #Function that keeps only numbers
    def convert_home(home):
        new_scorers = ([i for item in home for i in item.split()])
        home_list = [s for s in new_scorers if s.isdigit()]
        return home_list
    
    
    def convert_away(away):
        new_scorers = ([i for item in away for i in item.split()])
        away_list = [s for s in new_scorers if s.isdigit()]
        return away_list
    
    #Lists of minutes of goals scored home and away
    home_minutes = (convert_home(check_comas_home()))
    away_minutes = (convert_away(check_comas_away()))
    
    final_list.extend(combine())
 
#Dictionary created to see no. of goals for each minute
def final_results():
    d = Counter(final_list)
    #sort from 1min to 90min
    d = {int(k):int(v) for k,v in d.items()}
    final_dict = dict(sorted(d.items()))
    return final_dict
    

dict_final = final_results()

#DataFrame
df = pd.DataFrame(dict_final.items(), columns=['Minutes', 'No. of Goals'])
#print(df)


#Sum of Goals, if needed
Total = df['No. of Goals'].sum()
print (f'Total goals: {Total}')


#Export to CSV
df.to_csv('PremierLeague_16-17.csv', index=False)
