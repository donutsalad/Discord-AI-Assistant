import requests
from bs4 import BeautifulSoup, ResultSet
from googleapiclient.discovery import build

import Tools.Web.PhysOrg
import Tools.Web.Neuroscience
import Tools.ToolCall
import Tools.WebTool
import json

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
  
#Not sure if this is the best technique
def ReadGenericPage(web_tool: Tools.WebTool.WebTool):
  url = web_tool.paramone
  html = requests.get(url, headers = headers).text
  soup = BeautifulSoup(html, features="html.parser")

  results: ResultSet = soup.find_all(string = True)
  
  return [
    entry.text
    for entry in results
  ]

webtools = [
  {"tool_id": "get_latest_physorg_articles", "description": "Get the latest news articles from phys.org", "ParameterOne": "None", "ParameterTwo": "None", "method": Tools.Web.PhysOrg.get_latest_phys_articles},
  {"tool_id": "search_physorg_articles", "description": "Search phys.org for news articles based on a query", "ParameterOne": "Query string to search with", "ParameterTwo": "None", "method": Tools.Web.PhysOrg.search_physorg_articles},
  {"tool_id": "read_physorg_article", "description": "Read an article on phys.org", "ParameterOne": "URL of the article", "ParameterTwo": "None", "method": Tools.Web.PhysOrg.read_physorg_article},
  
  {"tool_id": "get_latest_neuroscience_articles", "description": "Get the latest news articles from Neuroscience News", "ParameterOne": "None", "ParameterTwo": "None", "method": Tools.Web.Neuroscience.get_latest_neuro_articles},
  {"tool_id": "search_neuroscience_articles", "description": "Search Neuroscience News for news articles based on a query", "ParameterOne": "Query string to search with", "ParameterTwo": "None", "method": Tools.Web.Neuroscience.search_neuro_articles},
  {"tool_id": "read_neuroscience_article", "description": "Read an article from Neuroscience News", "ParameterOne": "URL of the article", "ParameterTwo": "None", "method": Tools.Web.Neuroscience.read_neuro_article}
]

def GetAvailableWebTools(tool_call: Tools.ToolCall.ToolCall):
  return json.dumps([
    Tools.WebTool.WebTool(tool["tool_id"], tool["description"], tool["ParameterOne"], tool["ParameterTwo"]).as_dict()
    for tool in webtools
  ])

def CallWebTool(tool_call: Tools.ToolCall.ToolCall):
    
    for tool in webtools:
      if tool["tool_id"] == tool_call.args["tool_id"]:
        return tool["method"](Tools.WebTool.WebTool(tool_call.args["tool_id"], tool["description"], tool_call.args["ParameterOne"], tool_call.args["ParameterTwo"]))
      
    return "Please let the user know that this tool isn't implemented yet"
  