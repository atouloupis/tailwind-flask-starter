# main.py
import json
from flask import Blueprint, render_template,session
from sqlalchemy import select
from flask_login import login_required, current_user
from .models import files,filesresidence
from . import db

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
def index():
    return render_template('staticPages/index.html',var1='toto')

@main.route("/about")
def about():
	return render_template("staticPages/about.html")

@main.route('/tourdecontrol')
@login_required
def tourdecontrol():
    user_id = current_user.get_id()
    username = current_user.name
    timelines = [user_id,
                username,
                session.get("currentRes")
                ]
    return render_template("boardPages/tourdecontrol.html",timelines=timelines)


@main.route('/immeuble')
@login_required
def immeuble():
    currRes = session.get('currentRes')
    # Créer une requête select
    files_query = select(files.fileName,files.fileType,files.storageId)\
    .select_from(files)\
    .join(filesresidence,files.id==filesresidence.filesId)\
    .where(currRes["residenceId"]==filesresidence.residenceId)
    # Exécuter la requête et récupérer les résultats sous forme de liste
    files_list = db.session.execute(files_query).all()
    files_list = [{"fileName":member[0],"fileType":member[1].value,"url":member[2]} for member in files_list]
    return render_template("boardPages/immeuble.html", files=files_list)

@main.errorhandler(404)
def page_not_found(error):
  return redirect("/", code=302)
