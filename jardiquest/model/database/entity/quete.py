from jardiquest.setup_sql import db
from datetime import date, timedelta
import uuid

class Quete(db.Model):
    __tablename__ = "quete"

    idQuete = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), default="")
    periodicity = db.Column(db.Boolean, default=False)
    reward = db.Column(db.Float(), default=0.00)
    estimatedTime = db.Column(db.Integer)
    startingDate = db.Column(db.Date())
    timeBeforeExpiration = db.Column(db.Integer, nullable=False)
    accomplished = db.Column(db.Boolean(), default=False)

    id_jardin = db.Column(db.String(10), db.ForeignKey("jardin.idJardin"), nullable=False)
    id_user = db.Column(db.String(100), db.ForeignKey("user.email"))

    user = db.relationship("User", back_populates="quetes")
   
    
    
    def get_id(self):
        return self.idQuete


def update_quests(app):
    with app.app_context():
        quests = Quete.query.all()
        for quest in quests:
            if quest.startingDate and (date.today() - quest.startingDate).days > quest.timeBeforeExpiration:
                # If the quest is expired
                if quest.periodicity :
                    # If the quest is periodic, we create a new one
                    new_quest = Quete(idQuete= uuid.uuid1().hex, title = quest.title, description = quest.description, periodicity = True, 
                                    timeBeforeExpiration = quest.timeBeforeExpiration, reward = quest.reward, id_jardin = quest.id_jardin, 
                                    accomplished = False, startingDate = quest.startingDate + timedelta(days=quest.timeBeforeExpiration))
                    db.session.add(new_quest)
                else:
                    # If the quest is not periodic, we delete it
                    db.session.delete(quest)
        print("update")
        db.session.commit()    