from flask import Flask, render_template, request, redirect,session, jsonify, render_template_string,abort, url_for
import yaml
import mysql.connector
from flask_session import Session
from models.students_models import students
from models.Teachers_models import Teachers
from models.Course import Corso
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

with open('static/db.yaml', 'r') as file:
    database = yaml.safe_load(file)
conn = mysql.connector.connect(
    host=database['mysql_host'],
    user=database['mysql_user'],
    password=database['mysql_password'],
    database=database['mysql_database']
)
cursor = conn.cursor()
@app.route('/login', methods=['GET','POST'])
def login():
    cursor=conn.cursor()
    if request.method == 'POST':
        utenteDetails = request.form
        ruolo = utenteDetails["ruolo"]
        if ruolo=='studente':
            matricola = utenteDetails["matricola"]
            password = utenteDetails["password"]
            cursor.execute('SELECT matricola,email,online FROM utenti WHERE matricola = %s AND password = %s', (matricola, password))
            utente = cursor.fetchone()
            if utente:
                session['matricola'] = matricola
                cursor.execute('UPDATE utenti SET online = %s WHERE matricola = %s', ('Y', matricola))
                conn.commit()
                matricola = utente[0]
                email = utente[1]
                online = 'Y'
                cursor.close()
               # session['matricola']=matricola
                return render_template('/utente.html', matricola=matricola, email=email, online=online)
            else:

            # L'email non esiste, restituisci una messaggio di errore
                error_message = 'L\'account con questa email non esiste'
                abort(403, description=error_message)
            # L'email non esiste, restituisci un messaggio JSON
            #return jsonify({'error': 'L\'account con questa email non esiste'}), 403
            #return render_template('login.html')
        else:
            insegnanti=request.form
            email_istituzionale = insegnanti["email_insegnante"]
            password = insegnanti["password_insegnante"]
            cursor.execute('SELECT nome, cognome, email_istituzionale, password FROM insegnanti WHERE email_istituzionale = %s', (email_istituzionale,))
            teach = cursor.fetchone()
            conn.commit()
            if teach:
                session['email_insegnante'] = email_istituzionale
                nome=teach[0]
                cognome=teach[1]
                email_istituzionale=teach[2]
                return render_template('insegnanti.html', insegnanti=[teach])
            else:
            # L'email non esiste, restituisci una messaggio di errore
                error_message = 'L\'account con questa email non esiste'
                abort(403, description=error_message)
    return render_template('login.html')

@app.route('/corsi_insegnanti', methods=['GET'])
def corsi_insegnanti():
    if 'email_insegnante' in session:
        cursor.execute("SELECT*FROM iscrizioni")
        corsi_teach=cursor.fetchall()

@app.route('/richiedi_nuove_credenziali', methods=['POST'])
def richiedi_nuove_credenziali():
    if request.method == 'POST':
        if 'matricola' in session:
            matricola = request.form['matricola_attuale']
            email = request.form['email_studente']
            nuova_matricola = request.form['nuova_Matricola']
            nuova_email = request.form['nuova email']
            if nuova_matricola == matricola or nuova_email==email:
               return jsonify({'error': 'Matricola ed Email non possono essere uguali a quelle precedenti'})

            cursor.execute('SELECT matricola,email,online FROM utenti WHERE email = %s AND matricola = %s',(email, matricola))
            utente = cursor.fetchone()

            if utente:
                cursor.execute('UPDATE utenti SET matricola = %s, email = %s WHERE email = %s', (nuova_matricola, nuova_email, email))
                conn.commit()
                session['matricola'] = nuova_matricola
                session['email']=nuova_email
                online = utente[2]

            return render_template('/utente.html', matricola=nuova_matricola, email=nuova_email, online=online)

        if 'email_insegnante' in session:
            email_istituzionale = request.form['email_insegnante']
            nuova_email = request.form['nuova email']
            password = request.form['password']
            if nuova_email == email_istituzionale:
                return jsonify({'error': ' Email non può essere uguale a quella precedente'})
            cursor.execute('SELECT nome,cognome,email_istituzionale FROM insegnanti WHERE email_istituzionale = %s',
                           (email_istituzionale,))
            user = cursor.fetchone()
            if user:
                cursor.execute('UPDATE insegnanti SET email_istituzionale = %s WHERE email_istituzionale = %s',
                               (nuova_email, email_istituzionale))

                conn.commit()
                session['email_insegnante'] = nuova_email

                cursor.execute('SELECT  nome, cognome, email_istituzionale FROM insegnanti')
                insegnanti_data = cursor.fetchall()
                return render_template('insegnanti.html', insegnanti=insegnanti_data)
        error_message = 'L\'account non è loggato'
        abort(404, description=error_message)





@app.route('/logout', methods=['GET'])
def logout():
    if 'matricola' in session:

        matricola = session['matricola']
        cursor.execute('UPDATE utenti SET online = %s WHERE matricola = %s', ('N', matricola))
        conn.commit()
        session.clear()
        return redirect('/login')
    if 'email_insegnante' in session:
        conn.commit()
        session.clear()
        return redirect('/login')
    else:
        error = 'Non sei loggato'
        abort(404, error)

    return redirect('/login')

@app.route('/utente')
def utente():
    if 'matricola' not in session:
        session['online']='N'
        return redirect('/login')
    matricola = session['matricola']
    cursor.execute('SELECT matricola, email, online FROM utenti WHERE matricola = %s', (matricola,))
    utente = cursor.fetchone()

    if utente:
        matricola = utente[0]
        email = utente[1]
        online = utente[2]
        return render_template('utente.html', matricola=matricola, email=email, online=online)

    return render_template('utente.html')




