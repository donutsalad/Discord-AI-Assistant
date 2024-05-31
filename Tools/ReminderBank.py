import openai
import Tools.Embedding

import os
import pickle
import datetime
from typing import List

class ReminderBank:
  def __init__(self, filename):
    self.filename: str = filename
    self.reminders: List[Tools.Embedding.Reminder] = self.TryLoad(self.filename)
    
    
  def TryLoad(self, filename) -> List[Tools.Embedding.Reminder]:
    
    if os.path.isfile(filename):
      
      try:
        loaded: List[Tools.Embedding.Reminder] = []
        with open(filename, "rb") as file:
          loaded = pickle.load(file)
        return loaded
      
      except:
        raise Exception(f"Problem loading reminders from {filename}!")
    
    else:
      return []
    
  def Save(self):
    
    if os.path.isfile(self.filename):
      
      if os.path.isfile(f"{self.filename}.backup"):
        os.rename(f"{self.filename}.backup", f"{self.filename}.bkoa-{datetime.datetime.now().strftime("%d-%m-%Y-%H-%M")}")
        
      os.rename(self.filename, f"{self.filename}.backup")
    
    try:
      with open(self.filename, "wb") as file:
        pickle.dump(self.reminders, file)
    
    except Exception as e: raise Exception(f"Problem arised when saving reminders: {e}")
    
    
  def CheckTriggered(self, time: datetime) -> List[Tools.Embedding.Reminder]:
    triggered = []
    for reminder in self.reminders:
      if reminder.time < time:
        triggered.append(reminder)
        
    return triggered
  
  def NewReminder(self, client: openai.Client, time: datetime.datetime, abstract: str):
    self.reminders.append(Tools.Embedding.Reminder(time, abstract, Tools.Embedding.EmbedString(client, abstract)))
    
    try:
      self.Save()
          
    except Exception as e:
      #TODO: Make sure.
      print("Failed to save new reminder, potentially being saved too right now.")
    
  def GetUpcoming(self, count: int) -> List[Tools.Embedding.Reminder]:
    if len(self.reminders) == 0: return []
    self.reminders.sort(key = lambda x: x.time)
    return self.reminders[:count]
    
  def GetReminders(self, query: List[float], count: int) -> List[Tools.Embedding.ReminderQuery]:
    return Tools.Embedding.QueryReminder(self.reminders, query)[:count]
  
  def RemoveReminder(self, reminder: Tools.Embedding.Reminder) -> None:
    stored = None
    for entry in self.reminders:
      if entry.abstract == reminder.abstract:
        stored = entry
        break
      
    self.reminders.remove(stored)
    
    try:
      self.Save()
          
    except Exception as e:
      #TODO: Make sure.
      print("Failed to save reminders after deletion, potentially being saved too right now.")
