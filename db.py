from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3 as db

def init_db():
    conn = db.connect("emploi.db")  # connect(nom_fichier) renvoie un handler de connexion
    with open("schema.sql") as script:  # Ouverture du fichier contenant le schéma de la base
        conn.executescript(script.read())  # Sa lecture donne une chaîne qu'on passe à executescript(sql)
    conn.close()

init_db()

def recuperer_compte(login):
    """Renvoie un tuple de la forme (id_membre, mot de passe)
    ou None si aucun membre n'a le login indiqué."""

    with db.connect("emploi.db") as c:
        curs = c.execute(
            """SELECT id_m, mdp, pseudo FROM membres WHERE login = ?""",
            (login,)
        )
        return curs.fetchone()

def creer_compte(login, mdp, pseudo):
    with db.connect("emploi.db") as c:
        c.execute("""INSERT INTO membres (login, mdp, pseudo) VALUES (?, ?, ?);""", (login, generate_password_hash(mdp), pseudo))

def creer_emploi(nom, id):
    with db.connect("emploi.db") as c:
        c.execute("""INSERT INTO emploi (auteur_id, nom) VALUES (?, ?)""", (id, nom))

def recuperer_emplois(id):
    with db.connect("emploi.db") as c:
        curs = c.execute("""SELECT nom, cree_le, id_e FROM emploi WHERE auteur_id = ?""", (id,))
        emplois = curs.fetchall()
        result = [0] * len(emplois)
        for i in range(len(emplois)):
            curs = c.execute("""SELECT id_h, groupe_id, lieu_id, debut, fin FROM horaire WHERE emploi_id = ?""", (emplois[i][2],))
            horaires = curs.fetchall()
            result[i] = (emplois[i], horaires)
        return result

def recuperer_lieux(id):
    with db.connect("emploi.db") as c:
        curs = c.execute("""SELECT id_l, nom, adresse FROM lieu WHERE auteur_id = ?""", (id,))
        return curs.fetchall()

def inserer_horaire(horaire, lieu, id):
    with db.connect("emploi.db") as c:
        debut = f"{horaire.debut.year}-{horaire.debut.month}-{horaire.debut.day} {horaire.debut.hour}:00:00"
        fin = f"{horaire.fin.year}-{horaire.fin.month}-{horaire.fin.day} {horaire.fin.hour}:00:00"
        c.execute("""INSERT INTO horaire (emploi_id, lieu_id, debut, fin) VALUES (?, ?, ?, ?)""", (id, lieu, debut, fin))
    
    with db.connect("emploi.db") as c:
        curs = c.execute("""SELECT * FROM horaire WHERE emploi_id = 1""")
        for i in curs:
            print(i)