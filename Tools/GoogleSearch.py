from googleapiclient.discovery import build

import tokens
      
def google_search(search_term, api_key, cse_id, num, **kwargs):
  service = build("customsearch", "v1", developerKey = api_key)
  res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
  return res['items'][:-num]
  
def GetGoogleSearches(site: str, query: str, count: int):
  
  if site == "all":
    results = google_search(query, tokens.google_api_key, tokens.google_cse_key, num = count)
  
  else:
    results = google_search(f"{query} site:{site}", tokens.google_api_key, tokens.google_cse_key, num = count)
  
  return [
    dict(title = entry["title"], snippet = entry["snippet"], url = entry["link"])
    for entry in results
  ]