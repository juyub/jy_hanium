from flask import Flask, render_template, request
import DAO
import DataDAO
import graph

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('main.html')


@app.route('/data', methods=['POST'])
def ready_data():
    return render_template('data.html')


@app.route('/create_table', methods=['POST'])
def create_table():
    DataDAO.create_table()
    return render_template('data.html')


@app.route('/insert_table_data', methods=['POST'])
def insert_table():
    DataDAO.insert_table()
    return render_template('data.html')


@app.route('/create_data', methods=['POST'])
def create_data():
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    num_entries = int(request.form.get('num_entries'))

    DataDAO.create_data(start_date, end_date, start_time, end_time, num_entries)

    return render_template('data.html')


@app.route('/delete_table', methods=['POST'])
def delete_table():
    DataDAO.delete_table()
    return render_template('data.html')


@app.route('/delete_table_data', methods=['POST'])
def delete_table_data():
    DataDAO.delete_table_data()
    return render_template('data.html')


@app.route('/delete_data', methods=['POST'])
def delete_data():
    DataDAO.delete_data()
    return render_template('data.html')


@app.route('/daily_visitors', methods=['POST'])
def daily_visitors():
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')

    # Check if the start_date and end_date are provided
    if not start_date or not end_date:
        return render_template('main.html')

    data_by_date = DAO.get_data_by_date(start_date, end_date)
    hourly_data = DAO.get_data_by_hour(start_date, end_date)
    age_gender_dist = DAO.get_age_gender_distribution(start_date, end_date)
    gender_dist = DAO.get_gender_distribution(start_date, end_date)

    graph.line_graph_by_date(data_by_date)
    graph.create_line_graph(hourly_data)
    graph.bar_graph_by_age(age_gender_dist)
    graph.create_pie_chart(gender_dist)

    return render_template('graph.html',
                           data_by_date=data_by_date, hourly_data=hourly_data,
                           age_gender_dist=age_gender_dist, gender_dist=gender_dist)


if __name__ == "__main__":
    app.run(debug=True)
