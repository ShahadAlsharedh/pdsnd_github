import time
import pandas as pd
import numpy as np
import datetime as dt
import click

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

MonthName = ('january', 'february', 'march', 'april', 'may', 'june')

WeekDays = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
            'saturday')


def Opt(prompt, Opts=('y', 'n')):
    """Return a valid input from the user given an array of possible answers.
    """

    while True:
        Opt = input(prompt).lower().strip()
        # terminate the program if the input is end
        if Opt == 'end':
            exit()
        # triggers if the input has only one name
        elif ',' not in Opt:
            if Opt in Opts:
                break
        # triggers if the input has more than one name
        elif ',' in Opt:
            Opt = [i.strip().lower() for i in Opt.split(',')]
            if list(filter(lambda x: x in Opts, Opt)) == Opt:
                break

        prompt = ("\n Error something wrong happend here please retry \n>")

    return Opt


def get_filters():
    """Ask user to specify city(ies) and filters, month(s) and weekday(s).

    Returns:
        (str) city - name of the city(ies) to analyze
        (str) month - name of the month(s) to filter
        (str) day - name of the day(s) of week to filter
    """

    print("\n\nLet's explore some US bikeshare data!\n")

    print("Type end at any time if you would like to exit the program.\n")

    while True:
        city = Opt("\nPlease enter the city or cities you want, "
                      "New York City, Chicago or Washington? Use commas "
                      "to list the names.\n>", CITY_DATA.keys())
        month = Opt("\nEnter the month or months you want from Jan to June "
                       "Use commas to list the names.\n>",
                       MonthName)
        day = Opt("\nwhat weekday(s) do you want "
                     "Use commas to list the names.\n>", WeekDays)

        # confirm the user input
        confirmation = Opt("\nPlease confirm the information "
                              "to the bikeshare data."
                              "\n\n City(ies): {}\n Month(s): {}\n Weekday(s)"
                              ": {}\n\n [y] Yes\n [n] No\n\n>"
                              .format(city, month, day))
        if confirmation == 'y':
            break
        else:
            print("\n Try again \n")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """Load data for the specified filters of city(ies), month(s) and
       day(s) whenever applicable.

    Args:
        (str) city - name of the city(ies) to analyze
        (str) month - name of the month(s) to filter
        (str) day - name of the day(s) of week to filter
    Returns:
        df - Pandas DataFrame containing filtered data
    """

    print("\nThe program is loading the data for the filters of your Choice.")
    start_time = time.time()

    # filter the data according to the selected city filters
    if isinstance(city, list):
        df = pd.concat(map(lambda city: pd.read_csv(CITY_DATA[city]), city),
                       sort=True)
        # reorganize DataFrame columns after a city concat
        try:
            df = df.reindex(columns=['Unnamed: 0', 'Start Time', 'End Time',
                                     'Trip Duration', 'Start Station',
                                     'End Station', 'User Type', 'Gender',
                                     'Birth Year'])
        except:
            pass
    else:
        df = pd.read_csv(CITY_DATA[city])

    # create columns to display statistics
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.weekday_name
    df['Start Hour'] = df['Start Time'].dt.hour

    # filter the data according to month and weekday into two new DataFrames
    if isinstance(month, list):
        df = pd.concat(map(lambda month: df[df['Month'] ==
                           (months.index(month)+1)], month))
    else:
        df = df[df['Month'] == (month.index(month)+1)]

    if isinstance(day, list):
        df = pd.concat(map(lambda day: df[df['Weekday'] ==
                           (day.title())], day))
    else:
        df = df[df['Weekday'] == day.title()]

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)

    return df


def time_stats(df):
    """Display statistics on the most frequent times of travel."""

    print('\nDisplaying the statistics on the most frequent times of '
          'travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['Month'].mode()[0]
    print('For the selected filter, the month with the most travels is: ' +
          str(MonthName[most_common_month-1]).title() + '.')

    # display the most common day of week
    most_common_day = df['Weekday'].mode()[0]
    print('For the selected , the most common day of the week is: ' +
          str(most_common_day) + '.')

    # display the most common start hour
    most_common_hour = df['Start Hour'].mode()[0]
    print('For the selected , the most common start hour is: ' +
          str(most_common_hour) + '.')

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)


