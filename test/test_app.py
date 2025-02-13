import unittest
from unittest.mock import patch
from app import app

class FlaskAppTestCase(unittest.TestCase):

    # Função para configurar mocks
    def mock_services(self):
        return {
            "platforms": [{"text": "Facebook Ads", "value": "meta_ads"}],
            "accounts": [{"id": "1", "name": "Nalbert"}],
            "fields": [{"text": "Ad Name", "value": "adName"}],
            "insights": [{"clicks": 100, "spend": 50.0}]
        }

    # Função auxiliar para testar as rotas
    def run_test(self, route):
        mock_data = self.mock_services()

        with patch('app.get_platforms', return_value=mock_data["platforms"]), \
             patch('app.get_accounts', return_value=mock_data["accounts"]), \
             patch('app.get_fields', return_value=mock_data["fields"]), \
             patch('app.get_insights', return_value=mock_data["insights"]):

            with app.test_client() as client:
                response = client.get(route)
                self.assertEqual(response.status_code, 200)
                # Verifica se o tipo de conteúdo começa com 'text/csv'
                self.assertTrue(response.content_type.startswith('text/csv'))

    # Teste para o endpoint "/geral"
    def test_get_all_ads(self):
        self.run_test('/geral')

    # Teste para o endpoint "/geral/resumo"
    def test_get_summary_ads(self):
        self.run_test('/geral/resumo')

    # Teste para o endpoint "/<platform>"
    def test_get_platform_ads(self):
        self.run_test('/meta_ads')

    # Teste para o endpoint "/<platform>/resumo"
    def test_get_platform_summary(self):
        self.run_test('/meta_ads/resumo')

if __name__ == '__main__':
    unittest.main()
