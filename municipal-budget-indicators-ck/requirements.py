import os

from dataclasses import dataclass
from xml.etree import ElementTree
from datetime import date

import openpyxl as xl

from loguru import logger

@dataclass
class Header:
    filename: str = None
    org: str = None
    statement: str = None
    year: int = 0
    month: int = 0
    
    def is_full(self):
        if self.month == 12:
            return True
        else:
            return False

ns = {
    '001':'urn:cz:isvs:micr:schemas:Rozvaha:v1',
    '002': 'urn:cz:isvs:micr:schemas:VykazZiskuAztrat:v1',
    '051': 'urn:cz:isvs:micr:schemas:Fin_2_12_m:v1',
    'bus': 'urn:cz:isvs:micr:schemas:BusinessTypes:v2',
    'stm': 'urn:cz:isvs:micr:schemas:StatementTypes:v1'
}

def read_xml_header(root, code):
    global ns
    header = Header()
    match = root.find('.//' + code + ':VykazHlavicka/bus:SubjektICO' , ns)
    if match is not None:
        header.org = match.text
        header.statement = code

        match2 = root.find('.//' + code + ':VykazHlavicka/stm:DatumVykaz' , ns)
        if match2 is not None:
            file_date = date.fromisoformat(match2.text)
            header.year = file_date.year
            header.month = file_date.month

        return header
    return None


def get_file_header(path, file):
    global ns
    filepath = os.path.join(path,file)

    tree = ElementTree.parse(filepath)
    root = tree.getroot()

    codes = list(ns.keys())[:3]
    for code in codes:
        match = root.find('.//'+code+':VykazHlavicka', ns)
        if match is not None:
            header = read_xml_header(root, code)
            header.filename = file
            return header

    
def identify_xml_file(path, file, xml_full, xml_part):
    header = get_file_header(path, file)
    # fill header filenames to xml_full and xml_part
    if header.year in xml_full.keys():
        xml_full[header.year][header.statement] = header.filename
    elif header.year in xml_part.keys():
        xml_part[header.year][header.statement] = header.filename
    return header

def identify_xlsx_files(path, file, excel):
    dataframe = xl.load_workbook(os.path.join(path, file))
    # Define variable to read sheet
    df1 = dataframe.active
    name = df1['A2'].value
    # print(f'OpenPyXL header: {name}')

    if "rozpoč" in name: # File header 'Návrh rozpočtu' or 'Schválený rozpočet'
        if len(excel.keys()) > 0 and str(list(excel.keys())[0]) in name and name.endswith(str(list(excel.keys())[0])): # year we looking for at the end
            excel[list(excel.keys())[0]]['051'] = file


def find_required_files(path, xml_full, xml_part, excel):
    xml_files = [x for x in os.listdir(path) if x.endswith('.xml')]
    xlsx_files = [x for x in os.listdir(path) if x.endswith('.xlsx')]

    logger.trace(f'xml files: {xml_files} \nxlsx_files: {xlsx_files}')


    headers = []
    for file in xml_files:
        headers.append(identify_xml_file(path, file, xml_full, xml_part))
    for file in xlsx_files:
        identify_xlsx_files(path, file, excel)
    
    # test if we have all needed files
    header = ""
    for h in headers:
        if len(header) == 0:
            header = h.org
        if header != h.org:
            return False, None
    for key, value in xml_full.items():
        if not isinstance(value, dict):
            return False, None
        for k, v in value.items():
            if not isinstance(v, str) or not v.endswith('.xml'):
                return False, None
    for key, value in xml_part.items():
        if not isinstance(value, dict):
            return False, None
        for k, v in value.items():
            if not isinstance(v, str) or not v.endswith('.xml'):
                return False, None
    for key, value in excel.items():
        if not isinstance(value, dict):
            return False, None
        for k, v in value.items():
            if not isinstance(v, str) or not v.endswith('.xlsx'):
                return False, None
    return True, headers[0].org