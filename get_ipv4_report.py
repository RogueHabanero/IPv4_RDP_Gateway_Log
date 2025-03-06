import re
import os
import csv
import json
import requests
from requests.exceptions import HTTPError
from tkinter import filedialog as fd

N_A = "Not Available"
USER_AGENT = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"}
API_URL = "http://ipwho.is/"

BAD_RETURN = {"Continent":N_A, "Country":N_A, "Region":N_A, "City":N_A, "ASN":N_A, "Organization":N_A, "Internet Service Provider":N_A}




def get_file():
    filename = fd.askopenfilename()
    if not filename.lower().endswith('.log'):
        filename = fd.askopenfilename()
    return filename




def find_ipv4_addresses(file_path):
    #ipv4_addresses = []
    addresses = {}
    ipv4_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
    with open(file_path, 'r') as file:
        for line in file:
            matches = ipv4_pattern.findall(line)
            if matches:
                ipv4_address = matches[1]
                if (ipv4_address not in addresses):
                    addresses.update({ipv4_address:1}) #adds the IP address to the dictionary
                else:
                    addresses[ipv4_address] += 1 # adds on to the number of instances where it has been seen
    return addresses




def get_ipwhois_geolocation(IP_Address):
    if IP_Address == N_A:
        return BAD_RETURN

    full_url = API_URL + IP_Address
    response = requests.get(full_url, headers=USER_AGENT)
    response.raise_for_status()
    json_response = response.json()

    if json_response["success"] == False:
        return BAD_RETURN

    continent = json_response["continent"]
    country = json_response["country"]
    city = json_response["city"]
    region = json_response["region"]
    connection = json_response["connection"]
    asn = connection["asn"]
    org = connection["org"]
    isp = connection["isp"]
    return {"Continent": continent, "Country":country, "Region":region, "City":city, "ASN":asn, "Organization":org, "Internet Service Provider":isp}




def write_new_file(array_of_lines):
    fields = ["IP Address", "Count", "Continent", "Country", "Region", "City", "ASN", "Organization", "Internet Service Provider"]
    with open('IPv4_address_report.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames = fields)
        writer.writeheader()
        writer.writerows(array_of_lines)




def main():
    filename = get_file()
    addresses = find_ipv4_addresses(filename)
    array_of_lines = []

    for address in addresses:
        line_dict = {"IP Address": address, 'Count': addresses[address]}
        ip_geolocation_info = get_ipwhois_geolocation(address) #retreive geolocation from ipwhois.io
        line_dict.update(ip_geolocation_info)
        array_of_lines.append(line_dict)
    write_new_file(array_of_lines)


if __name__ == "__main__":
    main()
