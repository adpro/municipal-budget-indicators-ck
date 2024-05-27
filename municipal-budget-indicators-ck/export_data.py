import requests
import plotly.graph_objects as go

import os
import dataclasses
import csv
import uuid
import webbrowser

from loguru import logger

from dataclass_csv import DataclassWriter

from xml.etree import ElementTree
from datetime import date 
from decimal import Decimal
from dataclasses import dataclass, fields
from string import Template

from data_model import Year_Input_Data
from extensions import indicator_limits, resource_path
from indicators_model import FSO_MSK_Indicator
from indicators_definition import FSO_MSK_Indicators_Definition


# ### SCRIPT 09 CSV

def save_data_to_csv(org_id, year_start, year_stop, data, output_folder):
    header = list(range(year_start, year_stop+1, 1))
    header.insert(0, "Indikátor")
    filename = f"{org_id}_{year_start}-{year_stop}_indicators.csv"
    filepath = os.path.join(output_folder,filename)
    with open(filepath, 'w', encoding='UTF8') as f:
        # create the csv writer
        writer = csv.writer(f)
        writer.writerow(header)
        for indicator in fields(next(iter(data.values()))):           
            line = [getattr(data[year], indicator.name).value for year in data.keys() if issubclass(type(getattr(data[year], indicator.name)), FSO_MSK_Indicator)]
            if issubclass(type(getattr(data[next(iter(data.keys()))], indicator.name)), FSO_MSK_Indicator):
                line.insert(0, str(indicator.name))
            writer.writerow(line)
    return filepath

# ### SCRIPT 09 GRAPHS

colour_green = 'rgb(172,232,164)'
colour_yellow = 'rgb(241,228,25)'
colour_red = 'rgb(255,104,104)'
colour_blue = 'rgb(114,159,207)'
colour_error = 'rgb(153,153,153)'

def process_indicators_years_data_to_indicators_data(input_data: dataclass) -> dict:
    target_data = {}
    logger.trace(f'process_indicators_years_data_to_indicators_data: {input_data} \n')
    for indicator in fields(next(iter(input_data.values()))): 

        lst = []
        for year in input_data.keys():
            logger.trace(f'process_indicators_years_data_to_indicators_data: year: {year} \n')
            # print(f'{indicator.name} {issubclass(type(getattr(input_data[year], indicator.name)), FSO_MSK_Indicator)} {type(getattr(input_data[year], indicator.name))}')
            if(issubclass(type(getattr(input_data[year], indicator.name)), FSO_MSK_Indicator)):
                lst.append(vars(getattr(input_data[year], indicator.name)))
        # indicator_data = [vars(getattr(input_data[year], indicator.name)) for year in input_data.keys() if issubclass(type(getattr(input_data[year], indicator.name)), FSO_MSK_Indicator)]
        if issubclass(type(getattr(input_data[next(iter(input_data.keys()))], indicator.name)), FSO_MSK_Indicator):
            target_data[indicator.name] = lst #indicator_data
    logger.trace(f'process_indicators_years_data_to_indicators_data end\n')
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
        #  chart types https://plotly.com/python/reference/layout/yaxis/#layout-yaxis-type
        fig.update_yaxes(type="log") # select type of chart - log, linear
    filename = f"{indicator}-{str(uuid.uuid4())}.svg"
    filepath = os.path.join(dirpath, filename)
    fig.write_image(filepath)
    return filename

def get_decimal_indicator_limits(indicator):
    dec_ind_limits = [Decimal(str(x)) for x in indicator_limits[indicator]]
    return dec_ind_limits

def generate_chart(org_id, start_year, stop_year, input_list, indicator, dirpath):
    logger.trace(f'generate_chart: {org_id}, {start_year}, {stop_year}, **{input_list}**, {indicator}, {dirpath} \n')
    ind_def = FSO_MSK_Indicators_Definition()
    zero_based = True if ind_def.__dataclass_fields__[indicator].default.zero_based == True else False
    y = 0 if zero_based == False else 1
    chart_colours = add_colours_to_chart(input_list[indicator])
    years = list(range(start_year, stop_year+1))
    fsm_inds = get_indicator_values(input_list[indicator])
    dec_ind_limits = get_decimal_indicator_limits(indicator)
    ind_ok = [dec_ind_limits[0+y] for x in range(2)]
    ind_good = [dec_ind_limits[1+y] for x in range(2)]
    logger.trace(f'create_chart: **{fsm_inds}**, {years}, {chart_colours}, {indicator}, {ind_ok}, {ind_good}, {start_year}, {stop_year},  {dirpath}, {zero_based} \n')
    filepath = create_chart(fsm_inds, years, chart_colours, indicator, ind_ok, ind_good, 
                            start_year, stop_year, dirpath, zero_based)
    logger.trace(f'generate_chart end \n')
    return filepath


def generate_charts(org_id, start_year, stop_year, data, output_folder):
    logger.trace(f'generate_charts: {org_id}, {start_year}, {stop_year}, **{data}**, {output_folder} \n')
    uid = uuid.uuid4()
    dirpath = os.path.join(output_folder, str(uid))
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    charts_filepath = {indicator:generate_chart(org_id, start_year, stop_year, data, indicator, dirpath) for indicator in data}
    logger.trace(f'generate_charts end\n')
    return charts_filepath, dirpath, uid

def generate_report_file(org_id, uid, path, params):
    filename = f"{org_id}_{uid}_report.html"
    filepath = os.path.join(path, filename)
    module_path = os.path.dirname(os.path.realpath(__file__))
    resource_file = os.path.join("indicators_complete_template.html")
    res_path = resource_path(resource_file)
    if not os.path.exists(res_path):
        res_path = resource_file
    with open(res_path, encoding="utf8") as t:
        template = Template(t.read())
        output = template.safe_substitute(params)
        with open(filepath, "w", encoding="utf8") as fw:
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


def generate_html_report(indicators, chart_files, org_id, org_name, uid, path, event) -> str:
    ind_def = FSO_MSK_Indicators_Definition()
    
    report_type = 'Neuvedeno'
    if event == 'button_ro':
        report_type = 'Rozpočtové opatření'
    elif event == 'button_nr':
        report_type = 'Návrh rozpočtu'
    elif event == 'button_zu':
        report_type = 'Závěrečný účet'
    
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
    params['report_type'] = report_type
    report_path = generate_report_file(org_id, uid, path, params)
    return report_path


# ### calculation into csv file

def transpose_csv(infile, outfile):
    with open(infile, encoding="utf8") as f:
        reader = csv.reader(f)
        cols = []
        for row in reader:
            cols.append(row)
    with open(outfile, 'w', encoding="utf8") as f:
        writer = csv.writer(f, delimiter=';')
        for i in range(len(max(cols, key=len))):
            writer.writerow([(c[i] if i<len(c) else '') for c in cols])


def save_csv_inputs(inputs, start_year, stop_year, output_folder):
    filename = f'inputs_{start_year}_{stop_year}.csv'
    filepath_csv = os.path.join(output_folder, filename)        
    with open(filepath_csv, "w", encoding="utf8") as f:
        w = DataclassWriter(f, inputs, Year_Input_Data)
        w.write()
    transpose_csv(filepath_csv, filepath_csv)
    return filepath_csv
