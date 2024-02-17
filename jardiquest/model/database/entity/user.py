from datetime import date

from werkzeug.security import generate_password_hash

from jardiquest.setup_sql import db

import re

regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')


class User(db.Model):
    __tablename__ = "user"

    email = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(1000), nullable=False)
    role = db.Column(db.String(15), default="Participant")
    balance = db.Column(db.Float(), default=0.00)
    recruitmentDate = db.Column(db.Date())

    idJardin = db.Column(db.String(10), db.ForeignKey("jardin.idJardin"), default="")

    jardin = db.relationship("Jardin", back_populates="user")
    annonce = db.relationship("Annonce", back_populates="user")
    quetes = db.relationship("Quete", back_populates="user")

    def __init__(self, email, password, name):
        self.email = email
        self.password = generate_password_hash(password, method='sha256')
        self.name = name
        self.recruitmentDate = date.today()

    def update_password(self, new_password):
        self.password = generate_password_hash(new_password, method='sha256')

    def get_id(self):
        return self.email

    # return if the user as valid data or else the error message
    # use password not encoded because the sha256 algorithm will mess with the test of minimal len
    @staticmethod
    def is_valid_commit(email, name, password_not_encoded) -> (bool or str):
        rep = User.is_valid_commit_email_name(email, name)
        if type(rep) is not bool:
            return rep

        if password_not_encoded is None:
            return "Veuillez utiliser un mot de passe"
        if len(password_not_encoded) < 8:
            return "Veuillez utiliser un mot de passe avec au moins 8 caractères"
        return True

    @staticmethod
    def is_valid_commit_email_name(email, name) -> (bool or str):
        if email is None:
            return "Veuillez utiliser une adresse mail"
        if not re.fullmatch(regex, email):
            return "Veuillez utiliser une adresse mail valide"
        if name == '' or name is None:
            return "Veuillez utiliser un nom"
        return True

    @staticmethod
    def is_active():
        return False

    @staticmethod
    def is_authenticated():
        return True

    def update_garden(self, new_garden):
        self.idJardin = new_garden
    
    def update_role(self, new_role):
        self.role = new_role
    
    def update_balance(self, new_amount):
        self.balance = new_amount