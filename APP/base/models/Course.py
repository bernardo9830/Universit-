class Corso:
    def __init__(self, codice, nome, descrizione):
        self.codice=codice
        self.nome = nome
        self.descrizione = descrizione
        self.studenti_iscritti=[]
    def iscrivi_studente(self,matricola):
        self.studenti_iscritti.append(matricola)


    def get_info(self):
        return f"Corso: {self.nome}, Codice: {self.codice}, Descrizione: {self.descrizione}"
