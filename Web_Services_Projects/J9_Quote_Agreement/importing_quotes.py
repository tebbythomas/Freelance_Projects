"""

Steps to run:
python importing_quotes.py

Program written in Python 3

Program Output:
2 files:
1. XML Response file stored as - Response.xml
2. Quote Agreement stored as - Quote_Agreement.pdf

Program Description:
Program sends as HTTP POST request to the following URL:
https://secure.financepro.net/financepro/import_export/ImportQuote.aspx?fkey=OUksv35b8pjX8j7sbVBjS7ogONHNXLGM

The program sends an XML as part of the request. The XML file should be stored
in the same folder as this program
The program stored the response as an XML file and then parses the XML file
to get the URL of the Quote Agreement and sends an HTTP get request to the URL
and stores the PDF locally

"""
# Library to handle HTTP requests - both GET and POST
import requests
# Library to convert an XML to a Python Dictionary
import xmltodict


# Function to read input XML File and return the read file as a string
def read_input_xml(file_name):
    print("\nReading XML file:")
    print(file_name)
    with open(file_name, 'r') as file:
        xml_file = file.read()
    return xml_file


# Function to convert the XML response to a Python dictionary and return it
def convert_xml_to_dict(xml_string):
    print("\nConverting XML response to a Python dictionary")
    return xmltodict.parse(xml_string)


# Function to write the quote agreement response to a PDF file
def write_quote_agreement_pdf(pdf_response, quote_agreement_file_name):
    print("\nWriting the HTTP response to a PDF")
    with open(quote_agreement_file_name, 'wb') as f:
        f.write(pdf_response)
    print("\nPDF File written")


# Function to write the XML response to an XML file
def store_xml_response(xml_string, xml_file_name):
    print("\nWriting the HTTP response XML to a separate XML file")
    with open(xml_file_name, 'w') as f:
        f.write(xml_string)
    print("\nXML File written")


# Main function
def main():
    # Input XML File
    file_name = 'FPRequest20190801142242.xml'
    # Read XML contents
    xml_file = read_input_xml(file_name)
    # HTTP Header
    headers = {'Content-Type': 'application/xml'}
    # HTTP Post URL
    post_url = 'https://secure.financepro.net/financepro/import_export/ImportQuote.aspx?fkey=OUksv35b8pjX8j7sbVBjS7ogONHNXLGM'
    print("\nSending XML as a POST request to URL:")
    print(post_url)
    # Storing the HTTP Response
    response = requests.post(post_url, data=xml_file, headers=headers)
    print("\nHTTP Response Status Code:")
    print(response.status_code)
    print("\nThe response printed without modifications:")
    print(str(response.content))
    # Trimming the leading and trailing characters to only preserve the XML
    # portion of the response
    xml_string = str(response.content)[14:-1]
    xml_file_name = 'Response.xml'
    # Storing the XML response
    store_xml_response(xml_string, xml_file_name)
    print("\nHTTP Response XML stored in the following file:")
    print(xml_file_name)
    # Converting the XML to a dict
    output_dict = convert_xml_to_dict(xml_string)
    print("\nConverted Python Dictionary:")
    print(output_dict)
    # Parsing the dict to get the Quote Agreement URL
    quote_agreement_url = output_dict['FinanceProImport']['Quote']['QuoteAgreementURL']
    print("\nRequesting PDF from QuoteAgreementURL:")
    print(quote_agreement_url)
    # HTTP Get reqest to get the Quote Agreement PDF
    quote_agreement_response = requests.get(quote_agreement_url)
    print("\nQuote Agreement - HTTP Response Status Code:")
    print(quote_agreement_response.status_code)
    quote_agreement_file_name = 'Quote_Agreement.pdf'
    # Storing the Quote Agreement PDF
    write_quote_agreement_pdf(quote_agreement_response.content, quote_agreement_file_name)
    print("\nQuote agreement written to PDF:")
    print(quote_agreement_file_name)


# Entry point of code
if __name__ == '__main__':
    main()
