# Pastebin API

Hey all! This is a simple Pastebin API that allows you to create and retrieve pastes. 

## Setup Instructions

1. **Clone the repository** (if terminal):
   ```
   git clone <your-repo-url>
   cd <your-repo-directory>
   ```

2. **Configure the application:**

Open app.py and set the following variables:
`WEBHOOK:` Add your host URL.
`MONGO_URL`: Add your MongoDB connection string. You can get this from the MongoDB website.

3. **Install the required packages:**

```
pip install -r requirements
```

4. **Run the application:**

```
python3 app.py
```

**Usage**
You can use the API to create a new paste. Below is an example of how to do this using Python's requests library.

**Example Code**
```
import requests
import json

url = "http://localhost:1080/paste"  # Change this to your host URL if needed
headers = {
    "Content-Type": "application/json"
}
data = {
    "content": "hi"
}

response = requests.post(url, headers=headers, data=json.dumps(data))

print(response.json())
```
**Response**
The API will return a JSON response containing the URL to access your paste and the raw content URL. For example:

```
{
    "url": "http://localhost:1080/paste/<paste_id>",
    "raw": "http://localhost:1080/raw/<paste_id>"
}
```
