import psycopg2
from psycopg2 import sql
from psycopg2.extras import DictCursor

def connect_bd(dbname='barbershop', user='postgres',
                            password='1524'):
    conn = psycopg2.connect(dbname=dbname, user=user,
                            password=password, host='localhost')
    return conn

def show_table(name_table):
    conn = connect_bd()
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute('SELECT * FROM '+ name_table)
        for row in cursor:
            print(row)
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
        insert = sql.SQL('INSERT INTO clientsbarber (nameclient, telephone,date_of_record, id_master) VALUES {}').format(
            sql.SQL(',').join(map(sql.Literal, values))
        )
        cursor.execute(insert)
    conn.close()

    # print(args[-1])

    # with conn.cursor() as cursor:
    #     conn.autocommit = True
        # insert = sql.SQL('INSERT INTO clientsbarber (nameclient, telephone, id_master) VALUES {}').format(
        #     sql.SQL(',').join(map(sql.Literal, values))
        # )
        # cursor.execute(insert)
    # conn.close()


add_to_cliets('name','12345','2021-01-01 12:20:00','Alisa')
