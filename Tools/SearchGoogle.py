import json
import requests
from bs4 import BeautifulSoup, ResultSet
from googleapiclient.discovery import build

import Tools.ToolCall 
import Tools.GoogleSearch
import Tools.WebTools
import Tools.WebTool
  
import Tools.Web.NCBI
import Tools.Web.StackExchange
import Tools.Web.PhysOrg
  
def SearchGoogle(tool_call: Tools.ToolCall.ToolCall):
  
  query = tool_call.args["Query"]
  
  if tool_call.args.get("Count") is None: count = 1
  else: count = int(tool_call.args["Count"])
  
  if tool_call.args.get("SearchTools") is not None:
    query = f"{query} {tool_call.args["SearchTools"]}"
  
  return json.dumps(Tools.GoogleSearch.GetGoogleSearches("all", query, count))
  
  
def ReadPageFromGoogle(tool_call: Tools.ToolCall.ToolCall):

  if "stackoverflow.com" in tool_call.args["URL"] or "superuser.com" in tool_call.args["URL"] or "mathoverflow.new" in tool_call.args["URL"] or "serverfault.com" in tool_call.args["URL"]:
    return json.dumps(Tools.Web.StackExchange.GetStackPage(tool_call.args["URL"]))
  
  if "pubmed.ncbi.nlm.nih.gov" in tool_call.args["URL"]:
    return json.dumps(Tools.Web.NCBI.GetNCBIPage(tool_call.args["URL"]))
  
  if "phys.org" in tool_call.args["URL"]:
    return json.dumps(Tools.Web.PhysOrg.ReadPhysOrgArticle(tool_call.args["URL"]))
    
  
  return json.dumps(Tools.WebTools.ReadGenericPage(Tools.WebTool.WebTool("", "", tool_call.args["URL"], "")))