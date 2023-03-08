import psycopg2


def connect():
    """ Connect to the PostgreSQL database server """
    conn = psycopg2.connect(
        host="localhost",
        database="liecba",
        user="postgres",
        password="adminek123")
    try:
        # create a cursor
        cur = conn.cursor()
        create_table1 = """CREATE TABLE IF NOT EXISTS pacient (
                            id serial PRIMARY KEY,
                            name varchar(255) NOT NULL,
                            surname varchar(255) NOT NULL,
                            age integer NOT NULL,
                            sex varchar(255) NOT NULL,
                            height float NOT NULL,
                            weight float NOT NULL,
                            diagnosis varchar(255) NOT NULL
                        )"""

        create_table2 = """CREATE TABLE IF NOT EXISTS liecba (
                        id serial PRIMARY KEY,
                        pacient_id integer NOT NULL,
                        pulse integer NOT NULL,
                        blood_oxygenation integer NOT NULL,
                        systolic_blood_pressure integer NOT NULL,
                        diastolic_blood_pressure integer NOT NULL,
                        FOREIGN KEY (pacient_id) REFERENCES pacient (id)
                    )"""
        create_table3 = """CREATE TABLE IF NOT EXISTS hesla (
                        id serial PRIMARY KEY,
                        password varchar(255) NOT NULL
                    )"""
        cur.execute(create_table1)
        cur.execute(create_table2)
        cur.execute(create_table3)
        #sql3 = """INSERT INTO hesla (password) VALUES (%s)"""

        #cur.execute(sql3, ("heslo123"))
        # execute a statement
        # sql1 = """INSERT INTO pacient (name, surname, age, sex, height, weight, diagnosis) VALUES (%s, %s, %s , %s, %s, %s, %s)"""
        # sql2 = """INSERT INTO liecba (pacient_id, pulse, blood_oxygenation, systolic_blood_pressure, diastolic_blood_pressure) VALUES (%s, %s, %s, %s, %s)"""
        # cur.execute(sql1, ("Peter", "Maly", 20, "M", 180, 80, "Zlomenina"))
        # cur.execute(sql2, (1, 70, 100, 140, 80))

        sql_select = """SELECT * FROM pacient"""
        sql_select2 = """SELECT * FROM liecba"""
        sql_select3 = """SELECT * FROM hesla"""

        cur.execute(sql_select)
        records = cur.fetchall()
        cur.execute(sql_select2)
        records1 = cur.fetchall()

        cur.execute(sql_select3)
        records2 = cur.fetchall()

        conn.commit()
        cur.close()

        return records, records1, records2

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
