import os
import openai
import discord
import asyncio
import datetime

import log
import Tools
import Tools.ToolManager

prompt = ""
with open("prompt.txt", "r") as f:
  prompt = f.read()
  
if len(prompt) == 0:
  with open("prompt_template.txt") as f:
    prompt = f.read()

backend_message = """
The discord backend has just triggered an event.
A reminder that was set has elapsed. The reminder abstract was:
"""

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
  
  
  async def handle_run(self, dmessage: discord.Message, newthr):
    
    message = dmessage.content
    files = []
    
    if len(dmessage.attachments) > 0:
      for attachment in dmessage.attachments:
        filename = attachment.filename
        
        if os.path.exists(f"downloads/{filename}"):
          filename = f"{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - {filename}"
          
        await attachment.save(f"downloads/{filename}")
        files.append(filename)
        
      if len(dmessage.content) == 0:
        message = f"Ask me what I'd like to do with these files: {", ".join(files)}"
      
      message = f"{message} | attached files: {", ".join(files)}"
    
    async with dmessage.channel.typing():
      
      if newthr == True:
        self.run = self.client.beta.threads.create_and_run(
          assistant_id = self.assistant.id,
          thread={
            "messages": [
              {"role": "user", "content": f"[{datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S")}] {message}"}
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
                "content": f"[{datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S")}] {message}"
              }
            ]
        )
        
      await self.await_responce()
        
  
  async def handle_tool_call(self, run, user):
  
    results = []
    for tool in run.required_action.submit_tool_outputs.tool_calls:
      result = await self.toolmanager.handle_tool_call(tool, self.client, self.discorduser)
      results.extend(result)
      
    self.run = self.client.beta.threads.runs.submit_tool_outputs(
      thread_id = self.run.thread_id,
      run_id = self.run.id,
      tool_outputs = results
    )
    
    await self.await_responce()
    
  #Actually written by the bot lmao - i'm lazy
  def chunk_message(self, message, limit = 2000):
    chunks = []
    chunk = ""
    code_block_open = False

    for line in message.splitlines(keepends=True):
        if len(chunk) + len(line) <= limit:
            chunk += line
            if line.startswith("```"):
                code_block_open = not code_block_open
        else:
            if code_block_open and not chunk.endswith("```\n"):
                chunk += "```\n"
            chunks.append(chunk)
            chunk = ""
            if line.startswith("```"):
                code_block_open = not code_block_open
                chunk = line
            else:
                chunk = line
            if code_block_open:
                chunk += "```"  # reopen the code block in the new chunk

    if code_block_open and not chunk.endswith("```\n"):
        chunk += "```\n"
    chunks.append(chunk)
    return chunks
      
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
          
        if len(result) < 1999:
          await self.discorduser.dm_channel.send(result)
          
        else:
          chunks = self.chunk_message(result)
          for chunk in chunks:
            await self.discorduser.dm_channel.send(chunk)
          
        if final:
          print("Thread ending from end token.")
          await self.delete_thread()
        return
      
      case "requires_action":
        await self.handle_tool_call(self.run, self.discorduser)
      
      case _:
        await self.discorduser.dm_channel.send(f"Unhandled state from normal messages. ({self.run.status})")
        await self.delete_thread()
        

def Reminder_Prompt():
  return f"{prompt}\n{backend_message}"