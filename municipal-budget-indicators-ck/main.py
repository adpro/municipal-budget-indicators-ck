import argparse
import os
import platform
import subprocess
import sys
import traceback

import PySimpleGUI as sg

from datetime import date

from download_data import download_statement
from requirements import *
from parsing_data import *
from parsing_data_csv import *
from indicators_evaluation import *
from export_data import *
from data_model import Year_Input_Data
from indicators_model import FSO_MSK_Indicators, FSO_MSK_Indicator


MAIN_WINDOW_TITLE = 'Indikátory rozpočtu v0.1'
min_length = 8
INITIAL_FOLDER_IN = os.getcwd()
INITIAL_FOLDER_OUT = os.getcwd()
if len(str(os.environ.get('MUNICIPAL_BUDGET_INPUT'))) > min_length and len(str(os.environ.get('MUNICIPAL_BUDGET_OUTPUT'))) > min_length:
    INITIAL_FOLDER_IN = os.environ.get('MUNICIPAL_BUDGET_INPUT')
    INITIAL_FOLDER_OUT = os.environ.get('MUNICIPAL_BUDGET_OUTPUT')

def show_main_menu():
    layout =  [
                [sg.T('Výpočet indikátorů rozpočtu', font='Liberation_Serif 16')],
                [sg.Text('Složka se vstupními soubory:', size=(25, 1)), sg.InputText(), sg.FolderBrowse(initial_folder=INITIAL_FOLDER_IN)],
                [sg.Text('Složka pro výstupní soubory:', size=(25, 1)), sg.InputText(), sg.FolderBrowse(initial_folder=INITIAL_FOLDER_OUT)],
                [sg.Checkbox('Export indikátorů do CSV', default=True, key='export_indicators'), sg.Checkbox('Export položek a řádků zdroje', default=True, key='export_data')],
                [sg.Checkbox('Otevřít výstupní složku', default=True, key='open_dir'), sg.Checkbox('Otevřít výsledný report v prohlížeči', default=False, key='open_browser')],
                [sg.T('Vyberte typ výpočtu:')],
                [sg.Button('Rozpočtové opatření', key='button_ro'), sg.Button('Návrh rozpočtu', key='button_nr'), sg.Button('Závěrečný účet', key='button_zu')]
            ]
    event, values = sg.Window(MAIN_WINDOW_TITLE, layout, enable_close_attempted_event=True).read(close=True)
    return event, values


def fill_req_full_param(years, statements_codes):
    global required_years_xml_full
    for year in years:
        required_years_xml_full[year] = {}
        for code in statements_codes:
            required_years_xml_full[year][code] = None


def create_requirements(operation, statements_codes):
    global required_years_xml_full
    global required_years_xml_partial
    global required_excel_file
    current_year = date.today().year

    if operation == 'button_ro':
        years = list(range(current_year-5, current_year))
        fill_req_full_param(years, statements_codes)
        required_excel_file[current_year] = {}
    elif operation == 'button_nr':
        years = list(range(current_year-4, current_year+1))
        fill_req_full_param(years[:-1], statements_codes)
        required_years_xml_partial[years[-1]] = {}
        required_excel_file[current_year+1] = {}
    else: # button_zu, default
        years = list(range(current_year-6, current_year))
        fill_req_full_param(years, statements_codes)
    

def show_output_window(i, message):
    sg.one_line_progress_meter(MAIN_WINDOW_TITLE, i, 13, message, key='progress1', orientation='h')

