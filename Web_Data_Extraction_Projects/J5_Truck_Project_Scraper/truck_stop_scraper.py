'''
Program Description:
This program scrapes the Texas Department of Motor Vehicles Website:
https://apps.txdmv.gov/APPS/MCCS/Truckstop/Truckstop.asp
Given an input DOT number as a command line argument, the program scrapes all
the resultant information on the following tabs of the results page:
Certificate, Insurance, Vehicles, Vehicle History, Owner Info

The results are stored in a json file in a separate folder called Output.

Results are stored here:
Output/json_output.json

To run the code:
python truck_stop_scraper.py <DOT Num>

Egs:
python truck_stop_scraper.py 2029046
python truck_stop_scraper.py 2864343
python truck_stop_scraper.py 2148975
'''

import sys
import requests
from bs4 import BeautifulSoup
import json
import itertools
from datetime import datetime


# Function to parse address into street, city, county, state, zip code, etc
def address_parser(addr_str):
    addr_dict = dict()
    addr_list = addr_str.split("\n")
    addr_dict['Street 1'] = addr_list[0]
    addr_dict['Street 2'] = addr_list[1]
    info = addr_list[2].split(' ')
    city = info[0].strip()
    city = city[:-1]
    state = info[1].strip()
    zip_code = info[2].strip()
    zip_code = zip_code[:-1]
    addr_dict['City'] = city
    addr_dict['State'] = state
    addr_dict['Zip Code'] = zip_code
    addr_dict['County'] = addr_list[3]
    if len(addr_list) >= 5:
        addr_dict['Country'] = addr_list[4]
    else:
        addr_dict['Country'] = ""
    return addr_dict


# Function to get all details from the Certificate Tab
def get_certificate_info(certificate_req, session, cookies, output_value_dict):
    print("Scraping Certificate Info")
    # To retrieve intermediate URL
    response = requests.get(certificate_req, cookies=session.cookies.get_dict(), allow_redirects=True)
    # Referer used to complete <HTTP 302> redirection
    referer = response.url
    # Retrieving the final URL using previous html page as a referrer
    response = requests.get("https://apps.txdmv.gov/APPS/MCCS/Truckstop/Certificate/Certificate_General_Info.asp?", headers={"Referer": referer}, cookies=session.cookies.get_dict())
    output_value_dict['Certificate'] = dict()
    sub_dict = dict()
    soup = BeautifulSoup(response.text, 'html.parser')
    divTag = soup.find_all("div", {"class": "panel-body"})
    count = 1
    # Retrieving all the info in the certificate tab
    for tag in divTag:
        # This if condition retrieves the top section, i.e., Certificate, Business Type, DBA, etc
        if count == 1:
            div_tags = tag.find_all("div", {"class": "col-md-3 col-md-offset-1"})
            for tag in div_tags:
                string = str(tag.text).strip()
                lst = string.split(":")
                if "Status" in lst[1]:
                    lst[1] = lst[1][:-6]
                    sub_dict[lst[0]] = lst[1].strip()
                    sub_dict['Status'] = lst[2].strip()
                else:
                    sub_dict[lst[0]] = lst[1].strip()
        # This elif condition retrieves the physical and mailing address
        elif (len(divTag) == 3 and count == 2) or (len(divTag) == 4 and count == 3):
            div_tags = tag.find_all("div", {"class": "col-md-3"})
            for tag in div_tags:
                string = str(tag.text).strip()
                lst = string.split(":")
                if "Address" in lst[0]:
                    # Parse ddress into streets, city, state, etc
                    addr_dict = address_parser(lst[1].strip())
                    sub_dict[lst[0]] = addr_dict
                else:
                    sub_dict[lst[0]] = lst[1].strip()
        # This elif condition retrieves the phone num, fax num, etc
        elif len(divTag) == count:
            div_tags = tag.find_all("div")
            for i in range(len(div_tags)):
                if div_tags[i].has_attr('class') and div_tags[i]['class'][0] == 'col-md-3':
                    key = str(div_tags[i].text).strip()
                    value = str(div_tags[i + 1].text).strip()
                    sub_dict[key] = value
        count += 1
    output_value_dict['Certificate'] = sub_dict
    return output_value_dict


