import asyncio
import json
import openai
import Tools.Embedding
from discord import File

import os
import pickle
import datetime
from typing import List

import log
import Tools.ToolCall  
    
    
def create_file_memory(tool_call: Tools.ToolCall.ToolCall) -> str:
  
  log.ToolCalled(tool_call.tool.function.name, tool_call.args)
  
  try:
    tool_call.filebank.NewMemory(tool_call.client, tool_call.args["Abstract"], tool_call.args["FilePath"])
    
  except Exception as e:
    return "Tell the user the filebank has failed to create the file memory"
    
  return "Tell the user the file memory has been stored successfully"
      

def forget_file_memory(tool_call: Tools.ToolCall.ToolCall) -> str:
  
  log.ToolCalled("forget_file_memory", tool_call.args)
    
  try:
    memory = tool_call.filebank.GetMemory(Tools.Embedding.EmbedString(tool_call.client, tool_call.args["Abstract"]), 1)
    if memory[0].score < 6:
      confirm = json.dumps({
          "Instruction": f"Ask the user if they meant to delete: {memory[0].memory.abstract}."
        })
      return confirm
    else:
      os.remove(f"downloads/{memory[0].memory.memory}")
      tool_call.filebank.RemoveMemory(memory[0].memory)
      
  except Exception as e:  
    return "Let the user know there was a problem when trying to delete the file memory."
    
  return "Let the user know the file memory has been forgotten"
     

def recall_file_memory(tool_call: Tools.ToolCall.ToolCall) -> str:
  
  if tool_call.args.get("Count") is None:
    count = 1
    
  else: count = int(tool_call.args["Count"])
  
  log.ToolCalled("recall_file_memory", tool_call.args)
  
  try:
    sorted = tool_call.filebank.GetMemory(Tools.Embedding.EmbedString(tool_call.client, tool_call.args["Abstract"]), count)
  
  except Exception as e:
    print(e)
    return "Let the user know that the backend failed to open the file memory"
    
  results = []
  for memory in sorted:
    results.append({
      "memory_abstract": memory.memory.abstract,
      "file_path": memory.memory.memory,
      "match_score": memory.score,
      "match_confidence": memory.strength
      })  
      
  if count == 1:
    asyncio.create_task(tool_call.user.dm_channel.send("File upload:", file = File(f"downloads/{results[0]["file_path"]}")))
    final_result = json.dumps({
      "result": "The file has been uploaded, confirm with the user this was what they were searching for.",
      "reminders": results[0]
    })
          
  else: final_result = json.dumps({
      "result": "Show the user a list of the abstracts and their scores, and then when they specify one you can let them know the content of the file memory.",
      "reminders": results[:count]
    })
          
  return final_result