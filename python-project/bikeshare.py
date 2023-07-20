'''
This program is designed to look at the Bikeshare usage information for Chicago, New York City, and Washington in order to better understand common trends in locations, length of use, and user demographics.
'''

import time
import pandas as pd
import numpy as np
import bikeshare
 
# Load CSV files into dictionaries for cities, months, and weekdays
cities = pd.read_csv('cities.csv', dtype = str).set_index('city').to_dict(orient='index')
months = pd.read_csv('months.csv', dtype = str).set_index('month').to_dict(orient='index')
weekdays = pd.read_csv('weekdays.csv', dtype = str).set_index('weekday').to_dict(orient='index')
data_selection = pd.read_csv('data_selection.csv', dtype = str).set_index('selection').to_dict(orient='index')

def get_valid_input(valid_options):
'''
User is provided with a list of valid options pulled from the global dictionaries above. User input
is requested and matched against the dictionary, returning the dictionary key to be used as a filter.
'''
    input_str = 'Please choose from the available options: \n'
    for key, option in valid_options.items():
        input_str += f"{option['number']}. {key.title()}\n"
    
    while True:
        try:
            user_input = input(input_str).lower()
            for key, option in valid_options.items():
                if user_input == key or user_input in option.values():
                    return key
                    x = 1
                    break
                else:
                    x = 0
            if x == 0:
                print('Invalid input, please try again.\n')
        except:
            print('There was an error with your provided input. Please try again.')
            
def city_checker(): # Obtains city input and confirms selection.
# Only allows one city to be selected
    city = get_valid_input(cities)
    while True:
        check = str(input(f'It looks like you are trying to select {city.title()}, is this correct? (Y/N): ')).lower()
        if check == 'y' or check == 'yes':
            return city
        else:
            city = get_valid_input(cities)
 
def month_checker(): # Obtains month input and confirms selection.
# Will allow for all months to be selected, but otherwise only one is allowed.
    month = get_valid_input(months)
    while True:
        check = str(input(f'It looks like you are trying to select {month.title()}, is this correct? (Y/N): ')).lower()
        if check == 'y' or check == 'yes':
            return month
        else:
            month = get_valid_input(months)

def day_checker(): # Obtains which day of the week and confirms selection.
# Will allow for all days to be selected, but otherwise only one is allowed.
    day = get_valid_input(weekdays)
    while True:
        check = str(input(f'It looks like you are trying to select {day.title()}, is this correct? (Y/N): ')).lower()
        if check == 'y' or check == 'yes':
            return day
        else:
            day = get_valid_input(weekdays)

def load_data(city, month, day): # Pulls user inputs to filter data.
    # Loads data file into a dataframe converting each column into a string and stripping extra spaces
    filename = cities[city]['filename']
    df = pd.read_csv(filename, dtype = {'Trip Duration' : float}, parse_dates = ['Start Time', 'End Time'])

    # Ensure data frame is sorted by Start Time
    df = df.sort_values(by='Start Time')

    # Extracts month, day of week, and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # Converts Birth Year into a numeric value and fills in NaN values with None
    if 'Birth Year' in df.columns:
        df['Birth Year'] = pd.to_numeric(df['Birth Year']).replace('', None)

    # Filters by selected month
    if month != 'all':
        # Pulls the month number associated with the selected months as an int
        month = int(months[month]['number'])
            
        # Creates dataframe of selected months
        df = df[df['month'] == month]
    
    # Filters by selected day of week
    if day != 'all':
        # Create dataframe of selected days
        df = df[df['day_of_week'] == day.title()]
    
    print('-'*40)
    return df
    
def time_stats(df): # Displays statistics on the most frequent times of travel.
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Displays the most common month
    print('The most popular month is: ', df.groupby('month').size().idxmax())

    # Displays the most common day of week
    print('The most popular day of the week is: ', df.groupby('day_of_week').size().idxmax())

    # Displays the most common start hour
    print('The most popular hour is: ', df.groupby('hour').size().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df): # Displays statistics on the most popular stations and trip.
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Displays most commonly used start station
    print('The most used starting station is: ', df.groupby('Start Station').size().idxmax())

    # Displays most commonly used end station
    print('The most used ending station is: ', df.groupby('End Station').size().idxmax())

    # Displays most frequent combination of start station and end station trip
    station_combinations = df.groupby(['Start Station', 'End Station']).size()
    most_used_combination = station_combinations[station_combinations == station_combinations.max()]
    print('The most used station combination is:', most_used_combination.index[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df): # Displays statistics on the total and average trip duration.
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Displays total travel time
    print('The total travel time is: ', round(df['Trip Duration'].sum(),2))

    # Displays mean travel time
    print('The average travel time is: ', round(df['Trip Duration'].mean(),2))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df): # Displays statistics on bikeshare users.
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Displays counts of user types
    print('Total count by user types:\n', df['User Type'].value_counts().to_string())

    # Checks if 'Gender' column exists and displays counts
    if 'Gender' in df.columns:
        print('\nTotal count by Gender:\n', df['Gender'].fillna('Unk').value_counts().to_string())
    else:
        print('\nGender data is not available for this query.')
    
    # Checks if Birth Year column exists and displays earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('\nEarliest year of birth: ', int(df['Birth Year'].astype(float).min()))
        print('\nMost recent year of birth: ', int(df['Birth Year'].max()))
        print('\nMost common year of birth: ', int(df['Birth Year'].astype(float).mode().values[0]))
    else:
        print('\nBirth Year data is not available for this query.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_input(df): # Displays raw input for selected data 5 rows at a time
    x = 0
    print(df[x:(x+5)])
    while True:
        x += 5
        check = input('Would you like to view another 5 rows? (Y/N) ').lower()
        if x >= len(df):
            check2 = input('You have reached the end of the raw data, would you like to start over? (Y/N) ').lower()
            if check2 == 'y' or check == 'yes':
                x = 0
                print(df[x:(x+5)])
            elif check == 'n' or check == 'no':
                break
            else:
                print('Invalid response, please try again.')
        elif check == 'y' or check == 'yes' and x < len(df):
            print(df[x:(x+5)])
        elif check == 'n' or check == 'no':
            break
        else:
            print('Invalid response, please try again.')
        

def main(): # Loops through the program until the user inputs 'no'
    while True:
        df = load_data(city_checker(), month_checker(), day_checker())

        if not df.empty: # Checks that the selected data frame isn't empty, then provides data selection options
            while True:
                selection = get_valid_input(data_selection)
                function = getattr(bikeshare, data_selection[selection]['function'])
                function(df)
                print('-'*40)
                while True:
                    check = input('Would you like additional data from your query? (Y/N) ').lower()
                    if check == 'y' or check == 'yes':
                        break
                    elif check == 'n' or check == 'no':
                        break
                    else:
                        print('Invalid response, please try again.')
                if check == 'n' or check == 'no':
                        break
                            
        else:
            print('There does not appear to be any data for your selection.')

        while True:
            restart = input('Do you want to run a new query? (Y/N): ').lower()
            if restart == 'n' or restart == 'no':
                break
            elif restart == 'y' or restart == 'yes':
                break
            else:
                print('Invalid response, please try again.')
                
        if restart == 'n' or restart == 'no':
            print('Thank you for using the Bikeshare Data Program!')
            break

if __name__ == "__main__": # Starts the program
    print('Welcome to the Bikeshare Data Program, let\'s explore some data!')
    print('-'*40)
    main()