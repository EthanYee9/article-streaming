import pytest 
import datetime
from unittest.mock import patch, MagicMock
from src.extract import get_search_params, guardian_api_call

class TestGetSearchParamsFunction:
    def test_returns_search_dict_and_broker_id(self):
        search_dict = get_search_params("Machine learning ", "2025/06/01")
        
        assert isinstance(search_dict, dict) 

    def test_search_dict(self):
        search_dict = get_search_params("Machine learning")

        assert len(search_dict) == 3
        assert isinstance(search_dict["q"], str)
        assert isinstance(search_dict["from-date"], datetime.date) or search_dict["from-date"] is None
        assert isinstance(search_dict["api-key"], str)
        assert search_dict["q"] == "Machine learning"

    def test_from_date_has_correct_format_and_datetime_obj(self):
        search_dict = get_search_params("Machine learning", "2025/06/01")

        assert search_dict["from-date"].strftime("%Y/%m/%d")

@pytest.fixture
def mock_api_response():
    search_dict = {
        "q": "Machine learning", 
        "from-date": None,
        "api-key": "test"
    }
            
    fake_data = {
        "response": {
            "status": "ok",
            "results": [
                {
                    "id": "technology/2025/sep/01/the-good-and-bad-of-machine-learning",
                    "type": "article",
                    "sectionId": "technology",
                    "sectionName": "Technology",
                    "webPublicationDate": "2025-09-01T16:12:28Z",
                    "webTitle": "The good and bad of machine learning | Letters",
                    "webUrl": "https://www.theguardian.com/technology/2025/sep/01/the-good-and-bad-of-machine-learning",
                    "apiUrl": "https://content.guardianapis.com/technology/2025/sep/01/the-good-and-bad-of-machine-learning",
                    "isHosted": False,
                    "pillarId": "pillar/news",
                    "pillarName": "News"
                }
            ]
        }
    }
        
    with patch("src.extract.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = fake_data
        mock_get.return_value = mock_response
        yield search_dict, mock_get

class TestGuardianApiCall:
    def test_ok_response_status(self, mock_api_response):
        search_dict, mock_get = mock_api_response
        result = guardian_api_call(search_dict)
        assert result["response"]["status"] == "ok"
    
    def test_check_for_results(self, mock_api_response):
        search_dict, mock_get = mock_api_response
        result = guardian_api_call(search_dict)
        assert len(result["response"]["results"]) > 0

    def test_requests_called_with_correct_params(self, mock_api_response):
        search_dict, mock_get = mock_api_response
        guardian_api_call(search_dict)
        mock_get.assert_called_once_with("https://content.guardianapis.com/search", params=search_dict)

    def test_check_result_fields_data_type(self, mock_api_response):
        search_dict, mock_get = mock_api_response
        result = guardian_api_call(search_dict)
        for article in result["response"]["results"]:
            assert isinstance(article["id"], str)
            assert isinstance(article["type"], str)
            assert isinstance(article["sectionId"], str)
            assert isinstance(article["sectionName"], str)
            assert isinstance(article["webPublicationDate"], str)
            assert isinstance(article["webTitle"], str)
            assert isinstance(article["webUrl"], str)
            assert isinstance(article["apiUrl"], str)
            assert isinstance(article["isHosted"], bool)
            assert isinstance(article["pillarId"], str)
            assert isinstance(article["pillarName"], str)
