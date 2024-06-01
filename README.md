# Discord AI Assistant
### Detailed readme coming soon

A personal assistant based around GPT4o and the assistant's API that takes some effort out of life. Core functions currently available:
 - Memories (fuzzy search, create/recall/destroy)
 - Reminders (fuzzy search, create/find/list/destroy)
 - WebTools (list, call, and view generic page, and read all \<p\>'s from a url)
 - Wikipedia (get page content, get references)
 - Youtube (search youtube, get transcript)
 - Google (search google, read page \[using webtools generic page function\])

Web Tools are a way to create more functionality interfacing with websites and other functions in a way that doesn't clog up the function set in your assistant.
This way it enables you to add a bunch of web functions, that are only exposed to the bot when needed.

Included Demo Functions
----
 - Normal Function:
    - NCBI (search NCBI, get main text with a `/?report=printable`)
 - Web Tool Function:
    - Phys.org (get the latest articles, search phys.org and read an article)

I plan to make a video tutorial on how to create your own command but the tl;dr is create your own function and import it in ToolManager.py
and then create an entry in the list of available tools with "tool_id" being the assistant's json (on openai platform) and "method" being a reference to your function

Not too dissimilar is the WebTools.py file, the only major difference being that you include a description of the tool and generic parameters, and your tool recieves a `WebTool` object instead of a `ToolCall` object.


Setup
----
You'll need to add a file `tokens.txt` in the top directory in order for it to run. At the moment the names are a bit dumb but I'll change that very soon.

The tokens are:
 - `user id` your discord user ID (enable developer mode in discord if you haven't already - then click your pfp bottom left)
 - `discord` your bot token
 - `openai` your openai api key
 - `assistant id` your assistant's id
 - `google` your google api key
 - `search` your custom search's context id

Don't worry if you don't know how to get any of them, hopefully within June there will be a tutorial :)

Feel free to hit me up in the meantime if you have any questions, might take me some time to get back to you but happy to help!
I'm all about making life easier :)
