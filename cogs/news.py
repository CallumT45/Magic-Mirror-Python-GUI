from newsapi import NewsApiClient
from cogs import LoginsAndKeys as LaK
def main():
    # Init
    newsapi = NewsApiClient(api_key=LaK.api_keys["newsKey"])

    top_headlines = newsapi.get_top_headlines(category='general',
                                              language='en',
                                              country='ie')
    news_List = []
    for i in range(len(top_headlines['articles'])):
        news_List.append(top_headlines['articles'][i]['title'])
    return news_List



