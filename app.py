from flask import Flask, render_template, request, session, redirect, url_for, g
from db import recuperer_compte, creer_compte, creer_emploi, recuperer_lieux, recuperer_emplois, inserer_horaire
import datetime
from date import current_week, str_to_list, Horaire
from werkzeug.security import check_password_hash
import sqlite3 as db

app = Flask(__name__)
app.secret_key = "dev"

emplois = []
horaire = Horaire()
semaine = current_week()

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
        elif mdp is None:
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
        for _, value in request.form.items():
            if value == "":
                return redirect(url_for('register', erreur_none=True))
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
    elif 'erreur_none' in request.args:
        return render_template('register.html',erreur_none=request.args['erreur_none'])
    else:
        return render_template('register.html')

@app.route('/profil')
def profil():
    global emplois
    emplois = recuperer_emplois(session['userid'])
    return render_template('profil.html', emplois = emplois)

@app.route('/ajouter', methods=["GET", "POST"])
def ajouter():
    if request.method == "POST":
        creer_emploi(request.form['nom'], session['userid'])
        return redirect(url_for('profil'))
    else:
        return render_template('ajouter.html')

@app.route('/modifier', methods=["GET", "POST"])
def modifier():
    if request.method == "POST":
        print(session['emploicourant'][0][2])
        inserer_horaire(horaire, request.form["lieu"], session['emploicourant'][0][2])
        horaire.reset()
        return redirect(url_for('modifier'))
    if 'action' in request.args:
        retour = request.args["action"]
        if retour == 'reset':
            horaire.reset()
        else:
            retour = str_to_list(request.args["action"])
            borne_selec = datetime.datetime(semaine[retour[1]].jour.year, semaine[retour[1]].jour.month, semaine[retour[1]].jour.day, retour[0])
            horaire.set_borne(borne_selec)
    else:
        horaire.reset()
    return render_template('modifier.html', infos=(horaire, semaine, session['lieux']))

@app.route('/select/<retour>')
def select(retour):
    return redirect(url_for('modifier', action=retour))

@app.route('/setemploi/<id_emploi>')
def setemploi(id_emploi):
    for emploi in emplois:
        if emploi[0][2] == int(id_emploi):
            session['emploicourant'] = emploi
            return redirect(url_for('modifier'))

@app.route("/supprimer/<int:id_article>")
def supprimer(id_article):
    return redirect(url_for('accueil'))

