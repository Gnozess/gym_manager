from extensions import db
from datetime import datetime, date

class Membre(db.Model):
    __tablename__ = 'membres'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80), nullable=False)
    prenom = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telephone = db.Column(db.String(20), unique=True, nullable=True)
    date_inscription = db.Column(db.DateTime, default=datetime.utcnow)
    actif = db.Column(db.Boolean, default=True)

    abonnements = db.relationship('Abonnement', backref='membre', lazy=True)

    @property
    def abonnement_actif(self):
        from models.abonnement import Abonnement
        return Abonnement.query.filter_by(
            membre_id=self.id,
            statut='actif'
        ).filter(Abonnement.date_fin >= date.today()).first()

    @property
    def statut_abonnement(self):
        from models.abonnement import Abonnement
        ab = self.abonnement_actif
        if not ab:
            dernier = Abonnement.query.filter_by(
                membre_id=self.id
            ).order_by(Abonnement.date_fin.desc()).first()
            if dernier and dernier.est_expire:
                return 'expire'
            return 'aucun'
        if ab.expire_bientot:
            return 'bientot'
        return 'actif'