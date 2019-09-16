'''
Program Description:

Python program to interact with web service:
secure.financepro.net
WSDL:
https://secure.financepro.net/financepro/webservices/accountstatus.asmx?WSDL

Web service operation invovled in this code:

1. GetAccountStatusByAccountID :

Called when a user wants to retrieve basic account information (balance, fees,
current payment information, etc.) and knows the Account ID

    Inputs: accountID
    Returns: Results object

The credentials  - key, LoginName, LoginPassword are hardcoded
This program makes a SOAP request to GetAccountStatusByAccountID and stores the
response in a json file. File name: <accountID>.json
To run the program:
python get_account_info.py <account_num>

(Written in Python 3)
'''


# To interact with web service
import requests
import sys
import xmltodict
import json


# Function to parse response into a json object using xmltodict
def parse_response(xml_string):
    output_json = dict()
    output_json = json.dumps(xmltodict.parse(xml_string[2:-1], process_namespaces=False), indent=4)
    return output_json


# Function to form and send SOAP request to GetAccountStatusByAccountID
def get_account_status(wsdl_url, credentials, accountID):
    # SOAP Request headers defined here
    headers = {'Host': 'secure.financepro.net',
               'Content-Type': 'application/soap+xml',
               'charset': 'utf-8'}
    # Body of SOAP request sent here
    body = """<?xml version="1.0" encoding="utf-8"?>
    <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
      <soap12:Header>
        <AuthHeader xmlns="http://www.financepro.com/financepro/WebServices/">
          <Key>""" + credentials['key'] + """</Key>
          <Login>
            <LoginName>""" + credentials['login_name'] + """</LoginName>
            <LoginPassword>""" + credentials['login_password'] + """</LoginPassword>
          </Login>
          <LogImport>true</LogImport>
        </AuthHeader>
      </soap12:Header>
      <soap12:Body>
        <GetAccountStatusByAccountID xmlns="http://www.financepro.com/financepro/WebServices/">
          <accountID>""" + accountID + """</accountID>
        </GetAccountStatusByAccountID>
      </soap12:Body>
    </soap12:Envelope>"""
    print("Account ID entered:")
    print(accountID)
    print("Sending SOAP Request")
    response = requests.post(wsdl_url, data=body, headers=headers)
    return response


# Main function
def main():
    # Retrieve account id from command line
    accountID = str(sys.argv[1])
    # WSDL defined here
    wsdl_url = "https://secure.financepro.net/financepro/webservices/accountstatus.asmx?WSDL"

    # Hardcoded credentials defined here
    credentials = dict()
    credentials['key'] = "test"
    credentials['login_name'] = "test"
    credentials['login_password'] = "test"
    response = get_account_status(wsdl_url, credentials, accountID)
    print("\nSOAP Response Status Code:")
    print(response.status_code)
    output_json = parse_response(str(response.content))
    # Storing output as a json file
    file_name = accountID + '.json'
    f = open(file_name, "w")
    f.write(output_json)
    print("Result stored in file ", file_name)


# Entry point of code
if __name__ == '__main__':
    main()
