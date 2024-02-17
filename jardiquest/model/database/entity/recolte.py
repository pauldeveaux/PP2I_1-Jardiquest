from jardiquest.setup_sql import db


class Recolte(db.Model):
    __tablename__ = "recolte"

    idRecolte = db.Column(db.String(10), primary_key=True)
    quantity = db.Column(db.Float(), nullable=False)
    date = db.Column(db.Date())
    cost = db.Column(db.Float(), default=0.00)
    qtt_recommandee = db.Column(db.Float(), default=1.00)
    
    idCatalogue = db.Column(db.String(10), db.ForeignKey("catalogue.idCatalogue"))
    catalogue = db.relationship("Catalogue", back_populates="recolte")

    idJardin = db.Column(db.String(10), db.ForeignKey("jardin.idJardin"))
    jardin = db.relationship("Jardin", back_populates="recolte")

    commande = db.relationship("Commande", back_populates="recolte")

    def get_id(self):
        return self.idRecolte
