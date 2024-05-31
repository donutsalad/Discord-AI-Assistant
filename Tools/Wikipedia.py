import wikipedia
import json
import Tools.ToolCall

def SearchWikipedia(tool_call: Tools.ToolCall.ToolCall) -> str:
  try:
    result = wikipedia.WikipediaPage(tool_call.args["Query"]).content
  except Exception as e:
    result = "Let the user know that you couldn't find a page for the specific query, and let them know what the query was."
    
  return json.dumps(result)

def GetWikipediaReferences(tool_call: Tools.ToolCall.ToolCall) -> str:
  try:
    result = wikipedia.WikipediaPage(tool_call.args["Query"]).references
  except Exception as e:
    result = "Let the user know that you couldn't find a page for the specific query, and let them know what the query was."
    
  return json.dumps(result)