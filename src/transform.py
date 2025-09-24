import json

def order_by_newest(api_data: dict):
    articles = api_data["response"]["results"]
    sorted_articles = sorted(articles, key=lambda x: x["webPublicationDate"], reverse=True)
    with open("sorted.json", "w") as f:
        json.dump(sorted_articles, f, indent=2)

    return sorted_articles

def extract_relevant_fields(api_data: dict):
    articles = []

    for article in api_data:
        article_data = {}
        article_data["webPublicationDate"] = article["webPublicationDate"]
        article_data["webTitle"] = article["webTitle"]
        article_data["webUrl"] = article["webUrl"]
        article_data["content_preview"] = article["fields"]["body"][:1000]
        articles.append(article_data)
    
    return articles

def transform_data(api_data: dict):
    sorted_articles = order_by_newest(api_data)
    data = extract_relevant_fields(sorted_articles)
    with open("transform.json", "w") as f:
        json.dump(data, f, indent=2)
    return data 

# test code 
with open("sample.json", "r") as f:
    data = json.load(f)
transform_data(data)