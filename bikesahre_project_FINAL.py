#here we import all the necessary libraies for the project
#this project was created as a .py file meant to run on the terminal

import datetime
import pandas as pd
import numpy as np
import time
import csv
import os.path

#These are the relative paths for all the files needed in the rest of program
my_path = os.path.dirname(__file__)
path1 = os.path.join(my_path, "../chicago.csv")
path2 = os.path.join(my_path, "../washington.csv")
path3 = os.path.join(my_path, "../new_york_city.csv")

#CREATINg a function to ask user which city they want to look at
#this and the next 2 functions have a while loop to restart the functions in case user enters unspecified str
user_city =''
def get_city():
    '''Asks the user for a city and returns the filename for that city's bike share data.
        Args:
    none.
        Returns:(str) Filename for a city's bikeshare data.
    '''
    while True:
        user_city = str(input('\nHello! Let\'s explore some US bikeshare data!\n'
               'Would you like to see data for Chicago, NYC, or Washington?\n')).lower()
        if any ([user_city=='nyc', user_city=='chicago',user_city=='washington']) :
            break
        print ('Lets try again....')

    return user_city

CITY_DATA = { 'chicago': 'chicago.csv',
              'nyc': 'new_york_city.csv',
              'washington': 'washington.csv' }
#city=get_city()

#CREATINg a time function to see if user wants to parse data with a time period or not
def get_time_period():
    '''Asks the user for a time period and returns the specified filter.
    Args:none.
    Returns: a str specifiyin the filter either by month or day or none
    '''
    while True:
        time_period = str(input('\nWould you like to filter the data by month, day, or not at all? Type "none" for no time filter.\n')).lower()
        if any ([time_period=='month',time_period=='day',time_period=='none']) :
            break
        print ('Lets try again...get it right!, time flies...')
    return time_period

#CREATINg MONTH function to ask for WHICH MONTH user is interested
def get_month():
    '''Asks the user for a month and returns the specified month.
    Args:none
    Returns: a str with the specified month
    '''
    while True:
        month = str(input('\nWhich month would you like to select? january, february, march, april, may, or june?\n')).lower()
        if any ([month=='january',month=='february',month=='march',month=='april',month=='may',month=='june']) :

  break
        print ('Lets try again...')
    return month

#CREATINg DAY function to ask which day user is interested
def get_day():
    '''Asks the user for a day and returns the specified day
    Args:none
    Returns: a str with the day of the week
    '''
    while True:
        day = str(input('\nWhich day of the week? monday,tuesday,wednesday,thrusday,friday,saturday, or sunday?\n')).lower()
        if any ([day=='monday',day=='tuesday',day=='wednesday',day=='thrusday',day=='friday',day=='saturday',day=='sunday']) :
            break
        print ('Lets try again...')
    return day

#Here we create a dataframe that has a city, month or day parse
df=''
def load_data(city,month,day):
    '''Loads a dataframe of the user specified city and starts parsing the data with the time_period filter if applicable
    Args:from user inputs gets the city month or day arguments
    Returns: a dataframe where the date has been changed to the datetime format and extra columns such as month
    day_of_week and hour have been added for further statistical analysis
    '''
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    # filter by month if applicable
    if month != 'none':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'none':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

#STATSNo1:gives out the most popular month in integers, the day, and hours for specific data
def popular_month(df1):
    '''
    description:gives you the most popular month in the df1 created
    in the load_data function
    Arguments: df1 (a dataframe created from the city and time period constrains)
    Return:the most popular month as a number (january=1,february=2,etc)
    '''
    popular_month = df1['month'].mode()[0]
    print ('The most popular month of traveling is:',popular_month)

def popular_day(df1):
    '''
    description:gives you the most popular day in the df1 created
    in the load_data function
    Arguments: df1 (a dataframe created from the city and time period constrains)
    Return:a string indicating the most popular day
    '''
    popular_day = df1['day_of_week'].mode()[0]
    print ('The most popular day of traveling is:',popular_day)
#pop_day=popular_day()

def popular_hour(df1):
    '''
    description:gives you the most popular hour in the df1 created
    in the load_data function
    Arguments: df1 (a dataframe created from the city and time period constrains)
    Return:a integer indicating the most popular traveling hour
    '''
    popular_hour = df1['hour'].mode()[0]
    print ('The most popular hour of traveling is:',popular_hour)
#pop_hour=popular_hour()

#STATSNo2:calculates the most popular start and end AND the most popular combination of these
def popular_stations(df1):
    '''
    description:gives you the most popular start and end stations
    Arguments: df1 (a dataframe created from the city and time period constrains)
    Return:a str indicating the start and end stations
    '''
    popular_start_station_counts = df1['Start Station'].value_counts().index.tolist()
    pop_start_station=popular_start_station_counts[0]

    popular_end_station_counts = df1['End Station'].value_counts().index.tolist()
    pop_end_station=popular_end_station_counts[0]

    print ('Most popular start station:',pop_start_station,'AND','Most popular end station:',pop_end_station)

