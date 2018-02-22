import os
from flask import Flask, request, Response
from slackclient import SlackClient 
from twilio.twiml.messaging_response import Message, MessagingResponse 
from twilio.rest import Client

SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK_SECRET', None)
TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER', None)
USER_NUMBER = os.environ.get('USER_NUMBER', None)

app = Flask(__name__)
slack_client = SlackClient(os.environ.get('SLACK_TOKEN', None))
twilio_client = Client('TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN')

@app.route('/twilio', methods=['POST'])
def twilio_post():
  response = MessagingResponse()
  # print('Msgresponse', response)

  if request.form['From'] == USER_NUMBER:
    message = request.form['Body']
    slack_client.api_call("chat.postMessage", channel="#general", text=message, username='twiliobot', icon_emoji=':robot_face:')
  return Response(response, mimetype="text/xml"), 200

@app.route('/slack', methods=['POST'])
def slack_post():
  if request.form['token'] == SLACK_WEBHOOK_SECRET:
    channel = request.form['channel_name']
    username = request.form['user_name']
    text = request.form['text']
    response_message = username + " in " + channel + " says: " + text
    twilio_client.messages.create(to=USER_NUMBER, from_=TWILIO_NUMBER,
                                  body=response_message)
  return Response(), 200


if __name__ == '__main__':
  app.run(debug=True)


