import sys
import getopt
import csv
import requests
import xml.etree.ElementTree as ET
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC
from veracode_api_py import VeracodeAPI



def getBuilds(argv):

    application_input = ''
    try:
      opts, args = getopt.getopt(argv,"ha:",["appid="])
    except getopt.GetoptError:
      print ('Unrecognized option. Usage: get_oss_license_info_per_app.py -a <appid>')
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print ('Usage: get_oss_license_info_per_app.py -a <appid>')
         sys.exit()
      elif opt in ("-a", "--appid"):
         application_input = arg


    print ('Processing App ID: ' + application_input)
    build_details = VeracodeAPI().get_build_info(application_input)
    app_details = VeracodeAPI().get_app_info(application_input)
    #print (app_details)
    
    
    try:
        build_tree = ET.fromstring(build_details)
        app_tree = ET.fromstring(app_details)
        build_id = build_tree.attrib['build_id']
        global app_name
        app_name = app_tree[0].attrib['app_name']
        print ('Found application: '  + app_name + '. Processing Latest Build ID: ' + build_id)
    except:
        print ('AppID does not exist or no scans exist. Please verify appid is correct or has a published scan')
        sys.exit()
    
    #create CSV file with header

    with open(app_name+'-sbom-lic.csv', mode='w', newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=['Component Name','Version','License Name'])
        csv_writer.writeheader()

    parseSCA(VeracodeAPI().get_detailed_report(build_id))


def parseSCA(xmlFile):
    
    tree = ET.fromstring(xmlFile)

    for sca in tree.findall('{https://www.veracode.com/schema/reports/export/1.0}software_composition_analysis'):
        for vulns in sca.findall('{https://www.veracode.com/schema/reports/export/1.0}vulnerable_components'):
            for components in vulns.findall('{https://www.veracode.com/schema/reports/export/1.0}component'):
                csvdata = components.get("file_name") + "," + components.get("version") + ","
                
                for licenses in components.findall('{https://www.veracode.com/schema/reports/export/1.0}licenses'):
            
                    for lic in licenses.findall('{https://www.veracode.com/schema/reports/export/1.0}license'):
                        if lic.get("name") == '':
                            csvlic = lic.get("spdx_id")
                        else:    
                            csvlic = lic.get("name")
                        #csvrating = lic.get("risk_rating")
                        f = open(app_name+'-sbom-lic.csv', 'a', newline='')
                        f.write(csvdata+csvlic+"\n")
                        f.close()

def main():
    

    getBuilds(sys.argv[1:])


if __name__ == "__main__":
    try:
        arg1 = sys.argv[1]
    except IndexError:
        print ('No Arguments Supplied. Usage: get_oss_license_info_per_app.py -a <appid>')
        sys.exit(1)
    main()