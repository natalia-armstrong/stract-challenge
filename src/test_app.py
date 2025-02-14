import unittest
from unittest.mock import patch
import sys
import os

# Adicionando o diretório 'src' ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from app import app

class FlaskAppTestCase(unittest.TestCase):

    def mock_services(self):
        return {
            "platforms": [{"text": "Facebook Ads", "value": "meta_ads"}],
            "accounts": [{"id": "1", "name": "Nalbert"}],
            "fields": [{"text": "Ad Name", "value": "adName"}],
            "insights": [{"clicks": 100, "spend": 50.0}]
        }

    def run_test(self, route):
        mock_data = self.mock_services()

        with patch('routes.get_platforms', return_value=mock_data["platforms"]), \
             patch('routes.get_accounts', return_value=mock_data["accounts"]), \
             patch('routes.get_fields', return_value=mock_data["fields"]), \
             patch('routes.get_insights', return_value=mock_data["insights"]):

            with app.test_client() as client:
                response = client.get(route)
                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.content_type.startswith('text/csv'))

    def test_get_all_ads(self):
        self.run_test('/geral')

    def test_get_summary_ads(self):
        self.run_test('/geral/resumo')

    def test_get_platform_ads(self):
        self.run_test('/meta_ads')

    def test_get_platform_summary(self):
        self.run_test('/meta_ads/resumo')

if __name__ == '__main__':
    unittest.main()
