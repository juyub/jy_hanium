from util import get_connection


def get_data_by_hour(start_date, end_date):
    connection = get_connection()
    cursor = connection.cursor()

    query = f"""
        SELECT 
            visit_hour,
            gender,
            AVG(count) as avg_count
        FROM (
            SELECT 
                EXTRACT(HOUR FROM detect_time) as visit_hour,
                gender,
                COUNT(*) as count
            FROM detected_faces
            WHERE TRUNC(detect_time) BETWEEN TO_DATE('{start_date}', 'YYYY-MM-DD') 
                                        AND TO_DATE('{end_date}', 'YYYY-MM-DD')
            GROUP BY EXTRACT(HOUR FROM detect_time), gender
        )
        GROUP BY visit_hour, gender
        order by visit_hour, gender
    """

    cursor.execute(query)

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return data


def get_gender_distribution(start_date, end_date):
    connection = get_connection()
    cursor = connection.cursor()

    query = f"""
        SELECT 
            gender,
            COUNT(*) as gen_count
        FROM detected_faces
        WHERE TRUNC(detect_time) BETWEEN TO_DATE('{start_date}', 'YYYY-MM-DD') AND TO_DATE('{end_date}', 'YYYY-MM-DD')
        GROUP BY gender
     """

    cursor.execute(query)

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return data


def get_age_gender_distribution(start_date, end_date):
    connection = get_connection()
    cursor = connection.cursor()

    query = f"""
        SELECT 
            age,
            gender,
            COUNT(*) as a_g_count
        FROM detected_faces
        WHERE TRUNC(detect_time) BETWEEN TO_DATE('{start_date}', 'YYYY-MM-DD') AND TO_DATE('{end_date}', 'YYYY-MM-DD')
        GROUP BY age,gender
        ORDER BY age,gender
   """

    cursor.execute(query)

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    age_group_order = ['(0, 2)', '(4, 6)', '(8, 12)', '(15, 20)',
                       '(25, 32)', '(38, 43)', '(48, 53)', '(60, 100)']

    # Sort data by the defined order of age groups and gender
    data.sort(key=lambda row: (age_group_order.index(row[0]), row[1]))

    return data


def get_data_by_date(start_date, end_date):
    connection = get_connection()
    cursor = connection.cursor()

    query = f"""
        SELECT 
            TO_CHAR(TRUNC(detect_time), 'YYYY-MM-DD') as "visit_date",
             gender,
            COUNT(*) as gen_count
        FROM detected_faces
        WHERE TRUNC(detect_time) BETWEEN TO_DATE('{start_date}', 'YYYY-MM-DD') AND TO_DATE('{end_date}', 'YYYY-MM-DD')
        GROUP BY TRUNC(detect_time), gender
        ORDER BY TRUNC(detect_time), gender
    """

    cursor.execute(query)

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return data
