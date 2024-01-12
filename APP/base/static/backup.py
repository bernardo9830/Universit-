import subprocess
import datetime
import shlex

dati_db = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Mysql',
    'database': 'university'
}

timestamp = datetime.datetime.now()
dump_file = f'dump_{timestamp.strftime("%Y%m%d_%H%M%S")}.sql'

# Costruisci il comando senza la password sulla riga di comando
dump_command = f'mysqldump -h {dati_db["host"]} -u {dati_db["user"]} -p{dati_db["password"]} {dati_db["database"]}'

# Separa correttamente gli argomenti del comando
args = shlex.split(dump_command)

# Esegui il comando in modo interattivo
with open(dump_file, 'w') as output_file:
    subprocess.run(args, input=f"{dati_db['password']}\n", text=True, stdout=output_file)
