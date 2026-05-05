from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import date

scheduler = BlockingScheduler()

def envoyer_alertes_expiration():
    from app import create_app
    from models.abonnement import Abonnement
    from services.sms import sms_expiration

    app = create_app()
    with app.app_context():
        aujourd_hui = date.today()
        dans_7_jours = date.fromordinal(aujourd_hui.toordinal() + 7)

        abonnements = Abonnement.query.filter(
            Abonnement.statut == 'actif',
            Abonnement.date_fin == dans_7_jours
        ).all()

        print(f'[SCHEDULER] {len(abonnements)} abonnement(s) expirant dans 7 jours.')

        for ab in abonnements:
            membre = ab.membre
            forfait_nom = ab.forfait.nom if ab.forfait else 'Forfait'
            resultat = sms_expiration(
                membre,
                forfait_nom,
                ab.date_fin,
                ab.jours_restants
            )
            if resultat:
                print(f'SMS expiration envoye a {membre.prenom} {membre.nom}')
            else:
                print(f'Echec SMS pour {membre.prenom} {membre.nom}')

# Enregistrer la tâche correctement
scheduler.add_job(
    envoyer_alertes_expiration,
    trigger='cron',
    hour=8,
    minute=0,
    id='alertes_expiration'
)

if __name__ == '__main__':
    print('[SCHEDULER] Demarrage du planificateur...')
    print('[SCHEDULER] Alertes SMS programmees chaque jour a 08h00.')
    scheduler.start()