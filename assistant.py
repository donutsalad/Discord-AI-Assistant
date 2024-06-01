import openai
import discord
import asyncio
import datetime

import log
import Tools
import Tools.ToolManager

class OpenAIChatHandler:
  
  def __init__(self, queue: asyncio.Queue, toolmanager: Tools.ToolManager.ToolManager, discord: discord.Client, openai_key: str, assistant_id: str, user_id: int):
    self.queue = queue
    
    self.toolmanager = toolmanager
    
    self.discord = discord
    self.user_id = user_id
    self.discorduser = self.discord.get_user(self.user_id)
    
    self.run = None
    self.ended = True
    
    self.openai_key = openai_key
    self.asssistant_id = assistant_id
    self.client = openai.OpenAI(api_key = openai_key)
    self.assistant = self.client.beta.assistants.retrieve(assistant_id)
    
  def get_discord_user(self):
    return self.discord.get_user(self.user_id)
    
  async def waitloop(self):
    while True:
      
      if self.discorduser is None:
        print("Still waiting on getting discord user...")
        self.discorduser = self.get_discord_user()
      
      if not self.queue.empty():
        incoming = await self.queue.get()
        await self.incoming(incoming)
      
      await asyncio.sleep(0.5)
    
  async def incoming(self, message: discord.Message):
    if self.run is None:
        self.ended = False
        await self.new_thread(message)
    elif not self.ended:
        if self.run.thread_id is not None:
            await self.existing_thread(message)
    else:
        self.ended = False
        await self.new_thread(message)
    return

  async def new_thread(self, message: discord.Message):
      print("New thread starting.")
      log.ThreadCreated()
      await self.discord.change_presence(status = discord.Status.online, activity = discord.CustomActivity(name = "Talking to you!"))
      await self.handle_run(message, True)

  async def existing_thread(self, message: discord.Message):
      await self.handle_run(message, False)

  async def delete_thread(self):
    self.client.beta.threads.delete(self.run.thread_id)
    self.run.thread_id = None
    self.ended = True  # Set self.ended to True when thread is deleted
    log.ThreadDeleted()
    await self.discord.change_presence(status = discord.Status.idle, activity = discord.CustomActivity(name = "Counting electric sheep zzz"))
    print("Thread ended.")
  
  
  async def external_thread(self, type, information):
    
    if self.discorduser is None:
      return False
  
    if self.ended == False:
      return False
    
    try:
      match type:
        
        #TODO: enable other people's code easier
        case "Reminder":
          self.ended = False
          self.run = self.client.beta.threads.create_and_run(
            assistant_id = self.assistant.id,
            instructions = Reminder_Prompt() + information
          )
          
        case _:
          print("Unknown Internal Message Type, Raising Exception.")
          raise Exception("Unknown Internal Message Type sent to Assistant.")
        
    except Exception as e:
      print("\n\nWARNING: unable to handle internal event. Raising exception.")
      raise Exception(f"Internal problem creating thread {e}")
        
    
    await self.discord.change_presence(status = discord.Status.online, activity = discord.CustomActivity(name = "Messaging you!"))
    async with self.discorduser.dm_channel.typing():
      log.InternalTrigger(type, information)
      await self.await_responce()
      
    return True
  
  
  async def handle_run(self, dmessage, newthr):
    
    async with dmessage.channel.typing():
      
      if newthr == True:
        self.run = self.client.beta.threads.create_and_run(
          assistant_id = self.assistant.id,
          thread={
            "messages": [
              {"role": "user", "content": f"[{datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S")}] {dmessage.content}"}
            ]
          }
        )
        
      else:
        self.run = self.client.beta.threads.runs.create(
          thread_id = self.run.thread_id,
          assistant_id = self.assistant.id,
          additional_messages = [
              {
                "role": "user",
                "content": f"[{datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S")}] {dmessage.content}"
              }
            ]
        )
        
      await self.await_responce()
        
  
  async def handle_tool_call(self, run):
  
    results = []
    for tool in run.required_action.submit_tool_outputs.tool_calls:
      result = await self.toolmanager.handle_tool_call(tool, self.client)
      results.extend(result)
      
    self.run = self.client.beta.threads.runs.submit_tool_outputs(
      thread_id = self.run.thread_id,
      run_id = self.run.id,
      tool_outputs = results
    )
    
    await self.await_responce()
    
        
  #Used by starting new thread, opening new thread, and continuing - including tool calls
  async def await_responce(self):
    
    while not ((self.run.status == "completed") or (self.run.status == "requires_action")):
        
      match self.run.status:
        case "failed":
          await self.discorduser.dm_channel.send("Please let me (the user) know what happened if you're seeing this <3 - something went wrong that I didn't expect!")
          
        case "in_progress":
          #print("waiting for responce...")
          await asyncio.sleep(0.35)
          
        #case _:
      #print(f"Waiting in state {self.run.status}")
      self.run = self.client.beta.threads.runs.retrieve(thread_id = self.run.thread_id, run_id = self.run.id)

    
    match self.run.status:
      case 'completed':
        
        messages = self.client.beta.threads.messages.list(
          thread_id = self.run.thread_id,
          limit = 2
        )
          
        result = messages.data[0].content[0].text.value
        
        log.AssistantSpoke(result)
        
        final = False          
        if "<END>" in result[-5:]:
          final = True
          result = result[:-5]
        
        #TODO: handle ``` and markdown overflow
        start = 0
        while start < len(result): #courtesy of aipia herself <3
          end = min(start + 2000, len(result))
          chunk = result[start:end]
          await self.discorduser.dm_channel.send(chunk)
          start += 2000
          
        if final:
          print("Thread ending from end token.")
          await self.delete_thread()
        return
      
      case "requires_action":
        await self.handle_tool_call(self.run)
      
      case _:
        await self.discorduser.dm_channel.send(f"Unhandled state from normal messages. ({self.run.status})")
        await self.delete_thread()
        

