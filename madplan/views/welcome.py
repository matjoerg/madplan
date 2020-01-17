from flask import Blueprint, render_template

bp = Blueprint('welcome', __name__)

@bp.route('/')
def hello():
    return render_template('base.html')
