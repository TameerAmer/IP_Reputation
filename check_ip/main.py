import json
import os
from abuseipdb.api_call import make_ip_check_request, calculate_risk_level, status_code_message

def build_result(data):
    """
    Structures API response into standardized format with status codes.
    """
    code, message = status_code_message(data)
    if code != 0:
        return {"step_status": {"code": code, "message": message}, "api_object": {}}
    
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
    ip_address = os.getenv("IP_ADDRESS")
    response_data = make_ip_check_request(ip_address)
    result = build_result(response_data)
    response=json.dumps(result, indent=4)
    print(response)