import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def task_1(conn, c, count_1):
    # Purpose: Asks user for a range of years and a type of crime, will 
    # print a bar chart of the given data, and save the chart as a png image
    # Parameters: Takes in the connection to the database, cursor location,
    # and the current execuction count of the task
    # Return: None
    
    print('=== Task 1 ===')
    while True:
        try:
            start_year = input('Enter start year (YYYY): ')
            end_year = input('Enter end year (YYYY): ')
            crime_type = input('Enter crime type: ')
            
            if start_year > end_year: # error checking to see if range is valid
                print('\nStart year cannot be greater than end year. Please try again.\n')
                continue
                
            df = pd.read_sql_query(
                "SELECT crime_incidents.Month, crime.Incidents \
                FROM crime_incidents \
                LEFT JOIN (SELECT Month, COUNT(Incidents_Count) as Incidents \
                FROM crime_incidents \
                WHERE Crime_Type = '"+ crime_type + "' AND Year >= " + str(start_year) 
                + " AND Year <= " + str(end_year) + " \
                GROUP BY Month) \
                AS crime ON crime.Month=crime_incidents.Month \
                GROUP BY crime_incidents.Month \
                LIMIT 12", conn) # query that is executed with the given inputs
                
            plot = df.plot.bar(x='Month')
            break
        except:
            # if there are no data to plot or an error occurred when executing
            # the query, user will be asked to restart or quit the task
            user_input = input('\nAn error occurred or no data to plot. Press Enter to Restart or Q to Quit: ')
            if(user_input.lower() == 'q'):
                return
            else:
                continue
    
    plt.plot()
    plt.savefig('Q1-' + str(count_1) +'.png') # saves the chart as Q1-N.png
    plt.show()
    return