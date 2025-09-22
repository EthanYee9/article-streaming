import requests 

def inputs():
    search_dict = {
        "search_term": None, 
        "date_from": None, 
        "message_broker_id": None 
    }
    
    print("Please enter a search term: ...")
    search_dict["search_term"] =  input().strip()
    print("Please enter a search from date (dd-mm-yy) or leave blank to search all years: ...")
    search_dict["date_from"] =  input().strip()
    print("Please enter message broker ID: ...")
    search_dict["message_broker_id"] =  input().strip()

    return search_dict

inputs()