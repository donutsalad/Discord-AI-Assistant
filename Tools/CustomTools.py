import Tools.ToolCall
import Tools.CustomTool
import json


customtools = [
  
]

def GetAvailableCustomTools(tool_call: Tools.ToolCall.ToolCall):
  return json.dumps([
    Tools.CustomTool.CustomTool(tool["tool_id"], tool["description"], tool["ParameterOne"], tool["ParameterTwo"], tool["ParameterThree"], tool["ParameterFour"]).as_dict()
    for tool in customtools
  ])

def CallCustomTool(tool_call: Tools.ToolCall.ToolCall):
    
    for tool in customtools:
      if tool["tool_id"] == tool_call.args["tool_id"]:
        return tool["method"](Tools.WebTool.WebTool(tool_call.args["tool_id"], tool["description"], tool_call.args["ParameterOne"], tool_call.args["ParameterTwo"], tool["ParameterThree"], tool["ParameterFour"]))
      
    return "Please let the user know that this tool isn't implemented yet"
  