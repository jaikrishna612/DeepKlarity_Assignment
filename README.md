Overview
This project is a News Aggregator that scrapes articles from multiple online sources, categorizes them using Natural Language Processing (NLP), and provides access to the aggregated content via a REST API and a simple front-end interface.

Features
Web Scraping: Automatically scrapes news articles from various websites.
Article Categorization: Categorizes articles into topics such as Technology, Sports, Business, etc.
REST API: Provides endpoints to access news articles and categories.
Front-end Interface: Displays articles categorized by topics.
Article Search: Allows searching for articles based on keywords or categories.

How It Works
Scraping:
webScraping11.py collects articles from predefined sources, extracting details like title, summary, and publication date.
For web scraping used beautifulsoup.
Categorization:
webScraping11.py processes the articles and classifies them into various topics.
for categorizing them into topics used nlp and used navie bayes as classifier
API:
The API provides access to the articles, allowing filtering by category or searching by keywords.
Front-End:
The user interface allows users to view categorized articles and search through them.
Endpoints (REST API)
GET /api/articles: Fetch all articles.
GET /api/articles/<category>: Fetch articles filtered by category.
GET /api/search?query=<keyword>: Search articles by keyword.
GET /api/article/<id>: Fetch details of a specific article.
