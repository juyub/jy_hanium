from util import get_connection
import random
from datetime import datetime
import traceback


def create_table():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Create Gender table
        cursor.execute("""
            CREATE TABLE jy_Gender (
                gender_id INT PRIMARY KEY,
                gender VARCHAR(10)
            )
        """)

        # Create Age_group table
        cursor.execute("""
            CREATE TABLE jy_Age_group (
                age_group_id INT PRIMARY KEY,
                age_group VARCHAR(20)
            )
        """)

        # Create Location table
        cursor.execute("""
            CREATE TABLE jy_Location (
                location_id INT PRIMARY KEY,
                zone_name VARCHAR(50)
            )
        """)

        # Create Visit table
        cursor.execute("""
            CREATE TABLE jy_Visit (
                visit_id INT PRIMARY KEY,
                gender_id INT,
                age_group_id INT,
                location_id INT,
                visit_time TIMESTAMP,
                
                FOREIGN KEY (gender_id) REFERENCES jy_Gender(gender_id),
                FOREIGN KEY (age_group_id) REFERENCES jy_Age_group(age_group_id),
                FOREIGN KEY (location_id) REFERENCES jy_Location(location_id)
            )
        """)

        connection.commit()
    finally:
        cursor.close()
        connection.close()


def insert_table():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Insert data into Gender table
        for i in range(1, 3):
            gender = 'Male' if i == 1 else 'Female'
            query = f"INSERT INTO jy_Gender (gender_ID, gender) VALUES ({i}, '{gender}')"
            cursor.execute(query)

        # Insert data into Age_Group Table
        age_groups = ['0 - 2', '4 - 6', '8 - 12', '15 - 20', '25 - 32', '38 -43', '48-53', '60-100']
        for i in range(1, 9):
            query = f"INSERT INTO jy_Age_Group(Age_Group_Id , AGE_Group ) Values({i},'{age_groups[i-1]}')"
            cursor.execute(query)

        zones = ['Zone A', 'Zone B', 'Zone C', 'Zone D', 'Zone E', 'Zone F', 'Zone G', " Zone H"]
        for i in range(1, 9):
            query = f"INSERT INTO jy_Location(Location_Id , Zone_Name ) Values({i} ,'{zones[i-1]}')"
            cursor.execute(query)

        connection.commit()
    finally:
        cursor.close()
        connection.close()


def create_data(start_date, end_date, start_time, end_time, num_entries):
    # Convert the input dates and times into datetime objects
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    start_time = datetime.strptime(start_time, '%H:%M')
    end_time = datetime.strptime(end_time, '%H:%M')

    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Get the current maximum visit_id from the database
        cursor.execute("SELECT MAX(visit_id) FROM jy_Visit")
        max_visit_id = cursor.fetchone()[0] or 0

        for i in range(num_entries):
            gender_id = random.randint(1, 2)
            age_group_id = random.randint(1, 8)
            location_id = random.randint(1, 8)

            # Use the input start and end dates/times to generate a random datetime
            random_date = start_date + (end_date - start_date) * random.random()
            random_time = start_time + (end_time - start_time) * random.random()

            visit_time = datetime.combine(random_date, random_time.time())

            # Use the current maximum visit_id to generate a new unique visit_id
            visit_id = max_visit_id + i + 1

            query = f"""
              INSERT INTO jy_Visit (
                 visit_id,
                 gender_id,
                 age_group_id,
                 location_id,
                 visit_time )
              VALUES (
                  {visit_id},
                  {gender_id},
                  {age_group_id},
                  {location_id},
                  TO_TIMESTAMP('{visit_time.strftime("%Y-%m-%d %H:%M:%S")}', 'YYYY-MM-DD HH24:MI:SS')
              )"""

            cursor.execute(query)

        connection.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()  # This will print the stack trace to the console
    finally:
        cursor.close()
        connection.close()


def delete_table():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("DROP TABLE jy_Visit")
        cursor.execute("DROP TABLE jy_Location")
        cursor.execute("DROP TABLE jy_Age_group")
        cursor.execute("DROP TABLE jy_Gender")

        connection.commit()
    finally:
        cursor.close()
        connection.close()


def delete_table_data():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM jy_Location")
        cursor.execute("DELETE FROM jy_Age_group")
        cursor.execute("DELETE FROM jy_Gender")

        connection.commit()
    finally:
        cursor.close()
        connection.close()


def delete_data():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("TRUNCATE TABLE jy_Visit")
        connection.commit()
    finally:
        cursor.close()
        connection.close()
