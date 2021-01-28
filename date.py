from calendar import Calendar 
import datetime

jours = ('Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche')

def current_week():
    today = datetime.date.today()
    calendar = Calendar()
    months = calendar.monthdatescalendar(today.year, today.month)
    for week in months:
        for day in week:
            if day == today:
                curr_week = week
    result = []
    for i in range(len(curr_week)):
        result.append(Jour(curr_week[i].year, curr_week[i].month, curr_week[i].day, jours[i]))
    return result

def str_to_list(chaine):
    construc = []
    temp = ""
    for char in chaine:
        if char.isdigit():
            temp += char
        elif temp != "":
            construc.append(int(temp))
            temp = ""
    return construc

class Jour():
    def __init__(self, annee = None, mois = None, journ = None, jourl = None):
        self.annee = annee
        self.mois = mois
        self.journ = journ
        self.jourl = jourl

    def __str__(self):
        return f"annee : {self.annee}, mois : {self.mois}, jour : {self.journ} {self.jourl}"

class Borne():
    def __init__(self, jour = None, heure = None):
        if jour is None:
            self.annee = None
            self.mois = None
            self.jour = None
        else:
            self.annee = jour.annee
            self.mois = jour.mois
            self.jour = jour.journ
        self.heure = heure

    def __eq__(self, borne2):
        return self.annee == borne2.annee and self.mois == borne2.mois and self.jour == borne2.jour and self.heure == borne2.heure

    def __lt__(self, borne2):
        if self.annee < borne2.annee :
            return True
        elif self.annee > borne2.annee :
            return False
        if self.mois < borne2.mois :
            return True
        elif self.mois > borne2.mois :
            return False
        if self.jour < borne2.jour :
            return True
        elif self.jour > borne2.jour :
            return False
        if self.heure < borne2.heure:
            return True
        return False

    def __str__(self):
        return f"annee : {self.annee}, mois : {self.mois}, jour : {self.jour}, heure : {self.heure}"

class Horaire():
    def __init__(self, debut = None, fin = None):
        self.debut = debut
        self.fin = fin

    def set_borne(self, borne):
        if self.debut is None:
            self.debut = borne
        elif self.debut > borne:
            if self.fin is None:
                self.fin = self.debut   
                self.debut = borne
            else:
                self.debut = borne
        else:
            self.fin = borne

    def est_vide(self):
        return self.debut is None and self.fin is None

    def est_pret(self):
        return self.debut is not None and self.fin is not None

    def reset(self):
        self.debut = None
        self.fin = None

    def __str__(self):
        return f"debut : ({str(self.debut)}) fin : ({str(self.fin)})"