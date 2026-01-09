import os
import json
from abuseipdb.api_call import make_ip_check_request, calculate_risk_level, status_code_message

def separate_ip_addresses():
    """Separate IP addresses from environment variable and print them as a list."""
    raw = os.getenv("IP_ADDRESSES")
    if not raw:
        return []
    values = []
    parts = raw.split(",")
    for v in parts:
        clean_value = v.strip()
        # Only add to the list if the string isn't empty
        if clean_value != "":
            values.append(clean_value)
    return values

def make_requests(ip_addresses):
    """Make API requests for a list of IP addresses and return their results."""
    results = {}
    for ip in ip_addresses:
        result = make_ip_check_request(ip)
        results[ip] = result
    return results

def api_object_summary(results):
    total=len(results)
    success=0
    risk_counts={"HIGH":0,"MEDIUM":0,"LOW":0}
    for ip in results:
        if results[ip].get("error") is None:
            success+=1
            risk_counts[calculate_risk_level(int(results[ip]['abuseConfidenceScore']))]+=1
    failed=total-success
    summary={
        "total":total,
        "successful":success,
        "failed":failed,
        "risk_counts":risk_counts
    }
    return summary


def batch_status_code_message(results):
    """
    Maps batch outcomes to (code, message):
    - (0, "success"): All IPs checked successfully (valid IPs succeeded, invalid IPs caught)
    - (0, "partial_success"): Some valid IPs succeeded, some valid IPs had API failures
    - (1, "failed"): Input validation error (no IPs provided at all)
    - (2, "failed"): All API requests failed (all valid IPs failed)
    """
    if not results:
        return 1, "failed"  

    successes = 0
    api_failed = 0

    for res in results.values():
        code, _ = status_code_message(res)
        if code == 0: 
            successes += 1
        elif code == 2:  
            api_failed += 1
        # code == 1 (invalid_ip) doesn't count as failure(according to the example run)

    valid_attempts = successes + api_failed

    if valid_attempts == 0:
        return 1, "failed"  # no valid IPs provided (all were invalid)
    if api_failed == 0:
        return 0, "success"  # all valid IPs succeeded (invalids don't affect this)
    if successes > 0:
        return 0, "partial_success"  # some valid IPs succeeded, some failed
    return 2, "failed"  # all valid API requests failed

def results_summary(results):
    results_summary={}
    for ip in results:
        res={}
        if "error" not in results[ip]:
            abuse_confidence_score=int(results[ip]['abuseConfidenceScore'])
            res["risk_level"]=calculate_risk_level(abuse_confidence_score)
            res["abuse_confidence_score"]=abuse_confidence_score
            res["total_reports"]=results[ip]['totalReports']
            res["country_code"]=results[ip]['countryCode']
            res["isp"]=results[ip]['isp']
            results_summary[ip]=res
    return results_summary

def error_summary(results):
    errors={}
    for ip in results:
        if results[ip].get("error") is not None:
            errors[results[ip]["error"]] = results[ip].get("message")
    return errors

def final_summary(results):
    res={}
    step_status={}
    api_object={}
    code,message=batch_status_code_message(results)
    step_status["code"]=code
    step_status["message"]=message
    api_object["summary"]=api_object_summary(results)
    api_object["results"]=results_summary(results)
    
    res["step_status"]= step_status
    errors=error_summary(results)
    if errors:
        api_object["errors"]=errors
    res["api_object"]=api_object
    return res


if __name__ == "__main__":
    ip_addresses = separate_ip_addresses()
    results = make_requests(ip_addresses)
    summary = final_summary(results)
    response=json.dumps(summary, indent=4)  
    print(response)