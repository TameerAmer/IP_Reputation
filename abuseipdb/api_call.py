import requests
import os
import ipaddress


def is_valid_ip(ip):
    """Checks if a string is a valid IPv4 or IPv6 address."""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def calculate_risk_level(abuse_confidence_score):
    """
    Categorizes risk level (HIGH/MEDIUM/LOW) based on abuse confidence score.
    """
    confidence=int(os.getenv('CONFIDENCE_THRESHOLD', 70))
    if abuse_confidence_score >= confidence:
        return "HIGH"
    elif abuse_confidence_score>=25:
        return "MEDIUM"
    return "LOW"

def status_code_message(data):
    if data.get("error") == "invalid_ip":
        return 1, "failed"
    if data.get("error") == "api_failed":
        return 2, "failed"
    return 0, "success"

def make_ip_check_request():
    """
    Fetches IP reputation data from AbuseIPDB using environment variables.
    Returns the 'data' payload from the API or an error dictionary.
    """
    ip_address = os.getenv('IP_ADDRESS')
    if not is_valid_ip(ip_address):
        return {"error": "invalid_ip","message":"Invalid IP address format"}
    
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
        response = requests.get(url=url, headers=headers, params=querystring, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return {"error": "api_failed", "message":"API request failed"}

    data=response.json()
    if 'data' not in data: #if they change the structure in the future
        return {"error": "api_failed", "message":"API response missing data"}
    return data['data']