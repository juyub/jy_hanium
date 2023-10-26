import io
import urllib
import base64
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


def line_graph_date(data_by_date):
    # Separate data by gender
    male_data = [data for data in data_by_date if data[1] == 1]
    female_data = [data for data in data_by_date if data[1] == 2]

    # Get dates and counts for each gender
    male_dates = [data[0] for data in male_data]
    female_dates = [data[0] for data in female_data]
    male_counts = [data[2] for data in male_data]
    female_counts = [data[2] for data in female_data]

    # Convert string dates to datetime objects
    male_dates_formatted = [datetime.strptime(date, "%Y-%m-%d").strftime('%y%m%d') for date in male_dates]
    female_dates_formatted = [datetime.strptime(date, "%Y-%m-%d").strftime('%y%m%d') for date in female_dates]

    # Determine the start and end dates
    start_date_str, end_date_str = min(male_dates + female_dates), max(male_dates + female_dates)

    # Plotting the line graph
    plt.plot(male_dates_formatted, male_counts, label='male')
    plt.plot(female_dates_formatted, female_counts, label='female')

    plt.xticks([])

    # Format x-axis to show only the date (not time)
    plt.gcf().autofmt_xdate()

    # Set the title of the graph to be the range of dates
    plt.title(f'{start_date_str} ~ {end_date_str}')

    # Add legend
    plt.legend()

    # Save the figure to 'static' directory
    # plt.savefig('static/daily_visitors.png')

    #
    img = io.BytesIO()
    plt.savefig(img, format='png')

    # Clear the current figure
    plt.clf()

    #
    img.seek(0)
    graph_url = urllib.parse.quote(base64.b64encode(img.read()).decode())

    return graph_url


def line_graph_hour(hourly_data):
    hours = sorted(list(set([data[0] for data in hourly_data])))
    male_counts = [data[2] for data in hourly_data if data[1] == 1]
    female_counts = [data[2] for data in hourly_data if data[1] == 2]

    plt.plot(hours, male_counts, label='Male')
    plt.plot(hours, female_counts, label='Female')

    plt.legend()

    # Save the figure to 'static' directory
    # plt.savefig('static/hourly_visitors.png')

    #
    img = io.BytesIO()
    plt.savefig(img, format='png')

    # Clear the current figure
    plt.clf()

    #
    img.seek(0)
    graph_url = urllib.parse.quote(base64.b64encode(img.read()).decode())

    return graph_url


def bar_graph_by_ag(data):
    # Convert raw data to DataFrame
    df = pd.DataFrame(data, columns=['AGE_GROUP_ID', 'GENDER_ID', 'a_g_count'])

    # Map AGE_GROUP_ID to age range string
    age_group_dict = {1: '0 - 2', 2: '4 - 6', 3: '8 - 12', 4: '15 - 20',
                      5: '25 - 32', 6: '38 -43', 7: '48-53', 8: '60-100'}
    df['AGE_GROUP'] = df['AGE_GROUP_ID'].map(age_group_dict)

    # Convert AGE_GROUP to categorical data type with specified order
    df['AGE_GROUP'] = pd.Categorical(df['AGE_GROUP'], categories=age_group_dict.values(), ordered=True)

    # Classify by GENDER_ID into male and female
    df['GENDER'] = df['GENDER_ID'].apply(lambda x: 'Male' if x == 1 else 'Female')

    # Group by AGE_GROUP and GENDER, and calculate the sum of a_g_count for each group
    grouped_df = df.groupby(['AGE_GROUP', 'GENDER'], observed=True)['a_g_count'].sum().unstack()

    # Create a bar graph
    grouped_df.plot(kind='bar', stacked=False)
    plt.xticks(rotation=0)
    plt.xlabel('')

    # plt.savefig('static/age_gender_distribution.png')

    #
    img = io.BytesIO()
    plt.savefig(img, format='png')

    # Clear the current figure
    plt.clf()

    #
    img.seek(0)
    graph_url = urllib.parse.quote(base64.b64encode(img.read()).decode())

    return graph_url


def pie_chart_gend(gender_dist):
    genders = ['Male' if data[0] == 1 else 'Female' for data in gender_dist]
    counts = [data[1] for gender in genders for data in gender_dist if
              (gender == 'Male' and data[0] == 1) or (gender == 'Female' and data[0] == 2)]

    # Create pie chart
    plt.pie(counts, labels=genders)

    # plt.savefig('static/gender_distribution.png')

    #
    img = io.BytesIO()
    plt.savefig(img, format='png')

    # Clear the current figure
    plt.clf()

    #
    img.seek(0)
    graph_url = urllib.parse.quote(base64.b64encode(img.read()).decode())

    return graph_url
