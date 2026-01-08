import requests
import json
import os

# Defining the api-endpoint
url = 'https://api.abuseipdb.com/api/v2/check'

def make_ip_check_request():
    ip_address = os.getenv('IP_ADDRESS')
    api_key = os.getenv('ABUSEIPDB_API_KEY')

    querystring = {
            'ipAddress': ip_address,
            'maxAgeInDays': '90'   
        }
    
    headers = {
        'Accept': 'application/json',
        'Key': api_key
    }

    response = requests.request(method='GET', url=url, headers=headers, params=querystring)
    # Formatted output
    decodedResponse = json.loads(response.text)
    print(json.dumps(decodedResponse, sort_keys=True, indent=4))

if __name__ == "__main__":
    make_ip_check_request()