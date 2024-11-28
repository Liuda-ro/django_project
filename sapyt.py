import psycopg2

def create_connection():
    try:
        connection = psycopg2.connect(
            database="rental_db",
            user="postgres",
            password="L322434i",
            host="127.0.0.1",
            port="5432")
        print("Successfully connected to the database")
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None


def show_table_structure_and_data(connection):
    cursor = connection.cursor()

    # Орендарі під склад
    cursor.execute("""
    SELECT name_firm, boss, number_phone
    FROM orendsrs
    JOIN renta ON orendsrs.id_orendsrs = renta.id_orendsrs
    WHERE goal_rental = 'warehouse'
    ORDER BY name_firm;
    """)
    print("Орендарі під склад:")
    for row in cursor.fetchall():
        print(row)

    # Загальна орендна плата за кожне приміщення
    cursor.execute("""
    SELECT
        rooms.id_number_rooms AS room_id,
        SUM(rooms.area * rooms.cost_area_one_m * renta.count_days) AS total_rent_cost
    FROM rooms
    JOIN renta ON rooms.id_number_rooms = renta.id_number_rooms
    GROUP BY rooms.id_number_rooms;
    """)
    print("\nЗагальна орендна плата за кожне приміщення:")
    for row in cursor.fetchall():
        print(row)

    # Загальна площа приміщень за типами оздоблення
    cursor.execute("""
    SELECT
        decoration_floor,
        SUM(area) AS total_area
    FROM rooms
    GROUP BY decoration_floor;
    """)
    print("\nЗагальна площа приміщень за типами оздоблення:")
    for row in cursor.fetchall():
        print(row)

    # Кінцева дата дії договорів
    cursor.execute("""
    SELECT
        id_number_rental,
        date_start + INTERVAL '1 day' * count_days AS end_date
    FROM renta;
    """)
    print("\nКінцева дата дії договорів:")
    for row in cursor.fetchall():
        print(row)

    # Кількість приміщень за типом оренди та оздоблення
    cursor.execute("""
    SELECT
        goal_rental,
        decoration_floor,
        COUNT(*) AS total_rooms
    FROM renta
    JOIN rooms ON renta.id_number_rooms = rooms.id_number_rooms
    GROUP BY goal_rental, decoration_floor;
    """)
    print("\nКількість приміщень за типом оренди та оздоблення:")
    for row in cursor.fetchall():
        print(row)

    # Приміщення з заданим типом оздоблення
    decoration_type = 'euro'
    cursor.execute("""
    SELECT id_number_rooms, area, cost_area_one_m
    FROM rooms
    WHERE decoration_floor = %s;
    """, (decoration_type,))
    print(f"\nПриміщення з типом оздоблення '{decoration_type}':")
    for row in cursor.fetchall():
        print(row)



    cursor.close()


if __name__ == "__main__":
    connection = create_connection()
    if connection:
        show_table_structure_and_data(connection)
        connection.close()