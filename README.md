# Discord AI Assistant
### Detailed Tutorial and step by step README coming soon.

A personal assistant based around GPT4o and the assistant's API that takes some effort out of life.

One thing to note: conversations (threads) are terminated by an `<END>` token the prompt signifies to the assistant.
The benifit is that you don't wrack up input tokens to hold context. If the bot says "Counting electric sheep zzz" that means there is no live thread.
If you've asked it to summarise an article or generate code, and you don't need that context but you'd like to read another article etc, either say thanks that's all, or directly ask the assistant to terminate the thread.

Core functions currently available:
 - Memories (fuzzy search, create/recall/destroy)
 - Reminders (fuzzy search, create/find/list/destroy)
 - Files (fuzzy search, store/upload/destroy) \[Saves the CDN link for attachments.\]
   - Additionally saves the file to downloads folder 
 - Dropbox (simple glob listing for the dropbox folder, list/upload)
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
 - Web Tool Functions:
    - Phys.org (get the latest articles, search, and read an article)
    - NeuroscienceNews.com (get the latest articles, search, and read an article)

Extending Functionality
----
I plan to make a video tutorial on how to create your own command but the tl;dr is create your own function and import it in ToolManager.py
and then create an entry in the list of available tools with "tool_id" being the assistant's json (on openai platform) and "method" being a reference to your function

Not too dissimilar is the WebTools.py file, the only major difference being that you include a description of the tool and generic parameters, and your tool recieves a `WebTool` object instead of a `ToolCall` object.


Setup
----
To make sure you have all the libraries utilised in this project install the libraries requirements.txt
You'll need to create the file `tokens.txt` in the top directory in order for it to run. Use the `token_template.txt` file as a guide.

The tokens are:
 - `[Discord User ID]` - your discord user ID (enable developer mode in discord if you haven't already - then click your pfp bottom left)
 - `[Discord Bot Token]` - your bot token
 - `[Open AI API Key]` - your openai api key
 - `[Assistant ID]` - your assistant's id
 - `[Google API Token]` - your google api key
 - `[Google Search Context]` - your custom search's context id

Don't worry if you don't know how to get any of them, hopefully within June there will be a tutorial :)

Feel free to hit me up in the meantime if you have any questions, might take me some time to get back to you but happy to help!
I'm all about making life easier :)

(donutsalad on discord)
