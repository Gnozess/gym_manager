from extensions import db
from datetime import datetime

class Caisse(db.Model):
    __tablename__ = 'caisse'

    id = db.Column(db.Integer, primary_key=True)
    type_operation = db.Column(db.String(20), nullable=False)  # entree / sortie
    montant = db.Column(db.Float, nullable=False)
    motif = db.Column(db.String(255), nullable=False)
    mode_paiement = db.Column(db.String(50), nullable=True)
    date_operation = db.Column(db.DateTime, default=datetime.utcnow)
    abonnement_id = db.Column(db.Integer, db.ForeignKey('abonnements.id'), nullable=True)
    membre_id = db.Column(db.Integer, db.ForeignKey('membres.id'), nullable=True)

    abonnement = db.relationship('Abonnement', backref='operations_caisse', lazy=True)
    membre = db.relationship('Membre', backref='operations_caisse', lazy=True)

    MODES = {
        'especes': 'Especes',
        'orange_money': 'OrangeMoney',
        'mobi_cash': 'MobiCash',
        'sank_money': 'SankMoney',
        'telecel_money': 'TelecelMoney'
    }

    @property
    def mode_label(self):
        return self.MODES.get(self.mode_paiement, '—')

    def __repr__(self):
        return f'<Caisse {self.type_operation} {self.montant} FCFA>'