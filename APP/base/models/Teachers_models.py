class Teachers:
    def __init__(self, nome, cognome, email_istituzionale, password):
        self.nome = nome
        self.cognome = cognome
        self.password = password
        self.email_istituzionale = email_istituzionale

    def __repr__(self):
        return f"Teacher(nome={self.nome}, email={self.email_istituzionale})"
