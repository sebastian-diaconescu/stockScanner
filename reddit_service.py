import requests
from bs4 import BeautifulSoup
import praw
import pandas as pd
import datetime as dt

class RedditLoader:
    def GetPostsFromPraw(self, sub):
        return "yes"
           
   def GetPostsFromBF(self, sub):
        topCount = 2000
        minNewsLength = 20
        pageURl = "https://www.reddit.com/r/" + sub + "/new"

        headers={'User-Agent': 'Mozilla/5.0'}
        #TODO: move this into a method to optimize number of calls to finviz
        response = requests.get(pageURl, headers=headers)
        if (response.status_code != 200):
            return "no response from page " + response.status_code
        
        soup = BeautifulSoup(response.content, 'html.parser')
        postsDivs = soup.find_all("div", {"class": "Post"})      

        if (postsDivs == None):
            return []

        allArticles = []
        i = 0
        storedCount = 0
        return len(postsDivs)
        while(i < len(postsDivs) and storedCount < topCount):            
            title = postsDivs[i].find("h3").text
            
            postContents = postsDivs[i].find_all("p")
            if (postContents != None):
                content = ""
                for j in range (len(postContents)):
                    divText = postContents[j].text
                    content += divText
                    pass 

            if (len(content) > minNewsLength):
                res = {"title":title, "news":content}
                storedCount = storedCount + 1
                allArticles.append(res)
            
            i = i + 1                      

        return allArticles