from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db

class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='secretaire')
    actif = db.Column(db.Boolean, default=True)
    membre_id = db.Column(db.Integer, db.ForeignKey('membres.id'), nullable=True)

    ROLES = {
        'admin': 'Administrateur',
        'secretaire': 'Secretaire',
        'membre': 'Membre'
    }

    def set_password(self, mot_de_passe):
        self.mot_de_passe = generate_password_hash(mot_de_passe)

    def check_password(self, mot_de_passe):
        return check_password_hash(self.mot_de_passe, mot_de_passe)

    @property
    def role_label(self):
        return self.ROLES.get(self.role, self.role)

    @property
    def est_admin(self):
        return self.role == 'admin'

    @property
    def est_secretaire(self):
        return self.role == 'secretaire'

    @property
    def est_membre(self):
        return self.role == 'membre'