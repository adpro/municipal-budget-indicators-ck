import requests
import plotly.graph_objects as go

import os
import argparse
import dataclasses
import json
import csv
import uuid
import webbrowser

from dataclass_csv import DataclassWriter

from xml.etree import ElementTree
from datetime import date 
from decimal import Decimal
from dataclasses import dataclass, fields
from string import Template

from data_model import Year_Input_Data
from extensions import EnhancedJSONEncoder, indicator_limits
from indicators_model import FSO_MSK_Indicators, FSO_MSK_Indicator
from indicators_evaluation import *
from indicators_definition import FSO_MSK_Indicators_Definition, FSO_MSK_Indicator_desc


### SCRIPT 03

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


def get_decimal_value_from_FIN_XML(polozka, xpath):
    ret_value = Decimal('0.0')
    radek = rootFIN.find(xpath + polozka + '"]', ns)
    if radek is not None: 
        ret_value = Decimal(radek.find('fin212m:Vysledek', ns).text)        
    return ret_value


# Rozpocet
def get_FIN_4xx0(polozka):
    #return Decimal(rootFIN.find('.//fin212m:RekapitulacePrijmyVydaje/fin212m:Radek[fin212m:RadekCislo="' + polozka + '"]', ns).find('fin212m:Vysledek', ns).text)
    return get_decimal_value_from_FIN_XML(polozka, './/fin212m:RekapitulacePrijmyVydaje/fin212m:Radek[fin212m:RadekCislo="')

# returns sum of 5141
def get_FIN_Vydaje_Sum(polozka):
    sum = Decimal('0.0')
    for line in rootFIN.findall('.//fin212m:VydajeRozpoctove/fin212m:Radek[fin212m:Polozka="' + polozka + '"]',ns):
        sum+= Decimal(line.find('fin212m:Vysledek', ns).text)
    return sum

# neivesticni transfery
def get_FIN_41xx(polozka):
    return get_decimal_value_from_FIN_XML(polozka, './/fin212m:PrijmyRozpoctove/fin212m:Radek[fin212m:Polozka="')

# prevody vlastnim uctum
def get_FIN_534x(polozka):
    return get_decimal_value_from_FIN_XML(polozka, './/fin212m:VydajeRozpoctove/fin212m:Radek[fin212m:Polozka="')

def get_FIN_8xxx(radek):
    return get_decimal_value_from_FIN_XML(radek, './/fin212m:Financovani/fin212m:Radek[fin212m:RadekCislo="')

# 8xx2 ['8112','8122','8212','8222']
# 8x14 ['8114','8214']
# 8x13 ['8113','8213']
# 8x24 ['8124','8224']
# 8x23 ['8123','8223']
# 8xx4 ['8111','8124','8214','8224']
def get_sum_FIN_8xxx(radky):
    sum = Decimal('0.0')
    for line in radky:
        sum += get_FIN_8xxx(line)
    return sum


def get_ROZ(polozka, xpath, xpath2):
    ret_value = Decimal('0.0')
    radek = rootROZ.find(xpath + polozka + '"]', ns)
    if radek is not None: 
        ret_value = Decimal(radek.find(xpath2, ns).text)        
    return ret_value


def get_VZZ(polozka, xpath, xpath2):
    ret_value = Decimal('0.0')
    radek = rootVZZ.find(xpath + polozka + '"]', ns)
    if radek is not None: 
        ret_value = Decimal(radek.find(xpath2, ns).text)        
    return ret_value


