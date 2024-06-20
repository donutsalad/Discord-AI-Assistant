import json
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