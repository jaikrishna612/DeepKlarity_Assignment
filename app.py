from flask import Flask, request, jsonify, render_template
import csv
import json
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
def csv_to_dict(file_path, key_column=None):
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        if key_column is None:
            key_column = reader.fieldnames[0]
        
        data_dict = {}
        for row in reader:
            key = row.get(key_column)
            if key is not None:
                data_dict[key] = row  # Store the entire row as the value
            else:
                print(f"Warning: The specified key column '{key_column}' is missing in the row {row}")

        news_reports = [
            {
                "title": details["Title"],
                "category": details["Category"],
                "predicted_category": details["Predicted Category"],
                "publication_date": details["Publication Date"],
                "source": details["Source"],
                "summary": details["Summary"],
                "url": details["URL"],
                "id" : idx + 1
            }
            for idx,details in enumerate(data_dict.values())
        ]
        
    return news_reports

def fetch_articles_by_date_range(articles, start, end=None):
    final_result = []
    start_date = datetime.fromisoformat(start)

    end_date = datetime.fromisoformat(end) if end else datetime.now()

    for article in articles:
        try:
            publication_date = datetime.strptime(article.get("publication_date"), "%a, %d %b %Y %H:%M:%S %Z")
        except ValueError as e:
            print(f"Date parsing error: {e}")
            continue  

        if start_date <= publication_date <= end_date:
            article_data = {
                'id' : article.get('id'),
                'title': article.get('title'),
                'summary': article.get('summary'),
                'publication_date': article.get('publication_date'),
                'source': article.get('source'),
                'url': article.get('url'),
                'category': article.get('predicted_category'),
                "predicted_category": article["predicted_category"]
            }
            final_result.append(article_data)

    return final_result

def filter_articles_by_category(articles, category):
    final_result = []
    print(category)
    for article in articles:
        if article["predicted_category"].lower() == category.lower():
            article_data = {
                'id' : article.get('id'),
                "title": article["title"],
                "summary": article["summary"],
                "publication_date": article["publication_date"],
                "source": article["source"],
                "url": article["url"],
                "category": article["predicted_category"],
                "predicted_category": article["predicted_category"]
            }
            final_result.append(article_data)
    return final_result

def filter_articles_by_key_word(articles, keyWord):
    final_result = []
    print(keyWord)
    for article in articles:
        if keyWord.lower() in article["title"].lower() or keyWord.lower() in article["summary"].lower(): 
            article_data = {
                'id' : article.get('id'),
                "title": article["title"],
                "summary": article["summary"],
                "publication_date": article["publication_date"],
                "source": article["source"],
                "url": article["url"],
                "category": article["predicted_category"],
                "predicted_category": article["predicted_category"]
            }
            final_result.append(article_data)
    return final_result

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/getAllArticles', methods=['GET'])
def get_articles():
    category = request.args.get('category')
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')
    key = request.args.get('key')
    
    # Read articles from CSV
    articles = csv_to_dict('./news_articles_with_predicted_categories.csv')
    if category or start_date or end_date or key:
        if category :
            articles = filter_articles_by_category(articles, category)
        if start_date or end_date:
            articles = fetch_articles_by_date_range(articles, start_date, end_date)
        if key:
            articles = filter_articles_by_key_word(articles, key)
        return jsonify({"status": 200, "message": "Successful!", "data": articles})
    else:
        return jsonify({"status": 204, "message": "Missing Parameters"})

@app.route('/getArticle', methods=['GET'])
def get_articles_id():
    id = request.args.get('id')
    # Read articles from CSV
    articles = csv_to_dict('./news_articles_with_predicted_categories.csv')
    if id:
        article = [i for i in articles if int(i.get("id")) == int(id)]
        print(article,id)
        if not article:
            return jsonify({"status": 204, "message": "Invalid id"})
        else:
            return jsonify({"status": 200, "message": "Successful!", "data": article[0]})
    else:
        return jsonify({"status": 204, "message": "Missing Parameters"})