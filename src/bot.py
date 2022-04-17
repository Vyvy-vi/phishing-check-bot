import re

from utils.messages import WELCOME_MESSAGE
from utils.check_url import check_url

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
    normal_urls = re.findall(r"[a-z0-9]*\.[a-z0-9]*", string)
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
            + (normal_urls if (len(normal_urls) != 0) else [])
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
    elif incoming_msg.startswith("check "):
        # return a cat photo
        if incoming_msg == "check" or incoming_msg == "check ":
            msg.body("No URL found...")
        else:
            url = parse_urls(incoming_msg.split(" ")[1])
            if len(url) == 0:
                msg.body("No URL found...")
            else:
                msg.body(url[0])
    else:
        urls = parse_urls(incoming_msg)
        data = "Unknown Command. No URLs found..."
        if len(urls) != 0:
            data = ""
            for i, url in enumerate(urls):
                data = data + f"#{i} - {url}\n"
        msg.body(data)
    return str(resp)


if __name__ == "__main__":
    app.run()
