from util import get_connection

def get_data_by_hour():
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT 
            EXTRACT(HOUR FROM timestamp) as hour,
            gender_id,
            age_group_id,
            COUNT(*) as count
        FROM Visit
        WHERE EXTRACT(HOUR FROM timestamp) BETWEEN 9 AND 17
        GROUP BY EXTRACT(HOUR FROM timestamp), gender_id, age_group_id
    """

    cursor.execute(query)

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return data


def get_gender_distribution():
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT 
            gender_id,
            COUNT(*) as count
        FROM Visit
        GROUP BY gender_id
     """

    cursor.execute(query)

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return data


def get_age_gender_distribution():
    connection = get_connection()
    cursor = connection.cursor()

    query = """
       SELECT 
           age_group_id, 
           gender_id, 
           COUNT(*) as count 
       FROM Visit 
       GROUP BY age_group_id, gender_id
   """

    cursor.execute(query)

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return data

