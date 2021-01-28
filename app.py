from flask import Flask, render_template, request, session, redirect, url_for, g
from db import recuperer_compte, creer_compte
from date import current_week, str_to_list, Horaire, Borne
from werkzeug.security import check_password_hash
import sqlite3 as db

app = Flask(__name__)
app.secret_key = "dev"

@app.route('/')
def set_session():
    session.clear()
    return redirect(url_for('accueil'))

@app.route('/accueil')
def accueil():
    return render_template('accueil.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form["login"]
        mdp = request.form["mdp"]
        check = recuperer_compte(login)
        if check is None:
            session.clear()
            return redirect(url_for('login', erreur=True))
        if check_password_hash(check[1],mdp):
            session.clear()
            session['userid'] = check[0]
            session["username"] = login
            session["usernickname"] = check[2]
            return redirect(url_for('accueil'))
    try:
        return render_template('login.html',erreur=request.args['erreur'])
    except:
        return render_template('login.html',erreur=False)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('accueil'))

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        login = request.form["login"]
        mdp = request.form["mdp"]
        mdpcheck = request.form["mdpcheck"]
        pseudo = request.form["pseudo"]
        if recuperer_compte(login) is not None:
            return redirect(url_for('register', erreur_id=True))
        if mdp != mdpcheck:
            return redirect(url_for('register', erreur_mdp=True))
        creer_compte(login,mdp,pseudo)
        return redirect(url_for('login'))
    try:
        return render_template('register.html',erreur_id=request.args['erreur_id'])
    except:
        try:
            return render_template('register.html',erreur_mdp=request.args['erreur_mdp'])
        except:
            return render_template('register.html')

@app.route('/profil')
def profil():
    return render_template('profil.html')

horaire = Horaire()
semaine = current_week()

@app.route('/ajouter', methods=["GET", "POST"])
def ajouter():
    try:
        retour = str_to_list(request.args["h1"])
        borne_selec = Borne(semaine[retour[1]], retour[0])
        horaire.set_borne(borne_selec)
        return render_template('add.html', infos=(horaire, semaine))
    except KeyError:
        horaire.reset()
        return render_template('add.html', infos=(horaire, semaine))

@app.route('/select/<borne>')
def select(borne):
    return redirect(url_for('ajouter', h1=borne))

@app.route("/supprimer/<int:id_article>")
def supprimer(id_article):
    return redirect(url_for('accueil'))

