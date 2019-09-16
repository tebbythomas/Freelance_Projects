"""

Steps to run:
python python policy_list_report_scraper.py

Program written in Python 3

Program Output:
1 file:
Exported_data.csv - csv file that contains the policy list report data

Program Description:
Progam first fetches the ASP login page paramters - __VIEWSTATE, __VIEWSTATEGENERATOR,
etc and then inputs these paramters and the login credentials to login
Then the program stores cookie info and uses it along with the new page parameters
to access the policy list reports page.
The code then mimics the "Go" POST request with the date parameters (hardcoded)
along with other parameters to get the report details.
The export POST request is then performed using the new set of form paramters.
The response contains the final exported csv contents which are written to a csv file:
Exported_data.csv

"""
import sys
import requests
from bs4 import BeautifulSoup
import json


# Main Function
def main():
    # Login credentials
    credentials = dict()
    credentials['username'] = 'sample'
    credentials['password'] = 'sample'
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
    # Hardcoded Policy list data parameters
    policy_list_date_params = dict()
    policy_list_date_params['Date_Activated_Start_Date'] = '8/1/2009'
    policy_list_date_params['Date_Activated_End_Date'] = '8/31/2019'
    policy_list_date_params['Date_Change_Status_Start_Date'] = '8/1/2019'
    policy_list_date_params['Date_Change_Status_End_Date'] = '8/31/2019'
    print("\nPolicy List Dates that will be used:\n")
    for key, val in policy_list_date_params.items():
        print(key, ":", val)
    print("\nAccessing Policy List Report Page")
    reports_home_url = 'https://secure.financepro.net/financepro/Reports/ReportsHome.aspx'
    policy_list_url = 'https://secure.financepro.net/financepro/Reports/PolicyList.aspx'
    response = session.get(policy_list_url, cookies=cookies)
    soup = BeautifulSoup(response.content, 'html.parser')
    script_tags = soup.find_all("script")
    # Retrieving the form paramters to send in the POST request
    # 16th script tag contains json form paramters to send in the POST request
    parameters = script_tags[15].text
    # Retaining only the relevant json form parameters
    start_ind = parameters.find("JSON.parse")
    end_ind = parameters.find('")', start_ind)
    parameters = parameters[start_ind + len("JSON.parse") + 2:end_ind]
    parameters = parameters.replace("\\", "")
    policy_list_info_params = dict()
    # Getting the ASP accounts web page session paramters
    viewstate = soup.select('input[name=__VIEWSTATE]')[0]['value']
    viewstate_generator = soup.select('input[name=__VIEWSTATEGENERATOR]')[0]['value']
    event_validation = soup.select('input[name=__EVENTVALIDATION]')[0]['value']
    print("Parameters retrieved for making to Go POST request")
    # Storing paramters to get account details page
    policy_list_info_params['__VIEWSTATE'] = viewstate
    policy_list_info_params['__VIEWSTATEGENERATOR'] = viewstate_generator
    policy_list_info_params['__EVENTVALIDATION'] = event_validation
    policy_list_info_params['PolicyDateRange'] = 'rbPolicyActivation'
    # The data parameters need to manually changed
    policy_list_info_params['DateActivatedFilter$txtStartDate'] = policy_list_date_params['Date_Activated_Start_Date']
    policy_list_info_params['DateActivatedFilter$txtEndDate'] = policy_list_date_params['Date_Activated_End_Date']
    policy_list_info_params['DateChangeStatusFilter$txtStartDate'] = policy_list_date_params['Date_Change_Status_Start_Date']
    policy_list_info_params['DateChangeStatusFilter$txtEndDate'] = policy_list_date_params['Date_Change_Status_End_Date']
    policy_list_info_params['ddlAgent$ctlAjaxDropDown$hidSelectedItem'] = parameters
    policy_list_info_params['ddlGroupBy'] = 'AgentName, AccountNumber'
    policy_list_info_params['btnGo'] = 'Go'
    # Mimicing the POST request on clicking the "Go" button
    response = requests.post(policy_list_url, policy_list_info_params, cookies=cookies)
    soup = BeautifulSoup(response.content, 'html.parser')
    print("Go button POST request sent")
    viewstate = soup.select('input[name=__VIEWSTATE]')[0]['value']
    viewstate_generator = soup.select('input[name=__VIEWSTATEGENERATOR]')[0]['value']
    event_validation = soup.select('input[name=__EVENTVALIDATION]')[0]['value']
    policy_list_info_params['__VIEWSTATE'] = viewstate
    policy_list_info_params['__VIEWSTATEGENERATOR'] = viewstate_generator
    policy_list_info_params['__EVENTVALIDATION'] = event_validation
    policy_list_info_params['__EVENTARGUMENT'] = 'EXPORT'
    policy_list_info_params['__EVENTTARGET'] = 'Report'
    policy_list_info_params.pop('btnGo', None)
    print("Parameters retrieved for export csv POST request")
    # HTTP POST request to export CSV data
    response = requests.post(policy_list_url, policy_list_info_params, cookies=cookies)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Response contains the exported CSV file
    final_csv_output_string = str(soup).strip()
    print("\nCSV File contents exported:\n")
    print(final_csv_output_string)
    final_csv_output_string += "\n"
    # Writing the CSV contents to a CSV file
    csv_file_name = "Exported_data.csv"
    with open(csv_file_name, "w") as csv_file_handler:
        csv_file_handler.write(final_csv_output_string)
    print("\nCSV contents exported to file:")
    print(csv_file_name)
    print("\nLogging off")
    # Log off page called with cookie info
    log_off_url = 'https://secure.financepro.net/financepro/logoff.aspx'
    response = requests.get(log_off_url, cookies=cookies)
    final_url = 'https://www.deltafinanceoftexas.com/'
    response = requests.get(final_url)


# Entry point of code
if __name__ == "__main__":
    main()
