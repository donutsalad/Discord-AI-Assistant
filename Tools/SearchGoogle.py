import json
import requests
from bs4 import BeautifulSoup, ResultSet
from googleapiclient.discovery import build

import Tools.ToolCall 
import Tools.GoogleSearch
import Tools.WebTools
import Tools.WebTool
  
def SearchGoogle(tool_call: Tools.ToolCall.ToolCall):
  
  if tool_call.args.get("Count") is None: count = 1
  else: count = int(tool_call.args["Count"])
  
  return json.dumps(Tools.GoogleSearch.GetGoogleSearches("all", tool_call.args["Query"], count))
  
  
def ReadPageFromGoogle(tool_call: Tools.ToolCall.ToolCall):

  if "stackoverflow.com" in tool_call.args["URL"] or "superuser.com" in tool_call.args["URL"] or "mathoverflow.new" in tool_call.args["URL"] or "serverfault.com" in tool_call.args["URL"]:
      
    html = requests.get(tool_call.args["URL"], headers = Tools.WebTools.headers).text
    soup = BeautifulSoup(html, features="html.parser")

    answers = soup.find_all("div", class_ = "answercell")
    answers = [answer.find("div", class_ = "s-prose") for answer in answers]
    results: ResultSet = [answer.find_all(string = True) for answer in answers]
    
    return json.dumps(results)
    
  
  return json.dumps(Tools.WebTools.read_generic_page(Tools.WebTool.WebTool("", "", tool_call.args["URL"], "")))