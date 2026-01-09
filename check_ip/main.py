import json
import os

from abuseipdb.api_call import make_ip_check_request

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

def build_result(data):
    """
    Structures API response into standardized format with status codes.
    Error codes: 0=success, 1=invalid IP, 2=API failed.
    """
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