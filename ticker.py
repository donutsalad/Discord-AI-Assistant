import asyncio
import datetime
from Tools import MemoryBank, ReminderBank, Embedding

class Ticker:
  def __init__(self, reminderbank: ReminderBank.ReminderBank, memory: MemoryBank.MemoryBank, outqueue: asyncio.Queue):
    self.bank = reminderbank
    self.memory = memory

    self.outqueue = outqueue
    
  async def TickerLoop(self) -> None:
    savetime = datetime.datetime.now()
    
    while True:
      now = datetime.datetime.now()
        
      triggered = self.bank.CheckTriggered(now)
      for trigger in triggered:
        await self.outqueue.put(trigger)
        self.bank.RemoveReminder(trigger)
        
      if now > savetime:
        
        try:
          self.bank.Save()
          self.memory.Save()
          savetime = now + datetime.timedelta(minutes = 30)
          
        except Exception as e:
          #TODO: Make sure.
          print("Failed to save something, potentially being saved too right now.")
          savetime = now + datetime.timedelta(minutes = 1)
      
      await asyncio.sleep(1)