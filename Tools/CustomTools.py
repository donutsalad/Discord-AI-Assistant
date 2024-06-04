import Tools.Custom.ReadPDF
import Tools.ToolCall
import Tools.CustomTool
import json


customtools = [
  {
    'tool_id': "read_pdf", "description": "Read the contents of a pdf in order to fufill the users requests.", 
    "ParameterOne": "File name of the pdf.", "ParameterTwo": "None", "ParameterThree": "None", "ParameterFour": "None",
    "method": Tools.Custom.ReadPDF.ReadPDF
  }
]

def GetAvailableCustomTools(tool_call: Tools.ToolCall.ToolCall):
  return json.dumps([
    Tools.CustomTool.CustomTool(tool["tool_id"], tool["description"], tool["ParameterOne"], tool["ParameterTwo"], tool["ParameterThree"], tool["ParameterFour"]).as_dict()
    for tool in customtools
  ])

def CallCustomTool(tool_call: Tools.ToolCall.ToolCall):
    
    for tool in customtools:
      if tool["tool_id"] == tool_call.args["tool_id"]:
        return tool["method"](Tools.CustomTool.CustomTool(tool_call.args["tool_id"], tool["description"], tool_call.args["ParameterOne"], tool_call.args["ParameterTwo"], tool["ParameterThree"], tool["ParameterFour"]))
      
    return "Please let the user know that this tool isn't implemented yet"
  