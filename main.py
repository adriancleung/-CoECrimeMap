import sqlite3
import sys
import task_1 as t1
import task_2 as t2
import task_3 as t3
import task_4 as t4

def main():
    # Purpose: Connect to db and calls menu
    # Parameters: Takes no parameters
    # Return: None 
    
    try: # uses database that is passed in as a command line argument
        path = './' + str(sys.argv[1])
    except: # uses default database if no database is passed in as a command line argument
        path = './a4-sampled.db'
        
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys=ON;')
    
    menu(conn, c)
    
    conn.commit()
    conn.close()
    
    return 0

def menu(conn, c):
    # Purpose: Prints out the menu for the program
    # Parameters: Passes connected db and cursor
    # Return: None
    
    # Count number of executions for each task
    count_1 = 1
    count_2 = 1
    count_3 = 1
    count_4 = 1
    
    while True: 
        print('''
=== Assignment 4 Project ===
(1) Month-wise total count of certain crime type
(2) Map most/least populous neighbourhoods
(3) Top neighbourhoods and their crime count of certain crime type
(4) Top neighbourhoods with the highest crimes to population ratio
        
(q) Quit
''')
        
        user_input = str(input('Enter command: '))
        option_lst = ['1', '2', '3', '4', 'q']
        
        if user_input not in option_lst:
            print('\nInvalid command. Please enter again')
        else:
            if user_input == '1':
                t1.task_1(conn, c, count_1)
                count_1 += 1
            if user_input == '2':
                t2.task_2(conn, c, count_2)
                count_2 += 1
            if user_input == '3':
                t3.task_3(conn, c, count_3)
                count_3 += 1
            if user_input == '4':
                t4.task_4(c, count_4)
                count_4 += 1
            if user_input == 'q':
                break

main()