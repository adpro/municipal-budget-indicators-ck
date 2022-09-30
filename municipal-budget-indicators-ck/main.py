import argparse

from datetime import date 

from download_data import download_statement
from parsing_data import *
from indicators_evaluation import *
from export_data import *
from data_model import Year_Input_Data
from indicators_model import FSO_MSK_Indicators, FSO_MSK_Indicator

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

    ### SCRIPT 01 Download data
    for year in list_years:
        for code in statement_codes:
            print(f"Downloading statement {code} for org id {org_id} in year {year}...")
            not_exists_bool = download_statement(org_id, year, code)
            if not not_exists_bool:
                print(f'File exists, skipping...')

    indicators_years = {}
    for year in list_years:        
        ### SCRIPT 03 PARSING
        main_year = year
        print(f"Parsing xml data for org id {org_id} and year {main_year}...")

        data = Year_Input_Data()
        data.year = main_year
        data.organization_id = org_id

        rootFIN = get_xml_root(org_id, main_year, '051')
        fill_data_with_FIN(rootFIN, data)
        
        rootROZ = get_xml_root(org_id, main_year, '001')
        fill_data_with_ROZ(rootROZ, data)

        rootVZZ = get_xml_root(org_id, main_year, '002')
        fill_data_with_VZZ(rootVZZ, data)

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
    save_csv_inputs(inputs, start_year, stop_year)

