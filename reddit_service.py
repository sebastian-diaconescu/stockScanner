import requests
from bs4 import BeautifulSoup

class RedditLoader:
   def GetPostsFrom(self, sub):
        topCount = 20
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
        while(i < len(postsDivs) and i < topCount):
            res = []
            postContentDivs = postsDivs[i].find_all("div")

            title = postsDivs[i].find("h3").text
            res.append({"title":title})

            if (postContentDivs != None):
                for j in range (len(postContentDivs)):
                    divText = postContentDivs[j].text
                    res.append(divText)
                    pass
                allArticles.append(res)
            
            i = i + 1                      

        return allArticles
