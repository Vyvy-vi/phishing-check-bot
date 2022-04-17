import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

SAFE_BROWSING_API_KEY = os.getenv("GCP_API_KEY")
url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={SAFE_BROWSING_API_KEY}"
headers = {"content-type": "application/json"}


def check_url(target_url):
    if not target_url:
        return {"error": "No url argument provided"}
    payload = {
        "client": {"clientId": "0xfe12a052bbd9e", "clientVersion": "0.1"},
        "threatInfo": {
            "threatTypes": [
                "SOCIAL_ENGINEERING",
                "MALWARE",
                "POTENTIALLY_HARMFUL_APPLICATION",
            ],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
        },
    }
    payload["threatInfo"]["threatEntries"] = [{"url": target_url}]
    r = requests.post(url, headers=headers, json=payload)
    print(r.json())


check_url("https://github.com")
