import json
import discord

import log
import ticker

import Tools
import Tools.Dropbox
import Tools.SearchGoogle
import Tools.WebTools
import Tools.CustomTools
import Tools.Wikipedia
import Tools.Youtube
import Tools.Embedding
import Tools.MemoryBank
import Tools.ReminderBank
import Tools.Reminders
import Tools.Memory
import Tools.Files
import Tools.Reminders
import Tools.Dropbox
import Tools.ToolCall

tool_list = [
  {"tool_id": "set_new_reminder", "method": Tools.Reminders.set_new_reminder},
  {"tool_id": "get_reminders", "method": Tools.Reminders.get_reminders},
  {"tool_id": "get_reminders_semantically", "method": Tools.Reminders.get_reminders_semantically},
  {"tool_id": "remove_reminder", "method": Tools.Reminders.remove_reminder},
  {"tool_id": "create_memory", "method": Tools.Memory.create_memory},
  {"tool_id": "forget_memory", "method": Tools.Memory.forget_memory},
  {"tool_id": "recall_memory", "method": Tools.Memory.recall_memory},
  
  {"tool_id": "create_file_memory", "method": Tools.Files.create_file_memory},
  {"tool_id": "forget_file_memory", "method": Tools.Files.forget_file_memory},
  {"tool_id": "recall_file_memory", "method": Tools.Files.recall_file_memory},
  
  {"tool_id": "list_dropbox_files", "method": Tools.Dropbox.list_dropbox_files},
  {"tool_id": "upload_dropbox_file", "method": Tools.Dropbox.upload_dropbox_file},
  
  #Custom Functions
  {"tool_id": "get_customtools", "method": Tools.CustomTools.GetAvailableCustomTools},
  {"tool_id": "call_customtool", "method": Tools.CustomTools.CallCustomTool},
  
  #Core Web Functions
  {"tool_id": "get_webtools", "method": Tools.WebTools.GetAvailableWebTools},
  {"tool_id": "call_webtool", "method": Tools.WebTools.CallWebTool},

  {"tool_id": "search_google", "method": Tools.SearchGoogle.SearchGoogle},
  {"tool_id": "read_page_from_google", "method": Tools.SearchGoogle.ReadPageFromGoogle},
  
  {"tool_id": "search_youtube", "method": Tools.Youtube.GetYoutubeVideos},
  {"tool_id": "get_youtube_transcript", "method": Tools.Youtube.GetYoutubeTranscript},

  {"tool_id": "get_wikipedia_page", "method": Tools.Wikipedia.SearchWikipedia},
  {"tool_id": "get_wikipedia_references", "method": Tools.Wikipedia.GetWikipediaReferences}
]

class ToolManager:
  
  def __init__(self, discord: discord.Client, ticking: ticker.Ticker, memory: Tools.MemoryBank.MemoryBank, files: Tools.MemoryBank.MemoryBank, reminders: Tools.ReminderBank.ReminderBank):
    self.ticking = ticking
    self.MemoryBank = memory
    self.reminders = reminders
    self.files = files
    
    self.discord = discord

  async def handle_tool_call(self, tool, client, user):
  
    args = json.loads(tool.function.arguments)
    
    log.ToolCalled(tool.function.name, args)
    
    for method in tool_list:
      if method["tool_id"] == tool.function.name:
        return [{
          "tool_call_id": tool.id,
          "output": method["method"](Tools.ToolCall.ToolCall(tool.function.name, tool, args, client, self.discord, user, self.MemoryBank, self.reminders, self.files))
        }]
      
    return [{
      "tool_call_id": tool.id,
      "output": "Please let the user know that this tool isn't implemented yet"
    }]