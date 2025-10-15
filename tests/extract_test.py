import pytest
import datetime
import json
from unittest.mock import patch, MagicMock
from src.streaming_script import get_search_params, guardian_api_call, retrieve_api_key


class TestGetSearchParamsFunction:
    def test_returns_search_dict_and_broker_id(self):
        search_dict = get_search_params("Machine learning ", "api_key", "2025/06/01")

        assert isinstance(search_dict, dict)

    def test_search_dict(self):
        search_dict = get_search_params("Machine learning", "api_key")

        assert len(search_dict) == 4
        assert isinstance(search_dict["q"], str)
        assert (
            isinstance(search_dict["from-date"], datetime.date)
            or search_dict["from-date"] is None
        )
        assert isinstance(search_dict["api-key"], str)
        assert search_dict["q"] == "Machine learning"
        assert search_dict["show-fields"] == "body"

    def test_from_date_has_correct_format_and_datetime_obj(self):
        search_dict = get_search_params("Machine learning", "api_key", "2025/06/01")

        assert search_dict["from-date"].strftime("%Y/%m/%d")


@pytest.fixture
def mock_api_response():
    search_dict = {
        "q": "Machine learning",
        "from-date": None,
        "show-fields": "body",
        "api-key": "test",
    }

    fake_data = {
        "response": {
            "status": "ok",
            "results": [
                {
                    "id": "technology/2025/sep/16/how-ai-is-undermining-learning-and-teaching-in-universities",
                    "type": "article",
                    "sectionId": "technology",
                    "sectionName": "Technology",
                    "webPublicationDate": "2025-09-16T16:22:48Z",
                    "webTitle": "How AI is undermining learning and teaching in universities | Letter",
                    "webUrl": "https://www.theguardian.com/technology/2025/sep/16/how-ai-is-undermining-learning-and-teaching-in-universities",
                    "apiUrl": "https://content.guardianapis.com/technology/2025/sep/16/how-ai-is-undermining-learning-and-teaching-in-universities",
                    "fields": {
                        "body": '<p>In discussing generative artificial intelligence (<a href="https://www.theguardian.com/education/2025/sep/13/its-going-to-be-a-life-skill-educators-discuss-the-impact-of-ai-on-university-education">\u2018It\u2019s going to be a life skill\u2019: educators discuss the impact of AI on university education, 13 September</a>) you appear to underestimate the challenges that large language model (LLM) tools such as ChatGPT present to higher education. </p>'
                    },
                    "isHosted": False,
                    "pillarId": "pillar/news",
                    "pillarName": "News",
                }
            ],
        }
    }

    with patch("src.streaming_script.requests.get") as mock_get:
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
        mock_get.assert_called_once_with(
            "https://content.guardianapis.com/search", params=search_dict
        )

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
            assert isinstance(article["fields"], dict)
            assert isinstance(article["fields"]["body"], str)


@pytest.fixture
def mock_secret_manager_client():
    with patch("src.streaming_script.boto3.client") as mock_client:
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance
        yield mock_instance


class TestRetrieveApiKey:
    def test_returns_key(self, mock_secret_manager_client):
        fake_key = "26a07767-1132-1c68-b3b2-83c78e09r559"

        mock_secret_manager_client.get_secret_value.return_value = {
            "SecretString": json.dumps({"api_key": fake_key})
        }

        response = retrieve_api_key()

        assert len(response) == 36
        assert isinstance(response, str)
        assert response == fake_key
