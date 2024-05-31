import openai
import Tools.Embedding
import Tools.ToolCall 

import os
import pickle
import datetime
from typing import List

class MemoryBank:
  def __init__(self, filename):
    self.filename: str = filename
    self.memories: List[Tools.Embedding.Memory] = self.TryLoad(self.filename)
    
    
  def TryLoad(self, filename) -> bool:
    
    if os.path.isfile(filename):
      
      try:
        loaded: List[Tools.Embedding.Memory] = []
        with open(filename, "rb") as file:
          loaded = pickle.load(file)
        return loaded
      
      except:
        raise Exception(f"Problem loading memories from {filename}!")
    
    else:
      return []
    
  def Save(self):
    
    if os.path.isfile(self.filename):
      
      if os.path.isfile(f"{self.filename}.backup"):
        os.rename(f"{self.filename}.backup", f"{self.filename}.bkoa-{datetime.datetime.now().strftime("%d-%m-%Y-%H-%M")}")
        
      os.rename(self.filename, f"{self.filename}.backup")
      
    try:
      with open(self.filename, "wb") as file:
        pickle.dump(self.memories, file)
    
    except Exception as e: raise Exception(f"Problem arised when saving memories: {e}")

  
  def NewMemory(self, client: openai.Client, abstract: str, memory: str):
    self.memories.append(Tools.Embedding.Memory(abstract, memory, Tools.Embedding.EmbedString(client, abstract)))
    
    try:
      self.Save()
          
    except Exception as e:
      #TODO: Make sure.
      print("Failed to save new memory, potentially being saved too right now.")
    
  def GetMemory(self, query: List[float], count: int) -> List[Tools.Embedding.MemoryQuery]:
    return Tools.Embedding.QueryMemory(self.memories, query)[:count]
  
  def RemoveMemory(self, memory: Tools.Embedding.Memory) -> None:
    stored = None
    for entry in self.memories:
      if entry.abstract == memory.abstract:
        stored = entry
        break
      
    self.memories.remove(stored)
    
    try:
      self.Save()
          
    except Exception as e:
      #TODO: Make sure.
      print("Failed to save memories after deletion, potentially being saved too right now.")
  