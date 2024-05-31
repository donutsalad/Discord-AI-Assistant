import openai
import datetime
from typing import List

import numpy as np
from scipy import special
from scipy import spatial as sp

class Memory:
  def __init__(self, abstract: str, memory: str, embedding: List[float]):
    self.abstract: str = abstract
    self.memory: str = memory
    
    self.embedding: List[float] = embedding

class Reminder:
  def __init__(self, time: datetime.datetime, abstract: str, embedding: List[float]):
    self.time: datetime.datetime = time
    self.abstract: str = abstract
    
    self.embedding: List[float] = embedding
    
class MemoryQuery:
  def __init__(self, score: float, strength: float, memory: Memory):
    self.score: float = score
    self.strength: float = strength
    
    self.memory: Memory = memory
    
class ReminderQuery:
  def __init__(self, score: float, strength: float, reminder: Reminder):
    self.score: float = score
    self.strength: float = strength
    
    self.reminder: Reminder = reminder


def EmbedString(client: openai.OpenAI, text: str) -> List[float]:
  
  embedding = client.embeddings.create(
    input = text,
    model = "text-embedding-3-small"
  )
  
  return embedding.data[0].embedding


def QueryMemory(memorybank: List[Memory], query: List[float]) -> List[MemoryQuery]:
  if len(memorybank) == 0:
    return []
  
  cosine = [
    sp.distance.cosine(memory.embedding, query)
    for memory in memorybank
  ]
  
  #Score out of 10 (squared for increased specificity)
  inverted = np.ones_like(cosine) - cosine
  score = np.square(inverted)
  score = score * 10

  #Match confidence in p (%)
  strength = special.softmax(score * 10)
  
  result = [
    MemoryQuery(score[i], strength[i], memorybank[i])
    for i in range(len(memorybank))
  ]
  
  result.sort(reverse = True, key = lambda x: x.score)
  
  return result

def QueryReminder(reminderbank: List[Reminder], query: List[float]) -> List[ReminderQuery]:
  if len(reminderbank) == 0:
    return []
  
  cosine = [
    sp.distance.cosine(memory.embedding, query)
    for memory in reminderbank
  ]
  
  #Score out of 10 (squared for increased specificity)
  inverted = np.ones_like(cosine) - cosine
  score = np.square(inverted)
  score = score * 10

  #Match confidence in p (%)
  strength = special.softmax(score * 10)
  
  result = [
    ReminderQuery(score[i], strength[i], reminderbank[i])
    for i in range(len(reminderbank))
  ]
  
  result.sort(reverse = True, key = lambda x: x.score)
  
  return result