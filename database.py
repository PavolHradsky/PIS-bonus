import psycopg2
import bcrypt


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
        """
        salt = bcrypt.gensalt()
        password = b"admin"
        hashed = bcrypt.hashpw(password, salt)
        hashed_str = hashed.decode('utf-8')
        salt_str = salt.decode('utf-8')
        hashed_with_salt = f"{hashed_str}+++{salt_str}"
        """
        #sql3 = """INSERT INTO hesla (password) VALUES (%s)"""
        #cur.execute(sql3, (hashed_with_salt,))
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
    except Exception as e:
        print("Error connecting to database:", e)
        return None, None, None
