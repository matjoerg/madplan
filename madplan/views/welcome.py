from flask import Blueprint, render_template, request
from madplan.model import model
from madplan.objects.ugeplan import Ugeplan

bp = Blueprint('welcome', __name__)


@bp.route('/', methods=['POST', 'GET'])
def hello():
    db = model.get_db()
    cur = db.cursor()
    cur.execute("SELECT navn FROM Retter;")
    alle_retter = cur.fetchall()

    if request.method == "POST":
        if len(request.form) == 7:
            valgte_retter = request.form.to_dict()
            ugeplan = Ugeplan()
            for (ugedag, ret_navn) in zip(valgte_retter.keys(), valgte_retter.values()):
                if len(ret_navn) > 0:
                    ugeplan.tilfoj_ret(ret_navn, ugedag)
            ugeplan.lav_indkobsliste()
            return render_template('base.html', data=alle_retter, ugeplan=ugeplan)

        elif len(request.form) == 1:
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

            return render_template('base.html',
                                   data=alle_retter, valgt_ret=valgt_ret, valgt_ret_navn=ret_navn,
                                   varer=varer, kategorier=kategorier)

        elif 'valgt_ret_navn' in request.form.to_dict().keys():
            gemt_ret = request.form.to_dict()
            ret_navn = gemt_ret['valgt_ret_navn']

            cur.execute("""INSERT OR IGNORE INTO Retter (navn) 
                        VALUES ('{}');""".format(ret_navn))
            db.commit()
            cur.execute("""SELECT Retter.id FROM Retter 
                        WHERE Retter.navn = '{}';""".format(ret_navn))
            ret_id = cur.fetchall()[0]['id']
            a = 'hej'


    return render_template('base.html', data=alle_retter)


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
