# auth.py
import json
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required,current_user
from .models import user,userprofileresidence,residence,fileType
from sqlalchemy import select
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    if current_user.is_authenticated:
        # Rediriger l'utilisateur vers une autre page s'il est déjà connecté
        return render_template("boardPages/tourdecontrol.html")
    else:
        return render_template('staticPages/login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    curr_user = user.query.filter_by(email=email).first()
    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not curr_user or not check_password_hash(curr_user.password, password): 
        flash('Votre login ou mot de passe sont incorrects.')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    # save user info in the current_user session
    login_user(curr_user, remember=remember)
    #get de residence user list in DB
    residences_query = select(userprofileresidence.residenceId,userprofileresidence.isActive,userprofileresidence.profile,residence.label)\
    .join(residence,residence.id==userprofileresidence.residenceId)\
    .where(userprofileresidence.userId == current_user.get_id())
    # Exécuter la requête et récupérer les résultats sous forme de liste
    residences_list = db.session.execute(residences_query).all()
    residences_list_dicts = [{"residenceId": r[0],"residenceName": r[3], "isActive": r[1], "profile": r[2].name} for r in residences_list if r[1]==1]
    #save the residence list and current residence in session
    session["residence"] = residences_list_dicts
    session["currentRes"] = residences_list_dicts[0]
    fileTypes=[{"name":member.name,"value":member.value} for member in fileType]
    session["fileTypes"]=fileTypes
    return redirect(url_for('main.tourdecontrol'))

@auth.route('/signup')
def signup():
    return render_template('staticPages/signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    dateOfBirth = request.form.get('dateOfBirth')

    curr_user = user.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if curr_user: # if a user is found, we want to redirect back to signup page so user can try again  
        flash('Ce compte existe déjà')
        return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = user(email=email, name=name, password=generate_password_hash(password, method='pbkdf2'), dateOfBirth=dateOfBirth)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

