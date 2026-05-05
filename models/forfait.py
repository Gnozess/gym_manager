from extensions import db

class Forfait(db.Model):
    __tablename__ = 'forfaits'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    type_acces = db.Column(db.String(50), nullable=False)  # salle, fitness, salle+fitness
    prix_mensuel = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))
    actif = db.Column(db.Boolean, default=True)

    # Relation avec les abonnements
    abonnements = db.relationship('Abonnement', backref='forfait', lazy=True)

    def __repr__(self):
        return f'<Forfait {self.nom}>'