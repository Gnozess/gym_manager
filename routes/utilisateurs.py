from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from extensions import db
from models.admin import Admin
from models.membre import Membre
from werkzeug.security import generate_password_hash

utilisateurs_bp = Blueprint('utilisateurs', __name__)

ROLES = [
    ('admin', 'Administrateur'),
    ('secretaire', 'Secretaire'),
    ('membre', 'Membre'),
]


def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.est_admin:
            flash('Acces reserve aux administrateurs.', 'danger')
            return redirect(url_for('membres.dashboard'))
        return f(*args, **kwargs)
    return decorated_function


@utilisateurs_bp.route('/utilisateurs')
@login_required
@admin_required
def liste():
    utilisateurs = Admin.query.order_by(Admin.role).all()
    membres_sans_compte = Membre.query.filter(
        ~Membre.id.in_(
            db.session.query(Admin.membre_id).filter(Admin.membre_id != None)
        )
    ).all()
    return render_template('utilisateurs/liste.html',
        utilisateurs=utilisateurs,
        membres_sans_compte=membres_sans_compte,
        roles=ROLES
    )


@utilisateurs_bp.route('/utilisateurs/ajouter', methods=['POST'])
@login_required
@admin_required
def ajouter():
    nom = request.form.get('nom')
    email = request.form.get('email')
    mot_de_passe = request.form.get('mot_de_passe')
    role = request.form.get('role')
    membre_id = request.form.get('membre_id') or None

    if Admin.query.filter_by(email=email).first():
        flash('Un utilisateur avec cet email existe deja.', 'danger')
        return redirect(url_for('utilisateurs.liste'))

    utilisateur = Admin(
        nom=nom,
        email=email,
        role=role,
        actif=True,
        membre_id=int(membre_id) if membre_id else None
    )
    utilisateur.set_password(mot_de_passe)
    db.session.add(utilisateur)
    db.session.commit()
    flash(f'Utilisateur {nom} cree avec succes !', 'success')
    return redirect(url_for('utilisateurs.liste'))


@utilisateurs_bp.route('/utilisateurs/modifier/<int:id>', methods=['POST'])
@login_required
@admin_required
def modifier(id):
    utilisateur = Admin.query.get_or_404(id)

    if utilisateur.id == current_user.id:
        flash('Vous ne pouvez pas modifier votre propre compte ici.', 'danger')
        return redirect(url_for('utilisateurs.liste'))

    utilisateur.nom = request.form.get('nom')
    utilisateur.email = request.form.get('email')
    utilisateur.role = request.form.get('role')
    utilisateur.actif = request.form.get('actif') == 'on'
    membre_id = request.form.get('membre_id') or None
    utilisateur.membre_id = int(membre_id) if membre_id else None

    nouveau_mdp = request.form.get('mot_de_passe')
    if nouveau_mdp:
        utilisateur.set_password(nouveau_mdp)

    db.session.commit()
    flash(f'Utilisateur {utilisateur.nom} modifie avec succes !', 'success')
    return redirect(url_for('utilisateurs.liste'))


@utilisateurs_bp.route('/utilisateurs/supprimer/<int:id>', methods=['POST'])
@login_required
@admin_required
def supprimer(id):
    utilisateur = Admin.query.get_or_404(id)

    if utilisateur.id == current_user.id:
        flash('Vous ne pouvez pas supprimer votre propre compte.', 'danger')
        return redirect(url_for('utilisateurs.liste'))

    db.session.delete(utilisateur)
    db.session.commit()
    flash(f'Utilisateur {utilisateur.nom} supprime.', 'warning')
    return redirect(url_for('utilisateurs.liste'))