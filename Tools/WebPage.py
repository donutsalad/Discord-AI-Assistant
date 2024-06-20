import json

import Tools.ToolCall 
import Tools.GoogleSearch
import Tools.WebTools
import Tools.WebTool
  
import Tools.Web.NCBI
import Tools.Web.StackExchange
import Tools.Web.PhysOrg
  
def ReadSite(tool_call: Tools.ToolCall.ToolCall):

  if "stackoverflow.com" in tool_call.args["URL"] or "superuser.com" in tool_call.args["URL"] or "mathoverflow.new" in tool_call.args["URL"] or "serverfault.com" in tool_call.args["URL"]:
    return json.dumps(Tools.Web.StackExchange.GetStackPage(tool_call.args["URL"]))
  
  if "pubmed.ncbi.nlm.nih.gov" in tool_call.args["URL"]:
    return json.dumps(Tools.Web.NCBI.GetNCBIPage(tool_call.args["URL"]))
  
  if "phys.org" in tool_call.args["URL"]:
    return json.dumps(Tools.Web.PhysOrg.ReadPhysOrgArticle(tool_call.args["URL"]))
    
  
  return json.dumps(Tools.WebTools.ReadGenericPage(Tools.WebTool.WebTool("", "", tool_call.args["URL"], "")))