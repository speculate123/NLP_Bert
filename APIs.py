import config
import math
import requests
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
from twitter import Twitter
from twitter import OAuth

class TwitterAPI():   
    def __init__(self):
        self.oauth = OAuth (config.accesstoken, config.accesstokensecret, config.apikey, config.apisecretkey)
        self.api = Twitter(auth = self.oauth)
        print("Connecting to Twitter....")        
    def search(self, keyword, num):
        api = self.api
        search_result = api.search.tweets(q = keyword, count = num, tweet_mode = 'extended')
        dfsr = json_normalize(search_result)
        dfst = json_normalize(dfsr.statuses.values[0])
        return dfst.full_text.tolist()
class GSAPI():
    def __init__(self):
        self.results = []
    def search(self, keyword, num):
        results = []
        for i in range(math.floor(num/10)):
            url = f"https://www.googleapis.com/customsearch/v1?key={config.gsapikey}&cx={config.gscseid}&q={keyword}&start={i*10+1}"
            data = requests.get(url).json()
            search_items = data.get("items")
            for i, search_item in enumerate(search_items, start=1):
                snippet = search_item.get("snippet")
                results.append(snippet)
        return results
        
        
        
        
        
#def update_output(n_clicks, value):
#    query = value
#    url = f"https://www.googleapis.com/customsearch/v1?key={apikey}&cx={cseid}&q=#{query}&start={start}"
#    # make the API request
#    data = requests.get(url).json()
#    # get the result items
#    search_items = data.get("items")
#    resultss = []
#    for i, search_item in enumerate(search_items, start=1):
#        # get the page title
#        title = search_item.get("title")
#        # page snippet
#        snippet = search_item.get("snippet")
#        # alternatively, you can get the HTML snippet (bolded keywords)
#        html_snippet = search_item.get("htmlSnippet")
#        # extract the page url
#        link = search_item.get("link")
    