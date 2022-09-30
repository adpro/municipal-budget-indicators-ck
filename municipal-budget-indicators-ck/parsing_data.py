import os

from xml.etree import ElementTree
from decimal import Decimal
from dataclasses import dataclass, fields

from data_model import Year_Input_Data


# namespaces
ns = {'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
    'res': 'urn:cz:mfcr:monitor:schemas:MonitorResponse:v1',
    'fin212m': 'urn:cz:mfcr:monitor:schemas:MonitorFin212M:v1',
    'roz': 'urn:cz:mfcr:monitor:schemas:MonitorRozvaha:v1',
    'vzz': 'urn:cz:mfcr:monitor:schemas:MonitorVykazZiskuAZtrat:v1'
}

def get_xml_root(org_id, main_year, statement_code):
    filename = "{org_id}_{main_year}-12-31_{statement_code}.xml".format(
        org_id=org_id, main_year=main_year, statement_code=statement_code
    )
    filepath = os.path.join('..','sample-data','pokladna',filename)

    tree = ElementTree.parse(filepath)
    root = tree.getroot()
    return root


def get_decimal_value_from_FIN_XML(root, polozka, xpath):
    ret_value = Decimal('0.0')
    radek = root.find(xpath + polozka + '"]', ns)
    if radek is not None: 
        ret_value = Decimal(radek.find('fin212m:Vysledek', ns).text)        
    return ret_value


# Rozpocet
def get_FIN_4xx0(root, polozka):
    #return Decimal(rootFIN.find('.//fin212m:RekapitulacePrijmyVydaje/fin212m:Radek[fin212m:RadekCislo="' + polozka + '"]', ns).find('fin212m:Vysledek', ns).text)
    return get_decimal_value_from_FIN_XML(root, polozka, './/fin212m:RekapitulacePrijmyVydaje/fin212m:Radek[fin212m:RadekCislo="')

# returns sum of 5141
def get_FIN_Vydaje_Sum(root, polozka):
    sum = Decimal('0.0')
    for line in root.findall('.//fin212m:VydajeRozpoctove/fin212m:Radek[fin212m:Polozka="' + polozka + '"]',ns):
        sum+= Decimal(line.find('fin212m:Vysledek', ns).text)
    return sum

# neivesticni transfery
def get_FIN_41xx(root, polozka):
    return get_decimal_value_from_FIN_XML(root, polozka, './/fin212m:PrijmyRozpoctove/fin212m:Radek[fin212m:Polozka="')

# prevody vlastnim uctum
def get_FIN_534x(root, polozka):
    return get_decimal_value_from_FIN_XML(root, polozka, './/fin212m:VydajeRozpoctove/fin212m:Radek[fin212m:Polozka="')

def get_FIN_8xxx(root, radek):
    return get_decimal_value_from_FIN_XML(root, radek, './/fin212m:Financovani/fin212m:Radek[fin212m:RadekCislo="')

# 8xx2 ['8112','8122','8212','8222']
# 8x14 ['8114','8214']
# 8x13 ['8113','8213']
# 8x24 ['8124','8224']
# 8x23 ['8123','8223']
# 8xx4 ['8111','8124','8214','8224']
def get_sum_FIN_8xxx(root, radky):
    sum = Decimal('0.0')
    for line in radky:
        sum += get_FIN_8xxx(root, line)
    return sum


def get_ROZ(root, polozka, xpath, xpath2):
    ret_value = Decimal('0.0')
    radek = root.find(xpath + polozka + '"]', ns)
    if radek is not None: 
        ret_value = Decimal(radek.find(xpath2, ns).text)        
    return ret_value


def get_VZZ(root, polozka, xpath, xpath2):
    ret_value = Decimal('0.0')
    radek = root.find(xpath + polozka + '"]', ns)
    if radek is not None: 
        ret_value = Decimal(radek.find(xpath2, ns).text)        
    return ret_value


