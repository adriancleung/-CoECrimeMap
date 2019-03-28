import sqlite3
import folium
import os 
import webbrowser

def task_4(cursor, count_4):
    # Purpose: Given a range of years and an integer N, it will display on a map
    #          the name of the top N neighborhoods with the highest crimes to population ratio
    #          and the most frequent crimt type within the provided range.
    # Parameters: Passes a cursor connected to database and a count
    # Return: None       
    while True:
        print("=== (Task 4) ===")
        try:
            start_year = int(input('Enter start year (YYYY): '))
            end_year = int(input('Enter end year (YYYY): '))
            neighborhoods = int(input('Enter number of neighborhoods: '))
            cursor.execute('''
SELECT DISTINCT population.Neighbourhood_Name,
(SUM(Incidents_Count) * 1.0/(CANADIAN_CITIZEN + NON_CANADIAN_CITIZEN + NO_RESPONSE)) as Ratio,
coordinates.Latitude, coordinates.Longitude
FROM population
INNER JOIN crime_incidents ON population.Neighbourhood_Name = crime_incidents.Neighbourhood_Name
INNER JOIN coordinates ON population.Neighbourhood_Name = coordinates.Neighbourhood_Name
WHERE (Year BETWEEN :start AND :end) AND (CANADIAN_CITIZEN + NON_CANADIAN_CITIZEN + NO_RESPONSE) > 0 AND (coordinates.Latitude != 0 and coordinates.Longitude != 0)
GROUP BY population.Neighbourhood_Name
ORDER BY Ratio DESC
LIMIT :n;
           ''', {"start" : start_year, "end" : end_year, "n" : neighborhoods})
            rows = cursor.fetchall() # Gets the results of the top N neighborhoods with high crime to pop ratio
            m = folium.Map(location=[53.5444, -113.4909], zoom_start=11) # Makes a Map of Edmonton
            size = 500 # Size of bubble markers on map
            if not rows:
                print("Error. Upper bound and lower bound are conflicting")
                continue
            for item in rows:
                if (size < 200):
                    size = 200
                cursor.execute('''
SELECT Neighbourhood_Name, Crime_Type, MAX(SUM_INCIDENTS)
FROM (SELECT Neighbourhood_Name, Crime_Type, SUM(Incidents_Count) as SUM_INCIDENTS
    FROM crime_incidents
    WHERE Neighbourhood_Name = :name and (Year BETWEEN :start AND :end)
    GROUP BY Crime_Type);
                ''', {"start" : start_year, "end" : end_year, "name" : item[0]})
                crime = cursor.fetchall() # Gets the results of most frequent crime type
                folium.Circle(location=[item[2], item[3]], 
                              popup= str(item[0]) + "<br>" + str(crime[0][1])+"<br>"+ str(item[2]), 
                              radius= size, 
                              color= 'crimson', 
                              fill= True,
                              fill_color= 'crimson').add_to(m)    
                size = size * 0.90
            url = 'Q4-' + str(count_4) +'.html' # Store map onto a html url
            m.save(url) 
            webbrowser.open("file://"+ os.path.realpath(url)) # Opens up the html
            return
        except: # Catches any errors
            user_input = input("\nError occurred/Invalid Input. Press Enter to Restart or Q to Quit: ")
            if(user_input.lower() == 'q'):
                return
            else:
                continue