# main.py

from flask import Flask, render_template

import DAO2
from DAO import *
from DAO2 import *
from graph import create_line_graph, create_pie_chart, create_bar_chart  # Import the functions from graph.py

app = Flask(__name__)

@app.route('/')
def home():
    # hourly_data = get_data_by_hour()
    # create_line_graph(hourly_data)
    #
    # gender_dist = get_gender_distribution()
    # create_pie_chart(gender_dist)
    #
    # age_gender_dist = get_age_gender_distribution()
    # create_bar_chart(age_gender_dist)

    return render_template('data.html')

@app.route('/data', methods=['GET', 'POST'])
def show_data():
    data = DAO2.get_data()
    return render_template('data2.html', data=data)

@app.route('/create_data', methods=['POST'])
def create_data():
    DAO2.create_data()
    return

if __name__ == "__main__":
   app.run(debug=True)
