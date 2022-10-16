import requests
import os

def download_statement(org_id: str, year: int, statement: str) -> bool:

    # SOAP request URL
    url = "https://monitor.statnipokladna.cz/api/monitorws?WSDL"

    vars = {
        'organization_id': org_id,
        'year': year,
        'year_date': '{year}-12-31'.format(year=year),
        'statement_code': statement,
        'amounts': 1
    }
    # structured XML
    payload = """<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                    <soap:Header/>
                    <soap:Body>
                        <req:MonitorRequest
                            xmlns:req="urn:cz:mfcr:monitor:schemas:MonitorRequest:v1"
                            xmlns:mon="urn:cz:mfcr:monitor:schemas:MonitorTypes:v1">
                            <req:Hlavicka>
                                <mon:OrganizaceIC>{organization_id}</mon:OrganizaceIC>
                                <mon:Rok>{year}</mon:Rok>
                                <mon:Obdobi>{year_date}</mon:Obdobi>
                                <mon:Vykaz>{statement_code}</mon:Vykaz>
                                <mon:Rad>{amounts}</mon:Rad>
                            </req:Hlavicka>
                        </req:MonitorRequest>
                    </soap:Body>
                </soap:Envelope>"""

    # headers
    headers = {
        'Content-Type': 'text/xml; charset=utf-8'
    }

    filename = "{organization_id}_{year_date}_{statement_code}.xml".format(**vars)
    filepath = os.path.join("..", "sample-data",'pokladna', filename)

    if not os.path.exists(filepath):
        # POST request
        response = requests.request("POST", url, headers=headers, data=payload.format(**vars))
        with open(filepath, "w", encoding="utf8") as f:
            f.write(response.text)
        return True
    else:
        return False
