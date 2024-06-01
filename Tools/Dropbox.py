import asyncio
import glob
import json
import os
import Tools.ToolCall
from discord import File

def list_dropbox_files(tool_call: Tools.ToolCall.ToolCall) -> str:
  return json.dumps(glob.glob("dropbox/*"))

def upload_dropbox_file(tool_call: Tools.ToolCall.ToolCall):
  file: str = tool_call.args["FileName"]
  if not file.startswith("dropbox/"):
    file = f"dropbox/{file}"
  
  if not os.path.exists(file):
    return "File does not exist."
  
  else:
    asyncio.create_task(tool_call.user.dm_channel.send("File:", file = File(file)))
    return "Let the user know the file has been uploaded, and confirm with them that it is the correct file."