def open_folder(path):
    if platform.system() == "Windows":
        webbrowser.open(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


def exception_handler(exctype, value, tb):
    show_output_window(15, " ")
    sg.popup('Error!', exctype, value, traceback.extract_tb(tb), title=MAIN_WINDOW_TITLE)

# #########
#   MAIN
# #########

if __name__ == "__main__":
    sys.excepthook = exception_handler
    required_years_xml_full = {}
    required_years_xml_partial = {}
    required_excel_file = {}
    available_statement_codes = ['001', '002', '051']
    input_folder = None
    output_folder = None
    inputs = [] # list of input data of type Year_Input_Data

    event, values = show_main_menu()
    input_folder, output_folder, \
        export_indicators, export_data, \
        open_dir, open_browser = values[0], values[1], \
            values['export_indicators'], values['export_data'], \
            values['open_dir'], values['open_browser']
    # print(f'Input folder: {input_folder} \nOutput folder: {output_folder}')

    if event == 'WIN_CLOSED' or \
        event == 'WINDOW_CLOSE_ATTEMPTED_EVENT' or \
        event == '-WINDOW CLOSE ATTEMPTED-':
        exit(0)

    if len(str(input_folder)) == 0 or len(str(output_folder)) == 0:
        sg.popup("Chyba!",
            "Nebyly vybrány vstupná a/nebo výstupní složky.",
            "Program bude ukončen. Pro výpočet doplňte všechny parametry.",
            title=MAIN_WINDOW_TITLE)
        exit(1)

    if event == 'button_ro':
        sg.popup("Funkce není dosud implementována.",
            "Litujeme, ale zvolili jste výpočet, který tento program zatím neumí spočítat.",
            "Program bude ukončen.",
            title=MAIN_WINDOW_TITLE)
        exit(0)

    create_requirements(
        event, available_statement_codes
    )

    # print(f'Req Full: {required_years_xml_full} \nReq part: {required_years_xml_partial} \nExcel: {required_excel_file}')

    ok, org_id = find_required_files(input_folder,
                             required_years_xml_full,
                             required_years_xml_partial,
                             required_excel_file)
    print(f'All needed files: {ok}')
    if not ok:
        sg.popup('Ve vstupním adresáři nebyly nalezeny veškeré soubory nutné k výpočtu podle zvolené operace.', 
                'Doplňte chybějící soubory.',
                'Případně potřebné XML soubory mají různé IČO.',
                title="Chyba vstupních dat")
        exit(1)

    all_dicts = {**required_years_xml_full, **required_years_xml_partial, **required_excel_file}

    # window = show_output_window()
    show_output_window(2, "Vstupní data nalezeny.")

    # print(f'Req Full: {required_years_xml_full} \nReq part: {required_years_xml_partial} \nExcel: {required_excel_file}')
    # print(f'All dicts: {all_dicts}')

    # input variables
    # org_id = '00261220' # CK

    start_year = min(all_dicts.keys())
    stop_year = max(all_dicts.keys())

    indicators_years = {}
    progress = 3
    for year, files_dict  in all_dicts.items():
    # for year in list_years:        
    #     ### SCRIPT 03 PARSING
        main_year = year
        print(f"Parsing xml data for org id {org_id} and year {main_year}...")
        # window.Refresh()
        show_output_window(progress, f"Zpracovávám data pro rok {year}...")
        progress += 1

        data = Year_Input_Data()
        data.year = main_year
        data.organization_id = org_id

        for code, filename in files_dict.items():
            filepath = os.path.join(input_folder, filename)
            if code == '001':
                rootROZ = get_xml_root(filepath)
                fill_data_with_ROZ(rootROZ, data)
            elif code == '002':
                rootVZZ = get_xml_root(filepath)
                fill_data_with_VZZ(rootVZZ, data)
            elif code == '051':
                if filename.endswith('.xml'):
                    rootFIN = get_xml_root(filepath)
                    fill_data_with_FIN(rootFIN, data)
                elif filename.endswith('.xlsx'):
                    fill_xls_data_with_FIN(filepath, data)


        ### SCRIPT 05 CALCULATE INDICATORS
        print(f"For calculations using year: {main_year}")
        # window.Refresh()


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
        # window.Refresh()

        evaluate_indicators(inds) # replace line up
        indicators_years[year] = inds

    # ### SCRIPT 09 CHARTS
    
    show_output_window(9, "Generuji grafy...")
    data_chart = process_indicators_years_data_to_indicators_data(indicators_years)
    chart_files, dirpath, uid = generate_charts(org_id, start_year, stop_year, data_chart, output_folder)
    show_output_window(10, "Stahuji data o organizaci...")
    indicators = [name for name in data_chart.keys()]
    org_name = download_org_name(org_id, start_year)
    show_output_window(11, "Generuji HTML report...")
    report_file = generate_html_report(indicators, chart_files, org_id, org_name, uid, dirpath, event)
    show_output_window(12, "Vytvořen report soubor.")
    if open_browser:
        webbrowser.open_new_tab(f"file://" + os.path.realpath(report_file))
    print(f"Report: {report_file}")

    # ### SCRIPT 09 CSV

    if export_indicators:
        show_output_window(13, "Exportuji indikátory do CSV...")
        fp = save_data_to_csv(org_id, start_year, stop_year, indicators_years, dirpath) 

    ### save source and calculation data to csv file
    if export_data:
        show_output_window(14, "Exportuji vstupních data...")
        fp_csv = save_csv_inputs(inputs, start_year, stop_year, dirpath)
    
    
    if open_dir:
        open_folder(dirpath)
    show_output_window(15, " ")


    sg.popup('Hotovo.', 
            f'HTML report je uložen v souboru {os.path.abspath(report_file)}.',
            f'Export indikátorů do csv: {"Ano" if export_indicators else "Ne"} {os.path.abspath(fp) if export_indicators else ""}',
            f'Export položek a řádků zdroje: {"Ano" if export_data else "Ne"} {os.path.abspath(fp_csv) if export_data else ""}',
            title=MAIN_WINDOW_TITLE)

