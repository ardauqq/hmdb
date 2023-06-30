import psycopg2


def db_create(conn):
    with conn.cursor() as cur:
        cur.execute("""
                DROP TABLE phone_list;
                DROP TABLE clients;
                """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS clients(
            client_id SERIAL PRIMARY KEY,
            first_name VARCHAR(30) NOT NULL,
            last_name VARCHAR(30) NOT NULL,
            email VARCHAR(30) NOT NULL
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS phone_list(
            phone_id SERIAL PRIMARY KEY,
            client_id INTEGER REFERENCES clients(client_id),
            number VARCHAR(11) UNIQUE
        );
        """)

        conn.commit()


def new_client(conn, first_name, last_name, email, phones=None):
    with conn.cursor() as cur:
        client = (first_name, last_name, email)

        cur.execute("""
            INSERT INTO clients(first_name, last_name, email) VALUES(%s, %s, %s)""", client)

        conn.commit()


def new_phone_add(conn, client_id, phone):
    with conn.cursor() as cur:
        new_phone = (client_id, phone)

        cur.execute("""
            INSERT INTO phone_list(client_id, number) VALUES(%s, %s)""", new_phone)

        conn.commit()


def change_client(conn, client_id, first_name=None, last_name=None, email=None):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT * from clients
        WHERE client_id = %s
        """, (client_id,))

        current_client = cur.fetchone()

        if first_name is None:
            first_name = current_client[1]
        if last_name is None:
            last_name = current_client[2]
        if email is None:
            email = current_client[3]
        cur.execute("""
        UPDATE clients
        SET first_name = %s, last_name = %s, email = %s
        WHERE client_id = %s
        """, (first_name, last_name, email, client_id))

        conn.commit()


def del_phone(conn, client_id, number):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phone_list
        WHERE client_id = %s
        AND number = %s
        """, (client_id, number))

        conn.commit()


def del_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phone_list
        WHERE client_id = %s
        """, (client_id, ))

        conn.commit()

        cur.execute("""
        DELETE FROM clients
        WHERE client_id = %s
        """, (client_id, ))

        conn.commit()


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        if first_name is None:
            first_name = '%'
        else:
            first_name = f'%{first_name}%'
        if last_name is None:
            last_name = '%'
        else:
            last_name = f'%{last_name}%'
        if email is None:
            email = '%'
        else:
            email = f'%{email}%'
        if phone is None:
            cur.execute("""
                SELECT c.client_id, c.first_name, c.last_name, c.email, p.number FROM clients c
                LEFT JOIN phone_list p ON c.client_id = p.client_id
                WHERE c.first_name LIKE %s 
                AND c.last_name LIKE %s
                AND c.email LIKE %s
                """, (first_name, last_name, email))
        else:
            cur.execute("""
                SELECT c.client_id, c.first_name, c.last_name, c.email, p.number FROM clients c
                LEFT JOIN phone_list p ON c.client_id = p.client_id
                WHERE c.first_name LIKE %s 
                AND c.last_name LIKE %s
                AND c.email LIKE %s 
                AND p.number like %s
                """, (first_name, last_name, email, phone))

        return cur.fetchall()

with psycopg2.connect(database='***', user='***', password='***') as conn:
    # db_create(conn)
    # new_client(conn, 'Viktor', 'Batov', 'dede@dw23.ru')
    # new_phone_add(conn, 1, '79777333324')
    # new_phone_add(conn, 1, '77133332123')
    # change_client(conn, 1, 'Rinat', 'Adov', 'ewe@mail.ru')
    print(find_client(conn, phone='79777333324'))
conn.close()