from flask import Blueprint, render_template, request
from madplan.model import model
from madplan.objects.ugeplan import Ugeplan

bp = Blueprint('welcome', __name__)


@bp.route('/', methods=['POST', 'GET'])
def hello():
    db = model.get_db()
    cur = db.cursor()
    cur.execute("SELECT navn, sideret FROM Retter;")
    alle_retter = cur.fetchall()

    if request.method == "POST":
        if len(request.form) == 14:
            return make_indkøbliste(alle_retter)

        elif len(request.form) == 1:
            return get_vare(alle_retter, cur)

        elif 'valgt_ret_navn' in request.form.to_dict().keys():
            return save_vare(cur, db)

    return render_template('base.html', data=alle_retter)

def make_indkøbliste(alle_retter):
    valgte_retter = request.form.to_dict()
    ugeplan = Ugeplan()
    for (ugedag, ret_navn) in zip(valgte_retter.keys(), valgte_retter.values()):
        if len(ret_navn) > 0:
            ugeplan.tilfoj_ret(ret_navn, ugedag)
    ugeplan.lav_indkobsliste()
    return render_template('base.html', data=alle_retter, ugeplan=ugeplan)

def get_vare(alle_retter, cur):
    ret_navn = request.form.to_dict()['valgt_ret_navn']
    cur.execute("""SELECT Varer.navn, RetterVarer.antal, Kategorier.navn kategori FROM Retter 
                INNER JOIN Kategorier ON Varer.kategori_id = Kategorier.id
                INNER JOIN RetterVarer ON Retter.id = RetterVarer.ret_id 
                INNER JOIN Varer ON RetterVarer.vare_id = Varer.id 
                WHERE Retter.navn = '{}'
                ORDER BY Kategorier.sortering ASC;""".format(ret_navn))
    valgt_ret = cur.fetchall()

    cur.execute("""SELECT navn FROM Varer
                ORDER BY navn ASC;""")
    varer = cur.fetchall()
    cur.execute("""SELECT navn FROM Kategorier
                ORDER BY sortering ASC;""")
    kategorier = cur.fetchall()

    cur.execute("""SELECT sideret FROM Retter
                WHERE navn = '{}';""".format(ret_navn))
    ret_sideret = cur.fetchall()

    return render_template('base.html',
                           data=alle_retter, valgt_ret=valgt_ret, valgt_ret_navn=ret_navn,
                           valgt_ret_sideret=ret_sideret, varer=varer, kategorier=kategorier)

def save_vare(cur, db):
    gemt_ret = request.form.to_dict()
    ret_navn = gemt_ret['valgt_ret_navn']
    sideret = 1 if 'sideret' in gemt_ret.keys() else 0
    cur.execute("""INSERT OR IGNORE INTO Retter (navn, sideret) 
                VALUES ('{}', {});""".format(ret_navn, sideret))
    cur.execute("""SELECT id FROM Retter 
                WHERE navn = '{}';""".format(ret_navn))
    ret_id = cur.fetchall()[0]['id']

    cur.execute("""DELETE FROM RetterVarer 
                WHERE ret_id = {};""".format(ret_id))

    alle_varer = []
    vare_indices = [key for key in gemt_ret.keys() if ('antal' not in key and
                                                       'kategori' not in key and
                                                       'navn' not in key)
                    and gemt_ret[key] != '']
    for vare in vare_indices:
        ny_vare = {'navn': gemt_ret[vare],
                   'antal': gemt_ret[vare + '_antal'],
                   'kategori': gemt_ret[vare + '_kategori']}
        alle_varer.append(ny_vare)

    for vare in alle_varer:
        cur.execute("""INSERT OR IGNORE INTO Varer (navn, kategori_id) 
                    VALUES ('{}', (SELECT id FROM Kategorier WHERE navn='{}'));"""
                    .format(vare['navn'], vare['kategori']))
        cur.execute("""SELECT id FROM Varer 
                    WHERE navn = '{}';""".format(vare['navn']))
        vare_id = cur.fetchall()[0]['id']
        cur.execute("""INSERT OR REPLACE INTO RetterVarer (ret_id, vare_id, antal) 
                    VALUES ({}, {}, '{}');""".format(ret_id, vare_id, vare['antal']))

    db.commit()


def get_database():
    db = model.get_db()
    cur = db.cursor()
    cur.execute("""SELECT Retter.navn, Varer.navn vare, RetterVarer.antal, Kategorier.navn kategori FROM Retter
                INNER JOIN Varer ON RetterVarer.vare_id = Varer.id
                INNER JOIN RetterVarer ON Retter.id = RetterVarer.ret_id
                INNER JOIN Kategorier ON Varer.kategori_id = Kategorier.id
                ORDER BY Retter.navn ASC;""")
    database_raw = cur.fetchall()
    unique_keys = set([database_raw[i][0] for i in range(len(database_raw))])
    database = {}
    for ret_navn in unique_keys:
        database[ret_navn] = []
        for row in database_raw:
            if row['navn'] == ret_navn:
                database[ret_navn].append((row['vare'], row['antal'], row['kategori']))
    return database
