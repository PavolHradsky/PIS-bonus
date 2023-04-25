import psycopg2
import bcrypt


def connect(add, update, dict_values_patient, dict_values_problems):
    """ Connect to the PostgreSQL database server """
    conn = psycopg2.connect(
        host="horton.db.elephantsql.com",
        database="jyiqdclo",
        user="jyiqdclo",
        password="B85pFrz1g6uwlZ4ETbhpy7WdAhaRU8kE")  # possible to use .env file
    try:
        # create a cursor
        cur = conn.cursor()
        create_table1 = """CREATE TABLE IF NOT EXISTS pacient (
                                id serial PRIMARY KEY,
                                name varchar(255) NOT NULL,
                                surname varchar(255) NOT NULL,
                                age varchar(255) NOT NULL,
                                sex varchar(255) NOT NULL,
                                height varchar(255) NOT NULL,
                                weight varchar(255) NOT NULL
                            )"""
        create_table2 = """CREATE TABLE IF NOT EXISTS liecba (
                                id serial PRIMARY KEY,
                                pacient_id integer NOT NULL,
                                systolic_blood_pressure varchar(255) NOT NULL,
                                diastolic_blood_pressure varchar(255) NOT NULL,
                                blood_sugar varchar(255) NOT NULL,
                                cholesterol varchar(255) NOT NULL,
                                heart_rate varchar(255) NOT NULL,
                                EKG varchar(255) NOT NULL,
                                chest_pain varchar(255) NOT NULL,
                                FOREIGN KEY (pacient_id) REFERENCES pacient (id)
                            )"""
        create_table3 = """CREATE TABLE IF NOT EXISTS hesla (
                                id serial PRIMARY KEY,
                                password varchar(255) NOT NULL
                            )"""
        cur.execute(create_table1)
        cur.execute(create_table2)
        cur.execute(create_table3)

        if add:
            if dict_values_patient != {}:
                insert_patient = """INSERT INTO pacient (name, surname, age, sex, height, weight)
                                    VALUES ('{name}', '{surname}', '{age}', '{sex}', '{height}', '{weight}')""".format(
                    name=dict_values_patient['name'],
                    surname=dict_values_patient['surname'],
                    age=dict_values_patient['age'],
                    sex=dict_values_patient['sex'],
                    height=dict_values_patient['height'],
                    weight=dict_values_patient['weight']
                )
                cur.execute(insert_patient)

                # retrieve the patient ID from the database
                select_patient_id = """SELECT id FROM pacient WHERE name='{name}' AND surname='{surname}'""".format(
                    name=dict_values_patient['name'],
                    surname=dict_values_patient['surname']
                )
                cur.execute(select_patient_id)
                # get the ID value from the fetched result
                pacient_id = cur.fetchone()[0]

            if dict_values_problems != {}:
                insert_liecba = """INSERT INTO liecba (pacient_id, systolic_blood_pressure, diastolic_blood_pressure, blood_sugar, cholesterol, heart_rate, EKG, chest_pain)
                                    VALUES ('{pacient_id}', '{systolic_blood_pressure}', '{diastolic_blood_pressure}', '{blood_sugar}', '{cholesterol}', '{heart_rate}', '{EKG}', '{chest_pain}')""".format(
                    pacient_id=pacient_id,
                    systolic_blood_pressure=dict_values_problems['systolic_blood_pressure'],
                    diastolic_blood_pressure=dict_values_problems['diastolic_blood_pressure'],
                    blood_sugar=dict_values_problems['blood_sugar'],
                    cholesterol=dict_values_problems['cholesterol'],
                    heart_rate=dict_values_problems['heart_rate'],
                    EKG=dict_values_problems['EKG'],
                    chest_pain=dict_values_problems['chest_pain']
                )
                cur.execute(insert_liecba)
        if update:
            # % loop through the dictionary and update multiple columns
            for key, value in dict_values_patient.items():
                update_patient = """UPDATE pacient SET {key}='{value}' WHERE id={id}""".format(
                    key=key,
                    value=value,
                    id=dict_values_patient['id']
                )
                cur.execute(update_patient)
            for key, value in dict_values_problems.items():
                update_liecba = """UPDATE liecba SET {key}='{value}' WHERE id={id}""".format(
                    key=key,
                    value=value,
                    id=dict_values_problems['id']
                )
                cur.execute(update_liecba)

        # insert_patient = """INSERT INTO pacient (name, surname, age, sex, height, weight)
        #          VALUES ('Adam', 'Sivy', '35', 'M', '180', '80')"""
        # cur.execute(insert_patient)

        # insert_patient = """INSERT INTO pacient (name, surname, age, sex, height, weight)
        #           VALUES ('Monika', 'Siva', 'old', 'F', 'short', 'light')"""
        # cur.execute(insert_patient)

        # insert_liecba = """INSERT INTO liecba (pacient_id, systolic_blood_pressure, diastolic_blood_pressure, blood_sugar, cholesterol, heart_rate, EKG, chest_pain)
        #           VALUES ('1', '120', '80', '120', '180', '120', '0.1', 'typical')"""
        # cur.execute(insert_liecba)

        # insert_liecba = """INSERT INTO liecba (pacient_id, systolic_blood_pressure, diastolic_blood_pressure, blood_sugar, cholesterol, heart_rate, EKG, chest_pain)
        #           VALUES ('2', 'high', 'high', 'low', 'medium high', '120', 'abnormal', 'atypical')"""
        # cur.execute(insert_liecba)

        """
        salt = bcrypt.gensalt()
        password = b"admin"
        hashed = bcrypt.hashpw(password, salt)
        hashed_str = hashed.decode('utf-8')
        salt_str = salt.decode('utf-8')
        hashed_with_salt = f"{hashed_str}+++{salt_str}"
        """
        # sql3 = """INSERT INTO hesla (password) VALUES (%s)"""
        # cur.execute(sql3, (hashed_with_salt,))

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
