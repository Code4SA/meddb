from backend.models import *

countries = Country.query.all()
for country in countries:
    if country.code == "ZAF":
        country.default_fob_adjustment = 0.2
    else:
        country.default_fob_adjustment = 0.15
    db.session.add(country)
db.session.commit()

unknown_incoterm = Incoterm.query.filter(Incoterm.code=="UKN").one()

procurements = Procurement.query.all()
for procurement in procurements:
    if not procurement.incoterm:
        procurement.incoterm = unknown_incoterm
    if procurement.incoterm.code != "FOB":
        procurement.unit_price_usd_fob = procurement.unit_price_usd / (1.0 + procurement.country.default_fob_adjustment)
    else:
        procurement.unit_price_usd_fob = procurement.unit_price_usd
    db.session.add(procurement)


db.session.commit()