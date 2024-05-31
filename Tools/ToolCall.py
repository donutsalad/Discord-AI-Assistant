import openai
from openai import Client

import Tools.MemoryBank
import Tools.ReminderBank

class ToolCall:
  def __init__(self, call_type, tool, args, client, memorybank, reminderbank):
    self.call_type: str = call_type
    self.args: dict = args
    self.tool = tool
    self.client: openai.Client = client
    self.memorybank: Tools.MemoryBank.MemoryBank = memorybank
    self.reminderbank: Tools.ReminderBank.ReminderBank = reminderbank