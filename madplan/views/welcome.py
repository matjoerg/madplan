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
            ret_navn = request.form.to_dict()
            cur.execute("""SELECT Varer.navn, RetterVarer.antal, Kategorier.navn kategori FROM Retter 
                        INNER JOIN Kategorier ON Varer.kategori_id = Kategorier.id
                        INNER JOIN RetterVarer ON Retter.id = RetterVarer.ret_id 
                        INNER JOIN Varer on RetterVarer.vare_id = Varer.id 
                        WHERE Retter.navn = '{}';""".format(ret_navn['valgt_ret_navn']))
            valgt_ret = cur.fetchall()
            return render_template('base.html', data=alle_retter, valgt_ret=valgt_ret)

    return render_template('base.html', data=alle_retter)
