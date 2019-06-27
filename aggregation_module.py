import json
from models import Annonce
from ast import literal_eval

def post():
    '''
    Poste les annonces sur Trello
    '''
    posted = 0

    for annonce in Annonce.select().where(Annonce.posted2trello == False).order_by(Annonce.site.asc()):
        title = "%s de %sm² à %s @ %s€" % (annonce.title, annonce.surface, annonce.city, annonce.price)
        description = "Créé le : %s\n\n" \
                      "%s pièces, %s chambre(s)\n" \
                      "Charges : %s\n" \
                      "Tel : %s\n\n" % \
                      (annonce.created.strftime("%a %d %b %Y %H:%M:%S"), annonce.rooms, annonce.bedrooms, annonce.charges,
                       annonce.telephone)
        if annonce.description is not None:
            description += ">%s" % annonce.description.replace("\n", "\n>")

        card = get_list(annonce.site).add_card(title, desc=description)

        # On s'assure que ce soit bien un tableau
        if annonce.picture is not None and annonce.picture.startswith("["):
            # Conversion de la chaîne de caractère représentant le tableau d'images en tableau
            for picture in literal_eval(annonce.picture):
                card.attach(url=picture)
            # Il n'y a qu'une photo
        elif annonce.picture is not None and annonce.picture.startswith("http"):
            card.attach(url=annonce.picture)

        card.attach(url=annonce.link)

        annonce.posted2trello = True
        annonce.save()
        posted += 1
    return posted
