import json
from typing import List

import log
import Tools.ToolCall  
import Tools.Embedding
    
    
def create_memory(tool_call: Tools.ToolCall.ToolCall) -> str:
  
  log.ToolCalled(tool_call.tool.function.name, tool_call.args)
  
  try:
    tool_call.memorybank.NewMemory(tool_call.client, tool_call.args["Abstract"], tool_call.args["Memory"])
    
  except Exception as e:
    return "Tell the user the memorybank has failed to create the memory"
    
  return "Tell the user the memory has been stored successfully"
      

def forget_memory(tool_call: Tools.ToolCall.ToolCall) -> str:
  
  log.ToolCalled("forget_memory", tool_call.args)
    
  try:
    memory = tool_call.memorybank.GetMemory(Tools.Embedding.EmbedString(tool_call.client, tool_call.args["Abstract"]), 1)
    if memory[0].score < 6:
      confirm = json.dumps({
          "Instruction": f"Ask the user if she meant to delete: {memory[0].memory.abstract}."
        })
      return confirm
    else:
      tool_call.memorybank.RemoveMemory(memory[0].memory)
      
  except Exception as e:  
    return "Let the user know there was a problem when trying to delete the memory."
    
  return "Let the user know the memory has been forgotten"
     

def recall_memory(tool_call: Tools.ToolCall.ToolCall) -> str:
  
  if tool_call.args.get("Count") is None:
    count = 1
    
  else: count = int(tool_call.args["Count"])
  
  log.ToolCalled("recall_memory", tool_call.args)
  
  try:
    sorted = tool_call.memorybank.GetMemory(Tools.Embedding.EmbedString(tool_call.client, tool_call.args["Abstract"]), count)
  
  except Exception as e:
    print(e)
    return "Let the user know that the backend failed to open the memory"
    
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
      "Instruction": "If it has a high confidence you can just let her know the content - otherwise also let her know you're not sure if she means this particular memory.",
      "results": results[0]
    })
          
  else: final_result = json.dumps({
      "Instruction": "Show the user a list of the abstracts and their scores, and then when she specifies one you can let her know the content of the memory.",
      "results": results[:count]
    })
          
  return final_result