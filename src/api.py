import requests
import json
import csv

url = "https://mcs-website-widget.solsticecloud.com//Search/Search_Installers_TypeAndLocation"

payload = "{\"sourceLat\":\"54.559449\",\"sourceLng\":\"-4.4091917\",\"nearest\":\"99999\",\"selectedTechnologies\":\"\",\"selectedRegions\":\"\",\"sortMode\":1}"
headers = {
  'Accept': 'application/json, text/javascript, */*; q=0.01',
  'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
  'Connection': 'keep-alive',
  'Content-Type': 'application/json; charset=UTF-8',
  'Origin': 'https://mcscertified.com',
  'Referer': 'https://mcscertified.com/find-an-installer/',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'cross-site',
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
  'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Linux"'
}

response = requests.request("POST", url, headers=headers, data=payload).json()
response = json.loads(response)

# json_data = json.dumps(response)
# json_data = json.loads(json_data)

companies = []

for company in response:
    company_information = {
        "company_name": "",
        "email_address": "",
        "website_url": "",
        "contact_name": ""
        }

    company_information["company_name"] = company["Name"]
    company_information["email_address"] = company["Email"]
    company_information["website_url"] = company["Website"]
    company_information["contact_name"] = company["ContactName"]

    companies.append(company_information)

keys = companies[0].keys()

with open('solar_companies_mcs.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(companies)



