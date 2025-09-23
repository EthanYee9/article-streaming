import json

def order_by_newest(api_data: dict):
    articles = api_data["response"]["results"]
    sorted_articles = sorted(articles, key=lambda x: x["webPublicationDate"], reverse=True)
    with open("sorted.json", "w") as f:
        json.dump(sorted_articles, f, indent=2)

    return sorted_articles

def extract_relevant_fields(api_data: dict):
    article_data = {}

    for article in api_data["response"]["results"]:
        article_data["webPublicationDate"] = article["webPublicationDate"]
        article_data["webTitle"] = article["webTitle"]
        article_data["webUrl"] = article["webUrl"]
    return article_data


# test code 
with open("sample.json", "r") as f:
    data = json.load(f)
extract_relevant_fields(data)