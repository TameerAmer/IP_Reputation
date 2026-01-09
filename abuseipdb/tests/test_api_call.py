import unittest
import os
from unittest.mock import patch, MagicMock
import requests
from abuseipdb.api_call import is_valid_ip, make_ip_check_request, calculate_risk_level, status_code_message


class TestIsValidIp(unittest.TestCase):
    """Test cases for is_valid_ip function"""
    
    def test_valid_ipv4_address(self):
        """Test that valid IPv4 addresses are recognized"""
        self.assertTrue(is_valid_ip("118.25.6.39"))
        self.assertTrue(is_valid_ip("185.220.101.1"))
        self.assertTrue(is_valid_ip("8.8.8.8"))
        self.assertTrue(is_valid_ip("1.1.1.1"))
    
    def test_invalid_ip_address(self):
        """Test that invalid IP addresses are rejected"""
        self.assertFalse(is_valid_ip("118.25.6.39111"))
        self.assertFalse(is_valid_ip("25.6.39"))
        self.assertFalse(is_valid_ip("not_an_ip"))
        self.assertFalse(is_valid_ip(""))
        self.assertFalse(is_valid_ip("21"))
    
    def test_none_input(self):
        """Test handling of None input"""
        self.assertFalse(is_valid_ip(None))

class TestCalculateRiskLevel(unittest.TestCase):
    """Test cases for calculate_risk_level function"""
    
    def test_high_risk_level(self):
        """Test HIGH risk classification"""
        with patch.dict(os.environ, {'CONFIDENCE_THRESHOLD': '70'}):
            self.assertEqual(calculate_risk_level(100), "HIGH")
            self.assertEqual(calculate_risk_level(75), "HIGH")
            self.assertEqual(calculate_risk_level(70), "HIGH")
    
    def test_medium_risk_level(self):
        """Test MEDIUM risk classification"""
        with patch.dict(os.environ, {'CONFIDENCE_THRESHOLD': '70'}):
            self.assertEqual(calculate_risk_level(50), "MEDIUM")
            self.assertEqual(calculate_risk_level(25), "MEDIUM")
            self.assertEqual(calculate_risk_level(69), "MEDIUM")
    
    def test_low_risk_level(self):
        """Test LOW risk classification"""
        with patch.dict(os.environ, {'CONFIDENCE_THRESHOLD': '70'}):
            self.assertEqual(calculate_risk_level(0), "LOW")
            self.assertEqual(calculate_risk_level(10), "LOW")
            self.assertEqual(calculate_risk_level(24), "LOW")
            

class TestStatusCodeMessage(unittest.TestCase):
    """Test cases for status_code_message function"""

    def test_success_no_error_key(self):
        self.assertEqual(status_code_message({"ipAddress": "1.1.1.1"}), (0, "success"))

    def test_invalid_ip_error(self):
        self.assertEqual(status_code_message({"error": "invalid_ip"}), (1, "failed"))

    def test_api_failed_error(self):
        self.assertEqual(status_code_message({"error": "api_failed"}), (2, "failed"))



class TestMakeIpCheckRequest(unittest.TestCase):
    """Test cases for make_ip_check_request function"""
    
    def test_invalid_ip_from_env(self):
        """Test that invalid IP from environment returns error"""
        with patch.dict(os.environ, {'IP_ADDRESS': 'invalid_ip', 'ABUSEIPDB_API_KEY': 'test_key'}):
            result = make_ip_check_request()
            self.assertEqual(result, {"error": "invalid_ip"})
    
    def test_missing_ip_env_variable(self):
        """Test that missing IP_ADDRESS returns error"""
        with patch.dict(os.environ, {'ABUSEIPDB_API_KEY': 'test_key'}, clear=False):
            os.environ.pop('IP_ADDRESS', None)
            result = make_ip_check_request()
            self.assertEqual(result, {"error": "invalid_ip"})
    
    @patch('abuseipdb.api_call.requests.get')
    def test_successful_api_response(self, mock_get):
        """Test successful API response"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'data': {
                'ipAddress': '118.25.6.39',
                'abuseConfidenceScore': 50,
                'totalReports': 5,
                'countryCode': 'US',
                'isp': 'Example ISP',
                'isPublic': True
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        with patch.dict(os.environ, {'IP_ADDRESS': '118.25.6.39', 'ABUSEIPDB_API_KEY': 'test_key'}):
            result = make_ip_check_request()
            
            self.assertEqual(result['ipAddress'], '118.25.6.39')
            self.assertEqual(result['abuseConfidenceScore'], 50)
            self.assertEqual(result['totalReports'], 5)
            self.assertEqual(result['countryCode'], 'US')
            self.assertEqual(result['isp'], 'Example ISP')
            self.assertTrue(result['isPublic'])


    
    @patch('abuseipdb.api_call.requests.get')
    def test_api_response_without_data_key(self, mock_get):
        """Test API response without 'data' key"""
        mock_response = MagicMock()
        mock_response.json.return_value = {'error': 'some error'}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        with patch.dict(os.environ, {'IP_ADDRESS': '8.8.8.8', 'ABUSEIPDB_API_KEY': 'test_key'}):
            result = make_ip_check_request()
            self.assertEqual(result, {"error": "api_failed"})
    
    @patch('abuseipdb.api_call.requests.get')
    def test_api_timeout(self, mock_get):
        """Test API timeout handling"""
        mock_get.side_effect = requests.exceptions.Timeout("Request timeout")
        
        with patch.dict(os.environ, {'IP_ADDRESS': '8.8.8.8', 'ABUSEIPDB_API_KEY': 'test_key'}):
            result = make_ip_check_request()
            self.assertEqual(result, {"error": "api_failed"})



if __name__ == '__main__':
    unittest.main()
