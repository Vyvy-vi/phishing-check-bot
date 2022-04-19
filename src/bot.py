import re
import random

from utils.messages import WELCOME_MESSAGE, TIPS
from utils.check_url import check_url, check_urls

from flask import Flask, request, url_for, jsonify
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


def parse_urls(string: str):
    http_urls = re.findall(
        r"(http|ftp|https):\/\/([\w\-_]+(?:(?:\.[\w\-_]+)+))([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?",
        string,
    )
    string = re.sub(
        r"(http|ftp|https):\/\/([\w\-_]+(?:(?:\.[\w\-_]+)+))([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?",
        "|",
        string,
    )
    normal_urls = re.findall(r"[a-z0-9\-]*\.[a-z0-9]*", string)
    return list(
        set(
            (
                list(
                    map(
                        lambda el: el[0] + "://" + "/".join(el[1:-1]) + el[-1],
                        http_urls,
                    )
                )
                if (len(http_urls) != 0)
                else []
            )
            + (
                list(map(lambda el: "http://" + el, normal_urls))
                if (len(normal_urls) != 0)
                else []
            )
        )
    )


@app.route("/api/check", methods=["GET"])
def url_check_api():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "No url parameter provided"}), 400
    return jsonify(check_url(url)), 200


@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get("Body", "").lower()
    resp = MessagingResponse()
    msg = resp.message()
    if incoming_msg.startswith("help"):
        qr_file_url = url_for("static", filename="img/cyberial-anti-phishing.png")
        msg.body(WELCOME_MESSAGE)
        msg.media(qr_file_url)
    elif incoming_msg.startswith("tips") or incoming_msg.startswith("tip"):
        msg.body(random.choice(TIPS))
    elif incoming_msg.startswith("check "):
        if incoming_msg == "check" or incoming_msg == "check ":
            msg.body("No URL found...")
        else:
            url = parse_urls(incoming_msg.split(" ")[1])
            if len(url) == 0:
                msg.body("No URL found...")
            else:
                status = check_url(url)
                data = ""
                for key, value in status.items():
                    if value["safebrowsing_flag"] and value["exerra_phishing_flag"]:
                        data = f"{data}\n☠ *{key}* - "
                        data += "This is possibly a PHISHING website.\n*DO NOT OPEN THIS LINK*\n"
                    elif value["safebrowsing_flag"]:
                        data = f"{data}\n⚠️ *{key}* - "
                        data += "This is a possibly a malicious website.\n*DO NOT OPEN THIS LINK*\n"
                    elif value["exerra_phishing_flag"]:
                        data = f"{data}\n⚠️ *{key}* - "
                        data += "This is possibly a phishing or scam website.\n*BE CAUTIOUS WHEN OPENING THIS LINK. DO NOT ENTER ANY FINANCIAL INFORMATION OR OTP ON THIS WEBSITE*\n"
                    else:
                        data = f"{data}\n✅ *{key}* - "
                        data += "This link mostly appears to be safe...\n*YOU CAN OPEN THE LINK SAFELY*\n"
                msg.body(data)
    else:
        urls = parse_urls(incoming_msg)
        data = "Unknown Command. No URLs found..."
        if len(urls) != 0:
            data = ""
            if len(urls) == 1:
                status = check_url(urls[0])
            else:
                status = check_urls(urls)
            for key, value in status.items():
                if value["safebrowsing_flag"] and value["exerra_phishing_flag"]:
                    data = f"{data}\n☠ *{key}* - "
                    data += "This is possibly a PHISHING website.\n*DO NOT OPEN THIS LINK*\n"
                elif value["safebrowsing_flag"]:
                    data = f"{data}\n⚠️ *{key}* - "
                    data += "This is a possibly a malicious website.\n*DO NOT OPEN THIS LINK*\n"
                elif value["exerra_phishing_flag"]:
                    data = f"{data}\n⚠️ *{key}* - "
                    data += "This is possibly a phishing or scam website.\n*BE CAUTIOUS WHEN OPENING THIS LINK. DO NOT ENTER ANY FINANCIAL INFORMATION OR OTP ON THIS WEBSITE*\n"
                else:
                    data = f"{data}\n✅ *{key}* - "
                    data += "This link mostly appears to be safe...\n*YOU CAN OPEN THE LINK SAFELY*\n"
        msg.body(data)
    return str(resp)


if __name__ == "__main__":
    app.run()
+