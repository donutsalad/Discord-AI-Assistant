import json
import discord
import datetime

filename = "log"

def EscapedIncomingMessage(message: discord.Message):
  
  loggable = dict()
  loggable["time"] = message.created_at
  loggable["content"] = message.content
  
  with open(f"{filename}.escaped", "a") as file:
    json.dump(loggable, file, default=str)

def IncomingDiscordMessage(message: discord.Message):
  
  loggable = dict()
  loggable["time"] = message.created_at
  loggable["content"] = message.content
  
  with open(f"{filename}.incoming", "a") as file:
    json.dump(loggable, file, default=str)
    
def ToolCalled(tool, args):
  with open(f"{filename}.toolcalls", "a") as file:
    json.dump(dict(called = tool, args = args), file)
    
    
def AssistantSpoke(message: str):
  loggable = dict()
  loggable["time"] = datetime.datetime.now()
  loggable["content"] = message
  
  with open(f"{filename}.outgoing", "a") as file:
    json.dump(loggable, file, default=str)
    
def ToolWork(tool, args, toolwork):
  with open(f"{filename}.toolwork", "a") as file:
    json.dump(dict(tool = tool, args = args, work = toolwork), file, default=str)

    
def ThreadCreated():
  with open(f"{filename}.threads", "a") as file:
    json.dump(dict(code = "create", time = datetime.datetime.now()), file, default=str)
    
def ThreadDeleted():
  with open(f"{filename}.threads", "a") as file:
    json.dump(dict(code = "delete", time = datetime.datetime.now()), file, default=str)
    
    
def InternalTrigger(type, content):
  with open(f"{filename}.triggers", "a") as file:
    json.dump(dict(trigger_type = type, trigger_time = datetime.datetime.now(), content = content), file, default=str)