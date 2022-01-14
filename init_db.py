import psycopg2
from psycopg2.extras import DictCursor
from psycopg2 import sql

def connect_bd(dbname='barbershop', user='postgres',
                            password='1524'):
    conn = psycopg2.connect(dbname=dbname, user=user,
                            password=password, host='localhost')
    return conn

def show_table(name_table):
    conn = connect_bd()
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute('SELECT * FROM '+ name_table)
        table_data = cursor.fetchall()
    conn.close()
    return table_data


def add_to_masters(*args):
    conn = connect_bd()
    with conn.cursor() as cursor:
        conn.autocommit = True
        values = [args
        ]
        insert = sql.SQL('INSERT INTO masters (name) VALUES {}').format(
            sql.SQL(',').join(map(sql.Literal, values))
        )
        cursor.execute(insert)
    conn.close()

def add_to_cliets(*args):
    conn = connect_bd()
    with conn.cursor() as cursor:
        conn.autocommit = True
        values = list(args)
        cursor.execute('select id from masters where name = %s', (values[-1],))
        name = cursor.fetchone()[0]
        values[-1] = name
        values = [tuple(values)]
        insert = sql.SQL(
            'INSERT INTO clientsbarber (nameclient, telephone,date_of_record, id_master) VALUES {}').format(
            sql.SQL(',').join(map(sql.Literal, values))
        )
        cursor.execute(insert)
    conn.close()

def delete_from_table(query):
    conn = connect_bd()
    with conn.cursor() as cursor:
        conn.autocommit = True
        cursor.execute(query)
    conn.close()




