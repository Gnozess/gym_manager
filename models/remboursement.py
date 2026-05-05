from extensions import db
from datetime import datetime

class Remboursement(db.Model):
    __tablename__ = 'remboursements'

    id = db.Column(db.Integer, primary_key=True)
    abonnement_id = db.Column(db.Integer, db.ForeignKey('abonnements.id'), nullable=False)
    montant_rembourse = db.Column(db.Float, nullable=False)
    date_remboursement = db.Column(db.DateTime, default=datetime.utcnow)
    motif = db.Column(db.String(255), default='Annulation abonnement')

    abonnement = db.relationship('Abonnement', backref='remboursement', lazy=True)

    def __repr__(self):
        return f'<Remboursement {self.montant_rembourse} FCFA>'