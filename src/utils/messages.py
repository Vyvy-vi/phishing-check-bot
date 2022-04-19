"""
Copyright 2021 Vyom Jain
Use of this source code is governed by a BSD-style
license that can be found in the LICENSE file or at
https://github.com/Vyvy-vi/phishing-check-bot
"""

WELCOME_MESSAGE = """\
*Welcome to Cyberial Anti-Phishing bot*

To demo the bot, you could text "join stone-happily" to "+ 1 (415) 523-8886" or scan this QR Code.

_COMMANDS:_
help - shows this message
check <url> - check if a url contains phishing-attacks
tips - get tips related to prevention of phishing attacks
~news - get latest news about phishing attacks and web security~

You could also just forward links you get from messages to the bot, and wait for it to approve the link before clicking on the link.
"""
TIPS = [
    "*Suspect grammar and punctuation*\nProfessional copywriters go to great lengths to create emails with well-tested content, subject line, call-to-action etc. It is very likely that any email that contains poor grammar, punctuation or shows an illogical flow of content is likely written by inexperienced scammers and are fraudulent.",
    "*Messages asking for personal information can be scams*\nEstablished brands never ask you sensitive information via email. Any messages asking to enter or verify personal details or bank/credit card information should be treated as big red flags.",
    "*Offer of large financial rewards*\nThis pattern includes emails claiming that you have won a lottery when you never purchase one, offer of a large cash discount on something that you never purchased, large prize money in a contest that you never enrolled for and so on. The actual intention is usually to direct you to a site where the scammers can get your personal or financial information.",
    "*Watch out for shortened links*\nShortened links do not show a website’s real name and hence, can be more easily used to trick the recipient into clicking. Hackers can use shortened links to redirect you to fake look alike sites and capture sensitive information. Always place your cursor on the shortened link to see target location before clicking on it.",
    "*Verify the target site’s SSL credentials*\nSSL technology ensures safe, encrypted transmission of data over the internet. If you click on an email link and land on a site, then always verify its SSL credentials. A highly effective technique to prevent phishing is to never give out sensitive information (passwords, credit card details, security question answers etc.) on sites that do not have a valid SSL certificate installed.",
    "*Beware of pop-ups*\nUsing Iframe technology, popups can easily capture personal information and send to a different domain to the one showing up in the browser toolbar. Reputed, established sites rarely ask to enter sensitive information in popups and as a rule of thumb, no personal information should be entered in pop-ups even if they appear on domains with valid SSL and have passed all other phishing checks.",
]
