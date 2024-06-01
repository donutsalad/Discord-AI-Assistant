import requests
from bs4 import BeautifulSoup, ResultSet
from googleapiclient.discovery import build

import Tools.ToolCall 
import json
import Tools.GoogleSearch
import Tools.WebTools
import Tools.WebTool
  
def SearchGoogle(tool_call: Tools.ToolCall.ToolCall):
  
  if tool_call.args.get("Count") is None: count = 1
  else: count = int(tool_call.args["Count"])
  
  return json.dumps(Tools.GoogleSearch.GetGoogleSearches("all", tool_call.args["Query"], count))
  
  
def ReadPageFromGoogle(tool_call: Tools.ToolCall.ToolCall):
  return json.dumps(Tools.WebTools.ReadGenericPage(Tools.WebTools.read_generic_page(Tools.WebTool.WebTool("", "", tool_call.args["URL"], ""))))