import json
import Tools.ToolCall
from discord import File

def GenerateDallEImage(tool_call: Tools.ToolCall) -> str:
  promptString: str = tool_call.args["Prompt"]
  
  response = tool_call.client.images.generate(
    model="dall-e-3",
    prompt=promptString,
    size="1024x1024",
    quality="standard",
    n=1,
  )
  
  return json.dumps({
    "Instruction": f"Tell the user you have generated the image, and give them this link in plain text so discord can show the image {response.data[0].url}, and ask them if they'd like to generate a new one, and if they need any help with the prompt."
    })