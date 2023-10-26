from util import get_connection


def get_data_by_hour(start_date, end_date):
    connection = get_connection()
    cursor = connection.cursor()

    query = f"""
        SELECT 
            visit_hour,
            gender_id,
            AVG(count) as average_count
        FROM (
            SELECT 
                EXTRACT(HOUR FROM visit_time) as visit_hour,
                gender_id,
                COUNT(*) as count
            FROM jy_Visit
            WHERE TRUNC(visit_time) BETWEEN TO_DATE('{start_date}', 'YYYY-MM-DD') 
                                        AND TO_DATE('{end_date}', 'YYYY-MM-DD')
            GROUP BY EXTRACT(HOUR FROM visit_time), gender_id
        )
        GROUP BY visit_hour, gender_id
        order by visit_hour, gender_id
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
            gender_id,
            COUNT(*) as count
        FROM jy_Visit
        WHERE TRUNC(visit_time) BETWEEN TO_DATE('{start_date}', 'YYYY-MM-DD') AND TO_DATE('{end_date}', 'YYYY-MM-DD')
        GROUP BY gender_id
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
            AGE_GROUP_ID,
            GENDER_ID,
            COUNT(*) as a_g_count
        FROM jy_Visit
        WHERE TRUNC(visit_time) BETWEEN TO_DATE('{start_date}', 'YYYY-MM-DD') AND TO_DATE('{end_date}', 'YYYY-MM-DD')
        GROUP BY AGE_GROUP_ID,GENDER_ID
        ORDER BY AGE_GROUP_ID,GENDER_ID
   """

    cursor.execute(query)

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return data


def get_data_by_date(start_date, end_date):
    connection = get_connection()
    cursor = connection.cursor()

    query = f"""
        SELECT 
            TO_CHAR(TRUNC(visit_time), 'YYYY-MM-DD') as "visit_date",
             GENDER_ID,
            COUNT(*) as count
        FROM jy_Visit
        WHERE TRUNC(visit_time) BETWEEN TO_DATE('{start_date}', 'YYYY-MM-DD') AND TO_DATE('{end_date}', 'YYYY-MM-DD')
        GROUP BY TRUNC(visit_time), GENDER_ID
        ORDER BY TRUNC(visit_time), GENDER_ID
    """

    cursor.execute(query)

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return data
