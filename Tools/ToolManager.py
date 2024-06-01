import openai
import asyncio
import discord

import Tools.NCBI
import Tools.PhysOrg
import Tools.SearchGoogle
import Tools.Wikipedia
import Tools.Youtube
import log
import ticker
import Tools

import json
import datetime

import Tools.Embedding
import Tools.MemoryBank
import Tools.ReminderBank
import Tools.Reminders
import Tools.Memory
import Tools.Reminders
import Tools.ToolCall

tool_list = [
  {"tool_id": "set_new_reminder", "method": Tools.Reminders.set_new_reminder},
  {"tool_id": "get_reminders", "method": Tools.Reminders.get_reminders},
  {"tool_id": "get_reminders_semantically", "method": Tools.Reminders.get_reminders_semantically},
  {"tool_id": "remove_reminder", "method": Tools.Reminders.remove_reminder},
  {"tool_id": "create_memory", "method": Tools.Memory.create_memory},
  {"tool_id": "forget_memory", "method": Tools.Memory.forget_memory},
  {"tool_id": "recall_memory", "method": Tools.Memory.recall_memory},
  
  {"tool_id": "search_youtube", "method": Tools.Youtube.GetYoutubeVideos},
  {"tool_id": "get_youtube_transcript", "method": Tools.Youtube.GetYoutubeTranscript},

  {"tool_id": "get_latest_physorg_articles", "method": Tools.PhysOrg.get_latest_phys_articles},
  {"tool_id": "search_physorg_articles", "method": Tools.PhysOrg.search_physorg_articles},
  {"tool_id": "read_physorg_article", "method": Tools.PhysOrg.read_physorg_article},

  {"tool_id": "search_google", "method": Tools.SearchGoogle.SearchGoogle},
  {"tool_id": "read_page_from_google", "method": Tools.SearchGoogle.ReadPageFromGoogle},
  
  
  #Example Functions
  {"tool_id": "get_wikipedia_page", "method": Tools.Wikipedia.SearchWikipedia},
  {"tool_id": "get_wikipedia_references", "method": Tools.Wikipedia.GetWikipediaReferences},

  {"tool_id": "search_ncbi", "method": Tools.NCBI.search_ncbi},
  {"tool_id": "read_ncbi", "method": Tools.NCBI.read_ncbi}
]

class ToolManager:
  
  def __init__(self, ticking: ticker.Ticker, memory: Tools.MemoryBank.MemoryBank, reminders: Tools.ReminderBank.ReminderBank):
    self.ticking = ticking
    self.MemoryBank = memory
    self.reminders = reminders

  async def handle_tool_call(self, tool, client):
  
    args = json.loads(tool.function.arguments)
    
    log.ToolCalled(tool.function.name, args)
    
    for method in tool_list:
      if method["tool_id"] == tool.function.name:
        return [{
          "tool_call_id": tool.id,
          "output": method["method"](Tools.ToolCall.ToolCall(tool.function.name, tool, args, client, self.MemoryBank, self.reminders))
        }]
      
    return [{
      "tool_call_id": tool.id,
      "output": "Please let the user know that this tool isn't implemented yet"
    }]