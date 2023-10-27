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
    male_data = [data for data in data_by_date if data[1] == 'Male']
    female_data = [data for data in data_by_date if data[1] == 'Female']

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
    male_counts = [data[2] for data in hourly_data if data[1] == 'Male']
    female_counts = [data[2] for data in hourly_data if data[1] == 'Female']

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
    df = pd.DataFrame(data, columns=['age', 'gender', 'a_g_count'])

    # Map AGE_GROUP_ID to age range string
    # age_group_order = ['0-2', '4-6', '8-12', '15-20',
    #                    '25-32', '38-43', '48-53', '60-100']
    age_group_order = ['(0, 2)', '(4, 6)', '(8, 12)', '(15, 20)',
                       '(25, 32)', '(38, 43)', '(48, 53)', '(60, 100)']

    gender_order = ['Male', 'Female']

    df['age'] = pd.Categorical(df['age'], categories=age_group_order, ordered=True)
    df['gender'] = pd.Categorical(df['gender'], categories=gender_order, ordered=True)

    # Group by AGE and GENDER, and calculate the sum of a_g_count for each group
    grouped_df = df.groupby(['age', 'gender'], observed=True)['a_g_count'].sum().unstack()

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
    # Extract genders and counts from the data
    genders = [data[0] for data in gender_dist]
    counts = [data[1] for data in gender_dist]

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