def station_stats(df):
    """Display statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = str(df['Start Station'].mode()[0])
    print("For the selected , the most common start station is: " +
          most_common_start_station)

    # display most commonly used end station
    most_common_end_station = str(df['End Station'].mode()[0])
    print("For the selected , the most common start end is: " +
          most_common_end_station)

    # display most frequent combination of start station and
    # end station trip
    df['Start-End Combination'] = (df['Start Station'] + ' - ' +
                                   df['End Station'])
    most_common_start_end_combination = str(df['Start-End Combination']
                                            .mode()[0])
    print("For the selected , the most common start-end combination "
          "of stations is: " + most_common_start_end_combination)

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)


def trip_duration_stats(df):
    """Display statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time = (str(int(total_travel_time//86400)) +
                         'd ' +
                         str(int((total_travel_time % 86400)//3600)) +
                         'h ' +
                         str(int(((total_travel_time % 86400) % 3600)//60)) +
                         'm ' +
                         str(int(((total_travel_time % 86400) % 3600) % 60)) +
                         's')
    print('For the selected filters, the total travel time is : ' +
          total_travel_time + '.')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time = (str(int(mean_travel_time//60)) + 'm ' +
                        str(int(mean_travel_time % 60)) + 's')
    print("For the selected filters, the mean travel time is : " +
          mean_travel_time + ".")

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)


def user_stats(df, city):
    """Display statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts().to_string()
    print("Distribution for user types:")
    print(user_types)

    # Display counts of gender
    try:
        gender_distribution = df['Gender'].value_counts().to_string()
        print("\nDistribution for each gender:")
        print(gender_distribution)
    except KeyError:
        print("Error No data".format(city.title()))

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = str(int(df['Birth Year'].min()))
        print("\nFor the selected filter, the oldest person to ride one "
              "bike was born in: " + earliest_birth_year)
        most_recent_birth_year = str(int(df['Birth Year'].max()))
        print("For the selected filter, the youngest person to ride one "
              "bike was born in: " + most_recent_birth_year)
        most_common_birth_year = str(int(df['Birth Year'].mode()[0]))
        print("For the selected filter, the most common birth year amongst "
              "riders is: " + most_common_birth_year)
    except:
        print("Error Try again".format(city.title()))

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)


def RawData (df , Mark):
    
    #sort 5 raws of Data
    
    print("\n View Raw Data :")
    
    # Var of where the user last stopped 
    
    if Mark > 0:
        Last = Opt("If you want to continue type [y] else type[n]")
        
        if Last =='n':
            Mark = 0
        
    #columns
    
    if Mark == 0:
        ColSort = Opt("\nChoose the way you want to display the data :"
                      "\n type [un] for unsorted else type enter : \n" , 
                      ('st' , 'et' , 'td' , 'ss' , 'es' , '' , 'un'))
        
        Asc_Desc = Opt("\n if you want the data to be sorted descending type [d],ascending type [A] : " , ('a' , 'd'))
        
        # Asending or descending
        if Asc_Desc == 'a':
            Asc_Desc = True
        elif Asc_Desc =='d':
            Asc_Desc = False
            
            
        if ColSort == 'st':
            df = df.sort_values(['Start Time'], ascending = Asc_Desc )
        elif ColSort == 'et':
            df = df.sort_values(['End Time'], ascending = Asc_Desc )
        elif ColSort == 'td':
            df = df.sort_values(['Trip Duration'], ascending = Asc_Desc )
        elif ColSort == 'ss':
            df = df.sort_values(['Start Station'], ascending = Asc_Desc )
        elif ColSort == 'es':
            df = df.sort_values(['End Station'], ascending = Asc_Desc )
        elif ColSort == 'un':
            pass
    
    # loop for 5 raws
    
    while True:
        for i in range(Mark , len(df.index)):
            print("\n" + df.iloc[Mark:Mark+5].to_string() +"\n")
            Mark +=5
            
            if Opt("Would you like to keep going ? type [y] else type [n]") == 'y':
                continue
            
            else:
                break
        break
    
    return Mark

def main():
    while True:
        click.clear()
        city, month, day = get_filters()
        df = load_data(city, month, day)
        Mark = 0
        
        
        while True:
            Data = Opt(
                "\n Select the option you want "
                " \n [ts] Time Stats\n [ss] "
                "Station Stats\n [tds] Trip Duration Stats\n "
                "[us] User Stats \n [d] Raw Data \n \n" , ('ts' , 'ss' , 'tds' , 'us' ,'d'))
            
            
            
            click.clear()
            if Data == 'ts':
                time_stats(df)
            elif Data == 'ss':
                station_stats(df)
            elif Data == 'tds':
                trip_duration_stats(df)
            elif Data == 'us':
                user_stats(df, city)
            elif Data == 'd':
                Mark = RawData(df , Mark)
                break

        restart = Opt("\nWould you like to restart?\n type y ")
        if restart.lower() != 'y':
            break
        

if __name__ == "__main__":
    main()