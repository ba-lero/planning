from flask import Flask, render_template, request, session, redirect, url_for, g
from db import recuperer_compte, creer_compte, recuperer_lieux, inserer_horaire
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
            session["lieux"] = recuperer_lieux(session['userid'])
            return redirect(url_for('accueil'))
    if 'erreur' in request.args:
        return render_template('login.html',erreur=request.args['erreur'])
    else:
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
    if 'erreur_id' in request.args:
        return render_template('register.html',erreur_id=request.args['erreur_id'])
    elif 'erreur_mdp' in request.args:
        return render_template('register.html',erreur_mdp=request.args['erreur_mdp'])
    else:
        return render_template('register.html')

@app.route('/profil')
def profil():
    return render_template('profil.html')

horaire = Horaire()
semaine = current_week()

@app.route('/ajouter', methods=["GET", "POST"])
def ajouter():
    if request.method == "POST":
        inserer_horaire(horaire, request.form["lieu"])
        horaire.reset()
        return redirect(url_for('ajouter'))
    if 'action' in request.args:
        retour = request.args["action"]
        if retour == 'reset':
            horaire.reset()
        else:
            retour = str_to_list(request.args["action"])
            borne_selec = Borne(semaine[retour[1]], retour[0])
            horaire.set_borne(borne_selec)
    else:
        horaire.reset()
    return render_template('add.html', infos=(horaire, semaine, session['lieux']))

@app.route('/select/<retour>')
def select(retour):
    return redirect(url_for('ajouter', action=retour))

@app.route("/supprimer/<int:id_article>")
def supprimer(id_article):
    return redirect(url_for('accueil'))

