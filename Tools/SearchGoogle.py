import requests
from bs4 import BeautifulSoup, ResultSet
from googleapiclient.discovery import build

import Tools.ToolCall 
import json
import Tools.GoogleSearch
  
def GetPageFromGoogle(url: str):
  url = url
  html = requests.get(url, headers = Tools.GoogleSearch.headers).text
  soup = BeautifulSoup(html, features="html.parser")

  results: ResultSet = soup.find_all("p")
  
  return [
    entry.text
    for entry in results
  ]
  
def SearchGoogle(tool_call: Tools.ToolCall.ToolCall):
  if tool_call.args.get("Count") is None:
    count = 1
    
  else: count = int(tool_call.args["Count"])
  
  return json.dumps(Tools.GoogleSearch.GetGoogleSearches("all", tool_call.args["Query"], count))
  
def ReadPageFromGoogle(tool_call: Tools.ToolCall.ToolCall):
  
  return json.dumps(GetPageFromGoogle(tool_call.args["URL"]))