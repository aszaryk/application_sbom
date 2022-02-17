import sys
import getopt
import csv
import requests
import xml.etree.ElementTree as ET
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC
from veracode_api_py import VeracodeAPI



def getappids():

    print ('Getting Application List')
    app_list_xml = VeracodeAPI().get_app_list()


    with open('application_ids.csv', mode='w', newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=['Applicatio Name','APP ID'])
        csv_writer.writeheader()


    tree = ET.fromstring(app_list_xml)

    for apps in tree.findall('{https://analysiscenter.veracode.com/schema/2.0/applist}app'):
        appinfo = apps.get("app_name") + "," + apps.get("app_id")
        f = open('application_ids.csv', 'a', newline='')
        f.write(appinfo+"\n")
        f.close()
    print ('Finished writing application data to application_ids.csv')

def main():
    getappids()

if __name__ == "__main__":

    main()