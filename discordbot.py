import asyncio
import discord
import log

def SetupDiscordClient(aipiaqueue: asyncio.Queue, routerqueue: asyncio.Queue, user_id: int) -> discord.Client:
  client = discord.Client(intents = discord.Intents.all())
  
  @client.event
  async def on_ready() -> None:
    
    print(f"Logged onto discord under the username {client.user}. Attempting to fetch the user.")
    DiscordUser = client.get_user(user_id)
    if(DiscordUser is not None):
      print("We have the user!")
      if (DiscordUser.dm_channel is None):
        print("No DM Channel yet, creating one!")
        await DiscordUser.create_dm()

      await client.change_presence(status = discord.Status.idle, activity = discord.CustomActivity(name = "Just woke up!"))
    
    else:
      print("Unable to get the user?\nThrowing exception.")
      raise Exception("Unable to aquire the user.")
      
    
  @client.event
  async def on_message(message: discord.Message) -> None:   
    
    if message.author == client.user:
      return
    if message.author.id != user_id:
      return
    
    if message.content.startswith("!"):
      log.EscapedIncomingMessage(message)
      return
    
    try:
      log.IncomingDiscordMessage(message)
      await aipiaqueue.put(message)
      
    except Exception as e:
      await message.channel.send("Please let me (the user) know when you saw this. There's an error in the discord bot code!")
      print("Specific error:")
      print(e)
      
  return client
