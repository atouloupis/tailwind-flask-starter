# main.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import fileType

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
    # fileTypes=list(map(lambda c: c.value, fileType))
    # passer la liste des membres de l'enum filetype
    fileTypes = list(fileType.__members__.items())
    username = current_user.name
    timelines = [user_id,
                username,
                'This is the third event.'
                ]
    return render_template("boardPages/tourdecontrol.html",timelines=timelines, user=current_user,fileTypes=fileTypes)

@main.route('/immeuble')
@login_required
def immeuble():
    
    return render_template("boardPages/immeuble.html",user=current_user)

@main.errorhandler(404)
def page_not_found(error):
  return redirect("/", code=302)