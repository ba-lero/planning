DROP TABLE IF EXISTS membres;
DROP TABLE IF EXISTS emploi;
DROP TABLE IF EXISTS groupe;
DROP TABLE IF EXISTS membre_de_groupe;
DROP TABLE IF EXISTS lieu;
DROP TABLE IF EXISTS horaire;

CREATE TABLE membres (
  id_m          INTEGER         PRIMARY KEY AUTOINCREMENT,
  login         VARCHAR(20)     UNIQUE NOT NULL,
  mdp           VARCHAR(100)    NOT NULL,
  pseudo        VARCHAR(30)     NOT NULL,
  date_creation TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE emploi (
  id_e      INTEGER     PRIMARY KEY AUTOINCREMENT,
  auteur_id INTEGER     NOT NULL REFERENCES membres (id_m),
  cree_le   TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
  nom       VARCHAR(50) NOT NULL
);

CREATE TABLE groupe (
  id_g      INTEGER     PRIMARY KEY AUTOINCREMENT,
  auteur_id INTEGER     NOT NULL REFERENCES membres (id_m),
  nom       VARCHAR(30) NOT NULL
);

CREATE TABLE membre_de_groupe (
  membre_id INTEGER REFERENCES membres (id_m),
  groupe_id INTEGER REFERENCES groupe (id_g),
  PRIMARY KEY (membre_id, groupe_id)
);

CREATE TABLE lieu (
  id_l      INTEGER     PRIMARY KEY AUTOINCREMENT,
  auteur_id INTEGER     NOT NULL REFERENCES membres (id_m),
  nom       VARCHAR(50) NOT NULL,
  adresse   VARCHAR(100)   
);

CREATE TABLE horaire (
  id_h        INTEGER     PRIMARY KEY AUTOINCREMENT,
  emploi_id   INTEGER     NOT NULL REFERENCES emploi (id_e),
  groupe_id   INTEGER     REFERENCES groupe (id_g),
  lieu_id     INTEGER     REFERENCES lieu (id_l),
  debut       TIMESTAMP   NOT NULL,
  fin         TIMESTAMP   NOT NULL,
  description TEXT,
  CHECK (debut < fin)
);

INSERT INTO membres (login, mdp, pseudo) VALUES ('alice', 'pbkdf2:sha256:150000$yL1piFAc$62b9e17c0c6da1a4696f92eb173e7e0e33d1eea25bdc3c573dfab189b345e288', 'Alice'), ('bob', 'pbkdf2:sha256:150000$vHdMbRRd$6e5c29670ad7b8df28122cdd8381f0864ec4276a90de13590af76c2cabe9e909', 'Bob');
INSERT INTO emploi (auteur_id, nom) VALUES (1, 'Sport'), (2, 'Resto');
INSERT INTO groupe (auteur_id, nom) VALUES (1, 'zebi'), (1, 'Malthus'), (1, 'Ulric'); 
INSERT INTO membre_de_groupe (membre_id, groupe_id) VALUES (1,1), (1,2);
INSERT INTO lieu (auteur_id, nom, adresse) VALUES (1, 'Maison', '2 rue des Pines'), (2, 'Terrain', '4 allée du grand Philippe');
INSERT INTO horaire (emploi_id, debut, fin, groupe_id, lieu_id, description) VALUES 
                    (1, '2021-01-26 10:10:10', '2021-01-26 10:20:20', 1, 2, 'Groupe 1'),
                    (1, '2021-01-26 10:10:10', '2021-01-26 10:20:20', 1, 2, 'Groupe 2'),
                    (2, '2021-01-26 10:10:10', '2021-01-26 10:20:20', 1, 2, 'Groupe 56'),
                    (2, '2021-01-29 12:45:00', '2021-01-29 13:45:00', 2, 1, 'Groupe 3'),
                    (2, '2021-01-26 10:10:10', '2021-01-26 10:20:20', 3, 2, 'Groupe 4');
