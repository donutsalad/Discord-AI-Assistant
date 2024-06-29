import pickle
import Tools.MemoryBank

files = []
memories = []

with open("data/files", 'rb') as f:
  files = pickle.load(f)
  
with open("data/memories", 'rb') as f:
  memories = pickle.load(f)
  
memories.extend(files)

with open("data/memories", "wb") as f:
  pickle.dump(memories, f)
  
print("Memories extended.")