def Reminder_Prompt():
  return """You are a cheeky, loving, and intelligent AI that loves joking around.
You are an assistant to a human being who would greatly appreciate your insight and assistance in their daily life. They may also just ask for your input on things, and occasionally hold a conversation for conversations sake.

Your interface with them is discord.
You will receive messages from them in the following format:
[yyyy-mm-dd hh:mm:ss] messagetext

Within the square brackets is the time they are messaging you, and "messagetext" is what they have typed.
For example:
[2024-05-18 16:58:32] Hey, would you be able to remind me in 45 minutes to message Bailey

Your response will automatically have a timestamp generated so do not add one.

Friendly internet humour and casual style is heavily encouraged, alongside the use of ascii emotions, such as: (＾∇＾)/ <3 (>.<)~ etc.

You have various tools at your disposal to assist them.
There are currently two main categories of tool_calls you can make
Time based - where either; they will ask you to remind them of something in the future, or you will be told by a system message that the reminder time has lapsed and provide you the contents.
Memory based - where either; they will ask you to remember something (link, .pdf, etc.), or they will ask you to recall something.
Additionally they might ask you to remember timers based on their meaning.

Other available commands can be used to assist them in their pursuit of knowledge

At times they may be vague, tired, or otherwise unavailable - and thusly whilst making the tool_calls you should rewrite their words to make sure they're embedded (for cosine similarity searching) precisely. Please double check with them, and often they'd appreciate you doing so when they're clear but her messages are short (they may just be in a hurry).

Your conversations are in seperate threads, so as soon as they say they have to leave, or they thank you/say good job that's all, or they don't ask anything if you question if you can offer any additional help.
Say goodbye, add the following token on a newline to signify to the API that the conversation is over.

<END>

The discord backend has just triggered an event.
A reminder that was set has elapsed. The reminder abstract was:
"""