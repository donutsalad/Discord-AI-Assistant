import requests
from bs4 import BeautifulSoup, ResultSet
from googleapiclient.discovery import build

import Tools.ToolCall
import Tools.GoogleSearch
  
def GetNCBIPage(url: str):
  url = f"{url}/?report=printable"
  html = requests.get(url, headers = Tools.GoogleSearch.headers).text
  soup = BeautifulSoup(html, features="html.parser")

  results: ResultSet = soup.find_all("p")
  
  return [
    entry.text
    for entry in results
  ]
  