def fill_data_with_FIN(root, data):
    data.fin_4010 = get_FIN_4xx0(root,'4010')
    data.fin_4020 = get_FIN_4xx0(root,'4020')
    data.fin_4030 = get_FIN_4xx0(root,'4030')
    data.fin_4040 = get_FIN_4xx0(root,'4040')
    data.fin_4060 = get_FIN_4xx0(root,'4060')
    data.fin_4210 = get_FIN_4xx0(root,'4210')
    data.fin_4220 = get_FIN_4xx0(root,'4220')
    data.fin_4250 = get_FIN_4xx0(root,'4250')
    data.fin_4200 = get_FIN_4xx0(root,'4200')
    data.fin_4430 = get_FIN_4xx0(root,'4430')
    data.fin_4470 = get_FIN_4xx0(root,'4470')
    data.fin_5141 = get_FIN_Vydaje_Sum(root,'5141')
    # transfer
    data.fin_4111 = get_FIN_41xx(root,'4111')
    data.fin_4112 = get_FIN_41xx(root,'4112')
    data.fin_4113 = get_FIN_41xx(root,'4113')    # added later
    data.fin_4116 = get_FIN_41xx(root,'4116')
    data.fin_4119 = get_FIN_41xx(root,'4119')
    data.fin_4121 = get_FIN_41xx(root,'4121')
    data.fin_4122 = get_FIN_41xx(root,'4122')
    data.fin_4123 = get_FIN_41xx(root,'4123')
    data.fin_4129 = get_FIN_41xx(root,'4129')
    data.fin_4151 = get_FIN_41xx(root,'4151')
    data.fin_4152 = get_FIN_41xx(root,'4152')
    data.fin_4153 = get_FIN_41xx(root,'4153')
    data.fin_4155 = get_FIN_41xx(root,'4155')
    data.fin_4156 = get_FIN_41xx(root,'4156')
    data.fin_4159 = get_FIN_41xx(root,'4159')
    data.fin_4160 = get_FIN_41xx(root,'4160')
    # inv.
    data.fin_4211 = get_FIN_41xx(root,'4211')
    data.fin_4212 = get_FIN_41xx(root,'4212')
    data.fin_4213 = get_FIN_41xx(root,'4213')
    data.fin_4214 = get_FIN_41xx(root,'4214')
    data.fin_4216 = get_FIN_41xx(root,'4216')
    data.fin_4218 = get_FIN_41xx(root,'4218')
    data.fin_4219 = get_FIN_41xx(root,'4219')
    data.fin_4221 = get_FIN_41xx(root,'4221')
    data.fin_4222 = get_FIN_41xx(root,'4222')
    data.fin_4229 = get_FIN_41xx(root,'4229')
    data.fin_4231 = get_FIN_41xx(root,'4231')
    data.fin_4232 = get_FIN_41xx(root,'4232')
    data.fin_4233 = get_FIN_41xx(root,'4233')
    data.fin_4234 = get_FIN_41xx(root,'4234')
    data.fin_4235 = get_FIN_41xx(root,'4235')
    # internal transfer
    data.fin_5342 = get_FIN_534x(root,'5342')
    data.fin_5344 = get_FIN_534x(root,'5344')
    data.fin_5345 = get_FIN_534x(root,'5345')
    data.fin_5347 = get_FIN_534x(root,'5347')
    data.fin_5348 = get_FIN_534x(root,'5348')
    data.fin_5349 = get_FIN_534x(root,'5349')
    # leasing
    data.fin_5178 = get_FIN_Vydaje_Sum(root,'5178')
    data.fin_6143 = get_FIN_Vydaje_Sum(root,'6143')
    # finance
    data.fin_8122 = get_FIN_8xxx(root,'8122')
    data.fin_8124 = get_FIN_8xxx(root,'8124')
    data.fin_8xx2 = get_sum_FIN_8xxx(root,['8112','8122','8212','8222'])
    data.fin_8x14 = get_sum_FIN_8xxx(root,['8114','8214'])
    data.fin_8x13 = get_sum_FIN_8xxx(root,['8113','8213'])
    data.fin_8x24 = get_sum_FIN_8xxx(root,['8124','8224'])
    data.fin_8x23 = get_sum_FIN_8xxx(root,['8123','8223'])
    data.fin_8xx4 = get_sum_FIN_8xxx(root,['8111','8124','8214','8224'])



