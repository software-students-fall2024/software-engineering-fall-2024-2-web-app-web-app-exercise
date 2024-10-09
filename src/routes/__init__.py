from flask import Blueprint, render_template
routes=Blueprint('routes',__name__)
from . import login
from . import home
from . import search
from . import signup