def popular_trip(df1):
    '''
    description:gives you the most popular trip
    Arguments: df1 (a dataframe created from the city and time period constrains)
    Return:a str indicating the most popular combination of start and end stations
    '''
    combo_stations= df1['Start Station']+df1['End Station']
    combo_counts=combo_stations.value_counts().index.tolist()
    pop_combo=combo_counts[0]
    print ('Most popular trip:',pop_combo)

#print (pop_station)

def trip_duration(df1):
    '''
    description:gives you the total and average trip duration in seconds
    Arguments: df1 (a dataframe created from the city and time period constrains)
    Return:an int indicating the total and average trip duration in seconds
    '''
    total_trip_duration=np.sum(df1['Trip Duration'])
    mean_trip_duration=np.average(df1['Trip Duration'])
    print ('Total trip duration:',total_trip_duration,'Average trip duration:',mean_trip_duration)

#STATSNo3:calculates the number of users by type and gender,and gives you the oldest and youngest users_numbers
#also here only apply gender and birth year functions if data has it
def users(df1):
    '''
    description:gives you the total number of users by type (either subscriber or costumer)
    Arguments: df1 (a dataframe created from the city and time period constrains)
    Return:an int indicating the total number of users by type
    '''
    user_types = df1['User Type'].value_counts()
    print('These are numbers of user tyopes:\n',str(user_types))

def gender_counts(df1):
    '''
    description:gives you the total number of users by gender when included in the city data
    Arguments: df1 (a dataframe created from the city and time period constrains)
    Return:an int indicating the total number of males or females, or a non aplicable msg for the
    cities that dont include this info
    '''
    if 'Gender' in df1.columns:
        gender_count = df1['Gender'].value_counts()
        print('These are the number of users by gender:\n',gender_count)
    else:
        print('Gender type not found for this dataset')


def birth_years(df1):
    '''
        description:gives you the most common birthday, the oldest and youngest birth year if the city dataset includes this ingo
        Arguments: df1 (a dataframe created from the city and time period constrains)
        Return:an int indicating the common, oldest and youngest birth years of users
    '''
    if 'Birth Year' in df1.columns:
        BDAY_popular = df1['Birth Year'].mode()[0]
        BDAY_oldest=df1['Birth Year'].max()
        BDAY_youngest= df1['Birth Year'].min()
        print('Most popular B-DAY:',int(BDAY_popular),'The oldest BDAY:',int(BDAY_oldest),'The youngest BDAY:',int(BDAY_youngest))
    else:
        print('Birth year data not found for this dataset')
#Displays 3 random trips
def display_data(df1):
    '''
        description:asks whether user wants to see indicidual trips
        Arguments: df1 (a dataframe created from the city and time period constrains)
        Return:a random sample of 3 trips from the city dataframe
    '''
    while True:
        display = str(input('\nWould you like to view individual trip data?'
                    'Type \'yes\' or \'no\'.\n')).lower()
        if display =='no':
            break
        elif display =='yes':
            print('\n Here are 3 random trips:\n',df1.sample(n=3))
else:
            print('\n Lets try again...\n')

#This function calls all the other functions and follows the general logic of the program
def statistics():
    '''
        description: this is the main function. calls the get_city and time_period functions, has a conditional to parse the time_period,
        calls the load_data function, the rest of the STATS functions (see above STATS1-STATS3), also calls the
        display_data function, and finally the restart function
        Arguments: none
        Return:all the return values, strs,int, etc for the afore mentioned functions. and an option to restart the program
        as well as how long each of the STATS is taking to compute.
    '''
    # Filter by city (Chicago, New York, Washington)
    city=get_city()

    # Filter by time period (month, day, none)
    user_time_period = get_time_period()

    #CONDITOINAL TO KNOW WHAT TO DO WITH DAY OR MONTH OR NONE
    if user_time_period == 'none':
        month ='none'
        day='none'
    elif user_time_period == 'month':
        day='none'
        month=get_month()
    elif user_time_period == 'day':
        month ='none'
        day=get_day()

    print("Calculating the 1ST statistic...")
    print('')
    start_time = time.time()

    #LOAD data in df1
    df1 = load_data(city,month,day)

    #STATS1:
    pop_month=popular_month(df1)
    pop_day=popular_day(df1)
    pop_hour=popular_hour(df1)

    print("That took %s seconds." % (time.time() - start_time))
    print('')
    print("Calculating the 2ND statistic...")
    print('')
    #STATS2:
    pop_trip=popular_trip(df1)
    pop_station=popular_stations(df1)
    trip_lenght=trip_duration(df1)

    print("That took %s seconds." % (time.time() - start_time))
    print('')
    print("Calculating the LAST statistic...")
    print('')

    #STATS3:
    users_numbers=users(df1)
    gender_numbers=gender_counts(df1)
    print('')
    birth_data=birth_years(df1)

    #Display
    get_display=display_data(df1)

    # Restart?
    restart = str(input('\nWould you like to restart? Type \'yes\' or \'no\'.\n')).lower()
    if restart.lower() == 'yes':
        statistics()
    if restart.lower() == 'no':
        print('Bye...Bye...and ride on!')
    else:        print('Not right string...SORRY, please restart on your OWN')
if __name__ == "__main__":
	statistics()