def fill_data_with_FIN(data):
    data.fin_4010 = get_FIN_4xx0('4010')
    data.fin_4020 = get_FIN_4xx0('4020')
    data.fin_4030 = get_FIN_4xx0('4030')
    data.fin_4040 = get_FIN_4xx0('4040')
    data.fin_4060 = get_FIN_4xx0('4060')
    data.fin_4210 = get_FIN_4xx0('4210')
    data.fin_4220 = get_FIN_4xx0('4220')
    data.fin_4250 = get_FIN_4xx0('4250')
    data.fin_4200 = get_FIN_4xx0('4200')
    data.fin_4430 = get_FIN_4xx0('4430')
    data.fin_4470 = get_FIN_4xx0('4470')
    data.fin_5141 = get_FIN_Vydaje_Sum('5141')
    # transfer
    data.fin_4111 = get_FIN_41xx('4111')
    data.fin_4112 = get_FIN_41xx('4112')
    data.fin_4113 = get_FIN_41xx('4113')    # added later
    data.fin_4116 = get_FIN_41xx('4116')
    data.fin_4119 = get_FIN_41xx('4119')
    data.fin_4121 = get_FIN_41xx('4121')
    data.fin_4122 = get_FIN_41xx('4122')
    data.fin_4123 = get_FIN_41xx('4123')
    data.fin_4129 = get_FIN_41xx('4129')
    data.fin_4151 = get_FIN_41xx('4151')
    data.fin_4152 = get_FIN_41xx('4152')
    data.fin_4153 = get_FIN_41xx('4153')
    data.fin_4155 = get_FIN_41xx('4155')
    data.fin_4156 = get_FIN_41xx('4156')
    data.fin_4159 = get_FIN_41xx('4159')
    data.fin_4160 = get_FIN_41xx('4160')
    # inv.
    data.fin_4211 = get_FIN_41xx('4211')
    data.fin_4212 = get_FIN_41xx('4212')
    data.fin_4213 = get_FIN_41xx('4213')
    data.fin_4214 = get_FIN_41xx('4214')
    data.fin_4216 = get_FIN_41xx('4216')
    data.fin_4218 = get_FIN_41xx('4218')
    data.fin_4219 = get_FIN_41xx('4219')
    data.fin_4221 = get_FIN_41xx('4221')
    data.fin_4222 = get_FIN_41xx('4222')
    data.fin_4229 = get_FIN_41xx('4229')
    data.fin_4231 = get_FIN_41xx('4231')
    data.fin_4232 = get_FIN_41xx('4232')
    data.fin_4233 = get_FIN_41xx('4233')
    data.fin_4234 = get_FIN_41xx('4234')
    data.fin_4235 = get_FIN_41xx('4235')
    # internal transfer
    data.fin_5342 = get_FIN_534x('5342')
    data.fin_5344 = get_FIN_534x('5344')
    data.fin_5345 = get_FIN_534x('5345')
    data.fin_5347 = get_FIN_534x('5347')
    data.fin_5348 = get_FIN_534x('5348')
    data.fin_5349 = get_FIN_534x('5349')
    # leasing
    data.fin_5178 = get_FIN_Vydaje_Sum('5178')
    data.fin_6143 = get_FIN_Vydaje_Sum('6143')
    # finance
    data.fin_8122 = get_FIN_8xxx('8122')
    data.fin_8124 = get_FIN_8xxx('8124')
    data.fin_8xx2 = get_sum_FIN_8xxx(['8112','8122','8212','8222'])
    data.fin_8x14 = get_sum_FIN_8xxx(['8114','8214'])
    data.fin_8x13 = get_sum_FIN_8xxx(['8113','8213'])
    data.fin_8x24 = get_sum_FIN_8xxx(['8124','8224'])
    data.fin_8x23 = get_sum_FIN_8xxx(['8123','8223'])
    data.fin_8xx4 = get_sum_FIN_8xxx(['8111','8124','8214','8224'])



