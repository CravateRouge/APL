from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
from gevent.select import select
from mimify import cte
from sqlalchemy.sql.expression import column
from mercurial.transaction import transaction

db = SqliteExtDatabase('apl.db')

class BaseModel(Model):
    class Meta:
        database = db
        
class Annonce(BaseModel):
    # id = "pap-123456789"
    id = CharField(primary_key=True)
    price = FloatField()
    surface = FloatField()
    postalCode = SmallIntegerField()
    transactionType = CharField()

class VilleCourtage(BaseModel):
    ville = Charfield(primary_key=True)
    departement = Charfield()
    rent = FloatField()
    purchase = FloatField()

def create_tables():
    with db:
        db.create_tables([Annonce,VilleCourtage])

def villeCourtage_init():
    rentCTE = (Annonce
                    .select(Annonce.city, fn.AVG(Annonce.price/Annonce.surface).alias('rent'))
                    .where(Annonce.type == 'rent')
                    .group_by(Annonce.city)
                    .cte('rentCTE'))
    
    buyCTE = (Annonce
                   .select(Annonce.city, fn.AVG(Annonce.price/Annonce.surface)/(20*12).alias('purchase'))
                   .where(Annonce.type == 'purchase')
                   .group_by(Annonce.city)
                   .cte('buyCTE'))
    
    data_source = (rentCTE
                   .select_from(rentCTE.c.city, rentCTE.c.rent, buyCTE.c.purchase)
                   .join(buyCTE)
                   .with_cte(rentCTE,buyCTE))
    
    VilleCourtage.insert_many(data_source).execute()
