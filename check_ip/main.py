import json
import requests
import os
import ipaddress
# import dotenv
# dotenv.load_dotenv()

def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def make_ip_check_request():
    ip_address = os.getenv('IP_ADDRESS')
    if not is_valid_ip(ip_address):
        return {"error": "invalid_ip"}
    
    api_key = os.getenv('ABUSEIPDB_API_KEY')
    url = 'https://api.abuseipdb.com/api/v2/check'
    querystring = {
            'ipAddress': ip_address,
            'maxAgeInDays': '90'   
        }
    
    headers = {
        'Accept': 'application/json',
        'Key': api_key
    }

    try:
        response = requests.request(method='GET', url=url, headers=headers, params=querystring, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return {"error": "api_failed"}

    data=response.json()
    return data['data']


def calculate_risk_level(abuse_confidence_score):
    confidence=int(os.getenv('CONFIDENCE_THRESHOLD', 70))
    if abuse_confidence_score >= confidence:
        return "HIGH"
    elif abuse_confidence_score>=25:
        return "MEDIUM"
    return "LOW"

def build_result(data):
    code=0
    message="success"
    if data.get("error")=="invalid_ip":
        code=1
        message="failed"
        return {
        "step_status": {"code": code, "message": message},
        "api_object": {}
        }
    elif data.get("error")=="api_failed":
        code=2
        message="failed"
        return {
        "step_status": {"code": code, "message": message},
        "api_object": {}
        }

    ip=data['ipAddress']
    abuse_confidence_score=data['abuseConfidenceScore']
    risk_level=calculate_risk_level(abuse_confidence_score)
    total_reports=data['totalReports']
    country_code=data['countryCode']
    isp=data['isp']
    is_public=data['isPublic']

    result={
        "step_status":{
        "code":code,
        "message":message
    },
    "api_object": {
        "ip": ip,
        "risk_level": risk_level,
        "abuse_confidence_score": abuse_confidence_score,
        "total_reports": total_reports,
        "country_code": country_code,
        "isp": isp,
        "is_public": is_public
        }
    }
    return result

        
if __name__ == "__main__":
    response_data = make_ip_check_request()
    result = build_result(response_data)
    response=json.dumps(result, indent=4)
    print(response)