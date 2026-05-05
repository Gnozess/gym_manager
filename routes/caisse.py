from flask import Blueprint, render_template, request
from utils.decorateurs import admin_required
from flask_login import login_required
from models.caisse import Caisse
from datetime import date, datetime
from extensions import db
from services.sms import get_credit

caisse_bp = Blueprint('caisse', __name__)

MODES = {
    'especes': 'Especes',
    'orange_money': 'OrangeMoney',
    'mobi_cash': 'MobiCash',
    'sank_money': 'SankMoney',
    'telecel_money': 'TelecelMoney'
}


@caisse_bp.route('/caisse')
@login_required
@admin_required
@login_required
def index():
    periode = request.args.get('periode', 'jour')
    date_debut_custom = request.args.get('date_debut', '')
    date_fin_custom = request.args.get('date_fin', '')
    aujourd_hui = date.today()

    if periode == 'jour':
        date_debut = datetime.combine(aujourd_hui, datetime.min.time())
        date_fin = datetime.combine(aujourd_hui, datetime.max.time())
        titre_periode = "Aujourd'hui"
    elif periode == 'mois':
        date_debut = datetime(aujourd_hui.year, aujourd_hui.month, 1)
        date_fin = datetime.combine(aujourd_hui, datetime.max.time())
        titre_periode = aujourd_hui.strftime('%B %Y')
    elif periode == 'annee':
        date_debut = datetime(aujourd_hui.year, 1, 1)
        date_fin = datetime.combine(aujourd_hui, datetime.max.time())
        titre_periode = str(aujourd_hui.year)
    elif periode == 'custom' and date_debut_custom and date_fin_custom:
        date_debut = datetime.strptime(date_debut_custom, '%Y-%m-%d')
        date_fin = datetime.strptime(date_fin_custom, '%Y-%m-%d')
        date_fin = datetime.combine(date_fin.date(), datetime.max.time())
        titre_periode = (
            f"{date_debut.strftime('%d/%m/%Y')} au "
            f"{date_fin.strftime('%d/%m/%Y')}"
        )
    else:
        date_debut = datetime.combine(aujourd_hui, datetime.min.time())
        date_fin = datetime.combine(aujourd_hui, datetime.max.time())
        titre_periode = "Aujourd'hui"

    operations = Caisse.query.filter(
        Caisse.date_operation >= date_debut,
        Caisse.date_operation <= date_fin
    ).order_by(Caisse.date_operation.desc()).all()

    total_entrees = sum(o.montant for o in operations if o.type_operation == 'entree')
    total_sorties = sum(o.montant for o in operations if o.type_operation == 'sortie')
    solde_periode = total_entrees - total_sorties

    # Solde global toutes periodes
    total_caisse_entrees = db.session.query(
        db.func.sum(Caisse.montant)
    ).filter(Caisse.type_operation == 'entree').scalar() or 0

    total_caisse_sorties = db.session.query(
        db.func.sum(Caisse.montant)
    ).filter(Caisse.type_operation == 'sortie').scalar() or 0

    solde_global = total_caisse_entrees - total_caisse_sorties

    # Soldes par mode de paiement (entrees - sorties, afficher uniquement si positif)
    soldes_modes = {}
    for mode, label in MODES.items():
        total_entrees_mode = db.session.query(
            db.func.sum(Caisse.montant)
        ).filter(
            Caisse.type_operation == 'entree',
            Caisse.mode_paiement == mode
        ).scalar() or 0

        total_sorties_mode = db.session.query(
            db.func.sum(Caisse.montant)
        ).filter(
            Caisse.type_operation == 'sortie',
            Caisse.mode_paiement == mode
        ).scalar() or 0

        solde_mode = total_entrees_mode - total_sorties_mode

        if solde_mode > 0:
            soldes_modes[label] = solde_mode
    credit_sms = get_credit()
    return render_template('caisse/index.html',
        operations=operations,
        total_entrees=total_entrees,
        total_sorties=total_sorties,
        solde_periode=solde_periode,
        solde_global=solde_global,
        soldes_modes=soldes_modes,
        periode=periode,
        titre_periode=titre_periode,
        date_debut_custom=date_debut_custom,
        date_fin_custom=date_fin_custom,
        credit_sms=credit_sms,
        aujourd_hui=aujourd_hui.isoformat()
    )
    