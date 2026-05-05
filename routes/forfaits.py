from flask import Blueprint, render_template, redirect, url_for, flash, request
from utils.decorateurs import admin_required
from flask_login import login_required
from extensions import db
from models.forfait import Forfait
from models.config import Config

forfaits_bp = Blueprint('forfaits', __name__)

@forfaits_bp.route('/forfaits')
@login_required
def liste():
    forfaits = Forfait.query.filter_by(actif=True).all()
    prix_journalier_simple = Config.get('journalier_simple', 2000)
    prix_journalier_complet = Config.get('journalier_complet', 3000)
    return render_template('forfaits/liste.html',
        forfaits=forfaits,
        prix_journalier_simple=prix_journalier_simple,
        prix_journalier_complet=prix_journalier_complet
    )

@forfaits_bp.route('/forfaits/ajouter', methods=['GET', 'POST'])
@login_required
@admin_required
def ajouter():
    if request.method == 'POST':
        nom = request.form.get('nom')
        type_acces = request.form.get('type_acces')
        prix_mensuel = float(request.form.get('prix_mensuel'))
        description = request.form.get('description')

        forfait = Forfait(
            nom=nom,
            type_acces=type_acces,
            prix_mensuel=prix_mensuel,
            description=description
        )
        db.session.add(forfait)
        db.session.commit()
        flash(f'Forfait "{nom}" créé avec succès !', 'success')
        return redirect(url_for('forfaits.liste'))

    return render_template('forfaits/ajouter.html')

@forfaits_bp.route('/forfaits/modifier/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def modifier(id):
    forfait = Forfait.query.get_or_404(id)

    if request.method == 'POST':
        forfait.nom = request.form.get('nom')
        forfait.type_acces = request.form.get('type_acces')
        forfait.prix_mensuel = float(request.form.get('prix_mensuel'))
        forfait.description = request.form.get('description')
        db.session.commit()
        flash(f'Forfait "{forfait.nom}" modifié avec succès !', 'success')
        return redirect(url_for('forfaits.liste'))

    return render_template('forfaits/modifier.html', forfait=forfait)

@forfaits_bp.route('/forfaits/supprimer/<int:id>', methods=['POST'])
@login_required
@admin_required
def supprimer(id):
    forfait = Forfait.query.get_or_404(id)
    forfait.actif = False
    db.session.commit()
    flash(f'Forfait "{forfait.nom}" supprimé.', 'warning')
    return redirect(url_for('forfaits.liste'))

@forfaits_bp.route('/forfaits/config-journalier', methods=['POST'])
@login_required
@admin_required
def config_journalier():
    prix_simple = float(request.form.get('journalier_simple'))
    prix_complet = float(request.form.get('journalier_complet'))
    Config.set('journalier_simple', prix_simple)
    Config.set('journalier_complet', prix_complet)
    flash('Prix journaliers mis à jour !', 'success')
    return redirect(url_for('forfaits.liste'))