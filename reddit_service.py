import requests
from bs4 import BeautifulSoup

class RedditLoader:
   def GetPostsFrom(self, sub):
        topCount = 5
        pageURl = "https://www.reddit.com/r/" + sub + "/new"

        headers={'User-Agent': 'Mozilla/5.0'}
        #TODO: move this into a method to optimize number of calls to finviz
        response = requests.get(pageURl, headers=headers)
        if (response.status_code != 200):
            return "no response from page " + response.status_code
        
        soup = BeautifulSoup(response.content, 'html.parser')
        postsDiv = soup.find_all("div", {"class": "Post"})

        allArticles = []
        i = 0

        if (postsDiv == None):
            return []

        while(i<len(postsDiv) and i < topCount):
            res = []
            postContentDivs = postsDiv.find("div")
            if (postContentDivs != None):
                for i in range (postContentDivs.len):
                    divText = postContentDivs[i].text
                    res.append(divText)
                    pass
                allArticles.append(res)
            
            i = i + 1                      

        return allArticles
