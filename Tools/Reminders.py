import json
import openai
import Tools.Embedding
import log
import Tools.ReminderBank

import os
import pickle
import datetime
from typing import List

import Tools.ToolCall  
     
      
def set_new_reminder(tool_call: Tools.ToolCall.ToolCall) -> str:
  
  try:
    print(tool_call.tool.function.arguments)
    reminder_abstract = tool_call.args["Abstract"]
    reminder_time = datetime.datetime.strptime(tool_call.args["Time"], "%Y-%m-%d %H:%M:%S")
    tool_call.reminderbank.NewReminder(tool_call.client, reminder_time, reminder_abstract)
    
  except Exception as e:
    print(f"Exception raised :/ -> {e}")
    
  return "Let the user know you've set the reminder, and give her a confirmation :)"

def get_reminders(tool_call: Tools.ToolCall.ToolCall) -> str:
  
  if tool_call.args.get("Count") is None:
    count = 1
    
  else: count = int(tool_call.args["Count"])
  
  upcoming = tool_call.reminderbank.GetUpcoming(count)
  
  results = []
  for reminder in upcoming:
    results.append({
      "reminder_abstract": reminder.abstract,
      "reminder_time": reminder.time.strftime("[%Y-%m-%d %H:%M:%S]")
      })
    
  if len(results) == 0:
    return "Let the user know there are no reminders currently set"
    
  if count < 4:
    final_result = json.dumps({
      "reminders": results
    })
    
  else:
    final_result = json.dumps({
      "result": "Tell the user a summary of the reminders. If she asks for more detail then you can say more!",
      "reminders": results
    })
  
  return final_result

def get_reminders_semantically(tool_call: Tools.ToolCall.ToolCall) -> str:
    
  if tool_call.args.get("Count") is None:
    count = 1
    
  else: count = int(tool_call.args["Count"])
  
  search = tool_call.reminderbank.GetReminders(Tools.Embedding.EmbedString(tool_call.client, tool_call.args["Abstract"]), count)
  
  results = []
  for reminder in search:
    results.append({
      "reminder_abstract": reminder.reminder.abstract,
      "reminder_time": reminder.reminder.time.strftime("[%Y-%m-%d %H:%M:%S]"),
      "reminder_score": reminder.score,
      "reminder_confidence": reminder.strength
      })
    
  print(results)
    
  if len(results) == 0:
    return "Let the user know there are no reminders currently set"
    
  if count == 1:
    final_result = json.dumps({
      "result": "Ask the user if this is the reminder she meant.",
      "reminder": results[0]
    })
    
  else:
    final_result = json.dumps({
      "result": "Tell the user a summary of the reminders. If she asks for more detail then you can say more!",
      "reminders": results
    })
    

  return final_result

def remove_reminder(tool_call: Tools.ToolCall.ToolCall) -> str:
  
  reminder = None
  
  try:
    reminder = tool_call.reminderbank.GetReminders(Tools.Embedding.EmbedString(tool_call.client, tool_call.args["Abstract"]), 1)
    if reminder[0].score < 7:
      confirm = json.dumps({
        "Instruction": f"Ask the user if she meant to delete: {reminder[0].reminder.abstract}."
      })
      
      return confirm
      
    else:
      tool_call.reminderbank.RemoveReminder(reminder[0].reminder)
        
  except Exception as e:
    return "Let the user know that the backend failed to remove the reminder."
    
  return "Let the user know the reminder has been removed!"