def fill_data_with_ROZ(root, data):
    data.roz_A_brutto = get_ROZ(root,'A.', './/res:VykazData/roz:Rozvaha/roz:Aktiva/roz:Radek[roz:Polozka="', 'roz:ObdobiBezneBrutto')
    data.roz_B_brutto = get_ROZ(root,'B.', './/res:VykazData/roz:Rozvaha/roz:Aktiva/roz:Radek[roz:Polozka="', 'roz:ObdobiBezneBrutto')
    data.roz_A_netto = get_ROZ(root,'A.', './/res:VykazData/roz:Rozvaha/roz:Aktiva/roz:Radek[roz:Polozka="', 'roz:ObdobiBezneNetto')
    data.roz_B_netto = get_ROZ(root,'B.', './/res:VykazData/roz:Rozvaha/roz:Aktiva/roz:Radek[roz:Polozka="', 'roz:ObdobiBezneNetto')
    data.roz_B_III = get_ROZ(root,'B.III.', './/res:VykazData/roz:Rozvaha/roz:Aktiva/roz:Radek[roz:Polozka="', 'roz:ObdobiBezneNetto')
    data.roz_D = get_ROZ(root,'D.', './/res:VykazData/roz:Rozvaha/roz:Pasiva/roz:Radek[roz:Polozka="', 'roz:ObdobiBezne')
    data.roz_D_II = get_ROZ(root,'D.II.', './/res:VykazData/roz:Rozvaha/roz:Pasiva/roz:Radek[roz:Polozka="', 'roz:ObdobiBezne')
    data.roz_D_III = get_ROZ(root,'D.III.', './/res:VykazData/roz:Rozvaha/roz:Pasiva/roz:Radek[roz:Polozka="', 'roz:ObdobiBezne')
    data.roz_472 = get_ROZ(root,'472', './/res:VykazData/roz:Rozvaha/roz:Pasiva/roz:Radek[roz:SyntetickyUcet="', 'roz:ObdobiBezne')
    data.roz_068 = get_ROZ(root,'068', './/res:VykazData/roz:Rozvaha/roz:Aktiva/roz:Radek[roz:SyntetickyUcet="', 'roz:ObdobiBezneNetto')
    # synthetic
    synt_path = './/res:VykazData/roz:Rozvaha/roz:Pasiva/roz:Radek[roz:SyntetickyUcet="'
    synt_path2 = 'roz:ObdobiBezne'
    data.roz_281 = get_ROZ(root,'281', synt_path, synt_path2)
    data.roz_282 = get_ROZ(root,'282', synt_path, synt_path2 )
    data.roz_283 = get_ROZ(root,'283', synt_path, synt_path2 )
    data.roz_289 = get_ROZ(root,'289', synt_path, synt_path2 )
    data.roz_322 = get_ROZ(root,'322', synt_path, synt_path2 )
    data.roz_326 = get_ROZ(root,'326', synt_path, synt_path2 )
    data.roz_362 = get_ROZ(root,'362', synt_path, synt_path2 )
    data.roz_451 = get_ROZ(root,'451', synt_path, synt_path2 )
    data.roz_452 = get_ROZ(root,'452', synt_path, synt_path2 )
    data.roz_453 = get_ROZ(root,'453', synt_path, synt_path2 )
    data.roz_456 = get_ROZ(root,'456', synt_path, synt_path2 )
    data.roz_459 = get_ROZ(root,'459', synt_path, synt_path2 )

def fill_data_with_VZZ(root, data):
    data.vzz_551 = get_VZZ(root,'551', './/res:VykazData/vzz:VykazZiskuAZtrat/vzz:Naklady/vzz:Radek[vzz:SyntetickyUcet="', 'vzz:ObdobiBezneCinnostHlavni')
