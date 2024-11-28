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


def setup_database(connection):
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orendsrs (
        id_orendsrs SERIAL PRIMARY KEY,
        name_firm TEXT NOT NULL,
        boss TEXT,
        number_phone VARCHAR(15) CHECK (number_phone ~ '^[+][0-9]{12}$')
    );
    
    CREATE TABLE IF NOT EXISTS rooms (
        id_number_rooms SERIAL PRIMARY KEY,
        area FLOAT NOT NULL,
        cost_area_one_m FLOAT NOT NULL,
        floor INT NOT NULL,
        floor_phone BOOLEAN NOT NULL,
        decoration_floor VARCHAR(10) CHECK (decoration_floor IN ('normal', 'good', 'euro'))
    );
    
    CREATE TABLE IF NOT EXISTS renta (
        id_number_rental SERIAL PRIMARY KEY,
        date_start DATE NOT NULL,
        count_days INT NOT NULL CHECK (count_days > 0),
        goal_rental VARCHAR(10) CHECK (goal_rental IN ('office', 'kiosk', 'warehouse')),
        id_orendsrs INT REFERENCES orendsrs(id_orendsrs),
        id_number_rooms INT REFERENCES rooms(id_number_rooms)
    );
    """)

    cursor.execute("""
    INSERT INTO orendsrs(name_firm, boss, number_phone)
    VALUES
        ('Hermes corp.', 'John Watson', '+380667435289'),
        ('Mayk corp.', 'Nata Bears', '+380234698564'),
        ('Locwood corp.', 'Lusi Locwood', '+380952374518'),
        ('Pantera corp.', 'Jane Marpl', '+380994312654'),
        ('Send corp.', 'Dik Send', '+380456743210');
    """)

    cursor.execute("""
    INSERT INTO rooms(area, cost_area_one_m, floor, floor_phone, decoration_floor)
    VALUES
        (43.5, 4.9, 3, TRUE, 'good'),
        (30, 2, 1, FALSE, 'normal'),
        (25, 1.5, 1, TRUE, 'good'),
        (60, 4.1, 4, TRUE, 'euro'),
        (45, 6, 1, FALSE, 'euro'),
        (90, 3.9, 3, FALSE, 'good'),
        (35, 1.3, 2, FALSE, 'normal'),
        (56, 2, 1, TRUE, 'euro'),
        (48, 6.5, 6, TRUE, 'normal'),
        (76, 6.3, 5, FALSE, 'normal'),
        (100, 1.2, 2, TRUE, 'good');
    """)

    cursor.execute("""
    INSERT INTO renta(date_start, count_days, goal_rental, id_orendsrs, id_number_rooms)
    VALUES
        ('2024-02-25', 30, 'kiosk', 1, 2),
        ('2024-02-26', 120, 'office', 5, 11),
        ('2024-12-03', 10, 'warehouse', 3, 3),
        ('2024-08-11', 11, 'warehouse', 3, 5),
        ('2024-11-08', 34, 'office', 4, 6),
        ('2024-05-30', 50, 'warehouse', 4, 7),
        ('2024-06-15', 60, 'kiosk', 2, 1),
        ('2024-09-17', 180, 'office', 2, 4),
        ('2024-01-20', 90, 'warehouse', 1, 8),
        ('2024-10-21', 54, 'office', 1, 9),
        ('2024-12-20', 70, 'kiosk', 2, 10);
    """)

    connection.commit()
    cursor.close()
    print("Database setup complete.")

def check_tables(connection):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables
        WHERE table_schema = 'public';
    """)
    tables = cursor.fetchall()
    print("Таблиці в базі даних:", tables)
    cursor.close()

# Виклик функції після створення таблиць

if __name__ == "__main__":
    connection = create_connection()
    if connection:
        setup_database(connection)
        check_tables(connection)
        connection.close()


# #запити
# #Відобразити всіх орендарів, які орендують приміщення під склад. Відсортувати по назві фірми
# cursor.execute("""
# SELECT name_firm, boss, number_phone
# FROM orendsrs
# JOIN renta ON orendsrs.id_orendsrs = renta.id_orendsrs
# WHERE goal_rental = 'warehouse'
# ORDER BY name_firm;
# """)
# result = cursor.fetchall()
# print("Орендарі під склад:", result)
#
#
# #Порахувати загальну орендну плату за кожне приміщення (запит з обчислювальним полем);
# cursor.execute("""
# SELECT
#     rooms.id_number_rooms AS room_id,
#     SUM(rooms.area * rooms.cost_area_one_m * renta.count_days) AS total_rent_cost
# FROM rooms
# JOIN renta ON rooms.id_number_rooms = renta.id_number_rooms
# GROUP BY rooms.id_number_rooms;
# """)
# result = cursor.fetchall()
# print("Загальна орендна плата за кожне приміщення:", result)
#
#
# #Порахувати загальну площу приміщень з звичайним, поліпшеним та євро оздобленням (підсумковий запит);
# cursor.execute("""
# SELECT
#     decoration_floor,
#     SUM(area) AS total_area
# FROM rooms
# GROUP BY decoration_floor;
# """)
# result = cursor.fetchall()
# print("Загальна площа приміщень за типами оздоблення:", result)
#
# #Порахувати кінцеву дату дії кожного договору оренди (запит з обчислювальним полем);
# cursor.execute("""
# SELECT
#     id_number_rental,
#     date_start + INTERVAL '1 day' * count_days AS end_date
# FROM renta;
# """)
# result = cursor.fetchall()
# print("Кінцева дата дії договорів:", result)
#
#
# #Порахувати кількість приміщень які здаються під офіс, кіоск, склад для кожного типу оздоблення (перехресний запит);
# cursor.execute("""
# SELECT
#     goal_rental,
#     decoration_floor,
#     COUNT(*) AS total_rooms
# FROM renta
# JOIN rooms ON renta.id_number_rooms = rooms.id_number_rooms
# GROUP BY goal_rental, decoration_floor;
# """)
# result = cursor.fetchall()
# print("Кількість приміщень за типом оренди та оздоблення:", result)
#
# #Відобразити всі приміщення за обраним типом оздоблення (запит з параметром).
# decoration_type = 'euro'  # Замінити на потрібний тип
# cursor.execute("""
# SELECT id_number_rooms, area, cost_area_one_m
# FROM rooms
# WHERE decoration_floor = %s;
# """, (decoration_type,))
# result = cursor.fetchall()
# print(f"Приміщення з типом оздоблення {decoration_type}:", result)