import requests
from bs4 import BeautifulSoup, ResultSet
from googleapiclient.discovery import build

import Tools.WebTool
import json

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
  
class PhysOrgArticle:
    def __init__(self, link, text) -> None:
        self.link = link
        self.text = text

    def as_dict(self):
        return {
            "Link": self.link,
            "Title": self.text
        }


def GetLatestPhysOrg():
  
    url = "https://phys.org/latest-news/"
    html = requests.get(url, headers = headers).text
    soup = BeautifulSoup(html, features="html.parser")

    results: ResultSet = soup.find_all("a", class_="news-link")
    
    return [
        PhysOrgArticle(result["href"], result.content).as_dict()
        for result in results
    ]

def SearchPhysOrgArticles(query: str):
  
    url = f"https://phys.org/search/?search={query}&s=0"
    html = requests.get(url, headers = headers).text
    soup = BeautifulSoup(html, features="html.parser")

    results: ResultSet = soup.find_all("a", class_="news-link")
    
    return [
        PhysOrgArticle(result["href"], result.content).as_dict()
        for result in results
    ]

#

def ReadPhysOrgArticle(url: str):
    
    html = requests.get(url, headers = headers).text
    soup = BeautifulSoup(html, features="html.parser")

    article = soup.find("article")
    results: ResultSet = article.find_all("p")
    
    return [
        result.text
        for result in results
    ]

  
def get_latest_phys_articles(web_tool: Tools.WebTool.WebTool):
    return json.dumps({
        "Instruction": "Give a summary of the available news stories to the user",
        "Entries": GetLatestPhysOrg()
    })
  

def search_physorg_articles(web_tool: Tools.WebTool.WebTool):
    return json.dumps({
        "Instruction": "Give a summary of the available news stories to the user",
        "Entries": SearchPhysOrgArticles(web_tool.paramone)
    })

  
def read_physorg_article(web_tool: Tools.WebTool.WebTool):
    return json.dumps({
        "Instruction": "Give a summary of the available news stories to the user",
        "Paragraphs": ReadPhysOrgArticle(web_tool.paramone)
    })
  