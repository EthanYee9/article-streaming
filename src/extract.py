import requests 
from datetime import datetime
import os 
import dotenv 

dotenv.load_dotenv()

def get_search_params(search_term: str, message_broker_id: str, from_date: str = None):
    """
    Create a search dictionary and broker ID for Guardian API.

    Parameters:
        search_term (str): The term to search for.
        from_date (str): Optional start date in 'yyyy/mm/dd' format.
        message_broker_id (str): The message broker ID to publish to.

    Returns:
        tuple: (search_dict, message_broker_id)
    """
        
    search_dict = {
        "q": search_term.strip(), 
        "from-date": None,
        "order-by": "newest",
        "api-key": f"{os.environ["api-key"]}"
    }

    if from_date:
        search_dict["from-date"] = datetime.strptime(from_date, '%Y/%m/%d').date()
    
    return search_dict, message_broker_id

def guardian_api_call(search_term: str,  message_broker_id: str, from_date: str = None):
    """
    Call the Guardian API with search parameters and return the JSON data.
    """

    URL = "https://content.guardianapis.com/search"
    search_dict, message_broker_id = get_search_params(search_term, message_broker_id, from_date)
    response = requests.get(URL, params=search_dict)
    data = response.json()
    print(data)
    return data 

guardian_api_call("Machine learning", "Guardian", "2025/06/01")