import openai
from discord import Client, User

import Tools.MemoryBank
import Tools.ReminderBank

class ToolCall:
  def __init__(self, call_type, tool, args, client, discord, user, memorybank, reminderbank, filebank):
    self.call_type: str = call_type
    self.args: dict = args
    self.tool = tool
    self.client: openai.Client = client
    self.discord: Client = discord
    self.user: User = user
    self.memorybank: Tools.MemoryBank.MemoryBank = memorybank
    self.reminderbank: Tools.ReminderBank.ReminderBank = reminderbank
    self.filebank: Tools.MemoryBank.MemoryBank = filebank