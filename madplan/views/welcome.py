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
        valgte_retter = request.form.to_dict()
        ugeplan = Ugeplan()
        for (ugedag, ret_navn) in zip(valgte_retter.keys(), valgte_retter.values()):
            if len(ret_navn) > 0:
                ugeplan.tilfoj_ret(ret_navn, ugedag)
        ugeplan.lav_indkobsliste()
        return render_template('base.html', data=alle_retter, ugeplan=ugeplan)

    return render_template('base.html', data=alle_retter, ugeplan=False)
