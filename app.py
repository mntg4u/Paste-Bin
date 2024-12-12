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
            background: linear-gradient(135deg, #1f4037, #99f2c8);
            color: #f5f5f5;
            font-family: 'Roboto', Arial, sans-serif;
            padding: 20px;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            width: 90%;
            max-width: 600px;
            background: rgba(0, 0, 0, 0.8);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        }
        h1 {
            text-align: center;
            color: #99f2c8;
        }
        .code-container {
            background: #333;
            padding: 15px;
            border-radius: 5px;
            position: relative;
            overflow: auto;
        }
        .copy-button {
            background: linear-gradient(135deg, #6a11cb, #2575fc);
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            position: absolute;
            top: 10px;
            right: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .copy-button:hover {
            transform: scale(1.1);
            background: linear-gradient(135deg, #2575fc, #6a11cb);
        }
        pre {
            white-space: pre-wrap;
            word-wrap: break-word;
            color: #f5f5f5;
        }
        @media (max-width: 600px) {
            body {
                padding: 10px;
            }
            .container {
                padding: 15px;
            }
        }
    </style>
</head>
<body>

    <div class="container">
        <h1>Your Paste</h1>
        <div class="code-container">
            <button class="copy-button" onclick="copyToClipboard()">Copy</button>
            <pre><code>{{kundi}}</code></pre>
        </div>
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
