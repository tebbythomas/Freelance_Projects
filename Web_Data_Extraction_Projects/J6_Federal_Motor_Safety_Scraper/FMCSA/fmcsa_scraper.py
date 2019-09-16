'''
Program Description:
This program scrapes the Federal Motor Carrier Safety Administration Website:
https://ai.fmcsa.dot.gov/SMS/
Given an input DOT number, the program scrapes the following information on the
result page:
Name, DBA, U.S. Dot#, Address, Number of Vehicles, Drivers, Inspections

The results are stored in a json file in a separate folder called Output.

Results are stored here:
Output/<Dot_Number>.json

To run the code:
python fmcsa_scraper.py <DOT Num>

Egs:
python fmcsa_scraper.py 2029046
python fmcsa_scraper.py 2864343
python fmcsa_scraper.py 2148975

The program requests for the URL:
https://ai.fmcsa.dot.gov/SMS/Carrier/<DOT Num>/Overview.aspx?FirstView=True
Eg:
https://ai.fmcsa.dot.gov/SMS/Carrier/2029046/Overview.aspx?FirstView=True
Here the information is scraped

'''

import sys
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime


# Main Function
def main():
    # To keep track of execution start time
    start_time = datetime.now()
    # Variable to store the json putput
    output = {}
    # Getting the Dot # from the command line
    dot_val = str(sys.argv[1])
    # The page we want to scrape
    request_page = "https://ai.fmcsa.dot.gov/SMS/Carrier/" + dot_val + "/Overview.aspx?FirstView=True"
    # Response is stored here
    response = requests.get(request_page)
    print("Processing DOT #: {}".format(dot_val))
    # Parsing the response page
    soup = BeautifulSoup(response.text, 'html.parser')
    # All the information we want is stored in <div id="basicInfo">
    div_tag = soup.find("div", {"id": "basicInfo"})
    # If the div tag is not present then the dot number is an invalid one
    if div_tag is None:
        print("Invalid DOT #")
    else:
        print("Valid DOT #")
        output = dict()
        h3_tag = div_tag.find("h3")
        # The name is stored in an h3 tag
        output["Name"] = str(h3_tag.text).strip()
        # The labels in the basicInfo div tag serve as keys and the very next
        # line of text serves as the value in our output dictionary
        label_tags = div_tag.find_all("label")
        for label_tag in label_tags:
            key = str(label_tag.text).strip()[:-1]
            # If the key is an address then there are multiple lines to scrape
            # Also the address is split into street, city, state and zip code
            if 'Address' in key:
                address_parts = dict()
                next_el = label_tag.next_sibling
                street = str(next_el).strip()
                address_parts["Street"] = street
                next_el = next_el.next_sibling  # Contains a break line tag
                next_el = next_el.next_sibling  # Contains the next line of the address
                second_line = str(next_el).strip()
                second_line = second_line.split(" ")
                address_parts["City"] = second_line[0][:-1]
                address_parts["State"] = second_line[1]
                address_parts["Zip Code"] = second_line[2]
                output["Address"] = address_parts
            else:
                next_el = label_tag.next_sibling
                value = str(next_el).strip()
                output[key] = value
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
