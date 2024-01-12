class students:
    def __init__(self, matricola, email, password, online='N'):
        self.matricola = matricola
        self.email = email
        self.password = password
        self.online = online

    def __repr__(self):
        return f"Studente(matricola={self.matricola}, email={self.email}, online={self.online})"
