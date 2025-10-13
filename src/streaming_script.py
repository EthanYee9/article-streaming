import requests 
from datetime import datetime
import json
import boto3
from lxml import html

#-------------
#-EXTRACT API-
#-------------

def retrieve_api_key():
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(
        SecretId = "guardian_api_key"
    )
    parsed_secret = json.loads(response["SecretString"])
    return parsed_secret["api_key"]

def get_search_params(search_term: str, api_key, from_date: str = None):
    """
    Create a search dictionary and broker ID for Guardian API.

    Parameters:
        search_term (str): The term to search for.
        from_date (str): Optional start date in 'yyyy/mm/dd' format.
        message_broker_id (str): The message broker ID to publish to.

    Returns:
        dictionary: search_dict
    """
    
    stripped_search_term = search_term.strip()

    search_dict = {
        "q": stripped_search_term, 
        "from-date": None,
        "show-fields": "body",
        "api-key": api_key
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
    


def extract_api(search_term: str, from_date: str = None):
    api_key = retrieve_api_key()
    search_dict = get_search_params(search_term, api_key, from_date)
    article_data = guardian_api_call(search_dict)
    return article_data

#----------------
#-Transform Data-
#----------------

def order_by_newest(api_data: dict):
    articles = api_data["response"]["results"]
    sorted_articles = sorted(articles, key=lambda x: x["webPublicationDate"], reverse=True)
    with open("sorted.json", "w") as f:
        json.dump(sorted_articles, f, indent=2)

    return sorted_articles

def extract_relevant_fields(api_data: dict):
    articles = []

    for article in api_data:
        kinesis_record = {}
        article_data = {}
        article_data["webPublicationDate"] = article["webPublicationDate"]
        article_data["webTitle"] = article["webTitle"]
        article_data["webUrl"] = article["webUrl"]
        tree = html.fromstring(article["fields"]["body"][:1000])
        article_preview = tree.text_content()
        article_data["content_preview"] = article_preview
        kinesis_record["Data"] = json.dumps(article_data)
        kinesis_record["PartitionKey"] = article["sectionName"]
        articles.append(kinesis_record)
    
    return articles

def transform_data(api_data: dict):
    sorted_articles = order_by_newest(api_data)
    data = extract_relevant_fields(sorted_articles)
    with open("transform.json", "w") as f:
        json.dump(data, f, indent=2)
    
    return data 

#-----------
#-Load Data-
#-----------

def publish_to_kinesis(article_data: json, broker_id: str):
    client = boto3.client('kinesis', region_name="eu-west-2")
    
    response = client.put_records(
        Records = article_data,
        StreamName = broker_id,
    )
    print("Kinesis response:", response)
    return response

#----------------------
#-Orchestrate function-
#----------------------

def stream_articles(search_term: str, message_broker_id: str, from_date: str = None):
    article_data = extract_api(search_term, from_date)
    transformed_data = transform_data(article_data)
    publish_to_kinesis(transformed_data, message_broker_id)

stream_articles("Rock Climbing", "Guardian_content", "2020/01/01")