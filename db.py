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

def creer_lieu(id, nom, adresse):
    with db.connect("emploi.db") as c:
        c.execute("""INSERT INTO lieu (auteur_id, nom, adresse) VALUES (?, ?, ?)""", (id, nom, adresse))

def creer_groupe(id, nom):
    with db.connect("emploi.db") as c:
        c.execute("""INSERT INTO groupe (auteur_id, nom) VALUES (?, ?)""", (id, nom))
        c.execute("""INSERT INTO membre_de_groupe (membre_id, groupe_id) VALUES (?, (SELECT MAX(id_g) FROM groupe))""", (id,))

def recuperer_emplois(id):
    with db.connect("emploi.db") as c:
        curs = c.execute("""SELECT nom, cree_le, id_e FROM emploi WHERE auteur_id = ?""", (id,))
        emplois = curs.fetchall()
        result = [0] * len(emplois)
        for i in range(len(emplois)):
            curs = c.execute("""SELECT id_h, groupe_id, lieu_id, debut, fin, description FROM horaire WHERE emploi_id = ?""", (emplois[i][2],))
            horaires = curs.fetchall()
            result[i] = (emplois[i], horaires)
        return result

def recuperer_groupes(id):
    with db.connect("emploi.db") as c:
        curs = c.execute("""SELECT nom, id_g FROM groupe WHERE auteur_id = ?""", (id,))
        groupes = []
        for g in curs:
            curs2 = c.execute("""SELECT membres.pseudo FROM membres 
                JOIN membre_de_groupe ON membres.id_m = membre_de_groupe.membre_id
                WHERE membre_de_groupe.groupe_id = ?""", (g[1],))
            groupes.append((g, [m[0] for m in curs2]))
        return groupes

def recuperer_lieux(id):
    with db.connect("emploi.db") as c:
        curs = c.execute("""SELECT id_l, nom, adresse FROM lieu WHERE auteur_id = ?""", (id,))
        return curs.fetchall()

def inserer_horaire(horaire, lieu, id_h, id_g, desc):
    with db.connect("emploi.db") as c:
        debut = f"""{format_horaire(horaire.debut.year)}-{format_horaire(horaire.debut.month)}-{format_horaire(horaire.debut.day)} {format_horaire(horaire.debut.hour)}:{format_horaire(horaire.debut.minute)}:{format_horaire(horaire.debut.second)}"""
        fin = f"""{format_horaire(horaire.fin.year)}-{format_horaire(horaire.fin.month)}-{format_horaire(horaire.fin.day)} {format_horaire(horaire.fin.hour)}:{format_horaire(horaire.fin.minute)}:{format_horaire(horaire.fin.second)}"""
        c.execute("""INSERT INTO horaire (emploi_id, groupe_id, lieu_id, debut, fin, description) VALUES (?, ?, ?, ?, ?)""", (id_h, id_g, lieu, debut, fin, desc))

def inserer_personne_groupe(login, id_g):
    with db.connect("emploi.db") as c:
        c.execute("""INSERT INTO membre_de_groupe (membre_id, groupe_id) VALUES ((SELECT id_m FROM membres WHERE login = ?), ?)""", (login, id_g))

def recuperer_membre_de_groupe(id_g):
    with db.connect("emploi.db") as c:
        curs = c.execute("""SELECT membres.pseudo FROM membres 
                        JOIN membre_de_groupe ON membres.id_m = membre_de_groupe.membre_id
                        WHERE membre_de_groupe.groupe_id = ?""", (id_g,))
        return [m[0] for m in curs]

def recuperer_horaire_de_groupe(id_m):
    with db.connect("emploi.db") as c:
        curs = c.execute("""SELECT horaire.description, horaire.debut, horaire.fin FROM horaire 
                        JOIN membre_de_groupe ON horaire.groupe_id = membre_de_groupe.groupe_id
                        WHERE membre_de_groupe.membre_id = ?""", (id_m,))
        return curs.fetchall()

"""SELECT horaire.description, horaire.debut, horaire.fin, lieu.nom 
                        FROM horaire JOIN lieu ON lieu.id_l = horaire.lieu_id
                        JOIN membre_de_groupe ON membre_de_groupe.groupe_id = horaire.groupe_id
                        WHERE membre_de_groupe.membre_id = ?"""

def format_horaire(nb):
    result = str(nb)
    if len(result) == 1:
        result = "0" + result
    return result