def fill_data_with_ROZ(data):
    data.roz_A_brutto = get_ROZ('A.', './/res:VykazData/roz:Rozvaha/roz:Aktiva/roz:Radek[roz:Polozka="', 'roz:ObdobiBezneBrutto')
    data.roz_B_brutto = get_ROZ('B.', './/res:VykazData/roz:Rozvaha/roz:Aktiva/roz:Radek[roz:Polozka="', 'roz:ObdobiBezneBrutto')
    data.roz_A_netto = get_ROZ('A.', './/res:VykazData/roz:Rozvaha/roz:Aktiva/roz:Radek[roz:Polozka="', 'roz:ObdobiBezneNetto')
    data.roz_B_netto = get_ROZ('B.', './/res:VykazData/roz:Rozvaha/roz:Aktiva/roz:Radek[roz:Polozka="', 'roz:ObdobiBezneNetto')
    data.roz_B_III = get_ROZ('B.III.', './/res:VykazData/roz:Rozvaha/roz:Aktiva/roz:Radek[roz:Polozka="', 'roz:ObdobiBezneNetto')
    data.roz_D = get_ROZ('D.', './/res:VykazData/roz:Rozvaha/roz:Pasiva/roz:Radek[roz:Polozka="', 'roz:ObdobiBezne')
    data.roz_D_II = get_ROZ('D.II.', './/res:VykazData/roz:Rozvaha/roz:Pasiva/roz:Radek[roz:Polozka="', 'roz:ObdobiBezne')
    data.roz_D_III = get_ROZ('D.III.', './/res:VykazData/roz:Rozvaha/roz:Pasiva/roz:Radek[roz:Polozka="', 'roz:ObdobiBezne')
    data.roz_472 = get_ROZ('472', './/res:VykazData/roz:Rozvaha/roz:Pasiva/roz:Radek[roz:SyntetickyUcet="', 'roz:ObdobiBezne')
    data.roz_068 = get_ROZ('068', './/res:VykazData/roz:Rozvaha/roz:Aktiva/roz:Radek[roz:SyntetickyUcet="', 'roz:ObdobiBezneNetto')
    # synthetic
    synt_path = './/res:VykazData/roz:Rozvaha/roz:Pasiva/roz:Radek[roz:SyntetickyUcet="'
    synt_path2 = 'roz:ObdobiBezne'
    data.roz_281 = get_ROZ('281', synt_path, synt_path2)
    data.roz_282 = get_ROZ('282', synt_path, synt_path2 )
    data.roz_283 = get_ROZ('283', synt_path, synt_path2 )
    data.roz_289 = get_ROZ('289', synt_path, synt_path2 )
    data.roz_322 = get_ROZ('322', synt_path, synt_path2 )
    data.roz_326 = get_ROZ('326', synt_path, synt_path2 )
    data.roz_362 = get_ROZ('362', synt_path, synt_path2 )
    data.roz_451 = get_ROZ('451', synt_path, synt_path2 )
    data.roz_452 = get_ROZ('452', synt_path, synt_path2 )
    data.roz_453 = get_ROZ('453', synt_path, synt_path2 )
    data.roz_456 = get_ROZ('456', synt_path, synt_path2 )
    data.roz_459 = get_ROZ('459', synt_path, synt_path2 )

def fill_data_with_VZZ(data):
    data.vzz_551 = get_VZZ('551', './/res:VykazData/vzz:VykazZiskuAZtrat/vzz:Naklady/vzz:Radek[vzz:SyntetickyUcet="', 'vzz:ObdobiBezneCinnostHlavni')

# ### SCRIPT 05

# ### SCRIPT 07

def evaluate_indicators(data):
    eval_VPCP(data.VPCP)
    eval_RS(data.RS, data.RS_RZD)
    eval_CPBR(data.CPBR)
    eval_SBR(data.SBR)
    eval_BUKBV(data.BUKBV)
    eval_BUKBP(data.BUKBP)
    eval_KVBP(data.KVBP)

    eval_URM(data.URM)
    eval_IA(data.IA)
    eval_KSKV(data.KSKV)
    eval_SKR(data.SKR)
    eval_KPIT(data.KPIT)

    eval_CDSBR(data.CDSBR)
    eval_DSSBR(data.DSSBR)
    eval_PUSBR(data.PUSBR)
    eval_DSC(data.DSC)
    eval_KDS(data.KDS)
    eval_CZCA(data.CZCA)
    eval_CZCA1(data.CZCA1)

    eval_CL(data.CL)
    eval_OL(data.OL)
    eval_FZ(data.FZ)

# ### SCRIPT 09 CSV

def save_data_to_csv(org_id, year_start, year_stop, data):
    header = list(range(year_start, year_stop+1, 1))
    header.insert(0, "Indikátor")
    filename = f"{org_id}_{year_start}-{year_stop}_indicators.csv"
    filepath = os.path.join('..','sample-data','output',filename)
    with open(filepath, 'w', encoding='UTF8') as f:
        # create the csv writer
        writer = csv.writer(f)
        writer.writerow(header)
        for indicator in fields(next(iter(data.values()))):           
            line = [getattr(data[year], indicator.name).value for year in data.keys() if issubclass(type(getattr(data[year], indicator.name)), FSO_MSK_Indicator)]
            if issubclass(type(getattr(data[year], indicator.name)), FSO_MSK_Indicator):
                line.insert(0, str(indicator.name))
            writer.writerow(line)

# ### SCRIPT 09 GRAPHS

colour_green = 'rgb(172,232,164)'
colour_yellow = 'rgb(241,228,25)'
colour_red = 'rgb(255,104,104)'
colour_blue = 'rgb(114,159,207)'
colour_error = 'rgb(153,153,153)'

