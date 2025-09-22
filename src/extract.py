import requests 
from datetime import datetime
import os 
import dotenv 

URL = "https://content.guardianapis.com/search"

def inputs():
    dotenv.load_dotenv()
    search_dict = {
        "q": None, 
        "from-date": None,
        "api-key": f"{os.environ["api-key"]}"
    }
    
    print("Please enter a search term: ...")
    search_dict["q"] =  input().strip()

    print("Please enter a search from date (yyyy/mm/dd) or leave blank to search all years: ...")
    date_str =  input().strip() 
    if date_str:
        search_dict["from-date"] = datetime.strptime(date_str, '%Y/%m/%d').date()
    else:
        search_dict["from-date"] = None
    
    print("Please enter message broker ID: ...")
    message_broker_id =  input().strip()
    print(search_dict["api-key"])
    return search_dict, message_broker_id

def guardian_api_call():
    search_dict, message_broker_id = inputs()
    response = requests.get(URL, params=search_dict)
    data = response.json()
    print(data)

guardian_api_call()