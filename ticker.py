import asyncio
import datetime
from Tools import MemoryBank, ReminderBank

class Ticker:
  def __init__(self, reminderbank: ReminderBank.ReminderBank, memory: MemoryBank.MemoryBank, files: MemoryBank.MemoryBank, outqueue: asyncio.Queue):
    self.reminders = reminderbank
    self.memory = memory
    self.files = files

    self.outqueue = outqueue
    
  async def TickerLoop(self) -> None:
    savetime = datetime.datetime.now()
    
    while True:
      now = datetime.datetime.now()
        
      triggered = self.reminders.CheckTriggered(now)
      for trigger in triggered:
        await self.outqueue.put(trigger)
        self.reminders.RemoveReminder(trigger)
        
      if now > savetime:
        
        try:
          self.reminders.Save()
          self.memory.Save()
          self.files.Save()
          savetime = now + datetime.timedelta(minutes = 30)
          
        except Exception as e:
          #TODO: Make sure.
          print("Failed to save something, potentially being saved too right now.")
          savetime = now + datetime.timedelta(minutes = 1)
      
      await asyncio.sleep(1)