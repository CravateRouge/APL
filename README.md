# \#APL (Acheter Pour Louer)
_Un programme inspiré par [VikParuchuri/apartment-finder](https://github.com/VikParuchuri/apartment-finder) 
qui récupère les annonces immoblières de Leboncoin, Logic Immo, PaP et SeLoger pour les aggréger dans une base de données.

## Pré-requis
* Python 3
* [peewee](http://docs.peewee-orm.com/en/latest/)
* [Requests](https://requests.readthedocs.io/en/master/)
* [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [lxml](http://lxml.de/index.html)

### Paramètres de recherche
Les paramètres de recherce communs à tous les services sont dans le fichier 
`parameters.json` qu'il faut créer avant d'utiliser le programme :
```json
{
    "ad-providers": ["leboncoin", "logic-immo"],
    "cities":
    [
        ["Nanterre", 92000, 920050],
        ["Rueil-Malmaison", 92500, 920063]
    ],
    "price": [200, 900],
    "surface": [30, 70],
    "rooms": [2, 5],
    "bedrooms": [1, 2],

    "leboncoin": {
      "c": 10,
      "f": "p",
      "ret": [1, 2],
      "q": "terasse"
    },

    "seloger": {
      "idtt": 1,
      "idtypebien": "1,2",
      "getDtCreationMax": 1
    },
    
    "pap": {
        "recherche[produit]": "location",
        "recherche[typesbien][]": "appartement",
        "order": "date-desc"
    },
    
    "logic-immo": {
        "domain": "rentals",
        "order": "date-desc"
    }
}

```
Les paramètres sont donc :
 * `ad-providers` spécifie les fournisseurs d'annonces selectionnées : 
    * logic_immo : www.logic-immo.com
    * seloger : www.seloger.com
    * leboncoin : www.leboncoin.com
    * pap : www.pap.fr
 * `cities ` contient les villes, avec leur nom, code postal puis le code INSEE utilisé par SeLoger,
 * `price`, `surface`, `rooms` et `bedrooms`  sont donc respectivement le prix, la surface, le nombre de pièces et le 
 nombre de chambres avec les bornes minimales et maximales,
 * `leboncoin` contient les paramètres propres à LeBonCoin :
   * `c` représente la catégorie des annonces : 
     * `9` pour les ventes immobilières, 
     * `10` pour les locations,
     * `11` pour les collocations. 
   * `ret` permet de filtrer le type de bien : _(optionnel)_
     * `1` pour les maisons,
     * `2` pour les appartements,
     * `3` pour les terrains,
     * `4` pour les parkings,
     * `5` pour les autres.
   * `f` permet de filtrer le type d'annonceur : _(optionnel)_
     * `p` pour les particuliers
     * `c` pour les professionnels
   * `furn` permet de choisir si un bien est meublé `1` ou non `2`. _(optionnel)_
   * `q` représente le contenu du champ de recherche. _(optionnel)_
 * `seloger` contient les paramètres propres à SeLoger :
   * `idtt` représente la catégorie des annonces : 
     * `1` pour les locations,
     * `2` pour les ventes.
   * `idtypebien` représente le type de bien : _(optionnel)_
     * `1` pour les appartements,
     * `2` pour les maisons et villas,
     * `3` pour les parkings et boxs,
     * `4` pour les terrains,
     * `6` pour les boutiques,
     * `7` pour les locaux,
     * `8` pour les bureaux,
     * `9` pour les lofts et ateliers.
   * `getDtCreationMax=1` est requis par l'API.
 * `pap` contient les paramètres propres à PAP :
   * `recherche[produit]` permet de préciser si l'on cherche une `location` ou une `vente`,
   * `recherche[typesbien][]` permet de préciser le type de bien cherché.
   * `recherche[tags][]` permet de renseigner des critères avancés : _(optionnel)_
     * `meuble` et `vide`
     * `longue-duree` et `courte-duree`
     * `duplex-triplex`
     * `plain-pied` et `dernier-etage`
     * `piscine`
     * `balcon-terrasse`
     * `garages-parking`
     * `acces-handicape`
 * `logic-immo` contient les paramètres propres à Logic Immo :
   * `domain` permet de préciser si l'on cherche un bien en location (`rentals`) ou en vente (`sales`)
   

## Déploiement sur un Raspberry Pi
_Testé sur un Raspberry Pi sous Raspbian Jessie._

1. Installer `python3-pip` et `python3-lxml` (en plus de Python 3)
    ```
    sudo apt install python3-pip python3-lxml -y
    ```
2. Installer les dépendances
    ```
    sudo pip3 install peewee requests requests_oauthlib pytz python-dateutil beautifulsoup4
    ```
3. Clonner le projet
    ```
    git clone https://github.com/CravateRouge/APL.git
    ```
4. Créer les fichiers `parameters.json` comme indiqué plus haut
5. Créer une tâche `cron` pour lancer ce script régulièrement (dans mon cas toutes les 2h)
    ```
    crontab -e
    ```
    ```
    0 */2 * * * python3 /home/pi/APL/main.py
    ```
