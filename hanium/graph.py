import matplotlib.pyplot as plt
import numpy as np

def create_line_graph(hourly_data):
    hours = sorted(list(set([data[0] for data in hourly_data])))
    male_counts = [sum(data[3] for data in hourly_data if data[0] == hour and data[1] == 1) for hour in hours]
    female_counts = [sum(data[3] for data in hourly_data if data[0] == hour and data[1] == 2) for hour in hours]

    plt.plot(hours, male_counts, label='Male')
    plt.plot(hours, female_counts, label='Female')

    plt.xlabel('Hour')
    plt.ylabel('Count')

    plt.legend()

    # Save the figure to 'static' directory
    plt.savefig('static/hourly_visitors.png')

    # Clear the current figure
    plt.clf()

def create_pie_chart(gender_dist):
    genders = ['Male' if data[0] == 1 else 'Female' for data in gender_dist]
    counts = [data[1] for gender in genders for data in gender_dist if
              (gender == 'Male' and data[0] == 1) or (gender == 'Female' and data[0] == 2)]

    # Create pie chart
    plt.pie(counts, labels=genders)

    # Save the figure to 'static' directory
    plt.savefig('static/gender_distribution.png')

    # Clear the current figure
    plt.clf()


def create_bar_chart(age_gender_dist):
    age_groups = sorted(list(set([data[0] for data in age_gender_dist])))
    genders = ['Male', 'Female']

    male_counts = [sum(data[2] for data in age_gender_dist
                       if (data)[0] == age_group_id and (data)[1] == 1)
                            for age_group_id in age_groups]

    female_counts = [sum(data[2] for data in age_gender_dist
                         if (data)[0] == age_group_id and (data)[1] == 2)
                            for age_group_id in age_groups]

    bar_width = 0.35

    # Create an array with the position of each bar along the x-axis.
    index = np.arange(len(age_groups))

    fig, ax = plt.subplots(figsize=(12, 8))

    # Create bars for male counts.
    ax.bar(index - bar_width / 2, male_counts, bar_width, label='Male')

    # Create bars for female counts.
    ax.bar(index + bar_width / 2, female_counts, bar_width, label='Female')

    # Add x and y labels.
    plt.xlabel('Age Group')
    plt.ylabel('Count')

    plt.xticks(index, age_groups)

    plt.legend()

    # Save the figure to 'static' directory
    plt.savefig('static/age_gender_distribution.png')

    plt.clf()









