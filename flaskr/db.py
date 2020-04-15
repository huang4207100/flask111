import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
import pymysql


def get_db():
    if 'db' not in g:
        # g.db = sqlite3.connect(
        #     current_app.config['DATABASE'],
        #     detect_types=sqlite3.PARSE_DECLTYPES
        # )
        #
        g.db = pymysql.connect(
            host=current_app.config['DATABASE']['host'],
            user=current_app.config['DATABASE']['user'],
            password=current_app.config['DATABASE']['password'],
            db='1982906',
            charset=current_app.config['DATABASE']['charset'],
            cursorclass=pymysql.cursors.DictCursor
        )

        # g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()
    sql = ""
    with current_app.open_resource("schema.sql") as f:
        sqls = f.read().decode('utf-8').split(';')[0:-1]
        print(sqls)
        #按照每个sql的; 执行sql脚本
        for sql in sqls:
            with db.cursor() as cursor:
                print(sql)
                cursor.execute(sql+';')
            db.commit()

def insert_sql(sql):
    db = get_db()
    with db.cursor() as cursor:
        # Create a new record
        # sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
        cursor.execute(sql)

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    db.commit()

def select_sql(sql):
    db = get_db()
    with db.cursor() as cursor:
        # Read a single record
        # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
        return result


@click.command("init-db")
@with_appcontext
def init_db_command():
    """clear the existing data and create new tables"""
    init_db()
    click.echo("Initialized the database.")

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)