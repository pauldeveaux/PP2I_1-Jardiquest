from jardiquest.setup_sql import db


class Jardin(db.Model):
    __tablename__ = "jardin"

    idJardin = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    moneyName = db.Column(db.String(100), default="Monnaie")
    description = db.Column(db.String(200), default="Un jardin bien sympa !")
    ville = db.Column(db.String(100), default="")
    adresse = db.Column(db.String(100), default="")
    nbParticipants = db.Column(db.Integer, default=0)

    recolte = db.relationship("Recolte", back_populates="jardin")
    annonce = db.relationship("Annonce", back_populates="jardin", uselist=False)
    user = db.relationship("User", back_populates="jardin")

    def get_id(self):
        return self.idCatalogue

    def update_name(self, new_name):
        self.name = new_name
    
    def update_money(self, new_money):
        self.moneyName = new_money

    def update_description(self, new_description):
        self.description = new_description

    def update_address(self, new_address):
        self.adresse = new_address
    
    def update_city(self, new_city):
        self.ville = new_city

    def update_nbParticipants(self, nb):
        self.nbParticipants = int(nb)