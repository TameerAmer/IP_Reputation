import unittest
from unittest.mock import patch
from check_ip_batch.main import ( 
    separate_ip_addresses, 
    make_requests, 
    api_object_summary, 
    batch_status_code_message, 
    results_summary, 
    error_summary, 
    final_summary
)

class TestMainFunctions(unittest.TestCase):

    @patch('os.getenv')
    def test_separate_ip_addresses(self, mock_getenv):
        """
        Validate splitting and trimming of IPs from IP_ADDRESSES env var.
        Ensures empty entries are discarded and an empty env yields an empty list.
        """
        mock_getenv.return_value = '192.168.1.1, 10.0.0.1, '
        result = separate_ip_addresses()
        self.assertEqual(result, ['192.168.1.1', '10.0.0.1'])

        mock_getenv.return_value = ''
        result = separate_ip_addresses()
        self.assertEqual(result, [])

    @patch('check_ip_batch.main.time.sleep')
    @patch('check_ip_batch.main.make_ip_check_request')
    def test_make_requests(self, mock_make_request, mock_sleep):
        """
        Verify request dispatch maps IP -> result using a mocked API call.
        Rate limiting (time.sleep) is mocked to keep tests fast.
        """
        mock_make_request.return_value = {'abuseConfidenceScore': 50}
        result = make_requests(['192.168.1.1', '10.0.0.1'])
        self.assertEqual(result['192.168.1.1']['abuseConfidenceScore'], 50)
        self.assertEqual(result['10.0.0.1']['abuseConfidenceScore'], 50)
        # Verify sleep was called once between 2 requests (rate limiting)
        self.assertEqual(mock_sleep.call_count, 1)

    @patch('check_ip_batch.main.calculate_risk_level')
    def test_api_object_summary(self, mock_risk_level):
        """
        Check summary counts and risk distribution.
        Risk tiering is mocked for deterministic behavior.
        """
        mock_risk_level.side_effect = lambda x: 'HIGH' if x >= 50 else 'MEDIUM'
        results = {
            '192.168.1.1': {'abuseConfidenceScore': 50},
            '10.0.0.1': {'abuseConfidenceScore': 20},
            'invalid_ip': {'error': 'invalid_ip', 'message': 'Invalid IP address'}
        }
        summary = api_object_summary(results)
        self.assertEqual(summary['total'], 3)
        self.assertEqual(summary['successful'], 2)
        self.assertEqual(summary['failed'], 1)
        self.assertEqual(summary['risk_counts']['HIGH'], 1)
        self.assertEqual(summary['risk_counts']['MEDIUM'], 1)

    @patch('check_ip_batch.main.status_code_message')
    def test_batch_status_code_message(self, mock_status):
        """
        Ensure batch status resolves to partial_success when some valid
        requests succeed and some fail; invalid IPs are ignored for success.
        """
        mock_status.side_effect = [(0, 'success'), (2, 'failed'), (1, 'failed')]
        results = {
            '192.168.1.1': {'abuseConfidenceScore': 50},
            '10.0.0.1': {'abuseConfidenceScore': 20},
            'invalid_ip': {'error': 'invalid_ip'}
        }
        code, message = batch_status_code_message(results)
        self.assertEqual(code, 0)
        self.assertEqual(message, 'partial_success')

    @patch('check_ip_batch.main.calculate_risk_level')
    def test_results_summary(self, mock_risk_level):
        """
        Extract important fields and apply mocked risk tiering.
        """
        mock_risk_level.return_value = 'MEDIUM'
        results = {
            '192.168.1.1': {'abuseConfidenceScore': 50, 'totalReports': 5, 'countryCode': 'US', 'isp': 'ISP1'},
            '10.0.0.1': {'abuseConfidenceScore': 20, 'totalReports': 2, 'countryCode': 'CA', 'isp': 'ISP2'}
        }
        summary = results_summary(results)
        self.assertEqual(summary['192.168.1.1']['risk_level'], 'MEDIUM')
        self.assertEqual(summary['10.0.0.1']['total_reports'], 2)

    def test_error_summary(self):
        """
        Group errors by type and retain the associated message.
        """
        results = {
            '192.168.1.1': {'error': None},
            '10.0.0.1': {'error': 'invalid_ip', 'message': 'Invalid IP address'}
        }
        errors = error_summary(results)
        self.assertEqual(errors['invalid_ip'], 'Invalid IP address')

    @patch('check_ip_batch.main.calculate_risk_level')
    @patch('check_ip_batch.main.status_code_message')
    def test_final_summary(self, mock_status, mock_risk_level):
        """
        Validate top-level final summary shape and content, with mocked
        status and risk tiering to avoid external dependencies.
        """
        mock_status.side_effect = [(0, 'success'), (0, 'success')]
        mock_risk_level.return_value = 'MEDIUM'
        results = {
            '192.168.1.1': {'abuseConfidenceScore': 50, 'totalReports': 5, 'countryCode': 'US', 'isp': 'ISP1'},
            '10.0.0.1': {'abuseConfidenceScore': 20, 'totalReports': 2, 'countryCode': 'CA', 'isp': 'ISP2'}
        }
        summary = final_summary(results)
        self.assertIn('step_status', summary)
        self.assertIn('api_object', summary)
        self.assertIn('results', summary['api_object'])

if __name__ == '__main__':
    unittest.main()