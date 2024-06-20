discord_token = ""
user_id = ""
openai_key = ""
assistant_id = ""
google_api_key = ""
google_cse_key = ""

aquired = 0
with open("tokens.txt", "r") as f:
  while aquired < 6:
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
    elif line.startswith("[Google API Token]"):
      google_api_key = f.readline().rstrip("\n")
      aquired += 1
    elif line.startswith("[Google Search Context]"):
      google_cse_key = f.readline().rstrip("\n")
      aquired += 1
    else: raise Exception("Unrecognised token")