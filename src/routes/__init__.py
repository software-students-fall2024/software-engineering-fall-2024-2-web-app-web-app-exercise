from flask import Blueprint, render_template

routes=Blueprint('routes',__name__)
@routes.app_errorhandler(404)
def not_found(e):
    return render_template('404.html')
from . import login