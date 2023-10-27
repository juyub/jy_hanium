from util import get_connection
import random
from datetime import datetime, timedelta
import traceback


def create_table():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Create Gender table
        cursor.execute("""
            CREATE TABLE detected_faces (
                face_id NUMBER,
                gender VARCHAR2(10),
                age VARCHAR2(10),
                detect_time TIMESTAMP
            )
        """)

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
        cursor.execute("SELECT MAX(face_id) FROM detected_faces")
        max_face_id = cursor.fetchone()[0] or 0

        GENDER_LIST = ['Male', 'Female']
        AGE_INTERVALS = ['(0, 2)', '(4, 6)', '(8, 12)', '(15, 20)',
                         '(25, 32)', '(38, 43)', '(48, 53)', '(60, 100)']

        for i in range(num_entries):
            gender_id_index = random.randint(0, 1)
            age_group_index = random.randint(0, 7)

            random_date = start_date + (end_date - start_date) * random.random()
            random_time = start_time + (end_time - start_time) * random.random()

            visit_time = datetime.combine(random_date, random_time.time())

            # Use the current maximum visit_id to generate a new unique visit_id
            face_id = max_face_id + i + 1

            query = f"""
                INSERT INTO detected_faces (
                    face_id,
                    gender,
                    age,
                    detect_time )
                VALUES (
                    {face_id},
                    '{GENDER_LIST[gender_id_index]}',
                    '{AGE_INTERVALS[age_group_index]}',
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
        cursor.execute("DROP TABLE detected_faces")

        connection.commit()
    finally:
        cursor.close()
        connection.close()


def delete_data():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("TRUNCATE TABLE detected_faces")
        connection.commit()
    finally:
        cursor.close()
        connection.close()
