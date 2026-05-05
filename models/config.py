from extensions import db

class Config(db.Model):
    __tablename__ = 'config'

    id = db.Column(db.Integer, primary_key=True)
    cle = db.Column(db.String(100), unique=True, nullable=False)
    valeur = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))

    @staticmethod
    def get(cle, defaut=0):
        config = Config.query.filter_by(cle=cle).first()
        return config.valeur if config else defaut

    @staticmethod
    def set(cle, valeur):
        config = Config.query.filter_by(cle=cle).first()
        if config:
            config.valeur = valeur
        else:
            config = Config(cle=cle, valeur=valeur)
            db.session.add(config)
        db.session.commit()