# Function to scrape all insurance tab details
def get_insurance_info(insurance_request, session, cookies, output_value_dict):
    print("Scraping Insurance Info")
    # To get intermediate URL
    response = requests.get(insurance_request, cookies=session.cookies.get_dict(), allow_redirects=True)
    # Intermediate URL
    referer = response.url
    # To get the final HTML Page
    response = requests.get("https://apps.txdmv.gov/APPS/MCCS/Truckstop/Certificate/Certificate_Policy.asp", headers={"Referer": referer}, cookies=session.cookies.get_dict())
    # Parsing the HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    # All the data is stored in a table
    table_tag = soup.find_all("table", {"class": "table table-striped table-bordered dt-responsive"})
    sub_dict = dict()
    for tag in table_tag:
        tr_tags = tag.find_all("tr")
        keys = list()
        for i in range(len(tr_tags)):
            # Table headers are scraped here
            if i == 0:
                th_tags = tr_tags[i].find_all("th")
                for th_tag in th_tags:
                    keys.append(str(th_tag.text).strip())
            # Table body is scraped here - only first 5 policies are needed
            elif i < 6:
                values = list()
                td_tags = tr_tags[i].find_all("td")
                for td_tag in td_tags:
                    values.append(str(td_tag.text).strip())
                # Keys are table headers and values are table row data
                new_dict = dict(zip(keys, values))
                sub_dict[i] = new_dict
    output_value_dict['Insurance'] = {'Policy List': sub_dict}
    return output_value_dict


# Function to get all vehicle details
def get_vehicle_info(vehicle_request, session, cookies, output_value_dict):
    print("Scraping Vehicle Info")
    # To get intermediate URL
    response = requests.get(vehicle_request, cookies=session.cookies.get_dict(), allow_redirects=True)
    # Intermediate Referrer URL
    referer = response.url
    # To get the final HTML Page
    response = requests.get("https://apps.txdmv.gov/APPS/MCCS/Truckstop/Certificate/Certificate_Vehicle.asp", headers={"Referer": referer}, cookies=session.cookies.get_dict())
    # Parsing the HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    # All the data is stored in a table
    table_tag = soup.find_all("table", {"class": "table table-striped table-bordered dt-responsive"})
    sub_dict = dict()
    for tag in table_tag:
        tr_tags = tag.find_all("tr")
        keys = list()
        for i in range(len(tr_tags)):
            # Table headers are scraped here
            if i == 0:
                th_tags = tr_tags[i].find_all("th")
                for th_tag in th_tags:
                    keys.append(str(th_tag.text).strip())
            # Table body is scraped here
            else:
                values = list()
                td_tags = tr_tags[i].find_all("td")
                for td_tag in td_tags:
                    values.append(str(td_tag.text).strip())
                # Keys are table headers and values are table row data
                new_dict = dict(zip(keys, values))
                sub_dict[i] = new_dict
    output_value_dict['Vehicle'] = {'Vehicle List': sub_dict}
    return output_value_dict


# Function to scrape Vehicle History Tab
def get_vehicle_history_info(vehicle_history_request, session, cookies, output_value_dict):
    print("Scraping Vehicle History Info")
    # To get intermediate URL
    response = requests.get(vehicle_history_request, cookies=session.cookies.get_dict(), allow_redirects=True)
    # Intermediate Referrer URL
    referer = response.url
    # To get the final HTML Page
    response = requests.get("https://apps.txdmv.gov/APPS/MCCS/Truckstop/Certificate/Certificate_Vehicle_History.asp", headers={"Referer": referer}, cookies=session.cookies.get_dict())
    # Parsing the HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    # All the data is stored in a table
    table_tag = soup.find_all("table", {"class": "table table-striped table-bordered dt-responsive"})
    sub_dict = dict()
    for tag in table_tag:
        tr_tags = tag.find_all("tr")
        keys = list()
        for i in range(len(tr_tags)):
            # Table headers are scraped here
            if i == 0:
                th_tags = tr_tags[i].find_all("th")
                for th_tag in th_tags:
                    keys.append(str(th_tag.text).strip())
            # Table body is scraped here
            else:
                values = list()
                td_tags = tr_tags[i].find_all("td")
                for td_tag in td_tags:
                    values.append(str(td_tag.text).strip())
                # Keys are table headers and values are table row data
                new_dict = dict(zip(keys, values))
                sub_dict[i] = new_dict
    output_value_dict['Vehicle History'] = {'Vehicle History List': sub_dict}
    return output_value_dict


