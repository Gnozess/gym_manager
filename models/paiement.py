from extensions import db
from datetime import datetime

class Paiement(db.Model):
    __tablename__ = 'paiements'

    id = db.Column(db.Integer, primary_key=True)
    abonnement_id = db.Column(db.Integer, db.ForeignKey('abonnements.id'), nullable=False)
    montant = db.Column(db.Float, nullable=False)
    mode_paiement = db.Column(db.String(50), nullable=False, default='especes')
    numero_mobile = db.Column(db.String(20), nullable=True)
    reference_transaction = db.Column(db.String(100), nullable=True)
    date_paiement = db.Column(db.DateTime, default=datetime.utcnow)
    note = db.Column(db.String(255))

    MODES = {
        'especes': 'Especes',
        'orange_money': 'OrangeMoney',
        'mobi_cash': 'MobiCash',
        'sank_money': 'SankMoney',
        'telecel_money': 'TelecelMoney'
    }

    @property
    def mode_label(self):
        return self.MODES.get(self.mode_paiement, self.mode_paiement)

    def __repr__(self):
        return f'<Paiement {self.montant} FCFA - {self.mode_paiement}>'