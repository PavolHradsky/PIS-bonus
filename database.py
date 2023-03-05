#!/usr/bin/python
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
                    diagnosis varchar(255) NOT NULL
                )"""
        create_table2 = """CREATE TABLE IF NOT EXISTS liecba (
                  id serial PRIMARY KEY,
                  pacient_id integer NOT NULL,
                  liecba varchar(255) NOT NULL,
                  FOREIGN KEY (pacient_id) REFERENCES pacient (id)
              )"""

        # execute a statement
        sql1 = """INSERT INTO pacient (name, surname, diagnosis) VALUES (%s, %s, %s)"""
        sql2 = """INSERT INTO liecba (pacient_id, liecba) VALUES (%s, %s)"""

        sql_select = """SELECT * FROM pacient"""
        sql_select2 = """SELECT * FROM liecba"""

        cur.execute(create_table1)
        cur.execute(create_table2)
        cur.execute(sql1, ("Jozko", "Mrkvicka", "Katar"))
        cur.execute(sql2, (1, "Antibiotikum"))
        cur.execute(sql_select)
        records = cur.fetchall()
        print(records)
        cur.execute(sql_select2)
        records = cur.fetchall()
        print(records)

        conn.commit()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

