from googleapiclient.discovery import build

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

my_api_key = ""
my_cse_id = ""

aquired = 0
with open("tokens.txt") as f:
  while aquired < 2:
    line = f.readline()
    if line.startswith("google: "):
      my_api_key = line[8:].rstrip("\n")
      aquired += 1
    elif line.startswith("context: "):
      my_cse_id = line[9:].rstrip("\n")
      aquired += 1
      
def google_search(search_term, api_key, cse_id, **kwargs):
  service = build("customsearch", "v1", developerKey = api_key)
  res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
  return res['items']
  
def GetGoogleSearches(site: str, query: str, count: int):
  
  if site == "all":
    results = google_search(query, my_api_key, my_cse_id, num = count)
  
  else:
    results = google_search(f"{query} site:{site}", my_api_key, my_cse_id, num = count)
  
  return [
    dict(title = entry["title"], snippet = entry["snippet"], url = entry["link"])
    for entry in results
  ]