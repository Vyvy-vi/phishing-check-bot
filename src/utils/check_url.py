"""
Copyright 2021 Vyom Jain
Use of this source code is governed by a BSD-style
license that can be found in the LICENSE file or at
https://github.com/Vyvy-vi/phishing-check-bot
"""

import requests
import os
from dotenv import load_dotenv
from typing import List
from pysafebrowsing import SafeBrowsing

load_dotenv()

# Google Safe Browsing
SAFE_BROWSING_API_KEY = os.getenv("GCP_API_KEY")
sb_api = SafeBrowsing(SAFE_BROWSING_API_KEY)

# NoPhishy (Exerra)
EXERRA_RAPIDAPI_KEY = os.getenv("EXERRA_RAPIDAPI_KEY")
exerra_api_url = "https://exerra-phishing-check.p.rapidapi.com/"
querystring = {"url": "https://exerra.xyz"}

headers = {
    "X-RapidAPI-Host": "exerra-phishing-check.p.rapidapi.com",
    "X-RapidAPI-Key": EXERRA_RAPIDAPI_KEY,
}


def unshorten_url(url):
    return requests.head(url, allow_redirects=True).url


def check_url(target_url: str):
    if not target_url:
        return {"error": "No url argument provided"}
    target_url = unshorten_url(target_url)
    res = {target_url: {}}
    sb_res = sb_api.lookup_urls([target_url])
    domain = list(sb_res.keys())[0]
    res[target_url]["safebrowsing_flag"] = sb_res[domain]["malicious"]

    exerra_res = requests.request(
        "GET", exerra_api_url, headers=headers, params={"url": target_url}
    )
    if exerra_res.status_code == 200:
        res[target_url]["exerra_phishing_flag"] = exerra_res.json()["isScam"]
    return res


def check_urls(target_urls: List[str]):
    if not (target_urls and len(target_urls)):
        return {"error": "No url argument provided"}
    target_urls = [unshorten_url(url) for url in target_urls]
    res = {}
    sb_res = sb_api.lookup_urls(target_urls)
    for url in sb_res:
        res[url] = {}
        res[url]["safebrowsing_flag"] = sb_res[url]["malicious"]
    for url in target_urls:
        exerra_res = requests.request(
            "GET", exerra_api_url, headers=headers, params={"url": url}
        )
        if exerra_res.status_code == 200:
            res[url]["exerra_phishing_flag"] = exerra_res.json()["isScam"]
    return res


res = requests.request(
    "GET", "https://api.exerra.xyz/scam/all", headers=headers, data={}
)

with open("scam_links.txt", "w+") as f:
    f.write(res.text)
