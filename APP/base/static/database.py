import mysql.connector
# creazione connessione
db = mysql.connector.connect(

     host="localhost",
     user="root",
     password="Mysql",
     database='university'
)

cursor=db.cursor()
#cursor.execute("CREATE TABLE IF NOT EXISTS studenti (nome VARCHAR(20), cognome VARCHAR(20), immatricolazione DATE, matricola VARCHAR (6) PRIMARY KEY) ")
#cursor.execute("CREATE TABLE utenti (matricola VARCHAR(10) PRIMARY KEY, email VARCHAR(30) UNIQUE, password VARCHAR(20)) ")
#cursor.execute("ALTER TABLE utenti ADD (online VARCHAR(1)) ")
#cursor.execute("CREATE TABLE insegnanti ( id INT AUTO_INCREMENT PRIMARY KEY,  nome VARCHAR(20), cognome VARCHAR(20), email_istituzionale VARCHAR(20) UNIQUE, password VARCHAR(20))")
#cursor.execute("CREATE TABLE corso (codice VARCHAR(30) PRIMARY KEY, nome VARCHAR(30), descrizione VARCHAR(255))  ")
#cursor.execute("ALTER TABLE corso ADD FOREIGN KEY (matricola) REFERENCES utenti (matricola)")
#cursor.execute("ALTER TABLE corso DROP FOREIGN KEY corso_ibfk_1")
#cursor.execute("ALTER TABLE corso ADD CONSTRAINT corso_ibfk_1 FOREIGN KEY (matricola) REFERENCES utenti (matricola) ON UPDATE CASCADE ON DELETE CASCADE")
# create_table_query = """
# CREATE TABLE iscrizioni (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     matricola VARCHAR(255),
#     codice_corso VARCHAR(255),
#     FOREIGN KEY (matricola) REFERENCES utenti(matricola) ON UPDATE CASCADE ON DELETE CASCADE,
#     FOREIGN KEY (codice_corso) REFERENCES corso(codice) ON UPDATE CASCADE ON DELETE CASCADE
# );
# """
#
# cursor.execute(create_table_query)
# cursor.execute("ALTER TABLE corso DROP FOREIGN KEY corso_ibfk_1")
# cursor.execute("ALTER TABLE corso ADD CONSTRAINT corso_ibfk_1 FOREIGN KEY (matricola) REFERENCES utenti (matricola) ON UPDATE CASCADE ON DELETE SET NULL")
