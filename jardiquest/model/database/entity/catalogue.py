from jardiquest.setup_sql import db


class Catalogue(db.Model):
    __tablename__ = "catalogue"

    idCatalogue = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), default="")
    imagePath = db.Column(db.String(100), default="")
    image_source = db.Column(db.String(100), default="")
    description_source = db.Column(db.String(100), default="")
    
    recolte = db.relationship("Recolte", back_populates="catalogue")

    def get_id(self):
        return self.idCatalogue
