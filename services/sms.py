import requests

AQILAS_TOKEN = '3e637b36-2afc-48ed-aba3-1336ca50e6a2'
AQILAS_URL = 'https://www.aqilas.com/api/v1'
FROM = 'CF-RAGUILIO'


def envoyer_sms(numero, message):
    try:
        # Formater le numéro en international
        numero = numero.strip().replace(' ', '')
        if not numero.startswith('+'):
            numero = '+226' + numero

        response = requests.post(
            f'{AQILAS_URL}/sms',
            headers={'X-AUTH-TOKEN': AQILAS_TOKEN},
            json={
                'from': FROM,
                'text': message,
                'to': [numero]
            },
            timeout=10
        )
        data = response.json()
        if data.get('success'):
            print(f'SMS envoye a {numero} : {data}')
            return True
        else:
            print(f'Erreur SMS : {data}')
            return False
    except Exception as e:
        print(f'Exception SMS : {e}')
        return False


def get_credit():
    try:
        response = requests.get(
            f'{AQILAS_URL}/credit',
            headers={'X-AUTH-TOKEN': AQILAS_TOKEN},
            timeout=10
        )
        data = response.json()
        if data.get('success'):
            return data.get('credit', 0)
        return 0
    except Exception as e:
        print(f'Exception credit : {e}')
        return 0


def sms_paiement(membre, montant, forfait_nom, reste_a_payer):
    if not membre.telephone:
        return False
    message = (
        f"M./Mme {membre.nom}, "
        f"votre paiement de {int(montant):,} FCFA a ete enregistre "
        f"pour votre abonnement {forfait_nom}. "
        f"Reste a payer : {int(reste_a_payer):,} FCFA. "
        f"Merci !"
    )
    return envoyer_sms(membre.telephone, message)


def sms_paiement_journalier(membre, montant, type_acces):
    if not membre.telephone:
        return False
    message = (
        f"M./Mme {membre.nom}, "
        f"votre abonnement journalier ({type_acces}) "
        f"de {int(montant):,} FCFA a ete enregistre. "
        f"Bonne seance ! "
        f"CF-Raguilio."
    )
    return envoyer_sms(membre.telephone, message)


def sms_expiration(membre, forfait_nom, date_fin, jours_restants):
    if not membre.telephone:
        return False
    message = (
        f"M./Mme {membre.nom}, "
        f"votre abonnement {forfait_nom} expire "
        f"dans {jours_restants} jours "
        f"(le {date_fin.strftime('%d/%m/%Y')}). "
        f"CF-Raguilio."
    )
    return envoyer_sms(membre.telephone, message)

def sms_annulation(membre, forfait_nom, montant_rembourse):
    if not membre.telephone:
        return False
    message = (
        f"M./Mme {membre.nom}, "
        f"votre abonnement {forfait_nom} a ete annule. "
        f"Remboursement de {int(montant_rembourse):,} FCFA "
        f"a la caisse. "
        f"CF-Raguilio."
    )
    return envoyer_sms(membre.telephone, message)