import requests
from datetime import datetime
import json
import boto3
from lxml import html

# -------------
# -EXTRACT API-
# -------------


def retrieve_api_key(message_broker_id):
    """
    Retrieves api key saved to AWS Secrets Manager

    Parameters:
    message broker id (str): message broker identifier used to search for api key.

    Returns:
        string: The API key associated with the given message broker.
    """

    client = boto3.client("secretsmanager")
    response = client.get_secret_value(
        # SecretId = "guardian_api_key"
        SecretId=message_broker_id
    )
    parsed_secret = json.loads(response["SecretString"])
    return parsed_secret["api_key"]


def get_search_params(search_term: str, api_key, from_date: str = None):
    """
    Create a search dictionary and broker ID for Guardian API.

    Parameters:
        search_term (str): The term to search for.
        message_broker_id (str): The message broker ID to publish to.
        from_date (str): Optional start date in 'yyyy/mm/dd' format.

    Returns:
        dictionary: search_dict
    """

    search_dict = {
        "q": search_term.strip(),
        "from-date": None,
        "show-fields": "body",
        "api-key": api_key,
    }

    if from_date:
        try:
            search_dict["from-date"] = datetime.strptime(from_date, "%Y/%m/%d").date()
        except ValueError:
            raise ValueError(
                "from_date must be in the format of yyyy/mm/dd, e.g. 2001/06/17"
            )

    return search_dict


def guardian_api_call(search_dict: dict):
    """
    Call the Guardian API with search parameters and return the JSON data.

    Parameters:
        search_dict (dict): Dictionary containing search parameters for the API.

    Returns:
        dict: Parsed JSON response from the Guardian API.
    """

    URL = "https://content.guardianapis.com/search"
    response = requests.get(URL, params=search_dict, timeout=10)
    data = response.json()
    return data


def extract_api(search_term: str, message_broker_id: str, from_date: str = None):
    """
    Orchestrates a Guardian API request to retrieve articles based on a search term and optional date.

    Parameters:
        search_term (str): The keyword(s) to search for in Guardian articles.
        message_broker_id (str): Identifier for the message broker (used to retrieve API key from Secrets Manager).
        from_date (str, optional): Start date for the search in 'YYYY/MM/DD' format. Defaults to None.

    Returns:
        dict: Parsed JSON response from the Guardian API containing article data.
    """

    api_key = retrieve_api_key(message_broker_id)
    search_dict = get_search_params(search_term, api_key, from_date)
    article_data = guardian_api_call(search_dict)
    return article_data


# ----------------
# -Transform Data-
# ----------------


def order_by_newest(api_data: dict):
    """
    Sorts Guardian API articles by publication date, newest first.

    Parameters:
        api_data (dict): The JSON response from the Guardian API, expected to contain
                         a "response" key with "results" as a list of articles.

    Returns:
        list: Articles sorted by 'webPublicationDate' in descending order (newest first).
    """

    articles = api_data["response"]["results"]
    sorted_articles = sorted(
        articles, key=lambda x: x["webPublicationDate"], reverse=True
    )
    return sorted_articles


def extract_relevant_fields(api_data: dict):
    """
    Extracts relevant fields from Guardian API article data and prepares it for Kinesis.

    Parameters:
        api_data (dict): List of article dictionaries returned by the Guardian API.
                         Each article should contain keys like "webPublicationDate",
                         "webTitle", "webUrl", and "fields" with a "body" key.

    Returns:
        list: A list of dictionaries, each representing a Kinesis record with:
            - "Data": JSON string containing extracted fields including a plain-text
                      preview of the article body (first 1000 characters, HTML stripped).
            - "PartitionKey": The section name of the article.
    """

    articles = []

    for article in api_data:
        kinesis_record = {}
        article_data = {}
        article_data["webPublicationDate"] = article["webPublicationDate"]
        article_data["webTitle"] = article["webTitle"]
        article_data["webUrl"] = article["webUrl"]

        # convert html code to string
        tree = html.fromstring(article["fields"]["body"][:1000])
        article_preview = tree.text_content()

        article_data["content_preview"] = article_preview
        kinesis_record["Data"] = json.dumps(article_data, ensure_ascii=False)
        print(kinesis_record["Data"])
        kinesis_record["PartitionKey"] = article["sectionName"]
        articles.append(kinesis_record)

    return articles


def transform_data(api_data: dict):
    """
    Orchestrates the transformation of Guardian API data for Kinesis.

    Steps:
        1. Sort articles by newest publication date.
        2. Extract relevant fields and convert HTML body to plain-text preview.
        3. Prepare Kinesis-ready records.

    Parameters:
        api_data (dict): Raw API response from the Guardian API.

    Returns:
        list: A list of dictionaries, each representing a Kinesis record with:
            - "Data": JSON string of extracted fields.
            - "PartitionKey": The article's section name.
    """

    sorted_articles = order_by_newest(api_data)
    data = extract_relevant_fields(sorted_articles)
    return data


# -----------
# -Load Data-
# -----------


def publish_to_kinesis(article_data: json, broker_id: str):
    """
    Publishes a batch of articles to an AWS Kinesis stream.

    Parameters:
        article_data (list of dict): Each dict must have "Data" (JSON string) and "PartitionKey".
        broker_id (str): Kinesis stream name.

    Returns:
        dict: Response from Kinesis put_records call.
    """

    client = boto3.client("kinesis", region_name="eu-west-2")

    response = client.put_records(
        Records=article_data,
        StreamName=broker_id,
    )
    print("Kinesis response:", response)
    return response


# ----------------------
# -Orchestrate function-
# ----------------------


def stream_articles(event_dict: dict, context=None):
    """
    Orchestrates the process of fetching, transforming, and publishing articles to AWS Kinesis.

    This function performs the following steps:
        1. Extracts search parameters from the incoming event dictionary.
        2. Calls the Guardian API to retrieve articles based on the search parameters.
        3. Sorts and transforms the article data for Kinesis consumption.
        4. Publishes the processed records to the specified Kinesis stream.

    Parameters:
        event_dict (dict): A dictionary containing search parameters.
            Expected keys:
                - "search term" (str): The query string for the Guardian API.
                - "message_broker_id" (str): The Kinesis stream name to publish to.
                - "from_date" (str, optional): Start date for filtering articles (format "YYYY/MM/DD").
        context (object, optional): Lambda runtime information (not used in this function).

    Returns:
        None.
    """

    search_term = event_dict["search term"]
    message_broker_id = event_dict["message_broker_id"]
    from_date = event_dict["from_date"]

    article_data = extract_api(search_term, message_broker_id, from_date)
    transformed_data = transform_data(article_data)
    publish_to_kinesis(transformed_data, message_broker_id)