def process_indicators_years_data_to_indicators_data(input_data: dataclass) -> dict:
    target_data = {}
    for indicator in fields(next(iter(input_data.values()))): 

        lst = []
        for year in input_data.keys():
            # print(f'{indicator.name} {issubclass(type(getattr(input_data[year], indicator.name)), FSO_MSK_Indicator)} {type(getattr(input_data[year], indicator.name))}')
            if(issubclass(type(getattr(input_data[year], indicator.name)), FSO_MSK_Indicator)):
                lst.append(vars(getattr(input_data[year], indicator.name)))
        # indicator_data = [vars(getattr(input_data[year], indicator.name)) for year in input_data.keys() if issubclass(type(getattr(input_data[year], indicator.name)), FSO_MSK_Indicator)]
        if issubclass(type(getattr(input_data[next(iter(input_data.keys()))], indicator.name)), FSO_MSK_Indicator):
            target_data[indicator.name] = lst #indicator_data
    return target_data


def add_colours_to_chart(input_data: list):
    ret_list = []

    for x in input_data:
        if x['score'] == 'A':
            ret_list.append(colour_green)
        elif x['score'] == 'B':
            ret_list.append(colour_yellow)
        elif x['score'] == 'C':
            ret_list.append(colour_red)
        elif x['score'] == 'X':
            ret_list.append(colour_error)
        else:
            ret_list.append(colour_blue)
    return ret_list

def get_indicator_values(input):
    ret_list = []
    for x in input:
        ret_list.append(x['value'])
    return ret_list

