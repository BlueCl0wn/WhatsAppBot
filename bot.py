from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse

"""
sources:
 -  https://www.twilio.com/de/blog/whatsapp-chatbot-mit-python
 -  https://www.geeksforgeeks.org/building-whatsapp-bot-on-python/
 -
"""

app = Flask(__name__)


@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    print(f"incoming_msg: {incoming_msg}")
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if 'zitat' in incoming_msg:
        # return a quote
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'Bitte entschuldigen Sie. Ich konnte kein Zitat finden.'
        msg.body(quote)
        responded = True
    if 'katze' in incoming_msg:
        # return a cat pic
        msg.media('https://cataas.com/cat')
        responded = True
    if not responded:
        msg.body('Ich kenne mich leider nur mit Zitaten und Katzen aus.')
    print(f"resp: {str(resp)}")
    return str(resp)


if __name__ == '__main__':
    app.run(port=4001)
