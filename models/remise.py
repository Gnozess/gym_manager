from extensions import db
from datetime import datetime

class Remise(db.Model):
    __tablename__ = 'remises'

    id = db.Column(db.Integer, primary_key=True)
    abonnement_id = db.Column(db.Integer, db.ForeignKey('abonnements.id'), nullable=False)
    pourcentage = db.Column(db.Float, nullable=False)
    montant_remise = db.Column(db.Float, nullable=False)
    motif = db.Column(db.String(255))
    date_remise = db.Column(db.DateTime, default=datetime.utcnow)

    abonnement = db.relationship('Abonnement', backref='remise', lazy=True)

    def __repr__(self):
        return f'<Remise {self.pourcentage}% - {self.montant_remise} FCFA>'