import sqlite3
import folium
import os
import webbrowser

def task_2(conn, c, count_2):
    # Purpose: Asks uer to input the number of neighbourhoods to show and
    # the task will visualize, on a map, the N most populous and N least
    # populous neighbourhoods
    # Parameters: Takes in the connection to the database, cursor location,
    # and the current execuction count of the task
    # Return: None
    
    print('=== Task 2 ===')
    while True:
        try:
            num_of_locs = int(input('Enter number of locations: '))
            
            # General query that gets all neighbourhoods with population, 
            # latitudes, and longitudes that are not zeros and orders in
            # descending order based on population
            c.execute('''SELECT population.Neighbourhood_Name, 
SUM(CANADIAN_CITIZEN + NON_CANADIAN_CITIZEN + NO_RESPONSE) as pop, 
coordinates.Latitude, coordinates.Longitude
FROM population
LEFT JOIN coordinates ON coordinates.Neighbourhood_Name = population.Neighbourhood_Name
GROUP BY population.Neighbourhood_Name
HAVING pop > 0 AND coordinates.Latitude != 0 AND coordinates.Longitude != 0
ORDER BY pop DESC''')
    
            rows = c.fetchall()
            num_of_rows = len(rows)
            m = folium.Map(location=[53.5444, -113.4909], zoom_start=11)
    
            # checks to see whether the given input is greater than the
            # actual number of neighbourhoods. If so, add all neighbourhoods
            # to the map
            if (num_of_locs * 2) >= num_of_rows:
                for points in rows:
                    folium.Circle(
                        location = [points[2], points[3]],
                        popup = points[0] + '<br>' + str(points[1]),
                        radius = (points[1]) / 5, # scales down by 5 based on population
                        color = 'crimson',
                        fill = True,
                        fill_color = 'crimson'
                        ).add_to(m)
            else:
                # gets the N most populous neighbourhoods and add it to the map
                for points in range(0,num_of_locs):
                    folium.Circle(
                        location = [rows[points][2], rows[points][3]],
                        popup = rows[points][0] + '<br>' + str(rows[points][1]),
                        radius = (rows[points][1]) / 5, # scales down by 5 based on population
                        color = 'crimson',
                        fill = True,
                        fill_color = 'crimson'
                        ).add_to(m)
                
                # gets the N least populour neighbourhoods and add it to the map
                for points in range(num_of_rows - 1, (num_of_rows - 1) - num_of_locs, -1):
                    folium.Circle(
                        location = [rows[points][2], rows[points][3]],
                        popup = rows[points][0] + '<br>' + str(rows[points][1]),
                        radius = (rows[points][1]) * 5, # scales up by 5 based on population
                        color = 'blue',
                        fill = True,
                        fill_color = 'blue'
                        ).add_to(m)
            break
        except:
            # if an error occurred, user will be asked to restart or quit the
            # task
            user_input = input('\nAn error occurred. Press Enter to Restart or Q to Quit: ')
            if(user_input.lower() == 'q'):
                return
            else:
                continue            
            
    url = 'Q2-' + str(count_2) + '.html' 
    m.save(url) # saves map as Q2-N.html
    webbrowser.open('file://' + os.path.realpath(url)) # opens map in browser
    return