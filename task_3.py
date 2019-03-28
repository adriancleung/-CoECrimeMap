import sqlite3
import pandas as pd
import folium
import os 
import webbrowser
import math

def task_3(conn, cursor, count_3):
    # Purpose: Given a range of years, a crime type, and an integer N, it will display on a map
    #          the top N neighbourhoods in terms of incidents of the specified crime
    #          in that range of years.
    #          Erroneous input results in an error and the option to try input again.
    # Parameters: Passes a cursor connected to database and a count
    # Return: None       
    while True:
        print("=== Task 3 ===")
        try:
            start_year = int(input('Enter start year (YYYY): '))
            end_year = int(input('Enter end year (YYYY): '))
            N = int(input('Enter number of neighborhoods: '))
            crime_type = str(input('Enter the crime type: '))
            
            cursor.execute('''
SELECT crime.Neighbourhood_Name, sum(crime.Incidents_Count) as Number_of_Incidents, Latitude, Longitude
FROM crime_incidents as crime
JOIN coordinates ON crime.Neighbourhood_Name = coordinates.Neighbourhood_Name
WHERE (Year BETWEEN :start AND :end) AND (crime.Crime_Type = :crime_type)
GROUP BY crime.Neighbourhood_Name
ORDER BY Number_of_Incidents DESC
LIMIT :N;
''', {"start" : start_year, "end" : end_year, "crime_type" : crime_type, "N" : N})
            
            table = cursor.fetchall() # columns: Neighbourhood, Number_of_Incidents, Latitude, Longitude
            m = folium.Map(location=[53.5444, -113.4909], zoom_start=11) # Map of Edmonton
            size = 450 # Largest desired size; bubbles' size proportional to crime rate of interest
            prev_crime_rate = table[0][1]
            
            for item in table:
                
                size = size * math.sqrt(item[1]/prev_crime_rate) # scale down by ratio of current crime rate to last neighbourhood's rate
                prev_crime_rate = item[1]
                if size < 150:
                    size = 150 # minimum size of 150
                
                lat = item[2]
                long = item[3]
                folium.Circle(location=[item[2], item[3]], 
                              popup= str(item[0]) + "<br>"+ str(item[1]), 
                              radius= size, 
                              color= 'crimson', 
                              fill= True,
                              fill_color= 'crimson').add_to(m)
            url = 'Q3-' + str(count_3) +'.html' # Store map onto a html url
            m.save(url) 
            webbrowser.open("file://"+ os.path.realpath(url)) # Opens up the html
            return
        except: # Catches any errors
            user_input = input("\nError occurred/Invalid Input. Press Enter to Restart or Q to Quit: ")
            if(user_input.lower() == 'q'):
                return
            else:
                continue        
                