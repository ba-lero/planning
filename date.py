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
        result.append(Jour(curr_week[i]))
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

def jourl_avec_jour(annee, mois, jour):
    calendar = Calendar()
    months = calendar.monthdatescalendar(annee, mois)
    for week in months:
        for i in range(len(week)):
            if week[i].day == jour:
                return jours[i]

class Jour():
    def __init__(self, jour):
        self.jour = jour
        self.jourl = jourl_avec_jour(jour.year, jour.month, jour.day)

    def __str__(self):
        return f"annee : {self.jour.year}, mois : {self.jour.month}, jour : {self.jour.day} {self.jourl}"

class Horaire():
    def __init__(self, debut = None, fin = None):
        self.debut = debut
        self.fin = fin

    def set_borne(self, borne):
        if self.debut is None:
            self.debut = borne
            self.fin = borne + datetime.timedelta(hours = 1)
        elif self.debut > borne:
            if self.fin is None:
                self.fin = self.debut
                self.debut = borne
            else:
                self.debut = borne
        else:
            self.fin = borne + datetime.timedelta(hours = 1)

    def est_vide(self):
        return self.debut is None and self.fin is None

    def est_pret(self):
        return self.debut is not None and self.fin is not None

    def reset(self):
        self.debut = None
        self.fin = None

    def __str__(self):
        return f"debut : ({str(self.debut)}) fin : ({str(self.fin)})"