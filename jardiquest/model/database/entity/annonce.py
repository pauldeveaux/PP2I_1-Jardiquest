from datetime import datetime
from jardiquest.setup_sql import db


class Annonce(db.Model):
    __tablename__ = "annonce"

    idAnnonce = db.Column(db.Integer, primary_key=True)
    timestamps = db.Column(db.Date())
    message = db.Column(db.String(1000), default="")

    idJardin = db.Column(db.String(10), db.ForeignKey("jardin.idJardin"))
    jardin = db.relationship("Jardin", back_populates="annonce")

    email = db.Column(db.String(100), db.ForeignKey("user.email"))
    user = db.relationship("User", back_populates="annonce")

    def get_id(self):
        return self.idAnnonce

    def __init__(self, idAnnonce, msg, user):
        self.idAnnonce = idAnnonce
        self.timestamps = datetime.utcnow()
        self.message = msg
        self.idJardin = user.idJardin
        self.email = user.email
