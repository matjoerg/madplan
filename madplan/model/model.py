import sqlite3
import click
import json
from flask import current_app, g
from flask.cli import with_appcontext
import os

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        try:
            db.close()
        except:
            print("Database could not be closed.")

def init_db():
    db = get_db()

    with current_app.open_resource('model/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def seed_db():
    db = get_db()
    c = db.cursor()

    script_dir = os.path.dirname(__file__)
    retter = open(os.path.join(script_dir, "Retter.json"), 'r')
    varer = open(os.path.join(script_dir, "Varer.json"), 'r')
    retter_varer = open(os.path.join(script_dir, "RetterVarer.json"), 'r')

    json_retter = json.load(retter)
    json_varer = json.load(varer)
    json_retter_varer = json.load(retter_varer)

    sql_retter = "INSERT INTO Retter (id, navn) VALUES (?, ?);"
    alle_retter = [(ret['id'], ret['navn']) for ret in json_retter]
    c.executemany(sql_retter, alle_retter)

    sql_varer = "INSERT INTO Varer (id, navn, kategori) VALUES (?, ?, ?);"
    alle_varer = [(vare['id'], vare['navn'], vare['kategori']) for vare in json_varer]
    c.executemany(sql_varer, alle_varer)
    
    sql_retter_varer = "INSERT INTO RetterVarer (ret_id, vare_id, antal) VALUES (?, ?, ?);"
    alle_retter_varer = [(ret_vare['ret_id'], ret_vare['vare_id'], ret_vare['antal']) for ret_vare in json_retter_varer]
    c.executemany(sql_retter_varer, alle_retter_varer)

    db.commit()
    db.close()
    
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

@click.command('seed-db')
@with_appcontext
def seed_db_command():
    init_db()
    seed_db()
    click.echo('Seeded the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_db_command)
