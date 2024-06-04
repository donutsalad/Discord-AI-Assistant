import os
import json
from pypdf import PdfReader

import Tools.CustomTool

def ReadPDF(tool_call: Tools.CustomTool.CustomTool):

  file_name = tool_call.paramone
  
  if not file_name.startswith("downloads/"):
    file_name = f"downloads/{file_name}"
    
  if not os.path.exists(file_name):
    return "Let the user know this file is not found."

  reader = PdfReader(file_name)
  pages = [
    page.extract_text(extraction_mode = "layout")
    for page in reader.pages
  ]
  
  return json.dumps(pages)