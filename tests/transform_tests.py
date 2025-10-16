import pytest
import json
import re
from tests.data.transform_test_data import (
    api_response_data,
    test_data_descending_publication_dates,
    sample_articles,
)
from src.streaming_script import order_by_newest, extract_relevant_fields


class TestOrderByNewest:
    def test_returns_a_list_of_dict(self):
        input = api_response_data()
        output = order_by_newest(input)
        assert isinstance(output, list)

        for article in output:
            assert isinstance(article, dict)

    def test_descending_publication_dates(self):
        input = test_data_descending_publication_dates()
        output = order_by_newest(input)
        dates = [i["webPublicationDate"] for i in output]
        expected = sorted(dates, reverse=True)
        print(dates)
        print("expected: ---->", expected)
        assert dates == expected


@pytest.fixture
def dictionary_input():
    input = sample_articles()
    return input


class TestExtractRelevantFields:
    def test_extract_relevant_fields_returns_a_list_of_dict(self, dictionary_input):
        output = extract_relevant_fields(dictionary_input)
        assert isinstance(output, list)

        for article in output:
            assert isinstance(article, dict)

    def test_relevant_fields_present(self, dictionary_input):
        output = extract_relevant_fields(dictionary_input)
        for i in output:
            data = json.loads(i["Data"])
            i["Data"] = data
            assert isinstance(i["Data"]["webPublicationDate"], str)
            assert isinstance(i["Data"]["webTitle"], str)
            assert isinstance(i["Data"]["webUrl"], str)
            assert isinstance(i["Data"]["content_preview"], str)
            assert isinstance(i["PartitionKey"], str)

    def test_content_preview_field_less_than_1000_char(self, dictionary_input):
        output = extract_relevant_fields(dictionary_input)
        for i in output:
            data = json.loads(i["Data"])
            i["Data"] = data
            assert len(i["Data"]["content_preview"]) <= 1000

    def test_html_content_preview_coverted_to_string(self, dictionary_input):
        output = extract_relevant_fields(dictionary_input)
        for i in output:
            data = i["Data"]
            assert not bool(re.search(r"<[^>]+>", data))
            assert not bool(re.search(r"\\u[0-9a-fA-F]{4}", data))
