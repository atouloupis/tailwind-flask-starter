# main.py
import json
from flask import Blueprint, render_template,session
from sqlalchemy import select
from flask_login import login_required, current_user
from .models import fileType,files,userprofileresidence,filesresidence,residence
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
    fileTypes = list(fileType.__members__.items())
    username = current_user.name
    # Créer une requête select
    residences_query = select(userprofileresidence.residenceId,userprofileresidence.isActive,userprofileresidence.profile,residence.label)\
    .join(residence,residence.id==userprofileresidence.residenceId)\
    .where(userprofileresidence.userId == user_id)
    # Exécuter la requête et récupérer les résultats sous forme de liste
    residences_list = db.session.execute(residences_query).all()
    residences_list_dicts = [{"residenceId": r[0],"residenceName": r[3], "isActive": r[1], "profile": r[2].name} for r in residences_list if r[1]==1]
    session["residence"] = residences_list_dicts

    timelines = [user_id,
                username,
                residences_list_dicts[0]['profile']
                ]
    return render_template("boardPages/tourdecontrol.html",timelines=timelines, user=current_user,fileTypes=fileTypes,residencesList=residences_list_dicts)

@main.route('/immeuble')
@login_required
def immeuble():
    residenceList = session.get('residence')
    print(residenceList)

    # Créer une requête select
    files_query = select(files.fileName,files.fileType)\
    .select_from(files)\
    .join(filesresidence,files.id==residence.fileId)\
    .where(session.get('residence')==filesresidence.residenceId)
    # Exécuter la requête et récupérer les résultats sous forme de liste
    files_list = db.session.execute(files_query).all()
    return render_template("boardPages/immeuble.html",user=current_user, files=files_list)

@main.errorhandler(404)
def page_not_found(error):
  return redirect("/", code=302)


def alchemyencoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)