def create_chart(data, years, chart_colours, indicator, limits1, limits2, 
                start_year, stop_year, dirpath, zero_based_ind=False, log_scale=True) -> str:
    ind_def = FSO_MSK_Indicators_Definition()

    percent = True if ind_def.__dataclass_fields__[indicator].default.unit == '%' else False
    textpct = [f'{i:.2%}' for i in data] if percent == True else  [f'{i:.2f}' for i in data]
    ytitle = 'Procenta' if percent == True else 'Hodnota ukazatele - ' + ind_def.__dataclass_fields__[indicator].default.unit
    ytickformat = '.0%' if percent == True else '.2f'

    fig = go.Figure()
    if zero_based_ind == False:
        fig.add_trace(
            go.Scatter(
                x=[start_year, stop_year],
                y=limits1,
                name='Doporučené',
                mode='lines',
                line_shape='linear',
                marker_color='rgb(22, 130, 83)'
            ))
    fig.add_trace(
        go.Scatter(
            x=[start_year, stop_year],
            y=limits2 if zero_based_ind == False else limits1,
            name='Uspokojivé',
            mode='lines',
            line_shape='linear',
            marker_color='rgb(255, 134, 14)'
        ))
    if zero_based_ind == True:
        fig.add_trace(
            go.Scatter(
                x=[start_year, stop_year],
                y=limits2,
                name='Neuspokojivé',
                mode='lines',
                line_shape='linear',
                marker_color='rgb(201, 33, 30)'
            ))
    fig.add_trace(go.Bar(x=years,
                    y=data,
                    text=textpct,
                    name=indicator,
                    marker_color=chart_colours
                    ))

    fig.update_layout(
        title=f"{ind_def.__dataclass_fields__[indicator].default.short_name}",
        xaxis=dict(
            title="Roky",
            tickfont_size=14,
        ),
        yaxis=dict(
            gridcolor = 'rgb(238, 238, 238)',
            title=ytitle,
            titlefont_size=16,
            tickfont_size=14,
            tickformat=ytickformat
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    if sum(1 for number in data if number < 0) == 0:
        fig.update_yaxes(type="log")
    filename = f"{indicator}-{str(uuid.uuid4())}.svg"
    filepath = os.path.join(dirpath, filename)
    fig.write_image(filepath)
    return filename

def get_decimal_indicator_limits(indicator):
    dec_ind_limits = [Decimal(str(x)) for x in indicator_limits[indicator]]
    return dec_ind_limits

def generate_chart(org_id, start_year, stop_year, input_list, indicator, dirpath):
    ind_def = FSO_MSK_Indicators_Definition()
    zero_based = True if ind_def.__dataclass_fields__[indicator].default.zero_based == True else False
    y = 0 if zero_based == False else 1
    chart_colours = add_colours_to_chart(input_list[indicator])
    years = list(range(start_year, stop_year+1))
    fsm_inds = get_indicator_values(input_list[indicator])
    dec_ind_limits = get_decimal_indicator_limits(indicator)
    ind_ok = [dec_ind_limits[0+y] for x in range(2)]
    ind_good = [dec_ind_limits[1+y] for x in range(2)]
    filepath = create_chart(fsm_inds, years, chart_colours, indicator, ind_ok, ind_good, 
                            start_year, stop_year, dirpath, zero_based)
    return filepath


def generate_charts(org_id, start_year, stop_year, data):
    uid = uuid.uuid4()
    dirpath = os.path.join('..','sample-data', 'output', str(uid))
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    charts_filepath = {indicator:generate_chart(org_id, start_year, stop_year, data, indicator, dirpath) for indicator in data}
    return charts_filepath, dirpath, uid

def generate_report_file(org_id, uid, path, params):
    filename = f"{org_id}_{uid}_report.html"
    filepath = os.path.join(path, filename)
    with open("indicators_complete_template.html") as t:
        template = Template(t.read())
        output = template.safe_substitute(params)
        with open(filepath, "w") as fw:
            fw.write(output)
    return filepath

def download_org_name(org: str, year: int):
    # SOAP request URL
    url = "https://monitor.statnipokladna.cz/api/monitorws?WSDL"

    vars = {
        'organization_id': org,
        'year': year,
        'statement_code': 100,
    }
    # structured XML
    payload = """<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Header/><soap:Body><req:MonitorRequest xmlns:req="urn:cz:mfcr:monitor:schemas:MonitorRequest:v1" xmlns:mon="urn:cz:mfcr:monitor:schemas:MonitorTypes:v1"><req:Hlavicka>
                                <mon:OrganizaceIC>{organization_id}</mon:OrganizaceIC>
                                <mon:Rok>{year}</mon:Rok>
                                <mon:Vykaz>{statement_code}</mon:Vykaz>
                            </req:Hlavicka></req:MonitorRequest></soap:Body></soap:Envelope>"""
    # headers
    headers = { 'Content-Type': 'text/xml; charset=utf-8'}
    # POST request
    response = requests.request("POST", url, headers=headers, data=payload.format(**vars))
    ns = {'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
        'res': 'urn:cz:mfcr:monitor:schemas:MonitorResponse:v1',
        'ukaz': 'urn:cz:mfcr:monitor:schemas:MonitorUkazatele:v1'
    }
    root = ElementTree.fromstring(response.text)
    org_name = root.find('.//ukaz:NazevUJ', ns).text
    return org_name


def generate_html_report(indicators, chart_files, org_id, org_name, uid, path) -> str:
    ind_def = FSO_MSK_Indicators_Definition()
    params = {}
    for name in indicators:
        report_ind_template = f'''
            <p>
                <img src="{chart_files[name]}" alt="Graf ukazatele {ind_def.__dataclass_fields__[name].default.short_name}">
            </p>    
        '''
        params[name.lower()] = report_ind_template
        params[f"{name.lower()}_name"] = f"{ind_def.__dataclass_fields__[name].default.short_name}"
    params['org_name'] = org_name
    params['org_id'] = org_id
    params['create_date'] = date.today()
    report_path = generate_report_file(org_id, uid, path, params)
    return report_path


# ### calculation into csv file

def transpose_csv(infile, outfile):
    with open(infile) as f:
        reader = csv.reader(f)
        cols = []
        for row in reader:
            cols.append(row)
    with open(outfile, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        for i in range(len(max(cols, key=len))):
            writer.writerow([(c[i] if i<len(c) else '') for c in cols])


def save_csv_inputs(inputs):
    filename = f'inputs_{start_year}_{stop_year}.csv'
    filepath_csv = os.path.join('..','sample-data','output',filename)        
    with open(filepath_csv, "w") as f:
        w = DataclassWriter(f, inputs, Year_Input_Data)
        w.write()
    transpose_csv(filepath_csv, filepath_csv)



# #########
#   MAIN
# #########

if __name__ == "__main__":

    # input variables
    org_id = '00261220' # CK
    start_year = 2021
    stop_year = 2021
    statement_code = ''
    available_statement_codes = ['001', '002', '051']
    inputs = [] # list of input data of type Year_Input_Data

    parser = argparse.ArgumentParser()
    parser.add_argument("--org", help = "set organization id", type=str)
    parser.add_argument('-f', "--year-start", help = "set starting year", type=int)
    parser.add_argument('-t', "--year-stop", help = "set stop year", type=int)
    parser.add_argument('-s', "--statement", help = "set statement code", type=str)
 
    args = parser.parse_args()
    if args.org:
        if  len(args.org) == 8:
            org_id = args.org
        else:
            print(f"Organization ID: {args.org} has wrong format. Using default one..")

    if args.year_start:
        if args.year_start >= 2011 and args.year_start <= date.today().year:
            start_year = args.year_start
        else:
            print(f"Year {args.year_start} is not in interval 2010 - current year. Using default one..")

    if args.year_stop:
        if args.year_stop >= 2011 and args.year_stop <= date.today().year:
            stop_year = args.year_stop
        else:
            print(f"Year {args.year_stop} is not in interval 2010 - current year. Using default one..")

    list_years = list(range(start_year, stop_year+1))

    if args.statement:
        if len(args.statement) == 3 and args.statement in available_statement_codes:
            statement_code = args.statement
    statement_codes = list(statement_code) if len(statement_code) == 3 else list(available_statement_codes)

    print(f"Using org id: {org_id}")
    print(f"Using years: {start_year}-{stop_year}")

    indicators_years = {}
    for year in list_years:        
        ### SCRIPT 03 PARSING
        main_year = year
        print(f"Parsing xml data for org id {org_id} and year {main_year}...")

        data = Year_Input_Data()
        data.year = main_year
        data.organization_id = org_id

        rootFIN = get_xml_root(org_id, main_year, '051')
        fill_data_with_FIN(data)
        
        rootROZ = get_xml_root(org_id, main_year, '001')
        fill_data_with_ROZ(data)

        rootVZZ = get_xml_root(org_id, main_year, '002')
        fill_data_with_VZZ(data)

        ### SCRIPT 05 CALCULATE INDICATORS
        print(f"For calculations using year: {main_year}")

        # process data into indicators
        #print("SBR v %: {:.2f}%".format(data.SBR()*100))
        inds = FSO_MSK_Indicators(
            FSO_MSK_Indicator(data.VPCP()),
            FSO_MSK_Indicator(data.RS()),
            FSO_MSK_Indicator(data.SBR()),
            FSO_MSK_Indicator(data.BUKBV()),
            FSO_MSK_Indicator(data.BUKBP()),
            FSO_MSK_Indicator(data.KVBP()),
            FSO_MSK_Indicator(data.CPBR()),
            FSO_MSK_Indicator(data.URM()),
            FSO_MSK_Indicator(data.IA()),
            FSO_MSK_Indicator(data.KSKV()),
            FSO_MSK_Indicator(data.SKR()),
            FSO_MSK_Indicator(data.KPIT()),
            FSO_MSK_Indicator(data.KVSBR()),
            FSO_MSK_Indicator(data.CDSBR()),
            FSO_MSK_Indicator(data.DSSBR()),
            FSO_MSK_Indicator(data.PUSBR()),
            FSO_MSK_Indicator(data.DSC()),
            FSO_MSK_Indicator(data.KDS()),
            FSO_MSK_Indicator(data.CZCA()),
            FSO_MSK_Indicator(data.CZCA1()),
            FSO_MSK_Indicator(data.CL()),
            FSO_MSK_Indicator(data.OL()),
            FSO_MSK_Indicator(data.FZ()),
            # helpers
            data.RS_RZD()
        )

        inputs.append(data)

        # ### SCRIPT 07 EVALUATE INDICATORS

        print(f"Evaluating indicators for year: {main_year}")

        evaluate_indicators(inds) # replace line up
        indicators_years[year] = inds

    # ### SCRIPT 09 CSV

    save_data_to_csv(org_id, start_year, stop_year, indicators_years) 

    # ### SCRIPT 09 CHARTS

    data_chart = process_indicators_years_data_to_indicators_data(indicators_years)
    chart_files, dirpath, uid = generate_charts(org_id, start_year, stop_year, data_chart)
    indicators = [name for name in data_chart.keys()]
    org_name = download_org_name(org_id, stop_year)
    report_file = generate_html_report(indicators, chart_files, org_id, org_name, uid, dirpath)
    webbrowser.open_new_tab(f"file://" + os.path.realpath(report_file))
    print(f"Report: {report_file}")

    ### save source and calculation data to csv file
    save_csv_inputs(inputs)

