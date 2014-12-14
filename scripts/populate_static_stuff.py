from backend.models import *

countries = Country.query.all()

registers = [
    ("Angola", "No regulatory authority", None),
    ("Botswana", "Register", "/static/docs/Botswana%20-%20Blue%20Book.pdf"),
    ("DRC", "Not yet available", None),
    ("Lesotho", "No regulatory authority", None),
    ("Madagascar", "Not yet available", None),
    ("Malawi", "Not yet available", None),
    ("Mauritius", "Not yet available", None),
    ("Mozambique", "Not yet available", None),
    ("Namibia", "Register", "http://www.nmrc.com.na/LinkClick424c.pdf?fileticket=ir5cbbaayg8%3d&tabid=677&language=en-US"),
    ("Seychelles", "No regulatory authority", None),
    ("South Africa", "Regulatory Authority", "http://www.mccza.com/dynamism/default_dynamic.asp?grpID=30&doc=dynamic_generated_page.asp&categID=165&groupID=30"),
    ("Swaziland", "No regulatory authority", None),
    ("Tanzania", "Register", "http://tfda.or.tz/index.php?option=com_phocadownload&view=category&id=65&Itemid=351"),
    ("Zambia", "Registration Information", "http://www.zamra.co.zm/info"),
    ("Zimbabwe", "Register", "http://www.mcaz.co.zw/index.php/downloads/category/17-registers"),
    ]

tenders = [
    {
        "country": "Namibia",
        "organisation": "Central Medical Stores",
        "type": "International Tender for Essential Medicines",
        "start_date": "August 2014",
        "duration": "2 Year framework",
        },
    {
        "country": "Madagascar",
        "organisation": "SALAMA",
        "type": "International Tender for Essential Medicines and Medical Supplies",
        "start_date": "November 2014",
        "duration": "1 Year",
        },
    {
        "country": "Tanzania",
        "organisation": "Medical Stores Department (MSD)",
        "type": "International Tender for Essential Medicines and Medical Supplies",
        "start_date": "March 2015",
        "duration": "2 Year framework",
        },
    {
        "country": "DRC",
        "organisation": "FEDECAME",
        "type": "Limited International Tender for Essential Medicines and Medical Supplies",
        "start_date": "May 2015",
        "duration": "1 Year",
        },
    {
        "country": "Namibia",
        "organisation": "Central Medical Stores",
        "type": "International Tender for Anti-Retroviral Medicines",
        "start_date": "June 2015",
        "duration": "1 Year (renewable)",
        },
    {
        "country": "Namibia",
        "organisation": "Central Medical Stores",
        "type": "International Tender for Clinical Supplies",
        "start_date": "June 2016",
        "duration": "2 Year framework",
        },
    {
        "country": "Mauritius",
        "organisation": "MOH&QL",
        "type": "Annual Tenders for Medicines and Medical Supplies (34 Lots) for year 2015",
        "start_date": "July 2014 - 17 December 2014",
        "duration": "1 Year",
        },
    {
        "country": "South Africa",
        "organisation": "Department of Health",
        "type": 'All Pharmaceutical Tenders: see <a href="http://www.health.gov.za/vhb.php" target="_blank">http://www.health.gov.za/vhb.php</a>',
        "start_date": "N/A",
        "duration": "1 Year",
        },
    {
        "country": "Swaziland",
        "organisation": "Central Medical Stores",
        "type": 'International Tender for Essential Medicines and Medical Supplies',
        "start_date": "October 2014",
        "duration": "1 Year",
        },
    {
        "country": "Lesotho",
        "organisation": "National Drug Service Organisation",
        "type": 'International Tender for Anti-Retroviral Medicines',
        "start_date": "December 2014",
        "duration": "1 Year",
        },
    {
        "country": "Lesotho",
        "organisation": "National Drug Service Organisation",
        "type": 'International Tender for Laboratory Items & Consumables',
        "start_date": "January 2015",
        "duration": "1 Year",
        },
    {
        "country": "Lesotho",
        "organisation": "National Drug Service Organisation",
        "type": 'International Tender for Pharmaceuticals',
        "start_date": "February 2015",
        "duration": "1 Year",
        },
    {
        "country": "Lesotho",
        "organisation": "National Drug Service Organisation",
        "type": 'International Tender for Anti-Retroviral Medicines',
        "start_date": "April 2015",
        "duration": "1 Year",
        },
    {
        "country": "Lesotho",
        "organisation": "National Drug Service Organisation",
        "type": 'International Tender for Anti-Retroviral Medicines',
        "start_date": "April 2015",
        "duration": "1 Year",
        },
    {
        "country": "Lesotho",
        "organisation": "National Drug Service Organisation",
        "type": 'International Tender for Medical Supplies',
        "start_date": "June 2015",
        "duration": "1 Year",
        },
    ]

link_list = [
    ("http://ecs.sadc.int/ppn", "Mailing list: SADC Pooled Procurement Network", "A network of officials responsible for pharmaceutical procurement within the SADC region."),
    ("http://apps.who.int/prequal/", "WHO | Prequalification of Medicines Programme", "WHO webpage for the UN Prequalification Programme for prequalification of product-manufacturing site combinations"),
    ("http://www.who.int/medicines/areas/access/ecofin/en/", "WHO | Medicines Price Information", ""),
    ("http://erc.msh.org/mainpage.cfm?file=1.0.htm&module=DMP&language=English", "MSH | International Drug Price Indicator Guide (IDPIG)", ""),
    ("http://www.haiweb.org/medicineprices/international-medicine-prices-sources.php", "haiweb.org | medicine prices", "HAI Multi Country Price Sources"),
    ("http://www.clintonhealthaccess.org/files/ARV%20Price%20Reduction%20Overview%20%2808.06.09%29.pdf", "CHAI ARV Price List", "The Clinton Foundation HIV/AIDS Initiative (CHAI) - ANTIRETROVIRAL (ARV) PRICE LIST"),
    ]

for link in link_list:
    tmp = ImportantLink()
    tmp.url = link[0]
    tmp.title = link[1]
    if link[2]:
        tmp.description = link[2]
    db.session.add(tmp)

for tender in tenders:
    tmp = TenderSchedule()
    country = Country.query.filter_by(name=tender['country']).one()
    tmp.country = country
    tmp.organisation = tender['organisation']
    tmp.description = tender['type']
    tmp.start_date = tender['start_date']
    tmp.duration = tender['duration']
    db.session.add(tmp)

for register in registers:
    tmp = MedicineRegister()
    country = Country.query.filter_by(name=register[0]).one()
    tmp.country = country
    tmp.description = register[1]
    tmp.url = register[2]
    db.session.add(tmp)

db.session.commit()