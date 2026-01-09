import unittest
import os
from unittest.mock import patch
from check_ip.main import calculate_risk_level, build_result


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


class TestBuildResult(unittest.TestCase):
    """Test cases for build_result function"""
    
    def test_successful_result_with_high_risk(self):
        """Test successful result building with HIGH risk"""
        data = {
            'ipAddress': '192.168.1.1',
            'abuseConfidenceScore': 85,
            'totalReports': 10,
            'countryCode': 'US',
            'isp': 'Example ISP',
            'isPublic': True
        }
        
        with patch.dict(os.environ, {'CONFIDENCE_THRESHOLD': '70'}):
            result = build_result(data)
        
        self.assertEqual(result['step_status']['code'], 0)
        self.assertEqual(result['step_status']['message'], 'success')
        self.assertEqual(result['api_object']['ip'], '192.168.1.1')
        self.assertEqual(result['api_object']['risk_level'], 'HIGH')
        self.assertEqual(result['api_object']['abuse_confidence_score'], 85)
        self.assertEqual(result['api_object']['total_reports'], 10)
        self.assertEqual(result['api_object']['country_code'], 'US')
        self.assertEqual(result['api_object']['isp'], 'Example ISP')
        self.assertTrue(result['api_object']['is_public'])
    
    def test_successful_result_with_medium_risk(self):
        """Test successful result building with MEDIUM risk"""
        data = {
            'ipAddress': '8.8.8.8',
            'abuseConfidenceScore': 50,
            'totalReports': 3,
            'countryCode': 'US',
            'isp': 'Google',
            'isPublic': True
        }
        
        with patch.dict(os.environ, {'CONFIDENCE_THRESHOLD': '70'}):
            result = build_result(data)
        
        self.assertEqual(result['step_status']['code'], 0)
        self.assertEqual(result['api_object']['risk_level'], 'MEDIUM')
    
    def test_successful_result_with_low_risk(self):
        """Test successful result building with LOW risk"""
        data = {
            'ipAddress': '10.0.0.1',
            'abuseConfidenceScore': 0,
            'totalReports': 0,
            'countryCode': 'US',
            'isp': 'Private Network',
            'isPublic': False
        }
        
        with patch.dict(os.environ, {'CONFIDENCE_THRESHOLD': '70'}):
            result = build_result(data)
        
        self.assertEqual(result['step_status']['code'], 0)
        self.assertEqual(result['api_object']['risk_level'], 'LOW')
    
    def test_invalid_ip_error(self):
        """Test handling of invalid IP error"""
        data = {"error": "invalid_ip"}
        result = build_result(data)
        
        self.assertEqual(result['step_status']['code'], 1)
        self.assertEqual(result['step_status']['message'], 'failed')
        self.assertEqual(result['api_object'], {})
    
    def test_api_failed_error(self):
        """Test handling of API failed error"""
        data = {"error": "api_failed"}
        result = build_result(data)
        
        self.assertEqual(result['step_status']['code'], 2)
        self.assertEqual(result['step_status']['message'], 'failed')
        self.assertEqual(result['api_object'], {})
    



if __name__ == '__main__':
    unittest.main()