# Function to scrape Owner Info Tab
def get_owner_info(owner_info_request, session, cookies, output_value_dict):
    print("Scraping Owner Info")
    # To get intermediate URL
    response = requests.get(owner_info_request, cookies=session.cookies.get_dict(), allow_redirects=True)
    # Intermediate Referrer URL
    referer = response.url
    # To get the final HTML Page
    response = requests.get("https://apps.txdmv.gov/APPS/MCCS/Truckstop/Certificate/Certificate_Owner.asp?", headers={"Referer": referer}, cookies=session.cookies.get_dict())
    # Parsing the HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    # All the data is stored in a table
    table_tag = soup.find_all("table", {"class": "table table-striped table-bordered dt-responsive"})
    sub_dict = dict()
    for tag in table_tag:
        tr_tags = tag.find_all("tr")
        keys = list()
        for i in range(len(tr_tags)):
            # Table headers are scraped here
            if i == 0:
                th_tags = tr_tags[i].find_all("th")
                for th_tag in th_tags:
                    keys.append(str(th_tag.text).strip())
            # Table body is scraped here
            else:
                values = list()
                td_tags = tr_tags[i].find_all("td")
                for td_tag in td_tags:
                    values.append(str(td_tag.text).strip())
                # Keys are table headers and values are table row data
                new_dict = dict(zip(keys, values))
                sub_dict[i] = new_dict
    output_value_dict['Owner Info'] = {'Owner List': sub_dict}
    return output_value_dict


# Main Function
def main():
    # To keep track of execution start time
    start_time = datetime.now()
    # Variable to store the json putput
    output = {}
    # Getting the Dot # from the command line
    dot_val = str(sys.argv[1])
    # Session which will be used to send cookies in each HTTP Request
    session = requests.Session()
    request_page = "https://apps.txdmv.gov/APPS/MCCS/Truckstop/Certificate/Certificate_Search_Process.asp?search_certificate_nbr=&search_us_dot_number=" + dot_val + "&search_customer_name=&search_dba_name=&search_vin_number=&search_city=&search_zip=&search_carrier_type="
    # Collect and parse first result page to check if DOT Num is valid
    response = requests.get(request_page)
    print("Processing DOT #: {}".format(dot_val))
    if "No records found." in str(response.content):
        print("Invalid DOT #")
        # Storing in json variable
        output[dot_val] = ["Not Found"]
    else:
        print("Valid DOT #")
        output[dot_val] = []
        # Data for each individual DOT Number
        output_value_dict = dict()
        # Parsing the HTML Output
        soup = BeautifulSoup(response.text, 'html.parser')
        for a in soup.find_all('a', href=True):
            if a.text and "certificate_id" in a['href']:
                output_value_dict['Certificate Number'] = str(a.text)
                td_tag = soup.find_all("td", {"style": "text-align:left"})
                for tag in td_tag:
                    # We are only interested in the company name from the result page
                    output_value_dict['Company Name'] = str(tag.text)
                    # Break after storing comapny name
                    break
                cookies = session.get(request_page)
                certificate_req = "https://apps.txdmv.gov/APPS/MCCS/Truckstop/" + a['href'][3:]
                # To scrape the Certificate tab
                output[dot_val] = get_certificate_info(certificate_req, session, cookies, output_value_dict)
        insurance_request = "https://apps.txdmv.gov/APPS/MCCS/Truckstop/Certificate/Certificate_Policy_Message.asp"
        # To scrape the Insurance tab
        output[dot_val] = get_insurance_info(insurance_request, session, cookies, output_value_dict)
        # To scrape the Vehicle tab
        vehicle_request = "https://apps.txdmv.gov/APPS/MCCS/Truckstop/Certificate/Certificate_Vehicle_Message.asp"
        output[dot_val] = get_vehicle_info(vehicle_request, session, cookies, output_value_dict)
        # To scrape the Vehicle History tab
        vehicle_history_request = "https://apps.txdmv.gov/APPS/MCCS/Truckstop/Certificate/Certificate_Vehicle_History_Message.asp"
        output[dot_val] = get_vehicle_history_info(vehicle_history_request, session, cookies, output_value_dict)
        # To scrape the Owner Info tab
        owner_info_request = "https://apps.txdmv.gov/APPS/MCCS/Truckstop/Certificate/Certificate_Owner_Message.asp?"
        output[dot_val] = get_owner_info(owner_info_request, session, cookies, output_value_dict)
        print("Finished Processing DOT #:", dot_val)
    # End of retrieval of information
    print("\n\nWriting Output to a json file")
    r = json.dumps(output)
    # Writing json output into a file
    file_name = 'Output/' + dot_val + '.json'
    with open(file_name, 'w') as f:
        json.dump(output, f)
    end_time = datetime.now()
    print("\n\nExecution Complete. Time taken to process : {}".format(end_time - start_time))


# Entry point of code
if __name__ == "__main__":
    main()
