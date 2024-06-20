import requests
from bs4 import BeautifulSoup, ResultSet
from googleapiclient.discovery import build

import Tools.ToolCall
import Tools.WebTools
  
def GetNCBIPage(url: str):
  url = f"{url}/?report=printable"
  html = requests.get(url, headers = Tools.WebTools.headers).text
  soup = BeautifulSoup(html, features="html.parser")

  results: ResultSet = soup.find_all("p")
  
  return [
    entry.text
    for entry in results
  ]
  