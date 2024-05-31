import json
import openai
import Tools.Embedding

import os
import pickle
import datetime
from typing import List

import log
import Tools.ToolCall  
    
    
def create_memory(tool_call: Tools.ToolCall.ToolCall) -> str:
  
  log.ToolCalled(tool_call.tool.function.name, tool_call.args)
  
  try:
    tool_call.memorybank.NewMemory(tool_call.client, tool_call.args["Abstract"], tool_call.args["Memory"])
    
  except Exception as e:
    return "Tell Izzy the memorybank has failed to create the memory"
    
  return "Tell Izzy the memory has been stored successfully"
      

def forget_memory(tool_call: Tools.ToolCall.ToolCall) -> str:
  
  log.ToolCalled("forget_memory", tool_call.args)
    
  try:
    memory = tool_call.memorybank.GetMemory(Tools.Embedding.EmbedString(tool_call.client, tool_call.args["Abstract"]), 1)
    if memory[0].score < 6:
      confirm = json.dumps({
          "Instruction": f"Ask Isabelle if she meant to delete: {memory[0].memory.abstract}."
        })
      return confirm
    else:
      tool_call.memorybank.RemoveMemory(memory[0].memory)
      
  except Exception as e:  
    return "Let Izzy know there was a problem when trying to delete the memory."
    
  return "Let Izzy know the memory has been forgotten"
     

def recall_memory(tool_call: Tools.ToolCall.ToolCall) -> str:
  
  if tool_call.args.get("Count") is None:
    count = 1
    
  else: count = int(tool_call.args["Count"])
  
  log.ToolCalled("recall_memory", tool_call.args)
  
  try:
    sorted = tool_call.memorybank.GetMemory(Tools.Embedding.EmbedString(tool_call.client, tool_call.args["Abstract"]), count)
  
  except Exception as e:
    print(e)
    return "Let Izzy know that the backend failed to open the memory"
    
  results = []
  for memory in sorted:
    results.append({
      "memory_abstract": memory.memory.abstract,
      "memory_content": memory.memory.memory,
      "match_score": memory.score,
      "match_confidence": memory.strength
      })  
      
  if count == 1:
    final_result = json.dumps({
      "result": "If it has a high confidence you can just let her know the content - otherwise also let her know you're not sure if she means this particular memory.",
      "reminders": results[0]
    })
          
  else: final_result = json.dumps({
      "result": "Show izzy a list of the abstracts and their scores, and then when she specifies one you can let her know the content of the memory.",
      "reminders": results[:count]
    })
          
  return final_result