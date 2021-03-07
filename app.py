from flask import Flask, render_template, request, session, redirect, url_for, g
from db import recuperer_compte, creer_compte, creer_emploi, creer_lieu, creer_groupe, recuperer_lieux, recuperer_emplois, recuperer_groupes, inserer_horaire, inserer_personne_groupe, recuperer_membre_de_groupe, recuperer_horaire_de_groupe
import datetime
from date import current_week, str_to_list, Horaire
from werkzeug.security import check_password_hash
import sqlite3 as db

app = Flask(__name__)
app.secret_key = "dev"

emplois = []
mes_groupes = []
horaire = Horaire()
cday = datetime.date.today()
semaine = current_week(cday)

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
    global cday 
    global semaine
    emplois = recuperer_emplois(session['userid'])
    cday = datetime.date.today()
    semaine = current_week(cday)
    horaires = recuperer_horaire_de_groupe(session['userid'])
    return render_template('profil.html', infos = (emplois, horaires))

@app.route('/groupes')
def groupes():
    global mes_groupes
    mes_groupes = recuperer_groupes(session['userid'])
    return render_template('groupes.html', groupes = mes_groupes)

@app.route('/ajouter_emploi', methods=["GET", "POST"])
def ajouter_emploi():
    if request.method == "POST":
        creer_emploi(request.form['nom'], session['userid'])
        return redirect(url_for('profil'))
    else:
        return render_template('ajouter_emploi.html')

@app.route('/ajouter_lieu', methods=["GET", "POST"])
def ajouter_lieu():
    if request.method == "POST":
        creer_lieu(session['userid'], request.form['nom'], request.form['adresse'])
        return redirect(url_for('profil'))
    else:
        return render_template('ajouter_lieu.html')

@app.route('/ajouter_groupe', methods=["GET", "POST"])
def ajouter_groupe():
    if request.method == "POST":
        creer_groupe(session['userid'], request.form['nom'])
        return redirect(url_for('groupes'))
    else:
        return render_template('ajouter_groupe.html')

@app.route('/modifier_emploi', methods=["GET", "POST"])
def modifier_emploi():
    global cday
    global semaine
    if request.method == "POST":
        inserer_horaire(horaire, request.form["lieu"], session['emploicourant'][0][2], request.form["groupe"], request.form["desc"])
        horaire.reset()
        return redirect(url_for('modifier'))
    if 'action' in request.args:
        retour = request.args["action"]
        if retour == 'reset':
            horaire.reset()
        elif retour == 'next':
            cday += datetime.timedelta(days = 7)
            semaine = current_week(cday)
        elif retour == 'previous':
            cday -= datetime.timedelta(days = 7)
            semaine = current_week(cday)
        else:
            retour = str_to_list(request.args["action"])
            borne_selec = datetime.datetime(semaine[retour[1]].jour.year, semaine[retour[1]].jour.month, semaine[retour[1]].jour.day, retour[0])
            horaire.set_borne(borne_selec)
    else:
        horaire.reset()
    session["groupes"] = recuperer_groupes(session['userid'])
    session["lieux"] = recuperer_lieux(session['userid'])
    return render_template('modifier_emploi.html', infos=(horaire, semaine))

@app.route('/modifier_groupe', methods=["GET", "POST"])
def modifier_groupe():
    if request.method == "POST":
        membre = recuperer_compte(request.form["login"])
        if membre is None:
            return redirect(url_for('modifier_groupe', erreur=True))
        inserer_personne_groupe(request.form["login"],session["groupecourant"][0][1])
        return redirect(url_for('modifier_groupe'))
    if 'erreur' in request.args:
        return render_template('modifier_groupe.html', erreur=request.args['erreur'])
    else:
        return render_template('modifier_groupe.html')

@app.route('/select/<retour>')
def select(retour):
    return redirect(url_for('modifier_emploi', action=retour))

@app.route('/setemploi/<id_emploi>')
def setemploi(id_emploi):
    for emploi in emplois:
        if emploi[0][2] == int(id_emploi):
            session['emploicourant'] = emploi
            return redirect(url_for('modifier_emploi'))

@app.route('/setgroupe/<id_groupe>')
def setgroupe(id_groupe):
    for groupe in mes_groupes:
        if groupe[0][1] == int(id_groupe):
            session['groupecourant'] = groupe
            return redirect(url_for('modifier_groupe'))

@app.route("/supprimer/<int:id_article>")
def supprimer(id_article):
    return redirect(url_for('accueil'))

