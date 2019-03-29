import time
import pandas as pd
import numpy as np
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTH_DICT = { "january" : 1, "february" : 2, "march" :3, "april" : 4, "may" : 5, "june" : 6, 
			   "july" : 7, "august" : 8, "september" : 9, "october" : 10, "november" : 11, "december" : 12 }
DAY_DICT = { "sunday" : 1, "monday" : 2, "tuesday" : 3, "wednesday" : 4, "thursday" : 5, "friday" : 6, "saturday" : 7 }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    selected_city = ""
    selected_month = ""
    selected_day = ""
    options = ""
    for city in CITY_DATA.keys():
        options += city + ", "
    options = options[:-2]
    while len(selected_city) == 0:
        selected_city = input("Select a city (all, " + options + "): ")
        if selected_city != "all" and not selected_city in CITY_DATA:
            print("Invalid choice. Try again")
            selected_city = ""
    
    # TO DO: get user input for month (all, january, february, ... , june)
    options = ""
    for month in MONTH_DICT.keys():
        options += month + ", "
    options = options[:-2]
    while len(selected_month) == 0:
        selected_month = input("Select a month (all, " + options + "): ")
        if selected_month != "all" and not selected_month in MONTH_DICT:
            print("Invalid choice. Try again")
            selected_month = ""
             
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    options = ""
    for day in DAY_DICT.keys():
        options += day + ", "
    options = options[:-2]
    while len(selected_day) == 0:
        selected_day = input("Select a day of the week (all, " + options + "): ")
        if selected_day != "all" and not selected_day in DAY_DICT:
            print("Invalid choice. Try again")
            selected_day = ""
     
    print('-'*40)
    return [selected_city, selected_month, selected_day]


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    df = pd.DataFrame()
    df2 = pd.DataFrame()
    ref_frame = pd.read_csv(CITY_DATA['chicago'], nrows = 1)
    if city != "all":
        df = pd.read_csv(CITY_DATA[city])
        df = df.reindex(columns = ref_frame.columns)   
    else:
        first_city = True
        for city_enum in CITY_DATA.values():
            if first_city:
                df = pd.read_csv(city_enum)
                df = df.reindex(columns = ref_frame.columns)   
                first_city = False
            else:
                df2 = pd.read_csv(city_enum)
                df2 = df2.reindex(columns = ref_frame.columns)   
                df = df.append(pd.read_csv(city_enum))

    #df = df.interpolate(method ='linear', limit_direction ='forward', axis = 0)

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    if month != "all":
        df['month'] = df['Start Time'].dt.month    
        df = df.loc[df['month'] == MONTH_DICT[month]]
        
    if day != "all":
        df['day_of_week'] = df['Start Time'].dt.dayofweek
        df = df.loc[df['day_of_week'] == DAY_DICT[day]]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    df['month'] = df['Start Time'].dt.month    
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    mode_month = df['month'].mode()[0]
    key = next(key for key, value in MONTH_DICT.items() if value == mode_month)
    print("The most frequent month of travel is", key)

    # TO DO: display the most common day of week
    mode_day_of_week = df['day_of_week'].mode()[0]
    key = next(key for key, value in DAY_DICT.items() if value == mode_day_of_week)
    print("The most frequent day of travel is", key)

    # TO DO: display the most common start hour
    mode_hour = df['hour'].mode()[0]
    print("The most frequent start hour is", mode_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most frequently used start station
    mode_start = df['Start Station'].mode()[0]
    print("The most frequently used start station is", mode_start)

    # TO DO: display most frequently used end station
    mode_end = df['End Station'].mode()[0]
    print("The most frequently used end station is", mode_end)

    # TO DO: display most frequent combination of start station and end station trip
    df['Route'] = df[['Start Station','End Station']].apply(lambda x: ' to '.join(x), axis=1)
    mode_route = df['Route'].mode()[0]
    print("The most frequently used route is", mode_route)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the mean and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display mean travel time
    total_time = int(df['Trip Duration'].sum())
    total_days = int(total_time / 86400)
    total_hours = int((total_time % 86400) / 3600)
    total_minutes = int((total_time % 3600) / 60)
    total_seconds = int(total_time % 60)
    print("The total travel time is %s days, %s hours, %s minutes, and %s seconds." % (total_days, total_hours, total_minutes, total_seconds))

    # TO DO: display mean travel time
    mean_time = int(df['Trip Duration'].mean())
    mean_minutes = int((mean_time % 3600) / 60)
    mean_seconds = int(mean_time % 60)
    print("The mean travel time is %s minutes, and %s seconds." % (mean_minutes, mean_seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    #df = df['User Type'].fillna(0)
    user_types = pd.value_counts(df['User Type'].values, sort=False)
    print("The user types are")
    print(user_types, "\n")


    # TO DO: Display counts of gender
    #df = df['Gender'].fillna(0)
    genders = pd.value_counts(df['Gender'].values, sort=False)
    if not genders.empty:
        print("The genders are")
        print(genders, "\n")
    else:
        print("No gender data found.")

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest_yob = int(df['Birth Year'].min())
        latest_yob = int(df['Birth Year'].max())
        mode_yob = int(df['Birth Year'].mode())
        print("The earliest year of birth is", earliest_yob)
        print("The latest year of birth is", latest_yob)
        print("The most common year of birth is", mode_yob)
    except:
        print("No birth year data found.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        filters = []
        filters = get_filters()
        city = filters[0]
        month = filters[1]
        day = filters[2]
        df = load_data(city, month, day)

        if df.empty:
            print("No data was returned.")
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            data_loop_count = 0
            show_data = "no"
            show_data = input('\nWould you like to see some raw data? Enter yes or no.\n')
            while show_data.lower() == 'yes':
                print(df[data_loop_count:].head(5))
                data_loop_count += 1
                show_data = input('\nWould you like to see some more raw data? Enter yes or no.\n')

        restart = input('\nWould you like to do a different analysis? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
