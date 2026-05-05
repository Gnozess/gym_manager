import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'changez-cette-cle'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///gym.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Render utilise postgres:// mais SQLAlchemy necessite postgresql://
    @staticmethod
    def init_app(app):
        db_url = os.environ.get('DATABASE_URL', '')
        if db_url.startswith('postgres://'):
            os.environ['DATABASE_URL'] = db_url.replace(
                'postgres://', 'postgresql://', 1
            )