@app.route('/')
def home():
    if 'email' in session:
        return redirect('/utente')
    return render_template('home.html')


@app.route('/registrati', methods=['GET', 'POST'])
def registrati():
    if request.method == 'POST':
        utentiDetails = request.form
        matricola = utentiDetails["matricola"]
        email = utentiDetails["email"]
        password = utentiDetails["password"]
        nuovo_studente = students(matricola, email, password)

        cursor = conn.cursor()
        cursor.execute('INSERT INTO utenti(matricola,email,password,online) VALUES(%s, %s, %s, %s)', (nuovo_studente.matricola, nuovo_studente.email, nuovo_studente.password, 'N'))
        conn.commit()
        cursor.close()
        return redirect('/utenti')

    return render_template('registrati.html')

@app.route('/insegnanti.html')
def insegnanti():
    cursor = conn.cursor()
    cursor.execute('SELECT  nome, cognome, email_istituzionale FROM insegnanti')
    insegnanti_data = cursor.fetchall()
    return render_template('insegnanti.html', insegnanti=insegnanti_data)

@app.route('/registrati_insegnante', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        insegnantidetails = request.form
        nome = insegnantidetails["nome"]
        cognome=insegnantidetails["cognome"]
        email_istituzionale = insegnantidetails["email_istituzionale"]
        password = insegnantidetails["password"]
        new_teacher = Teachers(nome, cognome, email_istituzionale, password)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO insegnanti(nome, cognome, email_istituzionale, password) VALUES(%s, %s, %s, %s)',
                       (new_teacher.nome, new_teacher.cognome, new_teacher.email_istituzionale, new_teacher.password))
        conn.commit()
        cursor.close()
        return redirect('/insegnanti.html')
    return render_template('registrati_insegnante.html')


@app.route('/utenti')
def utenti():
    cursor.execute('SELECT * FROM utenti')
    utentiDetails = cursor.fetchall()
    return render_template('utenti.html', utentiDetails=utentiDetails)

@app.route('/cancella', methods=['GET','POST'])
def cancella_account():
    if 'matricola' in session:
        matricola = session['matricola']
        if request.method == 'POST':
            if matricola:
                cursor.execute('DELETE FROM utenti WHERE matricola = %s', (matricola,))
                conn.commit()
                session.clear()  # Cancella anche la sessione dopo la cancellazione
                return redirect('/login')
    elif 'email_insegnante' in session:
        email_istituzionale = session['email_insegnante']
        if request.method == 'POST':
            if email_istituzionale:
                cursor.execute('DELETE FROM insegnanti WHERE email_istituzionale = %s', (email_istituzionale,))
                conn.commit()
                session.clear()  # Cancella anche la sessione dopo la cancellazione
                return redirect('/login')

    return render_template('login.html')


@app.route('/corsi')
def visualizza_corsi():
    corsi = []  # Definisci la variabile all'esterno del blocco condizionale
    corsi_iscritti = []
    #cursor = conn.cursor()
    if 'matricola' in session:
        matricola = session['matricola']
        cursor.execute('SELECT codice, nome, descrizione  FROM corso')
        corsi_data = cursor.fetchall()
        for row in corsi_data:
            corso=Corso(*row)
            corsi.append(corso)
        cursor.execute("SELECT codice, nome, descrizione FROM corso WHERE matricola = %s", (matricola,))
        corsi_iscritti_data = cursor.fetchall()
        corsi_iscritti = [Corso(*row) for row in corsi_iscritti_data]
        return render_template('corsi.html', corsi=corsi, corsi_iscritti=corsi_iscritti)
    return jsonify({'error': 'L\'account con questa email non esiste'})


    #return render_template('corsi.html', corsi=corsi, corsi_iscritti=corsi_iscritti)

@app.route('/iscrivi_corso/<codice_corso>', methods=['GET', 'POST'])
def iscrivi_corso(codice_corso):
    if 'matricola' in session:
        matricola=session['matricola']
        cursor.execute("SELECT codice, nome, descrizione FROM corso WHERE codice=%s", (codice_corso,))
        corso_data=cursor.fetchone()
        cursor.execute("SELECT matricola FROM corso WHERE codice=%s", (codice_corso,))
        iscritti = cursor.fetchone()
        cursor.execute("INSERT INTO iscrizioni (matricola, codice_corso) VALUES (%s, %s) ", (matricola, codice_corso) )
        if matricola in iscritti:
            return jsonify({'error': 'Sei già iscritto a questo corso.'})
        elif corso_data:
            corso = Corso(*corso_data)
            corso.iscrivi_studente(matricola)
            cursor.execute('UPDATE corso SET matricola = %s WHERE codice = %s',
                           (matricola, codice_corso))
            conn.commit()
            # '/pagina_di_successo'
            return redirect(url_for('pagina_di_successo', codice_corso=codice_corso))
        else:
            abort(404 , 'corso non trovato')
    else:
        abort(403, 'Devi effettuare l\'accesso come studente per iscriverti a un corso')

#@app.route('/pagina_di_successo')
@app.route('/pagina_di_successo/<codice_corso>')
def pagina_di_successo(codice_corso):
    if 'matricola' in session:
        matricola = session['matricola']

        cursor.execute("SELECT codice, nome, descrizione FROM corso WHERE matricola=%s AND codice=%s", (matricola,codice_corso))
        corso_data = cursor.fetchone()
        if corso_data:
            nome_corso = corso_data[1]
            return render_template('Tabella corsi iscritti.html', matricola=matricola, nome_corso=nome_corso)

    abort(403, 'Devi effettuare l\'accesso come studente per visualizzare questa pagina')



if __name__ == '__main__':
    app.run(debug=True)

