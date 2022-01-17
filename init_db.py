import psycopg2
from psycopg2 import sql, Error
from psycopg2.extras import DictCursor

from config import DataBaseConfig
from log import LogError, LogInfo


def connect_bd(dbname=DataBaseConfig.dbname, user=DataBaseConfig.user,
               password=DataBaseConfig.password):
    try:
        conn = psycopg2.connect(dbname=dbname, user=user,
                                password=password, host='localhost')
        LogInfo.log.info("connect DB")
        return conn
    except (Exception, Error) as e:
        LogError.log.error(e)


def show_table(name_table):
    conn = connect_bd()
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute('SELECT * FROM ' + name_table)
        table_data = cursor.fetchall()
    conn.close()
    LogInfo.log.info("query is complited")
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
    LogInfo.log.info("query is complited")


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
            'INSERT INTO clientsbarber (nameclient, telephone,dateofrecord, idmaster) VALUES {}').format(
            sql.SQL(',').join(map(sql.Literal, values))
        )
        cursor.execute(insert)
    conn.close()
    LogInfo.log.info("query is complited")


def delete_from_table(query):
    conn = connect_bd()
    with conn.cursor() as cursor:
        conn.autocommit = True
        cursor.execute(query)
    conn.close()
    LogInfo.log.info("query is complited")


def check_time_records(select_master):
    conn = connect_bd()
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute('select id from masters where name = %s', (select_master,))
        id_master = cursor.fetchone()[0]
        cursor.execute('SELECT dateofrecord FROM clientsbarber where idmaster = %s', (id_master,))
        table_data = [row[0] for row in cursor]
    conn.close()
    LogInfo.log.info("query is complited")
    return table_data


def show_records_to_masters():
    conn = connect_bd()
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute(
            'select c.nameclient,c.telephone,c.dateofrecord,m.name from clientsbarber as c inner join masters as m on c.idmaster=m.id')
        table_data = cursor.fetchall()
    conn.close()
    LogInfo.log.info("query is complited")
    return table_data
