import json
import re
import Tools.ToolCall

from youtubesearchpython import VideosSearch
from youtube_transcript_api import YouTubeTranscriptApi

def extract_youtube_id(url):
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

class VideoInformation:
    def __init__(self, rawresult) -> None:
        self.title = rawresult["title"]
        self.duration = rawresult["duration"]
        self.views = rawresult["viewCount"]["text"]
        self.channel = rawresult["channel"]["name"]
        self.link = rawresult["link"]

    def as_json(self):
        return json.dumps({
            "Title": self.title,
            "Duration": self.duration,
            "Views": self.views,
            "Channel": self.channel,
            "Link": self.link
        })
        

def GetYoutubeVideos(tool_call: Tools.ToolCall.ToolCall) -> str:
    videos = VideosSearch(tool_call.args["Query"], limit = int(tool_call.args["Count"]))
    results: dict = videos.result()
    return json.dumps({
        "Videos": [VideoInformation(video).as_json() for video in results["result"]]
    })

def GetYoutubeTranscript(tool_call: Tools.ToolCall.ToolCall) -> str:
    youtubeID: str = extract_youtube_id(tool_call.args["URL"])
    transcript = YouTubeTranscriptApi.get_transcript(youtubeID)
    return json.dumps({
        "Instruction": "Give a summary of the youtube video's key points, and elaborate further with times when prompted by the user.",
        "Transcript": json.dumps(transcript)
    })