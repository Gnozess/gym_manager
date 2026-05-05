from extensions import db
from datetime import datetime, date

class Abonnement(db.Model):
    __tablename__ = 'abonnements'

    id = db.Column(db.Integer, primary_key=True)
    membre_id = db.Column(db.Integer, db.ForeignKey('membres.id'), nullable=False)
    forfait_id = db.Column(db.Integer, db.ForeignKey('forfaits.id'), nullable=True)

    type_abonnement = db.Column(db.String(20), nullable=False)
    type_acces = db.Column(db.String(50), nullable=False)

    nombre_mois = db.Column(db.Integer, nullable=True)
    prix_mensuel = db.Column(db.Float, nullable=True)
    montant_brut = db.Column(db.Float, nullable=True)
    montant_total = db.Column(db.Float, nullable=False)

    date_debut = db.Column(db.Date, nullable=False)
    date_fin = db.Column(db.Date, nullable=False)
    date_annulation = db.Column(db.Date, nullable=True)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

    statut = db.Column(db.String(20), default='actif')

    paiements = db.relationship('Paiement', backref='abonnement', lazy=True)

    @property
    def montant_paye(self):
        return sum(p.montant for p in self.paiements)

    @property
    def reste_a_payer(self):
        return self.montant_total - self.montant_paye

    @property
    def est_solde(self):
        return self.reste_a_payer <= 0

    @property
    def jours_restants(self):
        delta = self.date_fin - date.today()
        return delta.days

    @property
    def jours_totaux(self):
        delta = self.date_fin - self.date_debut
        return delta.days

    @property
    def est_expire(self):
        return self.date_fin < date.today()

    @property
    def expire_bientot(self):
        return 0 <= self.jours_restants <= 7

    @property
    def montant_remboursement(self):
        return self.montant_paye

    def __repr__(self):
        return f'<Abonnement {self.type_abonnement} - Membre {self.membre_id}>'