import pytest 
import datetime
from src.extract import get_search_params, guardian_api_call

class TestGetSearchParamsFunction:
    def test_returns_search_dict_and_broker_id(self):
        search_dict, broker_id = get_search_params("Machine learning ", "Guardian", "2025/06/01")
        
        assert isinstance(search_dict, dict) 
        assert isinstance(broker_id, str)

    def test_search_dict(self):
        search_dict, broker_id = get_search_params("Machine learning", "Guardian")

        assert len(search_dict) == 3
        assert isinstance(search_dict["q"], str)
        assert isinstance(search_dict["from-date"], datetime.date) or search_dict["from-date"] is None
        assert isinstance(search_dict["api-key"], str)
        assert search_dict["q"] == "Machine learning"

    def test_from_date_has_correct_format(self):
        search_dict, broker_id = get_search_params("Machine learning", "Guardian", "2025/06/01")

        assert search_dict["from-date"].strftime("%Y/%m/%d")