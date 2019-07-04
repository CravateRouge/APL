import requests,re,json
from models import Annonce
from datetime import datetime
'''Module qui récupère les annonces de SeLoger.com'''

def addAnnonces(annonces):
    if annonces['products'] == []:
        return False 
    
    for annonce in annonces['products']:
        dbAnnonce, created = Annonce.create_or_get(
                id='seloger-' + annonce['idannonce'],
                price=annonce['prix'],
                surface=annonce['surface'],
                postalCode=annonce['codepostal'],
                transactionType=annonce['typedetransaction'][0]
            )
     
        if created:
            dbAnnonce.save()

    return True

def search(parameters):
    # Cherche tous les biens en IDF pour la vente
    cpt = 1
    while cpt != -1:
        request = requests.get("http://www.seloger.com/list.htm?types=1,2&enterprise=0&places=[{div:2238}]&qsVersion=1.0&LISTING-LISTpg="+cpt+parameters)
        annonces = json.loads(re.search("var ava_data =(.*)?;", request.text).group(1))
        
        cpt += 1
        if addAnnonces(annonces) == False:
            cpt = -1

def searchRentAndPurchase():
    #Pour achat
    search("&projects=2&natures=1,2")
    #Pour la loc
    search("&projects=1")
         
#     # Préparation des paramètres de la requête
#     payload = {
#         'px_loyermin': parameters['price'][0],
#         'px_loyermax': parameters['price'][1],
#         'surfacemin': parameters['surface'][0],
#         'surfacemax': parameters['surface'][1],
#         # Si parameters['rooms'] = (2, 4) => "2,3,4"
#         'nbpieces': list(range(parameters['rooms'][0], parameters['rooms'][1] + 1)),
#         # Si parameters['bedrooms'] = (2, 4) => "2,3,4"
#         'nb_chambres': list(range(parameters['bedrooms'][0], parameters['bedrooms'][1] + 1)),
#         'ci': [int(cp[2]) for cp in parameters['cities']]
#     }
#     # Insertion des paramètres propres à LeBonCoin
#     payload.update(parameters['seloger'])
# 
#     headers = {'user-agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; D5803 Build/MOB30M.Z1)'}
# 
#     request = requests.get("http://ws.seloger.com/search_4.0.xml", params=payload, headers=headers)
# 
#     xml_root = ET.fromstring(request.text)
# 
#     for annonceNode in xml_root.findall('annonces/annonce'):
#         # Seconde requête pour obtenir la description de l'annonce
#         _payload = {'noAudiotel': 1, 'idAnnonce': annonceNode.findtext('idAnnonce')}
#         _request = requests.get("http://ws.seloger.com/annonceDetail_4.0.xml", params=_payload, headers=headers)
# 
#         annonce, created = Annonce.create_or_get(
#             id='seloger-' + annonceNode.find('idAnnonce').text,
#             site='SeLoger',
#             # SeLoger peut ne pas fournir de titre pour une annonce T_T
#             title="Appartement " + annonceNode.findtext('nbPiece') + " pièces" if annonceNode.findtext('titre') is None else annonceNode.findtext('titre'),
#             description=ET.fromstring(_request.text).findtext("descriptif"),
#             telephone=ET.fromstring(_request.text).findtext("contact/telephone"),
#             created=datetime.strptime(annonceNode.findtext('dtCreation'), '%Y-%m-%dT%H:%M:%S'),
#             price=annonceNode.find('prix').text,
#             charges=annonceNode.find('charges').text,
#             surface=annonceNode.find('surface').text,
#             rooms=annonceNode.find('nbPiece').text,
#             bedrooms=annonceNode.find('nbChambre').text,
#             city=annonceNode.findtext('ville'),
#             link=annonceNode.findtext('permaLien'),
#         )
# 
#         if created:
#             annonce.save()
