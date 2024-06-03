import requests
from bs4 import BeautifulSoup, ResultSet
from googleapiclient.discovery import build

import Tools.ToolCall
import Tools.GoogleSearch
  
def GetStackPage(url: str):      
  html = requests.get(url, headers = Tools.GoogleSearch.headers).text
  soup = BeautifulSoup(html, features="html.parser")

  answers = soup.find_all("div", class_ = "answercell")
  answers = [answer.find("div", class_ = "s-prose") for answer in answers]
  results: ResultSet = [answer.find_all(string = True) for answer in answers]
  
  return results
  