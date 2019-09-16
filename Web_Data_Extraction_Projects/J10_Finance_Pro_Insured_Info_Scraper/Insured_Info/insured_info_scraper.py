"""

Steps to run:
python insured_info_scraper.py <account number>
Eg:
python insured_info_scraper.py 20011

Program written in Python 3

Program Output:
1 file:
Insured_Info_<account_num>.json - json file that contains the insured info details

Program Description:
Progam first fetches the ASP login page paramters - __VIEWSTATE, __VIEWSTATEGENERATOR,
etc and then inputs these paramters and the login credentials to login
Then the program stores cookie info and uses it along with the new page parameters
to access the quotes page.
The code then access the account details page by sending the account number
(retrieved as a command line argument) along with other parameter to get the
account details.
The insured information is then scraped and stored into a dictionary var which is
written into a json file

"""
import sys
import requests
from bs4 import BeautifulSoup
import json


# Main Function
def main():
    # Variable to store the json putput
    insured_information = {}
    # Getting the account number from the command line
    account_num = str(sys.argv[1])
    print("Account number entered:")
    print(account_num)
    # Login credentials
    credentials = dict()
    credentials['username'] = 'samplecsrtest'
    credentials['password'] = 'Ik vaari aa---123'
    print("Getting login session parameters to login")
    # Home page URL
    home_page_url = 'https://secure.financepro.net/financepro/default.aspx?company=deltafinance'
    # Storing the session info
    session = requests.Session()
    response = session.get(home_page_url)
    # Parsing the response using Beautiful Soup
    soup = BeautifulSoup(response.content, 'html.parser')
    # Storing 3 ASP web-page specific form parameters to use to login
    viewstate = soup.select('input[name=__VIEWSTATE]')[0]['value']
    viewstate_generator = soup.select('input[name=__VIEWSTATEGENERATOR]')[0]['value']
    event_validation = soup.select('input[name=__EVENTVALIDATION]')[0]['value']
    login_form_parameters = dict()
    login_form_parameters['__VIEWSTATE'] = viewstate
    login_form_parameters['__VIEWSTATEGENERATOR'] = viewstate_generator
    login_form_parameters['__EVENTVALIDATION'] = event_validation
    login_form_parameters['tblForm$txtUserName'] = credentials['username']
    login_form_parameters['tblForm$txtPassword'] = credentials['password']
    login_form_parameters['tblForm$btnLogin'] = 'Log In'
    login_form_parameters['tblForm$txtCompanyCode'] = 'deltafinance'
    # Storing the cookies post login
    response = session.post(home_page_url, login_form_parameters)
    cookies = session.cookies.get_dict()
    # Logging in
    response = requests.post(home_page_url, login_form_parameters)
    print("Logged in")
    print("Accessing the accounts page session paramaters to navigate to accounts page")
    accounts_url = 'https://secure.financepro.net/financepro/account/account.aspx'
    # Sending the same session cookies
    response = session.get(accounts_url, cookies=cookies)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Getting the ASP accounts web page session paramters
    viewstate = soup.select('input[name=__VIEWSTATE]')[0]['value']
    viewstate_generator = soup.select('input[name=__VIEWSTATEGENERATOR]')[0]['value']
    event_validation = soup.select('input[name=__EVENTVALIDATION]')[0]['value']
    print("Parameters retrieved")
    # Storing paramters to get account details page
    account_info_params = dict()
    account_info_params['__VIEWSTATE'] = viewstate
    account_info_params['__VIEWSTATEGENERATOR'] = viewstate_generator
    account_info_params['__EVENTVALIDATION'] = event_validation
    account_info_params['fndAccountSearch$hdnName'] = 'hvalue'
    # Account number sent as input here
    account_info_params['fndAccountSearch$txtAccountNumber'] = account_num
    account_info_params['fndAccountSearch$txtAccountStatus'] = '0'
    account_info_params['fndAccountSearch$txtCompanyCheckType'] = 'paid'
    account_info_params['fndAccountSearch$btnFind'] = 'Find Account'
    # POST request to get account and insured details
    print("\nAccessing Account Details Page")
    response = requests.post(accounts_url, account_info_params, cookies=cookies)
    soup = BeautifulSoup(response.content, 'html.parser')
    # All insured information is stored in span tags
    insured_name = soup.find("span", {"id": "lblInsuredName"}).text
    print("\nInsured Details are:\n")
    print("Insured name:")
    print(insured_name)
    insured_information['Name'] = insured_name
    insured_address = soup.find("span", {"id": "lblInsuredAddress"})
    # Converting the <br> tag into a new line char and then splitting the
    # address into its components
    insured_address = str(insured_address).replace("<br/>", "\n")
    insured_address = insured_address.replace('<span id="lblInsuredAddress">', '')
    insured_address = insured_address.replace('</span>', '')
    address_dict = dict()
    insured_address = insured_address.split("\n")
    address_dict['Line 1'] = insured_address[0]
    line2 = insured_address[1].split(" ")
    address_dict['City'] = line2[0][:-1]
    address_dict['State'] = line2[1]
    address_dict['Zip Code'] = line2[2]
    print("Insured address:")
    print("Address Line 1:")
    print(address_dict['Line 1'])
    print("City:")
    print(address_dict['City'])
    print("State:")
    print(address_dict['State'])
    print("Zip Code:")
    print(address_dict['Zip Code'])
    insured_information['Address'] = address_dict
    insured_telephone = soup.find("span", {"id": "lblInsuredPhone"}).text
    print("Insured telephone:")
    print(insured_telephone)
    insured_information['Telephone'] = insured_telephone
    # Writing the insured information into a json file
    file_name = 'Insured_Info_' + account_num + '.json'
    with open(file_name, 'w') as f:
        json.dump(insured_information, f)
    print("\nOutput File Created:")
    print(file_name)
    print("\nLogging off")
    # Log off page called with cookie info
    log_off_url = 'https://secure.financepro.net/financepro/logoff.aspx'
    response = requests.get(log_off_url, cookies=cookies)
    final_url = 'https://www.deltafinanceoftexas.com/'
    response = requests.get(final_url)


# Entry point of code
if __name__ == "__main__":
    main()
