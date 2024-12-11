from aiohttp import web
from uuid import uuid4
import re
import json
from pymongo import MongoClient

MONGO_URL = "" # add your mongo db url
WEBHOOK = "" # Remove this url and add yours

client = MongoClient(MONGO_URL)
myre = client['horrid-paste']
paste = myre['padtes_fck']

app = web.Application()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pastebin</title>
    <style>
        body {
            background-color: black;
            color: white;
            font-family: 'Courier New', Courier, monospace;
            padding: 20px;
        }
        .code-container {
            background-color: #1e1e1e;
            padding: 15px;
            border-radius: 5px;
            position: relative;
            overflow: auto;
            font-size: 16px;
            white-space: pre;
            line-height: 1.5;
        }
        .copy-button {
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 5px 10px;
            position: absolute;
            top: 10px;
            right: 10px;
            cursor: pointer;
        }
        .keyword {
            color: #569cd6; /* Color for keywords */
        }
        .string {
            color: #ce9178; /* Color for strings */
        }
        .comment {
            color: #6a9955; /* Color for comments */
        }
    </style>
</head>
<body>

    <h1>Your Paste</h1>
    
    <div class="code-container">
        <button class="copy-button" onclick="copyToClipboard()">Copy</button>
        <pre><code>{{kundi}}</code></pre>
    </div>

    <script>
        function copyToClipboard() {
            navigator.clipboard.writeText(document.querySelector('code').innerText)
                .then(() => {
                    alert('Code copied to clipboard!');
                })
                .catch(err => {
                    console.error('Could not copy text: ', err);
                });
        }
    </script>

</body>
</html>
"""

async def create_paste(request):
    data = await request.json()
    content = data.get('content', '')
    paste_id = str(uuid4())
    paste.insert_one({"paste_id": paste_id, "andi": content})
    return web.json_response({"url": f"{WEBHOOK}/paste/{paste_id}", "raw": f"{WEBHOOK}/raw/{paste_id}"}, status=201)

async def get_paste(request):
    paste_id = request.match_info['paste_id']
    content = paste.find_one({"paste_id": paste_id})
    if content is None:
        return web.json_response({"error": "Paste not found"}, status=404)
    return web.Response(text=HTML_TEMPLATE.replace("{{kundi}}", content['andi']), content_type='text/html')

async def get_raw_paste(request):
    paste_id = request.match_info['paste_id']
    content = paste.find_one({"paste_id": paste_id})
    if content is None:
        return web.json_response({"error": "Paste not found"}, status=404)
    return web.Response(text=content['andi'])

app.router.add_post('/paste', create_paste)
app.router.add_get('/paste/{paste_id}', get_paste)
app.router.add_get('/raw/{paste_id}', get_raw_paste)

if __name__ == '__main__':
    web.run_app(app, port=1080)
