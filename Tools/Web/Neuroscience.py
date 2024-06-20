import requests
from bs4 import BeautifulSoup, ResultSet
from googleapiclient.discovery import build

import Tools.WebTool 
import json

class NeuroPost:
    def __init__(self, link, text) -> None:
        self.link = link
        self.text = text

    def as_dict(self):
        return {
            "Link": self.link,
            "Title": self.text
        }


def GetLatestNews():
  
    url = "https://neurosciencenews.com/"
    html = requests.get(url, headers = Tools.WebTools.headers).text
    soup = BeautifulSoup(html, features="html.parser")

    posts = soup.find("div", class_ = "block-wrap")
    results: ResultSet = posts.find_all("a")
    
    return [
        NeuroPost(result["href"], result.content).as_dict()
        for result in results
    ]

def SearchNeuroArticles(query: str):
  
    url = f"https://neurosciencenews.com/?s={query}"
    html = requests.get(url, headers = Tools.WebTools.headers).text
    soup = BeautifulSoup(html, features="html.parser")

    posts = soup.find("div", class_ = "main-block-wrap")
    results: ResultSet = posts.find_all("a")
    
    return [
        NeuroPost(result["href"], result.content).as_dict()
        for result in results
    ]

#

def ReadNeuroArticle(url: str):
    
    html = requests.get(url, headers = Tools.WebTools.headers).text
    soup = BeautifulSoup(html, features="html.parser")
    
    results: ResultSet = soup.find_all("p")
    
    return [
        result.text
        for result in results
    ]

  
def get_latest_neuro_articles(web_tool: Tools.WebTool.WebTool):
    return json.dumps({
        "Instruction": "Give a summary of the available news stories to the user",
        "Entries": GetLatestNews()
    })
  

def search_neuro_articles(web_tool: Tools.WebTool.WebTool):
    return json.dumps({
        "Instruction": "Give a summary of the available news stories to the user",
        "Entries": SearchNeuroArticles(web_tool.paramone)
    })

  
def read_neuro_article(web_tool: Tools.WebTool.WebTool):
    return json.dumps({
        "Instruction": "Give a summary of the news story to the user",
        "Paragraphs": ReadNeuroArticle(web_tool.paramone)
    })
  