# Veracode OSS Components and License Info

Script to output OSS components and licenses from latest policy scan given an APP ID.  A second script to create inventory of all applications and their associated APP ID's is also included.

Uses Python3

## Setup

Clone this repository:

    git clone https://github.com/aszaryk/application_sbom

Install dependencies:

    cd application_sbom
    pip3 install -r requirements.txt

(Optional) Ensure you have created your credentials file in order to be able to interact with Veracode API calls. Documentation here: https://docs.veracode.com/r/c_configure_api_cred_file


## Usage

Tested using Python3 

## Generate List of Applications and ID's:
To generate your list of Applications and APP ID's, first run this script: 
    
    python3 get_all_app_id.py

The script will create a 'application_ids.csv' file. Look up the appid for which you wish to extract a list of components and license info.

## Generate component and license info for an application:


usage: 
    
    python3 get_oss_license_info_per_app.py -a <app_id>

The script will create a '<application name>-sbom-lic.csv' file using the name of the application as it appears in the Veracode platform as the initial portion of the filename. 

## NOTE
    
If you have not created a credentials file as per above instructions, you can set environment variables before running either script:
For example:

    export VERACODE_API_KEY_ID=<YOUR_API_KEY_ID>
    export VERACODE_API_KEY_SECRET=<YOUR_API_KEY_SECRET>
    
    
