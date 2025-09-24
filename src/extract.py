import requests 
from datetime import datetime
import os 
import dotenv 
import json

dotenv.load_dotenv()

def get_search_params(search_term: str, from_date: str = None):
    """
    Create a search dictionary and broker ID for Guardian API.

    Parameters:
        search_term (str): The term to search for.
        from_date (str): Optional start date in 'yyyy/mm/dd' format.
        message_broker_id (str): The message broker ID to publish to.

    Returns:
        dictionary: search_dict
    """
        
    search_dict = {
        "q": search_term.strip(), 
        "from-date": None,
        "show-fields": "body",
        "api-key": f"{os.environ["api-key"]}"
    }

    if from_date:
        try:
            search_dict["from-date"] = datetime.strptime(from_date, '%Y/%m/%d').date()
        except ValueError as e:
            raise ValueError("from_date must be in the format of yyyy/mm/dd, e.g. 2001/06/17")
    
    return search_dict


def guardian_api_call(search_dict: dict):
    """
    Call the Guardian API with search parameters and return the JSON data.
    """

    URL = "https://content.guardianapis.com/search"
    response = requests.get(URL, params=search_dict)
    data = response.json()
    with open("sample.json", "w") as f:
        json.dump(data, f, indent=2)
    return data 
    


def extract_api(search_term: str, message_broker_id: str, from_date: str = None):
    search_dict = get_search_params(search_term, from_date)
    article_data = guardian_api_call(search_dict)
    return article_data, message_broker_id


extract_api("Machine learning", "guardian api", "2020/01/01")

