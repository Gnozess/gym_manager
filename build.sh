#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python -c "
from app import create_app
from extensions import db
from models.admin import Admin
from models.config import Config

app = create_app()
with app.app_context():
    db.create_all()

    if not Admin.query.filter_by(email='admin@gym.com').first():
        admin = Admin(nom='Administrateur', email='admin@gym.com', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print('Admin cree')

    if not Config.query.filter_by(cle='journalier_simple').first():
        db.session.add(Config(cle='journalier_simple', valeur=2000, description='Prix journalier salle ou fitness'))
    if not Config.query.filter_by(cle='journalier_complet').first():
        db.session.add(Config(cle='journalier_complet', valeur=3000, description='Prix journalier salle + fitness'))
    db.session.commit()
    print('Configuration initialisee')
"