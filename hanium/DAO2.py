from util import get_connection


def get_data():
    connection = get_connection()
    cursor = connection.cursor()

    query = "SELECT id, title, content, created_date FROM test_table"

    cursor.execute(query)

    data = cursor.fetchall()

    cursor.close()
    connection.close()
    return data


import random
from datetime import datetime

import traceback

def create_data():
    try:
        connection = get_connection()
        cursor = connection.cursor()

        for i in range(100):
            gender_id = random.randint(1, 2)
            age_group_id = random.randint(1, 8)
            location_id = random.randint(1, 8)

            # timestamp between 11 and 13 on Sep.13th of year2023.
            hour = random.randint(9, 17)
            timestamp = datetime(year=2023, month=9, day=13,
                                 hour=hour,
                                 minute=random.randint(0,59))

            query=f"""
              INSERT INTO Visit (
                 visit_id,
                 gender_id,
                 age_group_id,
                 location_id,
                 timestamp )
              VALUES (
                  {i + 1},
                  {gender_id},
                  {age_group_id},
                  {location_id},
                  TO_TIMESTAMP('{timestamp.strftime("%Y-%m-%d %H:%M:%S")}', 'YYYY-MM-DD HH24:MI:SS')
              )"""

            cursor.execute(query)

        connection.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc() # This will print the stack trace to the console
    finally:
        cursor.close()
        connection.close()

