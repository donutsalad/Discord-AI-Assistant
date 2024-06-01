import requests
from bs4 import BeautifulSoup, ResultSet
from googleapiclient.discovery import build

import Tools.ToolCall 
import json
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
  
def search_ncbi(tool_call: Tools.ToolCall.ToolCall):
  if tool_call.args.get("Count") is None:
    count = 1
    
  else: count = int(tool_call.args["Count"])
  
  return json.dumps(Tools.GoogleSearch.GetGoogleSearches("ncbi.nlm.nih.gov", tool_call.args["Query"], count))
  
def read_ncbi(tool_call: Tools.ToolCall.ToolCall):
  
  return json.dumps(GetNCBIPage(tool_call.args["URL"]))
  