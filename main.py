import asyncio
import datetime

import discordbot
import assistant
import ticker

import Tools.Embedding
import Tools.Memory
import Tools.MemoryBank
import Tools.ReminderBank
import Tools.Reminders
import Tools.ToolManager

async def main():
  
  discord_token = ""
  user_id = 0
  openai_key = ""
  assistant_id = ""
  
  aquired = 0
  
  with open("tokens.txt", "r") as f:
    while aquired < 4:
      line = f.readline()
      if line.startswith("[Discord Bot Token]"):
        discord_token = f.readline().rstrip("\n")
        aquired += 1
      elif line.startswith("[Discord User ID]"):
        user_id = int(f.readline().rstrip("\n"))
        aquired += 1
      elif line.startswith("[Open AI API Key]"):
        openai_key = f.readline().rstrip("\n")
        aquired += 1
      elif line.startswith("[Assistant ID]"):
        assistant_id = f.readline().rstrip("\n")
        aquired += 1
      else: raise Exception("Unrecognised token")
  
  masterqueue = asyncio.Queue()
  routerqueue = asyncio.Queue()
  assistantqueue = asyncio.Queue()
  
  memories = Tools.MemoryBank.MemoryBank("data/memories")
  reminders = Tools.ReminderBank.ReminderBank("data/reminders")
  files = Tools.MemoryBank.MemoryBank("data/files")
  
  client = discordbot.SetupDiscordClient(assistantqueue, routerqueue, user_id)
  ticking = ticker.Ticker(reminders, memories, files, masterqueue)
  toolmanager = Tools.ToolManager.ToolManager(client, ticking, memories, files, reminders)
  
  assistant_handler = assistant.OpenAIChatHandler(assistantqueue, toolmanager, client, openai_key, assistant_id, user_id)
  
  asyncio.create_task(client.start(discord_token))
  asyncio.create_task(ticking.TickerLoop())
  asyncio.create_task(assistant_handler.waitloop())
  
  await main_loop(masterqueue, reminders, assistant_handler)
  
async def main_loop(masterqueue: asyncio.Queue, reminders: Tools.ReminderBank.ReminderBank, assistant_handler: assistant.OpenAIChatHandler):
  
  while True:
    
    while not masterqueue.empty():
      item = await masterqueue.get()
      
      if isinstance(item, Tools.Embedding.Reminder):
        try:
          new_thread = await assistant_handler.external_thread("Reminder", item.abstract)
          
          if not new_thread:
            print("Assistant is busy, appending back to list with a half minute delay...")
            delayed: Tools.Embedding.Reminder = item
            delayed.time = item.time + datetime.timedelta(seconds = 30)
            reminders.reminders.append(delayed)
            
          else:
            print("Assistant has been alerted of an internal ticker elapse.")
        
        except Exception as e:
          print(f"Internal Exception from creating new thread: \n{e}\n\n")
            
      else:
        print("Unhandled ticker type... Ignoring.")

    await asyncio.sleep(0.5)
  
if __name__ == "__main__":
  asyncio.run(main())