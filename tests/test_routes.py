import unittest
from app import app
from app.routes import feedback_data

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        # Clear feedback_data before each test
        feedback_data.clear()

    def test_predict(self):
        response = self.app.post('/predict', json={'features': [0.5, 0.8, 0.6]})
        self.assertEqual(response.status_code, 200)
        self.assertIn('color', response.get_json())

    def test_cors_headers(self):
        response = self.app.post('/predict', json={'features': [0.5, 0.8, 0.6]})
        self.assertIn('Access-Control-Allow-Origin', response.headers)
        self.assertEqual(response.headers['Access-Control-Allow-Origin'], '*')

    def test_feedback(self):
        """Test the feedback endpoint accepts data and returns success message"""
        test_data = {'rating': 5, 'comment': 'Great prediction!'}
        response = self.app.post('/feedback', json=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'message': 'Feedback received'})
        # Verify feedback was stored
        self.assertEqual(len(feedback_data), 1)
        self.assertEqual(feedback_data[0], test_data)

    def test_feedback_cors_headers(self):
        """Test CORS headers are present on feedback endpoint"""
        response = self.app.post('/feedback', json={'rating': 4})
        self.assertIn('Access-Control-Allow-Origin', response.headers)
        self.assertEqual(response.headers['Access-Control-Allow-Origin'], '*')

    def test_predict_color_format(self):
        """Test that predict returns a valid hex color"""
        response = self.app.post('/predict', json={'features': [0.5, 0.8, 0.6]})
        color = response.get_json()['color']
        self.assertTrue(color.startswith('#'))
        self.assertEqual(len(color), 7)

    def test_predict_different_features(self):
        """Test prediction with different feature values"""
        response = self.app.post('/predict', json={'features': [0.1, 0.2, 0.3]})
        self.assertEqual(response.status_code, 200)
        self.assertIn('color', response.get_json())

    def test_feedback_multiple_entries(self):
        """Test multiple feedback entries are stored"""
        self.app.post('/feedback', json={'rating': 5})
        self.app.post('/feedback', json={'rating': 3})
        self.assertEqual(len(feedback_data), 2)

    def test_predict_edge_cases(self):
        """Test prediction with edge case values (0 and 1)"""
        # Test with all zeros
        response = self.app.post('/predict', json={'features': [0.0, 0.0, 0.0]})
        self.assertEqual(response.status_code, 200)
        color = response.get_json()['color']
        self.assertTrue(color.startswith('#'))
        
        # Test with all ones
        response = self.app.post('/predict', json={'features': [1.0, 1.0, 1.0]})
        self.assertEqual(response.status_code, 200)
        color = response.get_json()['color']
        self.assertTrue(color.startswith('#'))

    def test_feedback_empty_data(self):
        """Test feedback with empty data"""
        response = self.app.post('/feedback', json={})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'message': 'Feedback received'})

    def test_feedback_none_values(self):
        """Test feedback with None values"""
        response = self.app.post('/feedback', json={'rating': None, 'comment': None})
        self.assertEqual(response.status_code, 200)

    def test_predict_produces_valid_hex_values(self):
        """Test that prediction produces valid hexadecimal color values"""
        response = self.app.post('/predict', json={'features': [0.5, 0.8, 0.6]})
        color = response.get_json()['color']
        # Verify it's a valid hex string
        try:
            int(color[1:], 16)  # Should be able to convert to int from hex
            is_valid = True
        except ValueError:
            is_valid = False
        self.assertTrue(is_valid)

if __name__ == '__main__':
    unittest.main()

